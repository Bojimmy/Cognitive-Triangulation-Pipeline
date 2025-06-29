#!/usr/bin/env python3
"""
Restaurant Management Domain Handler for X-Agent Pipeline
Specialized for restaurant operations, POS systems, menu management, and dining service workflows
"""

import re
from typing import Dict, List, Any
from .base_handler import BaseDomainHandler

class RestaurantManagementDomainHandler(BaseDomainHandler):
    """Domain handler for restaurant and food service management systems"""
    
    def get_domain_name(self) -> str:
        return "restaurant_management"
    
    def get_detection_keywords(self) -> List[str]:
        return [
            "restaurant", "menu", "orders", "kitchen", "waitstaff", "pos", 
            "reservations", "tables", "dining", "food", "beverage", "chef",
            "inventory", "ingredients", "recipes", "takeout", "delivery",
            "restaurant management", "food service", "hospitality", "dining room"
        ]
    
    def get_priority_score(self) -> int:
        return 4  # High priority for specialized service industry
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Extract restaurant-specific requirements"""
        requirements = []
        content_lower = content.lower()
        
        # Menu Management
        if any(term in content_lower for term in ['menu', 'dishes', 'recipes', 'ingredients']):
            requirements.append({
                'title': 'Digital Menu Management System',
                'description': 'Manage menu items, pricing, ingredients, and dietary information',
                'priority': 'high',
                'category': 'functional',
                'acceptance_criteria': [
                    'Create and edit menu items with photos',
                    'Manage pricing and seasonal availability',
                    'Track ingredient inventory and allergens',
                    'Support multiple menu formats (dine-in, takeout, delivery)'
                ]
            })
        
        # Order Management & POS
        if any(term in content_lower for term in ['orders', 'pos', 'payment', 'checkout']):
            requirements.append({
                'title': 'Point of Sale (POS) Integration',
                'description': 'Integrated ordering and payment processing system',
                'priority': 'high',
                'category': 'functional',
                'acceptance_criteria': [
                    'Process dine-in, takeout, and delivery orders',
                    'Accept multiple payment methods',
                    'Generate receipts and order tickets',
                    'Split bills and handle group orders'
                ]
            })
        
        # Table & Reservation Management
        if any(term in content_lower for term in ['tables', 'reservations', 'booking', 'seating']):
            requirements.append({
                'title': 'Table and Reservation Management',
                'description': 'Manage dining room layout, reservations, and table assignments',
                'priority': 'high',
                'category': 'functional',
                'acceptance_criteria': [
                    'Visual table layout management',
                    'Online reservation booking system',
                    'Waitlist management for walk-ins',
                    'Table assignment optimization'
                ]
            })
        
        # Kitchen Operations
        if any(term in content_lower for term in ['kitchen', 'chef', 'cooking', 'preparation']):
            requirements.append({
                'title': 'Kitchen Display System (KDS)',
                'description': 'Digital kitchen workflow and order management',
                'priority': 'high',
                'category': 'functional',
                'acceptance_criteria': [
                    'Display incoming orders by preparation time',
                    'Track order status and completion times',
                    'Manage special dietary requests',
                    'Coordinate between kitchen stations'
                ]
            })
        
        # Staff Management
        if any(term in content_lower for term in ['staff', 'waitstaff', 'servers', 'scheduling']):
            requirements.append({
                'title': 'Staff Scheduling and Management',
                'description': 'Manage restaurant staff schedules and performance',
                'priority': 'medium',
                'category': 'functional',
                'acceptance_criteria': [
                    'Create and manage staff schedules',
                    'Track server tables and sales performance',
                    'Manage time clock and payroll integration',
                    'Handle shift changes and availability'
                ]
            })
        
        # Inventory Management
        if any(term in content_lower for term in ['inventory', 'ingredients', 'supplies', 'stock']):
            requirements.append({
                'title': 'Inventory and Supply Management',
                'description': 'Track food inventory, ingredients, and supply levels',
                'priority': 'medium',
                'category': 'functional',
                'acceptance_criteria': [
                    'Monitor ingredient stock levels',
                    'Automatic reorder notifications',
                    'Track food costs and waste',
                    'Manage supplier relationships'
                ]
            })
        
        # Delivery & Takeout
        if any(term in content_lower for term in ['delivery', 'takeout', 'pickup', 'online orders']):
            requirements.append({
                'title': 'Delivery and Takeout Management',
                'description': 'Handle off-premise dining orders and delivery logistics',
                'priority': 'medium',
                'category': 'functional',
                'acceptance_criteria': [
                    'Integration with delivery platforms (DoorDash, Uber Eats)',
                    'Order tracking for customers',
                    'Pickup notification system',
                    'Delivery time estimation and routing'
                ]
            })
        
        return requirements
    
    def extract_stakeholders(self, content: str) -> List[str]:
        """Extract restaurant-specific stakeholders"""
        stakeholders = ['Restaurant Owners', 'Kitchen Staff', 'Waitstaff', 'Customers']
        content_lower = content.lower()
        
        if any(term in content_lower for term in ['manager', 'management']):
            stakeholders.append('Restaurant Managers')
        
        if any(term in content_lower for term in ['chef', 'head chef', 'kitchen']):
            stakeholders.append('Head Chef')
        
        if any(term in content_lower for term in ['bartender', 'bar', 'drinks']):
            stakeholders.append('Bar Staff')
        
        if any(term in content_lower for term in ['host', 'hostess', 'seating']):
            stakeholders.append('Host/Hostess Staff')
        
        if any(term in content_lower for term in ['delivery', 'driver']):
            stakeholders.append('Delivery Drivers')
        
        if any(term in content_lower for term in ['supplier', 'vendor', 'distributor']):
            stakeholders.append('Food Suppliers')
        
        if any(term in content_lower for term in ['health', 'inspection', 'compliance']):
            stakeholders.append('Health Inspectors')
        
        return stakeholders
    
    def get_cross_cutting_requirements(self, content: str) -> List[Dict[str, Any]]:
        """Get cross-cutting requirements for restaurant systems"""
        requirements = []
        
        # Health & Safety Compliance
        requirements.append({
            'title': 'Food Safety and Health Compliance',
            'description': 'Ensure compliance with health regulations and food safety standards',
            'priority': 'high',
            'category': 'compliance',
            'acceptance_criteria': [
                'Temperature monitoring and logging',
                'Food expiration date tracking',
                'Health inspection checklist management',
                'Allergen information and warnings'
            ]
        })
        
        # Real-time Operations
        requirements.append({
            'title': 'Real-time Order and Kitchen Synchronization',
            'description': 'Seamless communication between front-of-house and kitchen',
            'priority': 'high',
            'category': 'performance',
            'acceptance_criteria': [
                'Instant order transmission to kitchen',
                'Real-time inventory updates',
                'Live table status updates',
                'Push notifications for order ready'
            ]
        })
        
        # Analytics and Reporting
        requirements.append({
            'title': 'Restaurant Analytics and Reporting',
            'description': 'Business intelligence for restaurant performance optimization',
            'priority': 'medium',
            'category': 'analytics',
            'acceptance_criteria': [
                'Daily/weekly sales reports',
                'Popular menu item analysis',
                'Staff performance metrics',
                'Customer satisfaction tracking'
            ]
        })
        
        # Mobile Integration
        requirements.append({
            'title': 'Mobile Staff and Customer Apps',
            'description': 'Mobile applications for staff operations and customer engagement',
            'priority': 'medium',
            'category': 'accessibility',
            'acceptance_criteria': [
                'Server mobile ordering system',
                'Customer reservation and ordering app',
                'Manager dashboard mobile access',
                'Kitchen staff mobile notifications'
            ]
        })
        
        return requirements
    
    def detect_domain_confidence(self, content: str) -> float:
        """Calculate confidence score for restaurant domain detection"""
        content_lower = content.lower()
        keyword_matches = sum(1 for keyword in self.keywords if keyword in content_lower)
        
        # Restaurant-specific terms get higher weight
        specialized_terms = ['pos', 'kitchen display', 'reservations', 'waitstaff', 'food service']
        specialized_matches = sum(1 for term in specialized_terms if term in content_lower)
        
        # Food industry indicators
        food_terms = ['dining', 'cuisine', 'chef', 'restaurant', 'food service', 'hospitality']
        food_matches = sum(1 for term in food_terms if term in content_lower)
        
        # Calculate confidence (0.0 to 1.0)
        base_confidence = min(keyword_matches / 6.0, 1.0)
        specialized_bonus = min(specialized_matches / 3.0, 0.2)
        food_bonus = min(food_matches / 4.0, 0.2)
        
        return min(base_confidence + specialized_bonus + food_bonus, 1.0)
