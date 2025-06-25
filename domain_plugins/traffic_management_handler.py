
#!/usr/bin/env python3
"""
Traffic Management Domain Handler
Extracted from main.py ProductManagerXAgent
"""

from .base_handler import BaseDomainHandler
from typing import Dict, List, Any

class TrafficManagementDomainHandler(BaseDomainHandler):
    """Traffic Management domain handler"""
    
    def get_domain_name(self) -> str:
        return 'traffic_management'
    
    def get_detection_keywords(self) -> List[str]:
        return ['traffic', 'transportation', 'smart city', 'municipal', 'emergency', 'camera', 'sensor', 'routing']
    
    def get_priority_score(self) -> int:
        return 3  # High specificity
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()

        # Core traffic management capabilities
        if any(term in content_lower for term in ['camera', 'sensor', 'monitoring', 'detection']):
            requirements.append({
                'title': 'Traffic Camera Integration and Sensor Network Management',
                'priority': 'high',
                'category': 'functional'
            })

        if any(term in content_lower for term in ['mobile', 'citizen', 'public', 'user']):
            requirements.append({
                'title': 'Mobile Application for Citizen Traffic Information and Reporting',
                'priority': 'high',
                'category': 'functional'
            })

        if any(term in content_lower for term in ['emergency', 'ambulance', 'fire', 'police', 'routing']):
            requirements.append({
                'title': 'Emergency Vehicle Priority Routing and Traffic Signal Control',
                'priority': 'high',
                'category': 'functional'
            })

        if any(term in content_lower for term in ['analytics', 'dashboard', 'planning', 'data', 'insight']):
            requirements.append({
                'title': 'Traffic Analytics Dashboard for Urban Planning and Operations',
                'priority': 'medium',
                'category': 'functional'
            })

        if any(term in content_lower for term in ['api', 'third-party', 'integration', 'external']):
            requirements.append({
                'title': 'RESTful API for Third-Party Traffic Data Integration',
                'priority': 'medium',
                'category': 'functional'
            })

        if any(term in content_lower for term in ['environment', 'air quality', 'pollution', 'green']):
            requirements.append({
                'title': 'Environmental Impact Monitoring and Air Quality Integration',
                'priority': 'medium',
                'category': 'functional'
            })

        return requirements

    def extract_stakeholders(self, content: str) -> List[str]:
        stakeholders = ['Traffic Authorities', 'Citizens', 'Emergency Services', 'City Planners']
        content_lower = content.lower()
        
        if 'government' in content_lower or 'municipal' in content_lower:
            stakeholders.append('Government Agencies')
        if 'developer' in content_lower:
            stakeholders.append('Development Team')
        
        return stakeholders
