#!/usr/bin/env python3
"""
X-Agents Flask Backend Server with Feedback Loop
Provides REST API for the X-Agent pipeline processing with PM ↔ Scrum Master feedback loop
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import time
import json
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
import re
import os
import requests
import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def write_debug_log(message):
    with open('main_internal_debug.log', 'a') as f:
        f.write(f'{datetime.datetime.now()}: {message}\n')
    print(f"[DEBUG_LOG] {datetime.datetime.now()}: {message}")

class LazyDomainRegistryWithCreator:

    """Enhanced registry that scans plugins, loads on-demand, and creates missing plugins"""
    
    def __init__(self, plugins_dir="domain_plugins"):
        self.plugins_dir = plugins_dir
        self.available_domains = {}  # Plugin metadata only
        self.loaded_plugins = {}     # Actually loaded plugins
        self.plugin_creator = None   # Lazy load plugin creator too
        self.custom_plugins_created = 0  # Track custom plugins for billing
        self._scan_available_plugins()
    
    def _scan_available_plugins(self):
        """Scan folder structure without loading plugins"""
        import os
        import importlib.util
        
        if not os.path.exists(self.plugins_dir):
            print(f"⚠️  Plugin directory {self.plugins_dir} not found")
            return
            
        plugin_files = [f for f in os.listdir(self.plugins_dir) 
                       if f.endswith('.py') and not f.startswith('__')]
        
        print(f"🔍 Scanning {len(plugin_files)} available plugins...")
        
        for plugin_file in plugin_files:
            domain_name = plugin_file[:-3]  # Remove .py
            plugin_path = os.path.join(self.plugins_dir, plugin_file)
            
            # Store metadata without loading
            self.available_domains[domain_name] = {
                'file_path': plugin_path,
                'loaded': False,
                'domain_name': domain_name,
                'custom_created': False  # Track if custom created
            }
        
        print(f"📦 Found {len(self.available_domains)} available domains: {list(self.available_domains.keys())}")
        print(f"🚀 Plugins will load on-demand when needed")
    
    def list_domains(self):
        """List all available domains (loaded + unloaded)"""
        return list(self.available_domains.keys())
    
    def get_handler_or_create(self, content, domain_hint=None, allow_custom_creation=True):
        """Main workflow: Find suitable plugin or create new one"""
        
        print(f"🔍 [DEBUG] get_handler_or_create called with domain_hint: '{domain_hint}'")
        print(f"🔍 [DEBUG] Available domains: {list(self.available_domains.keys())}")
        
        # Step 1: If domain_hint is provided and exists, use it directly
        if domain_hint and domain_hint != "general" and domain_hint in self.available_domains:
            print(f"🎯 Using provided domain hint: {domain_hint}")
            handler = self.get_handler(domain_hint)
            if handler:
                print(f"✅ Using existing plugin: {domain_hint}")
                return handler, domain_hint, False, 0  # (handler, domain, newly_created, cost)
        else:
            if domain_hint:
                print(f"❌ [DEBUG] Domain hint '{domain_hint}' not in available domains or is 'general'")
        
        # Step 2: Try to detect domain from available plugins (fallback)
        detected_domain, confidence = self.detect_domain(content)
        
        print(f"🔍 Domain detection: {detected_domain} (confidence: {confidence:.2f})")
        
        # Step 3: If confidence is high enough, use existing plugin
        if confidence >= 0.6:  # Good confidence threshold
            handler = self.get_handler(detected_domain)
            if handler:
                print(f"✅ Using existing plugin: {detected_domain}")
                return handler, detected_domain, False, 0  # (handler, domain, newly_created, cost)
        
        # Step 4: No suitable plugin found - create new one if allowed
        if allow_custom_creation:
            print(f"❌ No suitable plugin found (best: {detected_domain}, confidence: {confidence:.2f})")
            print("🔧 Creating custom plugin...")
            
            return self._create_custom_plugin(content, domain_hint)
        else:
            # Return general handler or None if creation not allowed
            return None, 'general', False, 0
    
    def _create_custom_plugin(self, content, domain_hint=None):
        """Create new plugin using DomainPluginCreatorXAgent"""
        try:
            # Step 1: Lazy load plugin creator
            if not self.plugin_creator:
                from domain_plugin_creator_agent import DomainPluginCreatorXAgent
                self.plugin_creator = DomainPluginCreatorXAgent()
                print("🔧 Plugin Creator Agent loaded")
            
            # Step 2: Analyze content for plugin creation
            print("📊 Analyzing content for custom plugin requirements...")
            analysis_result = self.plugin_creator.analyze_content_for_plugin(content)
            
            if analysis_result['confidence'] < 0.7:
                print(f"⚠️  Plugin creator confidence too low: {analysis_result['confidence']}")
                print("🔄 Falling back to general domain processing")
                return None, 'general', False, 0
            
            # Step 3: Estimate cost for custom plugin
            estimated_cost = self._estimate_plugin_cost(content, analysis_result)
            print(f"💰 Estimated cost for custom plugin: ${estimated_cost}")
            
            # Step 4: Create the plugin (in real implementation, this would require payment)
            plugin_spec = analysis_result['suggested_plugin']
            print(f"🛠️  Creating custom plugin: {plugin_spec.get('domain_name', 'unknown')}")
            
            # Use asyncio.run() to handle the async function call
            creation_result = asyncio.run(self.plugin_creator.create_domain_plugin(plugin_spec))
            
            if creation_result['success']:
                new_domain = creation_result['domain_name']
                print(f"✅ Created new plugin: {new_domain}")
                
                # Step 5: Register new plugin in our system
                plugin_path = creation_result['file_path']
                self.available_domains[new_domain] = {
                    'file_path': plugin_path,
                    'loaded': False,
                    'domain_name': new_domain,
                    'custom_created': True,  # Mark as custom
                    'creation_cost': estimated_cost,
                    'created_timestamp': time.time()
                }
                
                # Step 6: Load the new plugin immediately
                handler = self.get_handler(new_domain)
                if handler:
                    self.custom_plugins_created += 1
                    print(f"🎉 Custom plugin ready for use! Total custom plugins: {self.custom_plugins_created}")
                    return handler, new_domain, True, estimated_cost  # (handler, domain, newly_created, cost)
                
            else:
                print(f"❌ Plugin creation failed: {creation_result['error']}")
                
        except Exception as e:
            print(f"❌ Plugin creation error: {e}")
            import traceback
            traceback.print_exc()
        
        # Fallback to general processing
        print("🔄 Falling back to general domain processing")
        return None, 'general', False, 0
    
    def _estimate_plugin_cost(self, content, analysis_result):
        """Estimate cost for creating custom plugin"""
        base_cost = 50  # Base fee for plugin creation
        
        # Complexity factors
        word_count = len(content.split())
        complexity_score = analysis_result.get('complexity_score', 0.5)
        
        # Calculate additional costs
        complexity_cost = (word_count // 100) * 10  # $10 per 100 words
        specialty_cost = int(complexity_score * 25)  # Up to $25 for complexity
        
        total_cost = base_cost + complexity_cost + specialty_cost
        return min(total_cost, 200)  # Cap at $200
    
    def get_handler(self, domain_name):
        """Load plugin on-demand and return handler (existing method)"""
        write_debug_log(f"[DEBUG] get_handler called for: {domain_name}")
        if domain_name not in self.available_domains:
            write_debug_log(f"[DEBUG] Domain '{domain_name}' not found in available plugins")
            return None
            
        # Check if already loaded
        if domain_name in self.loaded_plugins:
            write_debug_log(f"[DEBUG] Domain '{domain_name}' already loaded.")
            return self.loaded_plugins[domain_name]
        
        # Load plugin on-demand
        try:
            plugin_info = self.available_domains[domain_name]
            handler = self._load_plugin_now(domain_name, plugin_info['file_path'])
            
            if handler:
                self.loaded_plugins[domain_name] = handler
                self.available_domains[domain_name]['loaded'] = True
                write_debug_log(f"[DEBUG] Loaded domain plugin on-demand: {domain_name}")
                return handler
            
        except Exception as e:
            write_debug_log(f"[DEBUG] Failed to load domain plugin {domain_name}: {e}")
            return None
    
    def _load_plugin_now(self, domain_name, file_path):
        """Actually load a specific plugin (existing method)"""
        write_debug_log(f"[DEBUG] _load_plugin_now called for: {domain_name} at {file_path}")
        import importlib.util
        
        spec = importlib.util.spec_from_file_location(domain_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Look for handler class
        handler_class_name = f"{domain_name.title().replace('_', '')}DomainHandler"
        write_debug_log(f"[DEBUG] Expected handler class name: {handler_class_name}")
        if hasattr(module, handler_class_name):
            write_debug_log(f"[DEBUG] Found handler class: {handler_class_name}")
            return getattr(module, handler_class_name)()
        else:
            write_debug_log(f"⚠️  Handler class {handler_class_name} not found in {domain_name}")
            return None
    
    def detect_domain(self, content):
        """Enhanced domain detection with existing plugins, dynamically loading keywords."""
        content_lower = content.lower()
        
        best_match = 'general'
        best_score = 0
        
        write_debug_log(f"[DEBUG] Starting domain detection for content: {content_lower[:50]}...")
        write_debug_log(f"[DEBUG] Available domains: {list(self.available_domains.keys())}")

        # Iterate through all available domains (loaded or not)
        for domain_name in self.available_domains.keys():
            write_debug_log(f"[DEBUG] Checking domain: {domain_name}")
            handler = self.get_handler(domain_name) # This will load the plugin if not already loaded
            if handler and hasattr(handler, 'get_detection_keywords'):
                keywords = handler.get_detection_keywords()
                score = sum(1 for keyword in keywords if keyword in content_lower)
                write_debug_log(f"[DEBUG]   Keywords for {domain_name}: {keywords}")
                write_debug_log(f"[DEBUG]   Score for {domain_name}: {score}")
                if score > best_score:
                    best_match = domain_name
                    best_score = score
                    write_debug_log(f"[DEBUG]   New best match: {best_match} with score {best_score}")
        
        # Simple normalization for confidence. Adjust as needed.
        # Max score could be based on the highest number of keywords in any domain, or a fixed value.
        confidence = min(best_score / 3.0, 1.0)  # Assuming 3 keywords give high confidence
        write_debug_log(f"[DEBUG] Final detected domain: {best_match}, Confidence: {confidence:.2f}")
        return best_match, confidence
    
    def get_loaded_count(self):
        """Get count of actually loaded plugins"""
        return len(self.loaded_plugins)
    
    def get_available_count(self):
        """Get count of available plugins"""
        return len(self.available_domains)
    
    def rescan_plugins(self):
        """Rescan the plugin directory to pick up new plugins."""
        self.available_domains = {}
        self._scan_available_plugins()
        print("🔄 Rescanned available plugins.")

    def get_custom_plugin_stats(self):
        """Get statistics about custom plugins"""
        custom_plugins = [d for d in self.available_domains.values() if d.get('custom_created', False)]
        total_cost = sum(d.get('creation_cost', 0) for d in custom_plugins)
        
        return {
            'total_custom_plugins': len(custom_plugins),
            'total_revenue': total_cost,
            'loaded_custom_plugins': len([d for d in custom_plugins if d.get('loaded', False)])
        }

# Import lxml with error handling
try:
    from lxml import etree
except ImportError:
    print("Installing lxml...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'lxml'])
    from lxml import etree

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseXAgent(ABC):
    """Base X-Agent with XML processing and performance tracking"""

    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.metrics = {'total_time': 0.0}

    def process(self, input_xml: str) -> str:
        """Main processing with timing"""
        start_time = time.time()

        # Parse input
        parsed = etree.fromstring(input_xml.encode())

        # Process with agent intelligence
        result = self._process_intelligence(parsed)

        # Generate output XML
        output_xml = self._generate_xml(result)

        self.metrics['total_time'] = float((time.time() - start_time) * 1000)
        return output_xml

    @abstractmethod
    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Agent-specific processing logic"""
        pass

    @abstractmethod
    def _generate_xml(self, result: dict) -> str:
        """Generate XML output for next agent"""
        pass


