#!/usr/bin/env python3
"""
Education Management Domain Handler
A domain plugin to handle the management and administration of educational institutions, including features for monitoring student progress, assigning custom content, and enabling communication between parents and teachers.
"""

from .base_handler import BaseDomainHandler
from typing import Dict, List, Any

class EducationManagementDomainHandler(BaseDomainHandler):
    """Education Management domain handler"""
    
    def get_domain_name(self) -> str:
        return 'education_management'
    
    def get_detection_keywords(self) -> List[str]:
        return ['student', 'progress', 'custom content', 'dashboard', 'gamification', 'teacher']
    
    def get_priority_score(self) -> int:
        return 5  # 1-5 scale
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()
        
        # Generate 5-8 functional requirements based on domain analysis
        if 'dashboard' in content_lower:
            requirements.append({
                'type': 'functional',
                'description': 'a dashboard to monitor student progress, assign custom content, and generate reports'
            })
        if 'gamification' in content_lower:
            requirements.append({
                'type': 'functional',
                'description': 'include gamification elements to enhance engagement'
            })
        if 'progress' in content_lower and 'communicate' in content_lower:
            requirements.append({
                'type': 'functional',
                'description': "a portal to view their child's progress and communicate with teachers"
            })
        if 'scalability' in content_lower:
            requirements.append({
                'type': 'non-functional',
                'description': 'use modular architecture for scalability'
            })
        if 'error handling' in content_lower:
            requirements.append({
                'type': 'non-functional',
                'description': 'implement comprehensive error handling'
            })
        if 'security' in content_lower:
            requirements.append({
                'type': 'non-functional',
                'description': 'follow security best practices'
            })
        if 'testing' in content_lower:
            requirements.append({
                'type': 'non-functional',
                'description': 'include automated testing framework'
            })
        
        return requirements
    
    def extract_stakeholders(self, content: str) -> List[str]:
        """Extract domain-specific stakeholders"""
        base_stakeholders = ['school administrators', 'teachers', 'parents', 'students']
        
        # Add intelligent stakeholder detection based on content
        if 'administrator' in content.lower():
            base_stakeholders.append('IT administrators')
        if 'counselor' in content.lower():
            base_stakeholders.append('school counselors')
        if 'principal' in content.lower():
            base_stakeholders.append('school principals')
        
        return base_stakeholders
