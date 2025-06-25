
#!/usr/bin/env python3
"""
Fintech Domain Handler
Handles finance, banking, and financial technology requirements
"""

from .base_handler import BaseDomainHandler
from typing import Dict, List, Any

class FintechDomainHandler(BaseDomainHandler):
    """Financial Technology domain handler"""
    
    def get_domain_name(self) -> str:
        return 'fintech'
    
    def get_detection_keywords(self) -> List[str]:
        return [
            'finance', 'banking', 'payment', 'financial', 'trading', 'investment',
            'crypto', 'blockchain', 'wallet', 'transaction', 'money', 'currency',
            'loan', 'credit', 'debit', 'account', 'balance', 'fintech'
        ]
    
    def get_priority_score(self) -> int:
        return 5  # Very high priority - heavily regulated and security-critical
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()
        
        # Security and Compliance (Critical for fintech)
        if any(term in content_lower for term in ['financial', 'payment', 'banking', 'money']):
            requirements.append({
                'title': 'Financial Security and Regulatory Compliance Framework',
                'priority': 'high',
                'category': 'non-functional'
            })
        
        # Payment Processing
        if any(term in content_lower for term in ['payment', 'transaction', 'transfer', 'money']):
            requirements.append({
                'title': 'Secure Payment Processing and Transaction System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Account Management
        if any(term in content_lower for term in ['account', 'balance', 'wallet', 'portfolio']):
            requirements.append({
                'title': 'Financial Account Management and Balance Tracking',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Trading Platform
        if any(term in content_lower for term in ['trading', 'investment', 'stock', 'market']):
            requirements.append({
                'title': 'Trading Platform and Investment Management System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Fraud Detection
        if any(term in content_lower for term in ['fraud', 'security', 'risk', 'monitoring']):
            requirements.append({
                'title': 'Fraud Detection and Risk Monitoring System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Cryptocurrency Support
        if any(term in content_lower for term in ['crypto', 'blockchain', 'bitcoin', 'ethereum']):
            requirements.append({
                'title': 'Cryptocurrency Integration and Blockchain Support',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Financial Reporting
        if any(term in content_lower for term in ['report', 'analytics', 'statement', 'tax']):
            requirements.append({
                'title': 'Financial Reporting and Analytics Dashboard',
                'priority': 'medium',
                'category': 'functional'
            })
        
        return requirements
    
    def extract_stakeholders(self, content: str) -> List[str]:
        """Extract fintech domain stakeholders"""
        stakeholders = ['Financial Users', 'Compliance Officers', 'Security Team', 'Development Team']
        content_lower = content.lower()
        
        if any(term in content_lower for term in ['trader', 'investor']):
            stakeholders.append('Traders/Investors')
        if any(term in content_lower for term in ['bank', 'banker']):
            stakeholders.append('Banking Partners')
        if any(term in content_lower for term in ['regulator', 'compliance']):
            stakeholders.append('Financial Regulators')
        if any(term in content_lower for term in ['auditor', 'audit']):
            stakeholders.append('Financial Auditors')
            
        return stakeholders
