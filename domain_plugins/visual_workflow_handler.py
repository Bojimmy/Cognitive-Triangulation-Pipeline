
#!/usr/bin/env python3
"""
Visual Workflow Domain Handler
Handles canvas, drag-and-drop, and visual workflow requirements
"""

from .base_handler import BaseDomainHandler
from typing import Dict, List, Any

class VisualWorkflowDomainHandler(BaseDomainHandler):
    """Visual Workflow and Canvas domain handler"""
    
    def get_domain_name(self) -> str:
        return 'visual_workflow'
    
    def get_detection_keywords(self) -> List[str]:
        return [
            'canvas', 'visual', 'workflow', 'drag', 'drop', 'flowchart',
            'diagram', 'node', 'edge', 'graph', 'builder', 'designer',
            'visual editor', 'flow builder', 'process designer'
        ]
    
    def get_priority_score(self) -> int:
        return 4  # High priority - specific UI/UX requirements
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()
        
        # Canvas System
        if any(term in content_lower for term in ['canvas', 'visual', 'draw', 'design']):
            requirements.append({
                'title': 'Interactive Canvas System with Zoom and Pan Controls',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Drag and Drop
        if any(term in content_lower for term in ['drag', 'drop', 'draggable', 'move']):
            requirements.append({
                'title': 'Drag-and-Drop Interface with Node Manipulation',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Node Management
        if any(term in content_lower for term in ['node', 'element', 'component', 'block']):
            requirements.append({
                'title': 'Node Creation and Management System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Connection System
        if any(term in content_lower for term in ['connection', 'edge', 'link', 'flow']):
            requirements.append({
                'title': 'Node Connection and Edge Management System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Workflow Logic
        if any(term in content_lower for term in ['workflow', 'process', 'logic', 'automation']):
            requirements.append({
                'title': 'Workflow Logic Engine and Process Execution',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Template System
        if any(term in content_lower for term in ['template', 'preset', 'library', 'gallery']):
            requirements.append({
                'title': 'Template Library and Pre-built Component System',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Export/Import
        if any(term in content_lower for term in ['export', 'import', 'save', 'load']):
            requirements.append({
                'title': 'Workflow Export/Import and Sharing System',
                'priority': 'medium',
                'category': 'functional'
            })
        
        return requirements
    
    def extract_stakeholders(self, content: str) -> List[str]:
        """Extract visual workflow domain stakeholders"""
        stakeholders = ['Visual Designers', 'Workflow Users', 'UI/UX Team', 'Development Team']
        content_lower = content.lower()
        
        if any(term in content_lower for term in ['business', 'analyst']):
            stakeholders.append('Business Analysts')
        if any(term in content_lower for term in ['process', 'automation']):
            stakeholders.append('Process Managers')
        if any(term in content_lower for term in ['admin', 'administrator']):
            stakeholders.append('System Administrators')
            
        return stakeholders
