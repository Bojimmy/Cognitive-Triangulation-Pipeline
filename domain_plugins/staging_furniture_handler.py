
#!/usr/bin/env python3
"""
Staging Furniture Domain Handler
Handles requirements for furniture staging companies, interior design, and furniture management
"""

from .base_handler import BaseDomainHandler
from typing import Dict, List, Any
import re

class StagingFurnitureDomainHandler(BaseDomainHandler):
    """Handler for staging and furniture domain requirements"""
    
    def get_domain_name(self) -> str:
        return 'staging_furniture'
    
    def get_detection_keywords(self) -> List[str]:
        return [
            'staging', 'furniture', 'interior design', 'home staging', 
            'property staging', 'furniture rental', 'decor', 'furnishing',
            'room design', 'space planning', 'furniture inventory',
            'staging consultation', 'before and after', 'furniture placement',
            'design portfolio', 'staging services', 'furniture catalog',
            'room layout', 'furniture arrangement', 'staging project',
            'design consultation', 'furniture warehouse', 'staging company'
        ]
    
    def get_priority_score(self) -> int:
        return 4  # High specificity for staging/furniture domain
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()
        
        # Furniture inventory and catalog management
        if any(term in content_lower for term in ['inventory', 'catalog', 'furniture management', 'warehouse']):
            requirements.append({
                'title': 'Comprehensive Furniture Inventory Management System with Catalog',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Staging project management
        if any(term in content_lower for term in ['staging project', 'project management', 'staging services']):
            requirements.append({
                'title': 'Staging Project Management and Timeline Tracking System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Client consultation and communication
        if any(term in content_lower for term in ['consultation', 'client', 'customer', 'communication']):
            requirements.append({
                'title': 'Client Consultation Management and Communication Portal',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Room design and layout planning
        if any(term in content_lower for term in ['room design', 'space planning', 'layout', 'arrangement']):
            requirements.append({
                'title': 'Interactive Room Design and Space Planning Tool',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Before/after documentation
        if any(term in content_lower for term in ['before', 'after', 'documentation', 'portfolio']):
            requirements.append({
                'title': 'Before/After Documentation and Portfolio Management System',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Furniture rental and scheduling
        if any(term in content_lower for term in ['rental', 'booking', 'schedule', 'availability']):
            requirements.append({
                'title': 'Furniture Rental Scheduling and Availability Management',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Property and location management
        if any(term in content_lower for term in ['property', 'location', 'address', 'venue']):
            requirements.append({
                'title': 'Property and Location Management with Address Tracking',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Vendor and supplier management
        if any(term in content_lower for term in ['vendor', 'supplier', 'procurement', 'sourcing']):
            requirements.append({
                'title': 'Vendor and Supplier Management with Procurement Tracking',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Cost estimation and billing
        if any(term in content_lower for term in ['cost', 'pricing', 'billing', 'invoice', 'estimate']):
            requirements.append({
                'title': 'Cost Estimation and Billing Management System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Mobile access for on-site work
        if any(term in content_lower for term in ['mobile', 'on-site', 'field', 'tablet']):
            requirements.append({
                'title': 'Mobile-Optimized Interface for On-Site Staging Work',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Photo and visual management
        if any(term in content_lower for term in ['photo', 'image', 'visual', 'gallery']):
            requirements.append({
                'title': 'Photo Gallery and Visual Asset Management System',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Add cross-cutting requirements
        requirements.extend(self.get_cross_cutting_requirements(content))
        
        return requirements
    
    def extract_stakeholders(self, content: str) -> List[str]:
        """Extract staging/furniture specific stakeholders"""
        stakeholders = ['Staging Consultants', 'Interior Designers', 'Property Owners']
        content_lower = content.lower()
        
        if any(term in content_lower for term in ['real estate', 'realtor', 'agent']):
            stakeholders.append('Real Estate Agents')
        
        if any(term in content_lower for term in ['warehouse', 'logistics']):
            stakeholders.append('Warehouse Staff')
        
        if any(term in content_lower for term in ['delivery', 'transport']):
            stakeholders.append('Delivery Team')
        
        if any(term in content_lower for term in ['photographer', 'marketing']):
            stakeholders.append('Marketing Team')
        
        # Always include these
        stakeholders.extend(['Development Team', 'End Users'])
        
        return list(set(stakeholders))  # Remove duplicates