class AnalystXAgent(BaseXAgent):
    """Analyzes documents and detects domain type (runs once)"""

    def __init__(self):
        super().__init__("AnalystXAgent")

    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Detect document domain and type"""
        # Extract content from the text element
        text_elem = parsed_input.find('.//text')
        if text_elem is not None and text_elem.text:
            content = text_elem.text.lower()
        else:
            content_bytes = etree.tostring(parsed_input, encoding='unicode', method='text')
            content = content_bytes.lower() if content_bytes else ""

        # Use domain plugin system for intelligent detection
        from domain_plugins.registry import DomainRegistry
        registry = DomainRegistry()
        domain, confidence = registry.detect_domain(content)
        
        # Fallback to general if confidence is too low
        if confidence < 0.3:
            domain = 'general'

        return {
            'domain': domain,
            'complexity': min(len(content) // 500, 5),
            'content': content[:2000]  # Keep original content for PM
        }

    def _generate_xml(self, result: dict) -> str:
        """Generate analysis XML for Product Manager"""
        escaped_content = self._escape_xml_content(result['content'])
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<AnalysisPacket>
    <Domain>{result['domain']}</Domain>
    <Complexity>{result['complexity']}</Complexity>
    <Content><![CDATA[{result['content']}]]></Content>
</AnalysisPacket>"""

    def _escape_xml_content(self, content: str) -> str:
        """Properly escape XML special characters"""
        if not content:
            return ''
        return (content
                .replace('&', '&amp;')   # Must be first to avoid double-escaping
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&apos;'))


class ProductManagerXAgent(BaseXAgent):
    """Clean, Plugin-Based Product Manager using Domain Registry"""

    def __init__(self):
        super().__init__("ProductManagerXAgent")
        # Use enhanced lazy loading registry with plugin creator
        self.domain_registry = LazyDomainRegistryWithCreator()
        print("🔌 Enhanced Lazy Domain Registry with Plugin Creator initialized")

    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Extract requirements using domain plugins"""
        
        # Check if this is feedback from Scrum Master
        feedback_elem = parsed_input.find('Feedback')
        if feedback_elem is not None:
            return self._process_scrum_feedback(parsed_input)

        # Normal initial processing from Analyst
        domain_elem = parsed_input.find('Domain')
        content_elem = parsed_input.find('Content')
        domain = domain_elem.text if domain_elem is not None else "general"
        content = content_elem.text if content_elem is not None else ""

        return self._extract_requirements_with_plugins(content, domain)

    def _extract_requirements_with_plugins(self, content: str, domain_hint: str = None) -> dict:
        """Extract requirements using domain plugin system with auto-creation"""
        
        # First, try to extract explicit REQ-xxx patterns
        requirements = self._extract_explicit_requirements(content)
        
        if not requirements:
            # Use enhanced registry to get the handler for the detected domain
            handler = self.domain_registry.get_handler(domain_hint)
            newly_created = False
            cost = 0
            
            if handler:
                # Extract domain-specific requirements
                requirements = handler.extract_requirements(content)
                # Add cross-cutting requirements
                requirements.extend(handler.get_cross_cutting_requirements(content))
                # Get stakeholders
                stakeholders = handler.extract_stakeholders(content)
                
                # Log if we created a new plugin
                if newly_created:
                    logger.info(f"🆕 Created and used new plugin: {domain} (Cost: ${cost})")
                    
            else:
                # Fallback to generic requirements
                requirements = self._extract_generic_requirements()
                stakeholders = ['End Users', 'Development Team']
                domain = 'general'
                newly_created = False
                cost = 0
        else:
            stakeholders = self._detect_basic_stakeholders(content)
            domain = domain_hint or 'general'
            newly_created = False
            cost = 0

        # Format requirements with IDs
        formatted_requirements = self._format_requirements(requirements)
        
        # Extract personalization info
        person_info = self._extract_person_and_company(content)

        return {
            'domain': domain,
            'requirements': formatted_requirements,
            'stakeholders': stakeholders,
            'req_count': len(formatted_requirements),
            'feedback_applied': False,
            'person_name': person_info.get('person'),
            'company_name': person_info.get('company'),
            'plugin_created': newly_created,
            'plugin_cost': cost
        }

    def _extract_explicit_requirements(self, content: str) -> list:
        """Extract explicit REQ-xxx requirements from content"""
        requirements = []
        req_pattern = r'REQ-(\d+)[:\s]+(.*?)(?=\n|REQ-|\Z)'
        for match in re.finditer(req_pattern, content, re.DOTALL):
            extracted_title = match.group(2).strip()
            logger.debug(f"[Product Manager] Extracted explicit requirement title: {extracted_title}")
            requirements.append({
                'title': extracted_title[:100],
                'priority': 'high' if any(word in extracted_title.lower() for word in ['critical', 'must', 'essential', 'required']) else 'medium',
                'category': 'functional'
            })
        return requirements

    def _extract_generic_requirements(self) -> list:
        """Fallback generic requirements"""
        return [
            {'title': 'Core System Architecture and Data Management', 'priority': 'high', 'category': 'functional'},
            {'title': 'User Interface and Experience Implementation', 'priority': 'high', 'category': 'functional'},
            {'title': 'API Development and Integration Framework', 'priority': 'medium', 'category': 'functional'}
        ]

    def _format_requirements(self, requirements: list) -> list:
        """Format requirements with IDs and deduplication"""
        seen_titles = set()
        formatted = []
        
        for i, req in enumerate(requirements[:8], 1):  # Limit to 8
            title = req['title']
            if title not in seen_titles:
                formatted.append({
                    'id': f"REQ-{i:03d}",
                    'title': title,
                    'priority': req.get('priority', 'medium')
                })
                seen_titles.add(title)
        
        return formatted

    def _detect_basic_stakeholders(self, content: str) -> list:
        """Basic stakeholder detection"""
        stakeholders = ['End Users', 'Development Team']
        content_lower = content.lower()
        
        if any(term in content_lower for term in ['business', 'management', 'executive']):
            stakeholders.append('Business Stakeholders')
        if any(term in content_lower for term in ['admin', 'administrator', 'ops']):
            stakeholders.append('System Administrators')
            
        return stakeholders

    def _extract_person_and_company(self, content: str) -> dict:
        """Extract person and company names from content"""
        person_info = {'person': None, 'company': None}
        
        # Simple name extraction patterns
        person_match = re.search(r'(?:I am|My name is|I\'m)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', content)
        if person_match:
            person_info['person'] = person_match.group(1).strip()
        
        company_match = re.search(r'(?:at|for|from)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Inc|LLC|Corp|Company|Technologies)\.?))', content)
        if company_match:
            person_info['company'] = company_match.group(1).strip()
        
        return person_info

    def _process_scrum_feedback(self, feedback_input: etree.Element) -> dict:
        """Process feedback from Scrum Master"""
        domain = feedback_input.find('Domain').text
        feedback = feedback_input.find('Feedback').text
        original_content = feedback_input.find('OriginalContent').text

        logger.info(f"[Product Manager] Processing Scrum Master feedback: {feedback}")

        # Re-extract requirements with feedback context
        result = self._extract_requirements_with_plugins(original_content, domain)
        
        # Apply feedback adjustments
        if 'reduce scope' in feedback.lower():
            result['requirements'] = [req for req in result['requirements'] if req['priority'] == 'high'][:5]
        elif 'too complex' in feedback.lower():
            for req in result['requirements'][:6]:
                req['title'] = f"Basic {req['title'][:30]}"
                req['priority'] = 'medium'
            result['requirements'] = result['requirements'][:6]
        elif 'too many tasks' in feedback.lower():
            result['requirements'] = result['requirements'][:3]
        
        result['feedback_applied'] = True
        return result

    def _generate_xml(self, result: dict) -> str:
        """Generate requirements XML for Task Manager"""
        reqs_xml = '\n'.join([
            f'        <Requirement id="{req["id"]}" priority="{req["priority"]}">{req["title"]}</Requirement>'
            for req in result['requirements']
        ])

        stakeholders_xml = '\n'.join([
            f'        <Stakeholder>{stakeholder}</Stakeholder>'
            for stakeholder in result['stakeholders']
        ])

        feedback_note = "\n    <FeedbackApplied>true</FeedbackApplied>" if result['feedback_applied'] else ""

        # Add personalization info
        person_xml = ""
        if result.get('person_name'):
            person_xml += f"\n    <PersonName>{result['person_name']}</PersonName>"
        if result.get('company_name'):
            person_xml += f"\n    <CompanyName>{result['company_name']}</CompanyName>"

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<TaskPacket>
    <ProjectInfo>
        <Domain>{result['domain']}</Domain>
        <RequirementCount>{result['req_count']}</RequirementCount>
    </ProjectInfo>{feedback_note}{person_xml}
    <Requirements>
{reqs_xml}
    </Requirements>
    <Stakeholders>
{stakeholders_xml}
    </Stakeholders>
</TaskPacket>"""


class TaskManagerXAgent(BaseXAgent):
    """Breaks requirements into executable tasks (processes each PM iteration)"""

    def __init__(self):
        super().__init__("TaskManagerXAgent")

    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Generate tasks from requirements"""
        domain_elem = parsed_input.find('.//Domain')
        domain = domain_elem.text if domain_elem is not None else "general"
        requirements = parsed_input.findall('.//Requirement')
        feedback_applied = parsed_input.find('FeedbackApplied') is not None

        if feedback_applied:
            logger.info(f"[Task Manager] Processing updated requirements ({len(requirements)} requirements)")

        tasks = []
        task_id = 1

        # Generate tasks for each requirement
        for req in requirements:
            req_id = req.get('id')
            req_title = req.get('title', req.get('text', 'Requirement'))
            req_priority = req.get('priority', 'medium')

            # Standard task patterns per requirement
            patterns = ['Design', 'Implement', 'Test', 'Document']

            for pattern in patterns:
                # Adjust effort based on priority
                base_points = 3 if pattern == 'Implement' else 2

                if req_priority == 'high':
                    story_points = base_points + 1
                else:
                    story_points = base_points

                # Create meaningful task titles without truncation
                if pattern == 'Design':
                    task_title = f"Design architecture and specifications for {req_title[:60]}"
                elif pattern == 'Implement':
                    task_title = f"Develop and implement {req_title[:60]}"
                elif pattern == 'Test':
                    task_title = f"Test and validate {req_title[:60]}"
                elif pattern == 'Document':
                    task_title = f"Create documentation for {req_title[:60]}"
                else:
                    task_title = f"{pattern} {req_title[:60]}"

                # Calculate hours based on story points (rough estimate: 3-4 hours per story point)
                estimated_hours = story_points * 3.5

                tasks.append({
                    'id': f"TASK-{task_id:03d}",
                    'title': task_title,
                    'req_id': req_id,
                    'story_points': story_points,
                    'hours': int(estimated_hours),
                    'priority': req_priority
                })
                task_id += 1

        # Add domain-specific tasks
        if domain == 'visual_workflow':
            tasks.extend([
                {'id': f"TASK-{task_id:03d}", 'title': 'Canvas Setup', 'req_id': 'DOMAIN', 'story_points': 5, 'hours': 16, 'priority': 'high'},
                {'id': f"TASK-{task_id+1:03d}", 'title': 'Drag & Drop', 'req_id': 'DOMAIN', 'story_points': 8, 'hours': 24, 'priority': 'high'}
            ])
        elif domain == 'enterprise':
            tasks.extend([
                {'id': f"TASK-{task_id:03d}", 'title': 'Security Setup', 'req_id': 'DOMAIN', 'story_points': 6, 'hours': 20, 'priority': 'high'},
                {'id': f"TASK-{task_id+1:03d}", 'title': 'Compliance Framework', 'req_id': 'DOMAIN', 'story_points': 8, 'hours': 28, 'priority': 'high'}
            ])

        total_story_points = sum(task['story_points'] for task in tasks)
        expansion_ratio = len(tasks) / max(len(requirements), 1)

        logger.info(f"Generated {len(tasks)} tasks, {total_story_points} story points")

        return {
            'domain': domain,
            'tasks': tasks,
            'total_tasks': len(tasks),
            'story_points': total_story_points,
            'expansion_ratio': expansion_ratio,
            'req_count': len(requirements)
        }

    def _generate_xml(self, result: dict) -> str:
        """Generate task breakdown XML for Scrum Master"""
        tasks_xml = '\n'.join([
            f'        <Task id="{task["id"]}" req_id="{task["req_id"]}" points="{task["story_points"]}" hours="{task["hours"]}" priority="{task.get("priority", "medium")}">{task["title"]}</Task>'
            for task in result['tasks']
        ])

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<TaskBreakdown>
    <Summary>
        <Domain>{result['domain']}</Domain>
        <TotalTasks>{result['total_tasks']}</TotalTasks>
        <StoryPoints>{result['story_points']}</StoryPoints>
        <ExpansionRatio>{result['expansion_ratio']:.1f}x</ExpansionRatio>
        <RequirementCount>{result['req_count']}</RequirementCount>
    </Summary>
    <Tasks>
{tasks_xml}
    </Tasks>
</TaskBreakdown>"""


class POScrumMasterXAgent(BaseXAgent):
    """Final validation and release approval (generates feedback for PM)"""

    def __init__(self):
        super().__init__("POScrumMasterXAgent")

    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Validate project and approve/reject with specific feedback"""
        domain = parsed_input.find('.//Domain').text
        total_tasks = int(parsed_input.find('.//TotalTasks').text)
        story_points = int(parsed_input.find('.//StoryPoints').text)
        req_count = int(parsed_input.find('.//RequirementCount').text)

        logger.info(f"[Scrum Master] Reviewing: {total_tasks} tasks, {story_points} story points, {req_count} requirements")

        # Quality gates
        quality_checks = {
            'reasonable_task_count': total_tasks <= 50,
            'manageable_story_points': story_points <= 80,
            'adequate_scope': req_count >= 3,
            'good_task_ratio': (total_tasks / max(req_count, 1)) <= 15
        }

        quality_score = sum(quality_checks.values()) / len(quality_checks) * 100

        # Risk assessment
        if story_points > 100:
            risk = 'high'
        elif story_points > 60:
            risk = 'medium'
        else:
            risk = 'low'

        # Approval decision with specific feedback
        approved = quality_score >= 75 and risk != 'high'

        # Generate specific feedback for Product Manager
        feedback = self._generate_feedback(quality_checks, story_points, total_tasks, req_count, approved)

        return {
            'domain': domain,
            'approved': approved,
            'quality_score': quality_score,
            'risk_level': risk,
            'total_tasks': total_tasks,
            'story_points': story_points,
            'req_count': req_count,
            'feedback': feedback,
            'quality_checks': quality_checks
        }

    def _generate_feedback(self, quality_checks: dict, story_points: int, total_tasks: int, req_count: int, approved: bool) -> str:
        """Generate specific feedback for Product Manager"""

        if approved:
            return "APPROVED: Project scope and complexity are acceptable for execution"

        # Generate specific feedback based on what failed
        issues = []

        if story_points > 100:
            issues.append("too many story points - reduce scope significantly")
        elif story_points > 80:
            issues.append("reduce scope - story points too high")

        if total_tasks > 50:
            issues.append("too many tasks - simplify requirements")

        if not quality_checks['good_task_ratio']:
            issues.append("too complex - requirements generating too many tasks")

        if req_count > 8:
            issues.append("reduce scope - too many requirements")

        if not issues:
            issues.append("insufficient quality - improve requirements")

        return f"REJECTED: {', '.join(issues)}"

    def _generate_xml(self, result: dict) -> str:
        """Generate approval XML (with feedback if rejected)"""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<ReleaseApproval>
    <Decision approved="{str(result['approved']).lower()}">
        <QualityScore>{result['quality_score']:.1f}%</QualityScore>
        <RiskLevel>{result['risk_level']}</RiskLevel>
        <TotalTasks>{result['total_tasks']}</TotalTasks>
        <StoryPoints>{result['story_points']}</StoryPoints>
        <RequirementCount>{result['req_count']}</RequirementCount>
    </Decision>
    <Feedback>{result['feedback']}</Feedback>
</ReleaseApproval>"""


class XAgentPipeline:
    """Pipeline with Document Formatter → PM ↔ Scrum Master feedback loop"""

    def __init__(self):
        # Import document formatter to avoid startup issues
        try:
            from document_formatter_agent import DocumentFormatterXAgent
            self.document_formatter = DocumentFormatterXAgent()
            print("✅ Document Formatter integrated into pipeline")
        except ImportError as e:
            print(f"⚠️  Document Formatter not available: {e}")
            self.document_formatter = None
            
        self.analyst = AnalystXAgent()
        self.product_manager = ProductManagerXAgent()
        self.task_manager = TaskManagerXAgent()
        self.scrum_master = POScrumMasterXAgent()
        self.max_iterations = 3

    def format_document(self, raw_content: str) -> dict:
        """Step 1: Format document and return for user review"""
        if not self.document_formatter:
            return {
                'success': False, 
                'error': 'Document formatter not available'
            }
            
        try:
            logger.info("📝 Step 1: Formatting document for user review")
            formatted_result = self.document_formatter.format_document(raw_content)
            
            return {
                'success': True,
                'formatted_content': formatted_result['formatted_content'],
                'domain': formatted_result['identified_domain'],
                'requirements': formatted_result['extracted_requirements'],
                'stakeholders': formatted_result['stakeholders'],
                'validation_score': formatted_result['validation_score'],
                'message': 'Document formatted successfully. Review and send to analysis.'
            }
        except Exception as e:
            logger.error(f"Document formatting error: {e}")
            return {'success': False, 'error': str(e)}

    def execute_with_formatted_input(self, formatted_content: str) -> dict:
        """Step 2: Execute main pipeline with pre-formatted content"""
        logger.info("🚀 Step 2: Processing formatted document through main pipeline")
        
        # Create XML from formatted content (skip document formatter)
        document_xml = f"""<?xml version='1.0' encoding='UTF-8'?>
<Document>
    <text><![CDATA[{formatted_content}]]></text>
</Document>"""

        # Continue with existing pipeline starting from Analyst
        logger.info("🔍 Step 2a: Document Analysis (using formatted input)")
        analysis_xml = self.analyst.process(document_xml)
        
        # Continue with rest of existing execute() method
        logger.info("📋 Step 2b: Starting PM → Task Manager → Scrum Master cycle")
        current_input = analysis_xml
        iteration = 0
        final_pm_output = None
        final_task_output = None

        while iteration < self.max_iterations:
            iteration += 1
            logger.info(f"\n--- Iteration {iteration} ---")

            # Product Manager processes
            logger.info("📋 Product Manager: Creating/updating requirements")
            pm_output = self.product_manager.process(current_input)
            final_pm_output = pm_output

            # Task Manager breaks down requirements
            logger.info("🔧 Task Manager: Breaking down into tasks")
            task_output = self.task_manager.process(pm_output)
            final_task_output = task_output

            # Scrum Master reviews
            logger.info("✅ Scrum Master: Reviewing for approval")
            approval_output = self.scrum_master.process(task_output)

            # Check approval
            approval_tree = etree.fromstring(approval_output.encode())
            approved = approval_tree.find('.//Decision').get('approved') == 'true'
            feedback_text = approval_tree.find('Feedback').text

            if approved:
                logger.info(f"\n🎉 PROJECT APPROVED after {iteration} iteration(s)!")
                complete_result = self._create_complete_result(
                    analysis_xml, final_pm_output, final_task_output, approval_output, iteration, 'APPROVED'
                )
                return {
                    'success': True,
                    'iterations': iteration,
                    'final_output': complete_result,
                    'status': 'APPROVED'
                }

            logger.info(f"❌ Project rejected: {feedback_text}")

            if iteration >= self.max_iterations:
                logger.info(f"\n💔 PROJECT REJECTED after {self.max_iterations} iterations")
                complete_result = self._create_complete_result(
                    analysis_xml, final_pm_output, final_task_output, approval_output, iteration, 'REJECTED'
                )
                return {
                    'success': False,
                    'iterations': iteration,
                    'final_output': complete_result,
                    'status': 'REJECTED - Max iterations reached'
                }

            # Prepare feedback for Product Manager
            logger.info(f"🔄 Sending feedback to Product Manager for iteration {iteration + 1}")
            current_input = self._create_feedback_xml(feedback_text, analysis_xml)

        return {'success': False, 'status': 'Unexpected end'}

    def _escape_xml_content(self, content: str) -> str:
        """Properly escape XML special characters"""
        if not content:
            return ''
        return (content
                .replace('&', '&amp;')   # Must be first to avoid double-escaping
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&apos;'))

    def debug_xml_content(self, content):
        lines = content.split('\n')
        print(f"Total lines in XML: {len(lines)}")

        # Print lines around line 11
        for i in range(max(0, 8), min(len(lines), 15)):
            line_num = i + 1
            line = lines[i]
            marker = " <-- PROBLEM LINE" if line_num == 11 else ""
            print(f"Line {line_num}: '{line}'{marker}")

            if line_num == 11 and len(line) >= 25:
                char_25 = line[24]  # 0-indexed  
                print(f"Character 25: '{char_25}' (ASCII: {ord(char_25)})")
                print(f"Context around char 25: '{line[20:30]}'")

                # Check for unescaped ampersands
                ampersand_positions = [pos for pos, char in enumerate(line) if char == '&']
                if ampersand_positions:
                    print(f"Ampersand positions in line 11: {ampersand_positions}")
                    for pos in ampersand_positions:
                        context = line[max(0, pos-5):pos+10]
                        print(f"  Ampersand at position {pos}: '{context}'")

    def execute(self, document_content: str) -> dict:
        """Execute pipeline with Document Formatter → PM-Scrum Master feedback loop"""

        # Step 0: Document Formatting (runs once - optional but recommended)
        formatted_content = document_content
        if self.document_formatter:
            logger.info("📝 Step 0: Document Formatting and Standardization")
            try:
                format_result = self.document_formatter.format_document(document_content)
                formatted_content = format_result['formatted_content']
                logger.info(f"✅ Document formatted for domain: {format_result['identified_domain']}")
                logger.info(f"📊 Validation score: {format_result['validation_score']:.1f}%")
            except Exception as e:
                logger.warning(f"⚠️  Document formatting failed, using original: {e}")
                formatted_content = document_content

        logger.info("🔍 Step 1: Document Analysis (runs once)")
        # Step 1: Analyst runs once - use CDATA for safe content handling
        document_xml = f"""<?xml version='1.0' encoding='UTF-8'?>
<Document>
    <text><![CDATA[{formatted_content}]]></text>
</Document>"""

        # Debug the XML content before parsing
        logger.info("🔍 Debugging XML content...")

        analysis_xml = self.analyst.process(document_xml)

        logger.info("📋 Step 2: Starting PM → Task Manager → Scrum Master cycle")
        # Step 2: PM → Task Manager → Scrum Master cycle
        current_input = analysis_xml
        iteration = 0
        final_pm_output = None
        final_task_output = None

        while iteration < self.max_iterations:
            iteration += 1
            logger.info(f"\n--- Iteration {iteration} ---")

            # Product Manager processes (initial analysis or feedback)
            logger.info("📋 Product Manager: Creating/updating requirements")
            pm_output = self.product_manager.process(current_input)
            final_pm_output = pm_output  # Store latest PM output

            # Task Manager breaks down requirements
            logger.info("🔧 Task Manager: Breaking down into tasks")
            task_output = self.task_manager.process(pm_output)
            final_task_output = task_output  # Store latest task breakdown

            # Scrum Master reviews and approves/rejects
            logger.info("✅ Scrum Master: Reviewing for approval")
            approval_output = self.scrum_master.process(task_output)

            # Check approval
            approval_tree = etree.fromstring(approval_output.encode())
            approved = approval_tree.find('.//Decision').get('approved') == 'true'
            feedback_text = approval_tree.find('Feedback').text

            if approved:
                logger.info(f"\n🎉 PROJECT APPROVED after {iteration} iteration(s)!")
                # Create comprehensive result with all pipeline outputs
                complete_result = self._create_complete_result(
                    analysis_xml, final_pm_output, final_task_output, approval_output, iteration, 'APPROVED'
                )
                return {
                    'success': True,
                    'iterations': iteration,
                    'final_output': complete_result,
                    'status': 'APPROVED'
                }

            logger.info(f"❌ Project rejected: {feedback_text}")

            if iteration >= self.max_iterations:
                logger.info(f"\n💔 PROJECT REJECTED after {self.max_iterations} iterations")
                # Create comprehensive result even for rejection
                complete_result = self._create_complete_result(
                    analysis_xml, final_pm_output, final_task_output, approval_output, iteration, 'REJECTED'
                )
                return {
                    'success': False,
                    'iterations': iteration,
                    'final_output': complete_result,
                    'status': 'REJECTED - Max iterations reached'
                }

            # Prepare feedback for Product Manager
            logger.info(f"🔄 Sending feedback to Product Manager for iteration {iteration + 1}")
            current_input = self._create_feedback_xml(feedback_text, analysis_xml)

        return {'success': False, 'status': 'Unexpected end'}

    def _create_feedback_xml(self, feedback: str, original_analysis: str) -> str:
        """Create feedback XML for Product Manager"""
        analysis_tree = etree.fromstring(original_analysis.encode())
        domain = analysis_tree.find('Domain').text
        content_elem = analysis_tree.find('Content')
        content = content_elem.text if content_elem is not None else ""

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<FeedbackPacket>
    <Domain>{domain}</Domain>
    <Feedback><![CDATA[{feedback}]]></Feedback>
    <OriginalContent><![CDATA[{content}]]></OriginalContent>
</FeedbackPacket>"""

    def _create_complete_result(self, analysis_xml: str, pm_xml: str, task_xml: str, approval_xml: str, iterations: int, status: str) -> str:
        """Create comprehensive pipeline result with all agent outputs"""

        # Parse all XML outputs
        analysis_tree = etree.fromstring(analysis_xml.encode())
        pm_tree = etree.fromstring(pm_xml.encode())
        task_tree = etree.fromstring(task_xml.encode())
        approval_tree = etree.fromstring(approval_xml.encode())

        # Extract data
        domain = analysis_tree.find('Domain').text
        complexity = analysis_tree.find('Complexity').text

        # Extract requirements
        requirements = pm_tree.findall('.//Requirement')
        req_xml = '\n'.join([
            f'        <Requirement id="{req.get("id")}" priority="{req.get("priority")}">{req.text}</Requirement>'
            for req in requirements
        ])

        # Extract tasks
        tasks = task_tree.findall('.//Task')
        task_xml_formatted = '\n'.join([
            f'        <Task id="{task.get("id")}" req_id="{task.get("req_id")}" points="{task.get("points")}" hours="{task.get("hours")}" priority="{task.get("priority")}">{task.text}</Task>'
            for task in tasks
        ])

        # Extract summary data
        total_tasks = task_tree.find('.//TotalTasks').text
        story_points = task_tree.find('.//StoryPoints').text
        expansion_ratio = task_tree.find('.//ExpansionRatio').text

        # Extract approval data
        approved = approval_tree.find('.//Decision').get('approved')
        quality_score = approval_tree.find('.//QualityScore').text
        risk_level = approval_tree.find('.//RiskLevel').text
        feedback = approval_tree.find('Feedback').text

        # Create comprehensive result
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<CompletePipelineResult>
    <PipelineInfo>
        <Status>{status}</Status>
        <Iterations>{iterations}</Iterations>
        <ProcessingSteps>4</ProcessingSteps>
    </PipelineInfo>

    <Analysis>
        <Domain>{domain}</Domain>
        <Complexity>{complexity}</Complexity>
    </Analysis>

    <Requirements count="{len(requirements)}">
{req_xml}
    </Requirements>

    <TaskBreakdown>
        <Summary>
            <TotalTasks>{total_tasks}</TotalTasks>
            <StoryPoints>{story_points}</StoryPoints>
            <ExpansionRatio>{expansion_ratio}</ExpansionRatio>
        </Summary>
        <Tasks>
{task_xml_formatted}
        </Tasks>
    </TaskBreakdown>

    <Approval>
        <Decision approved="{approved}">
            <QualityScore>{quality_score}</QualityScore>
            <RiskLevel>{risk_level}</RiskLevel>
        </Decision>
        <Feedback>{feedback}</Feedback>
    </Approval>
</CompletePipelineResult>"""


# Flask Application
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize pipeline with lazy plugin loading
try:
    print("🔄 Initializing X-Agent Pipeline with Lazy Plugin Loading...")
    pipeline = XAgentPipeline()
    
    # Get plugin statistics
    available_count = pipeline.product_manager.domain_registry.get_available_count()
    loaded_count = pipeline.product_manager.domain_registry.get_loaded_count()
    
    print(f"🔌 Domain Plugin System Initialized (Lazy Loading)")
    print(f"📦 Available domains: {available_count} (loaded: {loaded_count})")
    print(f"🚀 Startup complete - plugins load on-demand!")
    
except Exception as e:
    print(f"❌ CRITICAL: Failed to initialize pipeline: {e}")
    import traceback
    traceback.print_exc()
    
    # Create emergency fallback
    class EmergencyPipeline:
        def execute(self, content):
            return {
                'success': False,
                'status': 'Pipeline initialization failed - check console for details',
                'final_output': f'<ErrorResult>Pipeline failed to initialize: {str(e)}</ErrorResult>'
            }
        def format_document(self, content):
            return {'success': False, 'error': 'Pipeline not available'}
        def execute_with_formatted_input(self, content):
            return self.execute(content)
    
    pipeline = EmergencyPipeline()
    print("🚨 Emergency pipeline created - basic functionality only")

def _convert_xml_to_natural_language(xml_output: str, status: str) -> str:
    """Convert XML pipeline output to natural language"""
    try:
        tree = etree.fromstring(xml_output.encode())

        # Extract key information
        pipeline_status = tree.find('.//Status')
        iterations = tree.find('.//Iterations')
        domain = tree.find('.//Domain')
        complexity = tree.find('.//Complexity')

        # Extract requirements
        requirements = tree.findall('.//Requirements/Requirement')

        # Extract tasks
        tasks = tree.findall('.//Tasks/Task')
        total_tasks = tree.find('.//TotalTasks')
        story_points = tree.find('.//StoryPoints')

        # Extract approval info
        approved = tree.find('.//Decision')
        quality_score = tree.find('.//QualityScore')
        feedback = tree.find('.//Feedback')

        # Build natural language output
        output = []

        # Check for personalization info
        person_name = None
        company_name = None
        if hasattr(tree, 'find'):
            person_elem = tree.find('.//PersonName')
            company_elem = tree.find('.//CompanyName')
            if person_elem is not None:
                person_name = person_elem.text
            if company_elem is not None:
                company_name = company_elem.text

        # Header with personalization
        output.append("🚀 **X-Agent Pipeline Analysis Results**\n")
        output.append("=" * 50)

        # Personalized greeting
        if person_name or company_name:
            greeting_parts = []
            if person_name:
                greeting_parts.append(f"**{person_name}**")
            if company_name:
                greeting_parts.append(f"**{company_name}**")

            if len(greeting_parts) == 2:
                greeting = f"\n👋 Hello {greeting_parts[0]} from {greeting_parts[1]}!"
            elif person_name:
                greeting = f"\n👋 Hello {greeting_parts[0]}!"
            else:
                greeting = f"\n🏢 Analysis for {greeting_parts[0]}"

            output.append(greeting)
            output.append("\nHere's your personalized project analysis:\n")

        # Pipeline Summary
        status_icon = "✅" if "APPROVED" in status else "❌"
        output.append(f"\n{status_icon} **Project Status:** {status}")
        if iterations is not None:
            output.append(f"🔄 **Processing Iterations:** {iterations.text}")

        # Domain Analysis
        if domain is not None:
            output.append(f"\n📊 **Project Domain:** {domain.text.title()}")
        if complexity is not None:
            output.append(f"📈 **Complexity Level:** {complexity.text}/5")

        # Requirements Section
        if requirements:
            output.append(f"\n📋 **Requirements Identified ({len(requirements)}):**")
            for req in requirements:
                priority_icon = "🔥" if req.get('priority') == 'high' else "📝"
                output.append(f"   {priority_icon} {req.get('id')}: {req.text}")

        # Task Breakdown
        if tasks:
            output.append(f"\n🔧 **Task Breakdown ({len(tasks)} tasks):**")
            if total_tasks is not None and story_points is not None:
                output.append(f"   📊 Total Story Points: {story_points.text}")

            # Group tasks by requirement
            req_tasks = {}
            for task in tasks:
                req_id = task.get('req_id', 'OTHER')
                if req_id not in req_tasks:
                    req_tasks[req_id] = []
                req_tasks[req_id].append(task)

            for req_id, task_list in req_tasks.items():
                if req_id != 'DOMAIN':
                    output.append(f"\n   📌 Tasks for {req_id}:")
                    for task in task_list[:3]:  # Show first 3 tasks per requirement
                        points = task.get('points', '0')
                        output.append(f"      • {task.text} ({points} points)")
                    if len(task_list) > 3:
                        output.append(f"      ... and {len(task_list) - 3} more tasks")

        # Project Health Assessment
        if quality_score is not None:
            score = float(quality_score.text.replace('%', ''))
            if score >= 80:
                health = "Excellent ✨"
            elif score >= 60:
                health = "Good 👍"
            else:
                health = "Needs Improvement ⚠️"
            output.append(f"\n🎯 **Project Health:** {health} ({quality_score.text})")

        # Feedback and Recommendations
        if feedback is not None:
            feedback_text = feedback.text
            if "APPROVED" in feedback_text:
                output.append(f"\n✅ **Approval:** {feedback_text}")
                output.append("\n🎉 **Next Steps:**")
                output.append("   • Begin development sprint planning")
                output.append("   • Set up development environment")
                output.append("   • Create detailed technical specifications")
                output.append("   • Establish testing framework")
            else:
                output.append(f"\n❌ **Issues Identified:** {feedback_text}")
                output.append("\n🔧 **Recommendations:**")
                if "reduce scope" in feedback_text.lower():
                    output.append("   • Focus on core features first")
                    output.append("   • Consider phased development approach")
                    output.append("   • Prioritize high-impact requirements")
                if "too complex" in feedback_text.lower():
                    output.append("   • Break down complex requirements")
                    output.append("   • Simplify user interface design")
                    output.append("   • Consider using existing frameworks")
                if "quality" in feedback_text.lower():
                    output.append("   • Add comprehensive testing requirements")
                    output.append("   • Include code review processes")
                    output.append("   • Define quality metrics")

        # Project Summary
        output.append(f"\n📈 **Project Summary:**")
        if requirements and tasks:
            output.append(f"   • {len(requirements)} core requirements identified")
            output.append(f"   • {len(tasks)} implementation tasks defined")
        if story_points is not None:
            effort_weeks = int(story_points.text) // 10  # Rough estimate
            output.append(f"   • Estimated effort: {effort_weeks}-{effort_weeks+2} weeks")

        output.append("\n" + "=" * 50)
        output.append("💡 **Tip:** You can refine these requirements and run the analysis again for better results!")

        return "\n".join(output)

    except Exception as e:
        return f"Analysis completed, but there was an issue formatting the results: {str(e)}\n\nRaw output:\n{xml_output}"

@app.route('/api/process', methods=['POST'])
def process_document():
    """Process document through X-Agent pipeline with feedback loop"""
    try:
        # Read raw text from request body
        document_content = request.data.decode('utf-8')

        logger.info(f"📥 Received document content: {document_content[:200]}...")

        if not document_content or not document_content.strip():
            logger.error("No document content provided")
            return jsonify({"error": "No document content provided"}), 400

        # Execute pipeline with feedback loop
        logger.info("🚀 Starting X-Agent pipeline execution...")
        result = pipeline.execute(document_content)

        logger.info(f"✅ Pipeline completed: {result.get('status', 'unknown')} after {result.get('iterations', 0)} iterations")

        if result['success']:
            # Convert XML to natural language
            natural_output = _convert_xml_to_natural_language(result['final_output'], result['status'])
            return natural_output, 200, {'Content-Type': 'text/plain'}
        else:
            # Convert rejection to natural language
            natural_output = _convert_xml_to_natural_language(result['final_output'], result['status'])
            return natural_output, 200, {'Content-Type': 'text/plain'}

    except ImportError as e:
        logger.error(f"Import error: {e}")
        return jsonify({"error": f"Missing dependencies: {str(e)}"}), 500
    except Exception as e:
        logger.error(f"API error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get pipeline status"""
    try:
        status = {
            'status': 'running',
            'agents_available': 4,  # Analyst, PM, Task Manager, Scrum Master
            'max_iterations': pipeline.max_iterations,
            'feedback_loop_enabled': True
        }
        return jsonify(status), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat_with_llm():
    """Chat endpoint with LLM integration"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        chat_history = data.get('history', [])

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Get API key from environment
        api_key = os.environ.get('OPENAI_API_KEY') or os.environ.get('LLM_API_KEY')
        if not api_key:
            # Provide structured guidance for mobile app requirements
            mobile_guidance = """I'm here to help you structure requirements for your mobile app! Since no API key is configured, here's a structured approach:

**Mobile App Requirements Structure:**

REQ-001: Platform Support (iOS, Android, or both)
REQ-002: User Authentication (login/registration system)
REQ-003: Core User Interface (main screens and navigation)
REQ-004: Data Storage (local vs cloud storage needs)
REQ-005: Offline Functionality (what works without internet)
REQ-006: Push Notifications (user engagement features)
REQ-007: Performance Requirements (load times, responsiveness)
REQ-008: Security Requirements (data encryption, secure APIs)

**Key Questions to Consider:**
- Who is your target user?
- What's the main problem your app solves?
- What platforms do you want to support?
- Do you need real-time features?
- What data does your app collect/store?

Format your specific requirements as REQ-001: Description, REQ-002: Description, etc."""

            return jsonify({"response": mobile_guidance}), 200

        # Prepare system prompt for requirements gathering
        system_prompt = """You are an AI assistant helping users gather and structure software requirements for an intelligent agent pipeline. 

Your role is to:
1. Help users clarify their project requirements
2. Guide them to structure requirements in REQ-001, REQ-002 format
3. Ask clarifying questions about scope, stakeholders, and technical constraints
4. Suggest breaking down complex requirements into smaller, manageable pieces
5. For mobile apps, focus on platform, user experience, data flow, and performance requirements

Keep responses concise and focused on requirements gathering. Always format requirements as REQ-001: Description, REQ-002: Description, etc."""

        # Build conversation context
        messages = [{"role": "system", "content": system_prompt}]

        # Add recent chat history (last 6 messages to stay within token limits)
        recent_history = chat_history[-6:] if len(chat_history) > 6 else chat_history
        for msg in recent_history:
            role = "user" if msg['type'] == 'user' else "assistant"
            messages.append({"role": role, "content": msg['content']})

        messages.append({"role": "user", "content": user_message})

        # Call OpenAI API (you can replace with other LLM providers)
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-3.5-turbo',
                'messages': messages,
                'max_tokens': 500,
                'temperature': 0.7
            },
            timeout=30
        )

        if response.status_code == 200:
            ai_response = response.json()['choices'][0]['message']['content']
            return jsonify({"response": ai_response}), 200
        else:
            logger.error(f"LLM API error: {response.status_code} - {response.text}")
            return jsonify({
                "response": "I'm having trouble connecting to the AI service. Please try again or structure your requirements manually using REQ-001, REQ-002 format."
            }), 200

    except Exception as e:
        logger.error(f"Chat API error: {e}")
        return jsonify({
            "response": "I encountered an error. Please try again or format your requirements as REQ-001: Description, REQ-002: Description, etc."
        }), 200

@app.route('/api/format-document', methods=['POST'])
def format_document():
    """Format document with system standards and keywords"""
    try:
        data = request.get_json()
        raw_content = data.get('content', '')
        target_domain = data.get('domain', None)
        
        if not raw_content:
            return jsonify({"error": "No content provided"}), 400
        
        # Initialize document formatter
        from document_formatter_agent import DocumentFormatterXAgent
        formatter = DocumentFormatterXAgent()
        
        # Format document
        result = formatter.format_document(raw_content, target_domain)
        
        return jsonify({
            "success": True,
            "formatted_content": result['formatted_content'],
            "requirements": result['extracted_requirements'],
            "domain": result['identified_domain'],
            "stakeholders": result['stakeholders'],
            "validation_score": result['validation_score']
        }), 200
        
    except Exception as e:
        logger.error(f"Document formatting error: {e}")
        return jsonify({"error": f"Formatting failed: {str(e)}"}), 500

@app.route('/api/create-plugin', methods=['POST'])
def create_domain_plugin():
    """Create new domain plugin (backend only)"""
    try:
        data = request.get_json()
        
        # Initialize plugin creator
        from domain_plugin_creator_agent import DomainPluginCreatorXAgent
        creator = DomainPluginCreatorXAgent()
        
        # Check if this is content analysis or plugin creation
        if 'content' in data:
            # Analyze content for plugin suggestions
            result = creator.analyze_content_for_plugin(data['content'])
            return jsonify({
                "success": True,
                "type": "analysis",
                "analysis": result['analysis'],
                "suggested_plugin": result['suggested_plugin'],
                "confidence": result['confidence']
            }), 200
        
        elif 'plugin_spec' in data:
            # Create actual plugin
            result = asyncio.run(creator.create_domain_plugin(data['plugin_spec']))
            
            if result['success']:
                # Reload domain registry to include new plugin
                pipeline.product_manager.domain_registry.rescan_plugins()
                
                return jsonify({
                    "success": True,
                    "type": "creation",
                    "domain_name": result['domain_name'],
                    "file_path": result['file_path'],
                    "registered": result['registered'],
                    "quality_analysis": result['analysis']
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "error": result['error']
                }), 400
        
        else:
            return jsonify({"error": "Must provide either 'content' for analysis or 'plugin_spec' for creation"}), 400
        
    except Exception as e:
        logger.error(f"Plugin creation error: {e}")
        return jsonify({"error": f"Plugin creation failed: {str(e)}"}), 500

@app.route('/api/list-domains', methods=['GET'])
def list_available_domains():
    """List all available domain plugins"""
    try:
        domains = pipeline.product_manager.domain_registry.list_domains()
        return jsonify({
            "success": True,
            "domains": domains,
            "total_count": len(domains)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    """Root route - eliminates 404 errors"""
    try:
        # Check if pipeline is initialized
        pipeline_status = "initialized" if pipeline else "not initialized"
        
        # Get plugin count if available
        plugin_count = 0
        if pipeline and hasattr(pipeline, 'product_manager'):
            try:
                domains = pipeline.product_manager.domain_registry.list_domains()
                plugin_count = len(domains)
            except:
                plugin_count = 0
        
        return jsonify({
            "service": "X-Agents Backend API",
            "status": "running",
            "pipeline_status": pipeline_status,
            "available_plugins": plugin_count,
            "frontend_url": "http://localhost:5173",
            "api_endpoints": {
                "process_documents": "POST /api/process",
                "format_documents": "POST /api/format-document", 
                "chat": "POST /api/chat",
                "status": "GET /api/status",
                "health": "GET /health"
            },
            "message": "X-Agents Backend is running successfully!"
        }), 200
    except Exception as e:
        return jsonify({
            "service": "X-Agents Backend API", 
            "status": "running_with_errors",
            "error": str(e)
        }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "X-Agents Backend with Feedback Loop"}), 200

@app.route('/api/plugin-creation-cost', methods=['POST'])
def estimate_plugin_creation_cost():
    """Estimate cost for creating custom plugin"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        
        if not content:
            return jsonify({"error": "No content provided"}), 400
        
        # Quick analysis for cost estimation using the registry
        registry = pipeline.product_manager.domain_registry
        estimated_cost = registry._estimate_plugin_cost(content, {'complexity_score': 0.5})
        
        # Analysis factors for transparency
        complexity_factors = {
            'word_count': len(content.split()),
            'estimated_complexity': 0.5,
            'base_cost': 50,
            'total_cost': estimated_cost
        }
        
        return jsonify({
            "estimated_cost": f"${estimated_cost}",
            "complexity_analysis": complexity_factors,
            "cost_breakdown": {
                "base_fee": "$50 (plugin creation)",
                "complexity_fee": f"${estimated_cost - 50} (based on content complexity)",
                "total": f"${estimated_cost}"
            },
            "includes": [
                "Custom domain plugin creation",
                "Integration with existing system", 
                "Quality validation and testing",
                "Lifetime usage rights"
            ],
            "note": "Cost is charged only when plugin is successfully created and used"
        }), 200
        
    except Exception as e:
        logger.error(f"Plugin cost estimation error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/plugin-stats', methods=['GET'])
def get_plugin_stats():
    """Get plugin loading and creation statistics"""
    try:
        registry = pipeline.product_manager.domain_registry
        stats = registry.get_custom_plugin_stats()
        
        return jsonify({
            "success": True,
            "available_domains": registry.get_available_count(),
            "loaded_domains": registry.get_loaded_count(),
            "custom_plugins_created": stats['total_custom_plugins'],
            "total_revenue": f"${stats['total_revenue']:.2f}",
            "loaded_custom_plugins": stats['loaded_custom_plugins'],
            "domains": registry.list_domains()
        }), 200
        
    except Exception as e:
        logger.error(f"Plugin stats error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/custom-plugins', methods=['GET'])
def list_custom_plugins():
    """List all custom-created plugins"""
    try:
        registry = pipeline.product_manager.domain_registry
        custom_plugins = []
        
        for domain_name, plugin_info in registry.available_domains.items():
            if plugin_info.get('custom_created', False):
                custom_plugins.append({
                    'domain_name': domain_name,
                    'creation_cost': plugin_info.get('creation_cost', 0),
                    'created_timestamp': plugin_info.get('created_timestamp', 0),
                    'loaded': plugin_info.get('loaded', False),
                    'file_path': plugin_info.get('file_path', '')
                })
        
        return jsonify({
            "success": True,
            "custom_plugins": custom_plugins,
            "total_count": len(custom_plugins),
            "total_revenue": sum(p['creation_cost'] for p in custom_plugins)
        }), 200
        
    except Exception as e:
        logger.error(f"Custom plugins listing error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/test-plugin-creation', methods=['POST'])
def test_plugin_creation():
    """Test endpoint to trigger plugin creation for unknown domains"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        force_creation = data.get('force_creation', False)
        
        if not content:
            return jsonify({"error": "No content provided"}), 400
        
        # Test the plugin creation workflow
        registry = pipeline.product_manager.domain_registry
        
        if force_creation:
            # Force creation even if existing plugin might work
            handler, domain, newly_created, cost = registry._create_custom_plugin(content)
        else:
            # Normal workflow - only create if no suitable plugin exists
            handler, domain, newly_created, cost = registry.get_handler_or_create(content)
        
        return jsonify({
            "success": True,
            "domain": domain,
            "plugin_created": newly_created,
            "creation_cost": cost,
            "handler_available": handler is not None,
            "message": f"{'Created new plugin' if newly_created else 'Used existing plugin'} for domain: {domain}"
        }), 200
        
    except Exception as e:
        logger.error(f"Plugin creation test error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import sys
    import traceback
    
    try:
        print("🚀 Starting X-Agent Backend Server with Feedback Loop...")
        print("📡 API available at http://0.0.0.0:5002")
        print("🔍 DEBUG: Python process started successfully")
        
        # Force output flush for parallel mode visibility
        sys.stdout.flush()
        sys.stderr.flush()
        print("🔗 Endpoints:")
        print("   POST /api/process - Process documents with feedback loop")
        print("   POST /api/chat    - LLM-powered requirements chat")
        print("   GET  /api/status  - Get pipeline status")
        print("   GET  /health     - Health check")
        print("\n🔄 Feedback Loop Features:")
        print("   • Analyst → PM → Task Manager → Scrum Master")
        print("   • PM ↔ Scrum Master feedback loop (max 3 iterations)")
        print("   • Automatic scope reduction and quality improvement")

        # Test dependencies first
        print("\n🔧 Checking dependencies...")
        try:
            import flask
            print("✅ Flask available")
            from flask_cors import CORS
            print("✅ Flask-CORS available")
            from lxml import etree
            print("✅ lxml available")
            import requests
            print("✅ requests available")
        except ImportError as e:
            print(f"❌ Missing dependency: {e}")
            print("📦 Installing dependencies...")
            import subprocess
            subprocess.check_call(['pip', 'install', 'flask', 'flask-cors', 'lxml', 'requests'])
            print("✅ Dependencies installed")

        # Check if port is available
        print("\n🔍 Checking port availability...")
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('127.0.0.1', 5000))
            if result == 0:
                print("⚠️  Port 5000 is already in use, but continuing...")
            else:
                print("✅ Port 5000 is available")

        print(f"\n✅ Flask server starting on 0.0.0.0:5000...")
        print("🔧 Binding to 0.0.0.0:5000 for Replit compatibility...")
        
        # Add signal handling and process monitoring
        import signal
        import os
        
        def signal_handler(sig, frame):
            print(f'\n🛑 Received signal {sig}, shutting down gracefully...')
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        print(f"🔍 DEBUG: Flask process PID: {os.getpid()}")
        
        # Force flush output for parallel mode
        sys.stdout.flush()
        sys.stderr.flush()

        print("🔍 DEBUG: About to start Flask server...")
        print(f"🔍 DEBUG: Pipeline object: {type(pipeline)}")
        print(f"🔍 DEBUG: Flask app: {app}")
        sys.stdout.flush()
        
        # Test if we can create a simple route response
        try:
            with app.test_client() as client:
                print("✅ Flask app test client created successfully")
        except Exception as test_e:
            print(f"❌ Flask app test failed: {test_e}")
        
        # Enhanced Flask startup with better error handling
        try:
            print("🚀 Starting Flask with debug output...")
            app.run(
                host='0.0.0.0', 
                port=5002, 
                debug=False, 
                threaded=True, 
                use_reloader=False,
                use_debugger=False
            )
        except Exception as e:
            print(f"❌ FLASK STARTUP ERROR: {e}")
            print("🔍 This is why your Full Stack workflow isn't working!")
            print("🔍 Error details:")
            import traceback
            traceback.print_exc()
            
            # Try to give more specific error info
            if "Address already in use" in str(e):
                print("💡 Port 5000 is busy - trying to find what's using it...")
                import subprocess
                try:
                    result = subprocess.run(['lsof', '-i', ':5000'], capture_output=True, text=True)
                    print(f"Port 5000 usage: {result.stdout}")
                except:
                    print("Could not check port usage")
            
            sys.exit(1)

    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port 5000 is already in use. Attempting cleanup...")
            import subprocess
            import time
            try:
                # Kill any existing processes on port 5000
                subprocess.run(['lsof', '-ti:5000'], capture_output=True, check=False)
                subprocess.run(['kill', '-9'] + subprocess.run(['lsof', '-ti:5000'], capture_output=True, text=True).stdout.split(), check=False)
                time.sleep(2)
                print("🔄 Retrying Flask server startup...")
                app.run(host='0.0.0.0', port=5002, debug=False, threaded=True, use_reloader=False)
            except Exception as retry_e:
                print(f"❌ Failed to restart: {retry_e}")
                print("💡 Try manually stopping the workflow and restarting it")
        else:
            print(f"❌ Network error: {e}")
            import traceback
            traceback.print_exc()
    except Exception as e:
        print(f"❌ CRITICAL ERROR: Flask server failed to start: {e}")
        print("🔍 Full error details:")
        import traceback
        traceback.print_exc()
        
        # Force error output to be visible in parallel mode
        sys.stderr.flush()
        sys.stdout.flush()
        
        print("\n💡 This is why your dashboard isn't working!")
        print("   The Python backend process is crashing, so the React frontend can't connect.")
        print("   Fix this error to get your Full Stack Dev workflow working.")