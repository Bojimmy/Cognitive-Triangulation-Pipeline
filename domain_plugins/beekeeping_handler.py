#!/usr/bin/env python3
"""
Beekeeping Domain Handler for X-Agent Pipeline
Specialized for apiary management, bee colony tracking, and honey production systems
"""

import re
from typing import Dict, List, Any
from .base_handler import BaseDomainHandler

class BeekeepingDomainHandler(BaseDomainHandler):
    """Domain handler for beekeeping and apiary management systems"""
    
    def get_domain_name(self) -> str:
        return "beekeeping"
    
    def get_detection_keywords(self) -> List[str]:
        return [
            "hive", "honey", "bees", "apiary", "colony", "queen", "pollen", 
            "nectar", "swarm", "beekeeping", "beekeeper", "honeycomb", 
            "brood", "worker", "drone", "royal jelly", "propolis", "wax"
        ]
    
    def get_priority_score(self) -> int:
        return 4  # High priority for specialized domain
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Extract beekeeping-specific requirements"""
        requirements = []
        content_lower = content.lower()
        
        # Hive Management Requirements
        if any(term in content_lower for term in ['hive', 'colony', 'management']):
            requirements.append({
                'title': 'Hive Management System',
                'description': 'Track individual hive health, population, and productivity',
                'priority': 'high',
                'category': 'functional',
                'acceptance_criteria': [
                    'Monitor hive population levels',
                    'Track queen bee status',
                    'Record inspection dates and findings'
                ]
            })
        
        # Honey Production Tracking
        if any(term in content_lower for term in ['honey', 'production', 'harvest']):
            requirements.append({
                'title': 'Honey Production Tracking',
                'description': 'Monitor honey production cycles and harvest yields',
                'priority': 'high',
                'category': 'functional',
                'acceptance_criteria': [
                    'Track seasonal production volumes',
                    'Record harvest dates and quantities',
                    'Monitor honey quality metrics'
                ]
            })
        
        # Health Monitoring
        if any(term in content_lower for term in ['health', 'disease', 'mite', 'varroa']):
            requirements.append({
                'title': 'Colony Health Monitoring',
                'description': 'Track bee colony health and disease prevention',
                'priority': 'high',
                'category': 'functional',
                'acceptance_criteria': [
                    'Monitor for common bee diseases',
                    'Track mite levels and treatments',
                    'Alert for health anomalies'
                ]
            })
        
        # Seasonal Management
        if any(term in content_lower for term in ['seasonal', 'winter', 'migration', 'feeding']):
            requirements.append({
                'title': 'Seasonal Management',
                'description': 'Manage seasonal activities and hive preparations',
                'priority': 'medium',
                'category': 'functional',
                'acceptance_criteria': [
                    'Track seasonal feeding schedules',
                    'Monitor winter preparation status',
                    'Plan for seasonal migrations'
                ]
            })
        
        # Equipment Management
        if any(term in content_lower for term in ['equipment', 'frames', 'super', 'smoker']):
            requirements.append({
                'title': 'Equipment Management',
                'description': 'Track beekeeping equipment and maintenance',
                'priority': 'medium',
                'category': 'functional',
                'acceptance_criteria': [
                    'Inventory management for frames and supers',
                    'Equipment maintenance scheduling',
                    'Purchase and replacement tracking'
                ]
            })
        
        return requirements
    
    def extract_stakeholders(self, content: str) -> List[str]:
        """Extract beekeeping-specific stakeholders"""
        stakeholders = ['Beekeepers', 'Apiary Managers']
        content_lower = content.lower()
        
        if 'commercial' in content_lower:
            stakeholders.extend(['Commercial Honey Producers', 'Distribution Partners'])
        
        if any(term in content_lower for term in ['organic', 'certification', 'quality']):
            stakeholders.append('Quality Certification Bodies')
        
        if any(term in content_lower for term in ['research', 'data', 'analytics']):
            stakeholders.append('Bee Research Scientists')
        
        if any(term in content_lower for term in ['local', 'farmers', 'pollination']):
            stakeholders.extend(['Local Farmers', 'Pollination Service Clients'])
        
        return stakeholders
    
    def get_cross_cutting_requirements(self, content: str) -> List[Dict[str, Any]]:
        """Get cross-cutting requirements for beekeeping systems"""
        requirements = []
        
        # Weather Integration
        requirements.append({
            'title': 'Weather Data Integration',
            'description': 'Integrate weather data for hive management decisions',
            'priority': 'medium',
            'category': 'integration',
            'acceptance_criteria': [
                'Real-time weather monitoring',
                'Weather-based activity recommendations',
                'Seasonal weather pattern analysis'
            ]
        })
        
        # Mobile Access
        requirements.append({
            'title': 'Mobile Field Access',
            'description': 'Mobile app for field inspections and data entry',
            'priority': 'high',
            'category': 'accessibility',
            'acceptance_criteria': [
                'Offline data entry capability',
                'Photo documentation support',
                'GPS location tracking for apiaries'
            ]
        })
        
        # Regulatory Compliance
        requirements.append({
            'title': 'Regulatory Compliance Tracking',
            'description': 'Track compliance with beekeeping regulations',
            'priority': 'medium',
            'category': 'compliance',
            'acceptance_criteria': [
                'Registration and licensing tracking',
                'Health inspection records',
                'Pesticide usage documentation'
            ]
        })
        
        return requirements
    
    def detect_domain_confidence(self, content: str) -> float:
        """Calculate confidence score for beekeeping domain detection"""
        content_lower = content.lower()
        keyword_matches = sum(1 for keyword in self.keywords if keyword in content_lower)
        
        # Specialized beekeeping terms get higher weight
        specialized_terms = ['apiary', 'varroa', 'brood', 'royal jelly', 'propolis']
        specialized_matches = sum(1 for term in specialized_terms if term in content_lower)
        
        # Calculate confidence (0.0 to 1.0)
        base_confidence = min(keyword_matches / 5.0, 1.0)
        specialized_bonus = min(specialized_matches / 3.0, 0.3)
        
        return min(base_confidence + specialized_bonus, 1.0)
