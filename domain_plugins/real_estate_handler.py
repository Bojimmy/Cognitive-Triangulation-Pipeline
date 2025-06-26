
#!/usr/bin/env python3
"""
Real Estate Domain Handler
Handles property management, real estate, and rental-related requirements
"""

from .base_handler import BaseDomainHandler
from typing import Dict, List, Any

class RealEstateDomainHandler(BaseDomainHandler):
    """Real Estate and Property Management domain handler"""
    
    def get_domain_name(self) -> str:
        return 'real_estate'
    
    def get_detection_keywords(self) -> List[str]:
        return [
            'property', 'real estate', 'mls', 'tenant', 'lease', 'rent', 'listing',
            'property management', 'rental', 'landlord', 'maintenance', 'vacancy',
            'apartment', 'commercial', 'residential', 'portfolio', 'unit',
            'application', 'screening', 'deposit', 'eviction', 'inspection',
            'property listing', 'tenant management', 'rent collection', 'property managers',
            'real estate agents', 'market data', 'lease management'
        ]
    
    def get_priority_score(self) -> int:
        return 5  # Highest priority - very specific domain
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()
        
        # MLS Integration System (specific detection)
        if any(term in content_lower for term in ['mls integration', 'mls', 'listing synchronization', 'market data']):
            requirements.append({
                'title': 'MLS Integration System with Property Listing Synchronization',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Property Listing Management
        if any(term in content_lower for term in ['property listing', 'listing', 'property catalog']):
            requirements.append({
                'title': 'Property Listing Management System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Tenant Management Portal (specific detection)
        if any(term in content_lower for term in ['tenant management', 'tenant portal', 'lease management', 'rent collection']):
            requirements.append({
                'title': 'Tenant Management Portal with Lease and Rent Collection',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Maintenance Request Tracking
        if any(term in content_lower for term in ['maintenance request', 'maintenance tracking', 'work order']):
            requirements.append({
                'title': 'Maintenance Request Management and Tracking System',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Rent Collection
        if any(term in content_lower for term in ['rent', 'payment', 'collection', 'billing']):
            requirements.append({
                'title': 'Automated Rent Collection and Payment Processing System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Maintenance Management
        if any(term in content_lower for term in ['maintenance', 'repair', 'service', 'work order']):
            requirements.append({
                'title': 'Maintenance Request Management and Work Order System',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Property Portfolio Management
        if any(term in content_lower for term in ['portfolio', 'multiple', 'properties', 'units']):
            requirements.append({
                'title': 'Multi-Property Portfolio Management Dashboard',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Tenant Screening
        if any(term in content_lower for term in ['screening', 'application', 'background', 'credit']):
            requirements.append({
                'title': 'Tenant Screening and Application Processing System',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Financial Reporting
        if any(term in content_lower for term in ['financial', 'report', 'income', 'expense', 'accounting']):
            requirements.append({
                'title': 'Financial Reporting and Property Accounting System',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Document Management
        if any(term in content_lower for term in ['document', 'lease', 'contract', 'agreement']):
            requirements.append({
                'title': 'Digital Document Management and Lease Agreement System',
                'priority': 'medium',
                'category': 'functional'
            })
        
        return requirements
    
    def extract_stakeholders(self, content: str) -> List[str]:
        """Extract real estate domain stakeholders"""
        stakeholders = ['Property Managers', 'Landlords', 'Tenants', 'Development Team']
        content_lower = content.lower()
        
        if any(term in content_lower for term in ['agent', 'broker', 'realtor']):
            stakeholders.append('Real Estate Agents')
        if any(term in content_lower for term in ['owner', 'investor']):
            stakeholders.append('Property Owners')
        if any(term in content_lower for term in ['maintenance', 'contractor']):
            stakeholders.append('Maintenance Contractors')
        if any(term in content_lower for term in ['legal', 'compliance']):
            stakeholders.append('Legal Compliance Team')
            
        return stakeholders
