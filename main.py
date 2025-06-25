
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
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from lxml import etree
import logging
import re
import os
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseXAgent(ABC):
    """Base X-Agent with XML processing and performance tracking"""
    
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.metrics = {'total_time': 0}
    
    def process(self, input_xml: str) -> str:
        """Main processing with timing"""
        start_time = time.time()
        
        # Parse input
        parsed = etree.fromstring(input_xml.encode())
        
        # Process with agent intelligence
        result = self._process_intelligence(parsed)
        
        # Generate output XML
        output_xml = self._generate_xml(result)
        
        self.metrics['total_time'] = (time.time() - start_time) * 1000
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
        content = etree.tostring(parsed_input, encoding='unicode', method='text').lower()
        
        # Simple domain detection
        if any(word in content for word in ['canvas', 'visual', 'workflow', 'drag']):
            domain = 'visual_workflow'
        elif any(word in content for word in ['enterprise', 'compliance', 'security']):
            domain = 'enterprise'
        else:
            domain = 'general'
        
        return {
            'domain': domain,
            'complexity': min(len(content) // 500, 5),
            'content': content[:2000]  # Keep original content for PM
        }
    
    def _generate_xml(self, result: dict) -> str:
        """Generate analysis XML for Product Manager"""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<AnalysisPacket>
    <Domain>{result['domain']}</Domain>
    <Complexity>{result['complexity']}</Complexity>
    <Content>{result['content']}</Content>
</AnalysisPacket>"""


class ProductManagerXAgent(BaseXAgent):
    """Extracts requirements and identifies stakeholders (can process feedback)"""
    
    def __init__(self):
        super().__init__("ProductManagerXAgent")
    
    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Extract requirements - handles both initial analysis and feedback"""
        
        # Check if this is feedback from Scrum Master
        feedback_elem = parsed_input.find('Feedback')
        if feedback_elem is not None:
            return self._process_scrum_feedback(parsed_input)
        
        # Normal initial processing from Analyst
        domain = parsed_input.find('Domain').text
        content = parsed_input.find('Content').text
        
        return self._extract_requirements(domain, content)
    
    def _extract_requirements(self, domain: str, content: str, feedback_context: str = None) -> dict:
        """Extract requirements from content with intelligent natural language processing"""
        
        requirements = []
        
        # First, try to extract explicit REQ-xxx patterns
        req_pattern = r'REQ-(\d+)[:\s]+(.*?)(?=\n|REQ-|\Z)'
        for match in re.finditer(req_pattern, content, re.DOTALL):
            requirements.append({
                'id': f"REQ-{match.group(1).zfill(3)}",
                'title': match.group(2).strip()[:100],  # Increased length
                'priority': 'high' if any(word in match.group(2).lower() for word in ['critical', 'must', 'essential', 'required']) else 'medium'
            })
        
        # If no explicit requirements found, use intelligent extraction
        if not requirements:
            requirements = self._extract_natural_language_requirements(content)
        
        # Apply feedback adjustments if provided
        if feedback_context:
            requirements = self._apply_feedback_to_requirements(requirements, feedback_context)
        
        # Enhanced stakeholder detection
        stakeholders = self._detect_stakeholders(content)
        
        return {
            'domain': domain,
            'requirements': requirements,
            'stakeholders': stakeholders,
            'req_count': len(requirements),
            'feedback_applied': feedback_context is not None
        }
    
    def _extract_natural_language_requirements(self, content: str) -> list:
        """Extract meaningful requirements from natural language text"""
        requirements = []
        content_lower = content.lower()
        
        # Define requirement patterns and keywords
        requirement_patterns = [
            # API and Integration patterns
            (r'api\s+for\s+([^.]+)', 'API Integration', 'high'),
            (r'integrate\s+with\s+([^.]+)', 'System Integration', 'high'),
            (r'third[- ]party\s+([^.]+)', 'Third-Party Integration', 'medium'),
            
            # Mobile and Web patterns
            (r'mobile\s+app\s+for\s+([^.]+)', 'Mobile Application', 'high'),
            (r'web\s+app\s+for\s+([^.]+)', 'Web Application', 'high'),
            (r'dashboard\s+for\s+([^.]+)', 'Dashboard Interface', 'medium'),
            
            # Security and Compliance
            (r'security\s+([^.]+)', 'Security Framework', 'high'),
            (r'privacy\s+([^.]+)', 'Privacy Compliance', 'high'),
            (r'compliance\s+([^.]+)', 'Regulatory Compliance', 'high'),
            (r'authentication\s+([^.]+)', 'User Authentication', 'high'),
            
            # Performance and Reliability
            (r'(\d+\.?\d*%)\s+uptime', 'System Reliability', 'high'),
            (r'real[- ]time\s+([^.]+)', 'Real-Time Processing', 'high'),
            (r'performance\s+([^.]+)', 'Performance Requirements', 'medium'),
            
            # Data and Analytics
            (r'analytics\s+([^.]+)', 'Analytics Platform', 'medium'),
            (r'reporting\s+([^.]+)', 'Reporting System', 'medium'),
            (r'data\s+([^.]+)', 'Data Management', 'medium'),
            
            # User Experience
            (r'user\s+interface\s+for\s+([^.]+)', 'User Interface', 'medium'),
            (r'notification\s+([^.]+)', 'Notification System', 'medium'),
            (r'alert\s+([^.]+)', 'Alert System', 'medium'),
        ]
        
        req_id = 1
        found_requirements = set()  # Prevent duplicates
        
        # Extract using patterns
        for pattern, req_type, priority in requirement_patterns:
            matches = re.finditer(pattern, content_lower)
            for match in matches:
                context = match.group(1).strip()[:60]  # Get context
                title = f"{req_type}: {context}"
                
                if title not in found_requirements and len(context) > 3:
                    requirements.append({
                        'id': f"REQ-{req_id:03d}",
                        'title': title.title(),
                        'priority': priority
                    })
                    found_requirements.add(title)
                    req_id += 1
        
        # Extract sentence-based requirements
        sentences = re.split(r'[.!?]+', content)
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:  # Skip very short sentences
                # Look for requirement indicators
                requirement_indicators = [
                    'need', 'require', 'must', 'should', 'implement', 'develop',
                    'create', 'build', 'support', 'provide', 'enable', 'allow'
                ]
                
                sentence_lower = sentence.lower()
                if any(indicator in sentence_lower for indicator in requirement_indicators):
                    # Clean up the sentence for requirement title
                    clean_sentence = sentence.replace('\n', ' ').strip()
                    if len(clean_sentence) > 10 and clean_sentence not in found_requirements:
                        priority = 'high' if any(word in sentence_lower for word in ['critical', 'must', 'essential']) else 'medium'
                        requirements.append({
                            'id': f"REQ-{req_id:03d}",
                            'title': clean_sentence[:100],  # Limit length
                            'priority': priority
                        })
                        found_requirements.add(clean_sentence)
                        req_id += 1
                        
                        if len(requirements) >= 12:  # Limit total requirements
                            break
        
        # If still no requirements, create basic functional requirements
        if not requirements:
            basic_reqs = [
                "Core System Functionality",
                "User Interface Implementation",
                "Data Management System",
                "Security and Authentication",
                "Performance Optimization"
            ]
            
            for i, req_title in enumerate(basic_reqs):
                requirements.append({
                    'id': f"REQ-{i+1:03d}",
                    'title': req_title,
                    'priority': 'medium'
                })
        
        return requirements[:10]  # Limit to 10 requirements max
    
    def _detect_stakeholders(self, content: str) -> list:
        """Enhanced stakeholder detection"""
        stakeholders = []
        content_lower = content.lower()
        
        stakeholder_patterns = {
            'End Users': ['user', 'citizen', 'customer', 'client', 'consumer'],
            'Development Team': ['developer', 'engineer', 'programmer', 'technical team'],
            'Business Stakeholders': ['business', 'management', 'executive', 'stakeholder'],
            'System Administrators': ['admin', 'administrator', 'ops', 'devops'],
            'Government Agencies': ['government', 'agency', 'municipal', 'city', 'public'],
            'Emergency Services': ['emergency', 'police', 'fire', 'ambulance', 'first responder'],
            'Traffic Authorities': ['traffic', 'transportation', 'transit', 'dot']
        }
        
        for stakeholder, keywords in stakeholder_patterns.items():
            if any(keyword in content_lower for keyword in keywords):
                stakeholders.append(stakeholder)
        
        return stakeholders if stakeholders else ['End Users', 'Development Team']
    
    def _process_scrum_feedback(self, feedback_input: etree.Element) -> dict:
        """Process feedback from Scrum Master and create updated PRD"""
        domain = feedback_input.find('Domain').text
        feedback = feedback_input.find('Feedback').text
        original_content = feedback_input.find('OriginalContent').text
        
        logger.info(f"[Product Manager] Processing Scrum Master feedback: {feedback}")
        
        # Apply feedback to create updated requirements
        return self._extract_requirements(domain, original_content, feedback)
    
    def _apply_feedback_to_requirements(self, requirements: list, feedback: str) -> list:
        """Apply Scrum Master feedback to adjust requirements"""
        
        if 'reduce scope' in feedback.lower():
            # Keep only high priority requirements
            high_priority_reqs = [req for req in requirements if req['priority'] == 'high']
            logger.info(f"Reducing scope: {len(requirements)} → {len(high_priority_reqs)} requirements")
            return high_priority_reqs[:5]  # Max 5 high priority
            
        elif 'too complex' in feedback.lower():
            # Simplify requirement titles and reduce count
            simplified_reqs = []
            for i, req in enumerate(requirements[:6]):  # Limit to 6
                simplified_reqs.append({
                    'id': req['id'],
                    'title': f"Basic {req['title'][:30]}",  # Simplify titles
                    'priority': 'medium'  # Lower priority
                })
            logger.info(f"Simplifying complexity: {len(requirements)} → {len(simplified_reqs)} simplified requirements")
            return simplified_reqs
            
        elif 'insufficient quality' in feedback.lower():
            # Add quality assurance requirements
            enhanced_reqs = requirements[:4]  # Reduce base requirements
            for req in enhanced_reqs:
                # Add quality sub-requirement
                enhanced_reqs.append({
                    'id': f"{req['id']}-QA",
                    'title': f"Quality Testing for {req['title'][:25]}",
                    'priority': 'high'
                })
            logger.info(f"Adding quality focus: {len(requirements)} → {len(enhanced_reqs)} requirements with QA")
            return enhanced_reqs
            
        elif 'too many tasks' in feedback.lower():
            # Significantly reduce requirements
            core_reqs = requirements[:3]  # Only top 3
            logger.info(f"Major scope reduction: {len(requirements)} → {len(core_reqs)} core requirements")
            return core_reqs
            
        else:
            # Default: moderate reduction
            moderate_reqs = requirements[:7]
            logger.info(f"Moderate adjustment: {len(requirements)} → {len(moderate_reqs)} requirements")
            return moderate_reqs
    
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
        
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<TaskPacket>
    <ProjectInfo>
        <Domain>{result['domain']}</Domain>
        <RequirementCount>{result['req_count']}</RequirementCount>
    </ProjectInfo>{feedback_note}
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
        domain = parsed_input.find('.//Domain').text
        requirements = parsed_input.findall('.//Requirement')
        feedback_applied = parsed_input.find('FeedbackApplied') is not None
        
        if feedback_applied:
            logger.info(f"[Task Manager] Processing updated requirements ({len(requirements)} requirements)")
        
        tasks = []
        task_id = 1
        
        # Generate tasks for each requirement
        for req in requirements:
            req_id = req.get('id')
            req_title = req.text
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
    """Pipeline with PM ↔ Scrum Master feedback loop"""
    
    def __init__(self):
        self.analyst = AnalystXAgent()
        self.product_manager = ProductManagerXAgent()
        self.task_manager = TaskManagerXAgent()
        self.scrum_master = POScrumMasterXAgent()
        self.max_iterations = 3
    
    def execute(self, document_content: str) -> dict:
        """Execute pipeline with PM-Scrum Master feedback loop"""
        
        logger.info("🔍 Step 1: Document Analysis (runs once)")
        # Step 1: Analyst runs once
        document_xml = f"<?xml version='1.0'?><Document>{document_content}</Document>"
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
        content = analysis_tree.find('Content').text
        
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<FeedbackPacket>
    <Domain>{domain}</Domain>
    <Feedback>{feedback}</Feedback>
    <OriginalContent>{content}</OriginalContent>
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

# Initialize pipeline
pipeline = XAgentPipeline()

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
        
        # Header
        output.append("🚀 **X-Agent Pipeline Analysis Results**\n")
        output.append("=" * 50)
        
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
            
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({"error": str(e)}), 500

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

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "X-Agents Backend with Feedback Loop"}), 200

if __name__ == "__main__":
    print("🚀 Starting X-Agent Backend Server with Feedback Loop...")
    print("📡 API available at http://0.0.0.0:5002")
    print("🔗 Endpoints:")
    print("   POST /api/process - Process documents with feedback loop")
    print("   POST /api/chat    - LLM-powered requirements chat")
    print("   GET  /api/status  - Get pipeline status")
    print("   GET  /health     - Health check")
    print("\n🔄 Feedback Loop Features:")
    print("   • Analyst → PM → Task Manager → Scrum Master")
    print("   • PM ↔ Scrum Master feedback loop (max 3 iterations)")
    print("   • Automatic scope reduction and quality improvement")
    
    app.run(host='0.0.0.0', port=5002, debug=True, threaded=True)
