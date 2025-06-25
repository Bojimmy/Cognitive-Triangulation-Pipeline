
#!/usr/bin/env python3
"""
Enterprise Domain Handler
Handles enterprise, compliance, and security requirements
"""

from .base_handler import BaseDomainHandler
from typing import Dict, List, Any

class EnterpriseDomainHandler(BaseDomainHandler):
    """Enterprise and Corporate domain handler"""
    
    def get_domain_name(self) -> str:
        return 'enterprise'
    
    def get_detection_keywords(self) -> List[str]:
        return [
            'enterprise', 'compliance', 'security', 'corporate', 'governance',
            'audit', 'policy', 'sso', 'ldap', 'active directory', 'rbac',
            'scalability', 'high availability', 'disaster recovery'
        ]
    
    def get_priority_score(self) -> int:
        return 4  # High priority - complex organizational requirements
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()
        
        # Security Framework
        if any(term in content_lower for term in ['security', 'enterprise', 'corporate']):
            requirements.append({
                'title': 'Enterprise Security Framework and Access Control',
                'priority': 'high',
                'category': 'non-functional'
            })
        
        # Single Sign-On
        if any(term in content_lower for term in ['sso', 'single sign-on', 'authentication', 'ldap']):
            requirements.append({
                'title': 'Single Sign-On (SSO) and Directory Integration',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Role-Based Access Control
        if any(term in content_lower for term in ['rbac', 'role', 'permission', 'access control']):
            requirements.append({
                'title': 'Role-Based Access Control (RBAC) System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Compliance Management
        if any(term in content_lower for term in ['compliance', 'audit', 'governance', 'policy']):
            requirements.append({
                'title': 'Compliance Management and Audit Trail System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Scalability
        if any(term in content_lower for term in ['scalability', 'scale', 'performance', 'load']):
            requirements.append({
                'title': 'Enterprise Scalability and Performance Framework',
                'priority': 'high',
                'category': 'non-functional'
            })
        
        # High Availability
        if any(term in content_lower for term in ['availability', 'uptime', 'redundancy', 'failover']):
            requirements.append({
                'title': 'High Availability and Disaster Recovery System',
                'priority': 'medium',
                'category': 'non-functional'
            })
        
        # Enterprise Integration
        if any(term in content_lower for term in ['integration', 'api', 'enterprise', 'legacy']):
            requirements.append({
                'title': 'Enterprise System Integration and API Gateway',
                'priority': 'medium',
                'category': 'functional'
            })
        
        return requirements
    
    def extract_stakeholders(self, content: str) -> List[str]:
        """Extract enterprise domain stakeholders"""
        stakeholders = ['Enterprise Users', 'IT Administrators', 'Security Team', 'Development Team']
        content_lower = content.lower()
        
        if any(term in content_lower for term in ['compliance', 'audit']):
            stakeholders.append('Compliance Officers')
        if any(term in content_lower for term in ['executive', 'management']):
            stakeholders.append('Executive Leadership')
        if any(term in content_lower for term in ['admin', 'administrator']):
            stakeholders.append('System Administrators')
        if any(term in content_lower for term in ['legal', 'policy']):
            stakeholders.append('Legal Team')
            
        return stakeholders
