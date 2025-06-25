
#!/usr/bin/env python3
"""
E-commerce Domain Handler
Handles online shopping, payment, and retail requirements
"""

from .base_handler import BaseDomainHandler
from typing import Dict, List, Any

class EcommerceDomainHandler(BaseDomainHandler):
    """E-commerce and Online Retail domain handler"""
    
    def get_domain_name(self) -> str:
        return 'ecommerce'
    
    def get_detection_keywords(self) -> List[str]:
        return [
            'ecommerce', 'e-commerce', 'shopping', 'cart', 'product', 'order',
            'payment', 'checkout', 'store', 'retail', 'inventory', 'catalog',
            'marketplace', 'merchant', 'customer', 'purchase', 'sale'
        ]
    
    def get_priority_score(self) -> int:
        return 4  # High priority - specific business domain
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()
        
        # Product Catalog Management
        if any(term in content_lower for term in ['product', 'catalog', 'inventory', 'item']):
            requirements.append({
                'title': 'Product Catalog Management and Inventory System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Shopping Cart
        if any(term in content_lower for term in ['cart', 'shopping', 'basket', 'add to cart']):
            requirements.append({
                'title': 'Shopping Cart and Session Management System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Payment Processing
        if any(term in content_lower for term in ['payment', 'checkout', 'billing', 'credit card']):
            requirements.append({
                'title': 'Secure Payment Processing and Checkout System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Order Management
        if any(term in content_lower for term in ['order', 'purchase', 'transaction', 'sale']):
            requirements.append({
                'title': 'Order Management and Processing System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # User Account System
        if any(term in content_lower for term in ['customer', 'account', 'profile', 'login']):
            requirements.append({
                'title': 'Customer Account Management and Profile System',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Search and Filtering
        if any(term in content_lower for term in ['search', 'filter', 'browse', 'category']):
            requirements.append({
                'title': 'Product Search and Advanced Filtering System',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Reviews and Ratings
        if any(term in content_lower for term in ['review', 'rating', 'feedback', 'comment']):
            requirements.append({
                'title': 'Product Reviews and Rating System',
                'priority': 'medium',
                'category': 'functional'
            })
        
        return requirements
    
    def extract_stakeholders(self, content: str) -> List[str]:
        """Extract e-commerce domain stakeholders"""
        stakeholders = ['Customers', 'Store Managers', 'Payment Processors', 'Development Team']
        content_lower = content.lower()
        
        if any(term in content_lower for term in ['merchant', 'seller', 'vendor']):
            stakeholders.append('Merchants/Vendors')
        if any(term in content_lower for term in ['admin', 'administrator']):
            stakeholders.append('Store Administrators')
        if any(term in content_lower for term in ['shipping', 'logistics']):
            stakeholders.append('Shipping Partners')
        if any(term in content_lower for term in ['marketing', 'promotion']):
            stakeholders.append('Marketing Team')
            
        return stakeholders
