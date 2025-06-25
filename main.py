
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
        """Extract requirements from content with optional feedback adjustments"""
        
        # Extract REQ-xxx patterns
        req_pattern = r'REQ-(\d+)[:\s]+(.*?)(?=\n|REQ-|\Z)'
        requirements = []
        
        for match in re.finditer(req_pattern, content, re.DOTALL):
            requirements.append({
                'id': f"REQ-{match.group(1).zfill(3)}",
                'title': match.group(2).strip()[:50],
                'priority': 'high' if 'critical' in match.group(2).lower() else 'medium'
            })
        
        # If no explicit requirements found, generate from content
        if not requirements:
            words = content.split()
            for i in range(min(5, len(words) // 20)):
                requirements.append({
                    'id': f"REQ-{i+1:03d}",
                    'title': f"Implement {' '.join(words[i*20:(i+1)*20])}"[:50],
                    'priority': 'medium'
                })
        
        # Apply feedback adjustments if provided
        if feedback_context:
            requirements = self._apply_feedback_to_requirements(requirements, feedback_context)
        
        # Basic stakeholder detection
        stakeholders = []
        if 'user' in content:
            stakeholders.append('End Users')
        if 'developer' in content:
            stakeholders.append('Development Team')
        if 'business' in content:
            stakeholders.append('Business Stakeholders')
        
        return {
            'domain': domain,
            'requirements': requirements,
            'stakeholders': stakeholders,
            'req_count': len(requirements),
            'feedback_applied': feedback_context is not None
        }
    
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
                base_hours = 12 if pattern == 'Implement' else 8
                
                if req_priority == 'high':
                    story_points = base_points + 1
                    hours = base_hours + 4
                else:
                    story_points = base_points
                    hours = base_hours
                
                tasks.append({
                    'id': f"TASK-{task_id:03d}",
                    'title': f"{pattern} {req_title[:30]}",
                    'req_id': req_id,
                    'story_points': story_points,
                    'hours': hours,
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
        
        while iteration < self.max_iterations:
            iteration += 1
            logger.info(f"\n--- Iteration {iteration} ---")
            
            # Product Manager processes (initial analysis or feedback)
            logger.info("📋 Product Manager: Creating/updating requirements")
            pm_output = self.product_manager.process(current_input)
            
            # Task Manager breaks down requirements
            logger.info("🔧 Task Manager: Breaking down into tasks")
            task_output = self.task_manager.process(pm_output)
            
            # Scrum Master reviews and approves/rejects
            logger.info("✅ Scrum Master: Reviewing for approval")
            approval_output = self.scrum_master.process(task_output)
            
            # Check approval
            approval_tree = etree.fromstring(approval_output.encode())
            approved = approval_tree.find('.//Decision').get('approved') == 'true'
            feedback_text = approval_tree.find('Feedback').text
            
            if approved:
                logger.info(f"\n🎉 PROJECT APPROVED after {iteration} iteration(s)!")
                return {
                    'success': True,
                    'iterations': iteration,
                    'final_output': approval_output,
                    'status': 'APPROVED'
                }
            
            logger.info(f"❌ Project rejected: {feedback_text}")
            
            if iteration >= self.max_iterations:
                logger.info(f"\n💔 PROJECT REJECTED after {self.max_iterations} iterations")
                return {
                    'success': False,
                    'iterations': iteration,
                    'final_output': approval_output,
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


# Flask Application
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize pipeline
pipeline = XAgentPipeline()

@app.route('/api/process', methods=['POST'])
def process_document():
    """Process document through X-Agent pipeline with feedback loop"""
    try:
        # Read raw text from request body
        document_content = request.data.decode('utf-8')
        
        if not document_content or not document_content.strip():
            return jsonify({"error": "No document content provided"}), 400
        
        # Execute pipeline with feedback loop
        result = pipeline.execute(document_content)
        
        if result['success']:
            # Return the XML result as plain text for frontend parsing
            return result['final_output'], 200, {'Content-Type': 'text/plain'}
        else:
            # Return rejection with details
            return result['final_output'], 200, {'Content-Type': 'text/plain'}
            
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

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "X-Agents Backend with Feedback Loop"}), 200

if __name__ == "__main__":
    print("🚀 Starting X-Agent Backend Server with Feedback Loop...")
    print("📡 API available at http://0.0.0.0:5000")
    print("🔗 Endpoints:")
    print("   POST /api/process - Process documents with feedback loop")
    print("   GET  /api/status  - Get pipeline status")
    print("   GET  /health     - Health check")
    print("\n🔄 Feedback Loop Features:")
    print("   • Analyst → PM → Task Manager → Scrum Master")
    print("   • PM ↔ Scrum Master feedback loop (max 3 iterations)")
    print("   • Automatic scope reduction and quality improvement")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
