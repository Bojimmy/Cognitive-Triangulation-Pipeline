#!/usr/bin/env python3
"""
Customer Support Domain Handler
Extracted from main.py ProductManagerXAgent
"""

import re
from .base_handler import BaseDomainHandler
from typing import Dict, List, Any

class CustomerSupportDomainHandler(BaseDomainHandler):
    """Customer Support domain handler"""

    def get_domain_name(self) -> str:
        return 'customer_support'

    def get_detection_keywords(self) -> List[str]:
        return ['support', 'ticket', 'helpdesk', 'customer service', 'agent', 'escalation', 'call center']

    def get_priority_score(self) -> int:
        return 1  # Low priority - most generic

    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()

        # Core ticketing system
        if any(term in content_lower for term in ['ticket', 'support', 'helpdesk', 'case']):
            requirements.append({
                'title': 'Intelligent Ticket Management and Routing System',
                'priority': 'high',
                'category': 'functional'
            })

        # Agent management
        if any(term in content_lower for term in ['agent', 'staff', 'representative', 'operator']):
            requirements.append({
                'title': 'Support Agent Dashboard and Workload Management',
                'priority': 'high',
                'category': 'functional'
            })

        # Escalation workflows
        if any(term in content_lower for term in ['escalation', 'escalate', 'priority', 'urgent']):
            requirements.append({
                'title': 'Automated Escalation and Priority Management System',
                'priority': 'high',
                'category': 'functional'
            })

        # Knowledge base
        if any(term in content_lower for term in ['knowledge', 'knowledge base', 'documentation', 'self-service']):
            requirements.append({
                'title': 'Self-Service Knowledge Base and FAQ System',
                'priority': 'medium',
                'category': 'functional'
            })

        # CRM integration
        if any(term in content_lower for term in ['salesforce', 'crm', 'customer data', 'integration']):
            requirements.append({
                'title': 'CRM Integration and Customer Data Synchronization',
                'priority': 'high',
                'category': 'functional'
            })

        # Telephony integration
        if any(term in content_lower for term in ['phone', 'call', 'telephony', 'voice', 'pbx']):
            requirements.append({
                'title': 'Telephony System Integration and Call Management',
                'priority': 'high',
                'category': 'functional'
            })

        # Volume handling
        volume_match = re.search(r'(\d+,?\d*)\s*(?:monthly|per month|tickets)', content_lower)
        if volume_match:
            volume = volume_match.group(1)
            requirements.append({
                'title': f'High-Volume Ticket Processing ({volume} monthly capacity)',
                'priority': 'high',
                'category': 'non-functional'
            })

        # Multi-channel support
        if any(term in content_lower for term in ['email', 'chat', 'phone', 'social', 'channel']):
            requirements.append({
                'title': 'Multi-Channel Support (Email, Chat, Phone, Social Media)',
                'priority': 'medium',
                'category': 'functional'
            })

        # HIPAA compliance specifically
        if any(term in content_lower for term in ['hipaa', 'healthcare', 'medical', 'patient']):
            requirements.append({
                'title': 'HIPAA Compliance and Healthcare Data Protection',
                'priority': 'high',
                'category': 'non-functional'
            })

        return requirements

    def extract_stakeholders(self, content: str) -> List[str]:
        stakeholders = ['Support Agents', 'Customers', 'Management']
        content_lower = content.lower()

        if 'enterprise' in content_lower or 'business' in content_lower:
            stakeholders.append('Business Stakeholders')
        if 'developer' in content_lower:
            stakeholders.append('Development Team')

        return stakeholders