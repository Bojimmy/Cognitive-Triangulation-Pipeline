
#!/usr/bin/env python3
"""
Healthcare Domain Handler
Handles medical, patient, and healthcare-related requirements
"""

from .base_handler import BaseDomainHandler
from typing import Dict, List, Any

class HealthcareDomainHandler(BaseDomainHandler):
    """Healthcare and Medical domain handler"""
    
    def get_domain_name(self) -> str:
        return 'healthcare'
    
    def get_detection_keywords(self) -> List[str]:
        return [
            'healthcare', 'medical', 'patient', 'hospital', 'clinic', 'hipaa',
            'doctor', 'nurse', 'appointment', 'prescription', 'diagnosis',
            'treatment', 'medical record', 'health', 'wellness', 'telemedicine'
        ]
    
    def get_priority_score(self) -> int:
        return 5  # Very high priority - heavily regulated domain
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()
        
        # HIPAA Compliance (Critical for healthcare)
        if any(term in content_lower for term in ['patient', 'medical', 'health', 'hipaa']):
            requirements.append({
                'title': 'HIPAA Compliance and Data Security Framework',
                'priority': 'high',
                'category': 'non-functional'
            })
        
        # Patient Management System
        if any(term in content_lower for term in ['patient', 'medical record', 'chart']):
            requirements.append({
                'title': 'Electronic Health Records (EHR) Management System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Appointment Scheduling
        if any(term in content_lower for term in ['appointment', 'schedule', 'booking']):
            requirements.append({
                'title': 'Medical Appointment Scheduling and Calendar System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Prescription Management
        if any(term in content_lower for term in ['prescription', 'medication', 'drug', 'pharmacy']):
            requirements.append({
                'title': 'Prescription Management and Drug Interaction System',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Telemedicine
        if any(term in content_lower for term in ['telemedicine', 'virtual', 'remote', 'video call']):
            requirements.append({
                'title': 'Telemedicine Platform with Video Consultation',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Billing and Insurance
        if any(term in content_lower for term in ['billing', 'insurance', 'claim', 'payment']):
            requirements.append({
                'title': 'Medical Billing and Insurance Claims Processing',
                'priority': 'medium',
                'category': 'functional'
            })
        
        return requirements
    
    def extract_stakeholders(self, content: str) -> List[str]:
        """Extract healthcare domain stakeholders"""
        stakeholders = ['Patients', 'Healthcare Providers', 'IT Security Team', 'Development Team']
        content_lower = content.lower()
        
        if any(term in content_lower for term in ['doctor', 'physician']):
            stakeholders.append('Doctors/Physicians')
        if any(term in content_lower for term in ['nurse', 'nursing']):
            stakeholders.append('Nurses')
        if any(term in content_lower for term in ['admin', 'administrator']):
            stakeholders.append('Hospital Administrators')
        if any(term in content_lower for term in ['compliance', 'hipaa']):
            stakeholders.append('Compliance Officers')
        if any(term in content_lower for term in ['pharmacy', 'pharmacist']):
            stakeholders.append('Pharmacists')
            
        return stakeholders
