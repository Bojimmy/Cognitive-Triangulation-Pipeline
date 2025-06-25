
#!/usr/bin/env python3
"""
Mobile App Domain Handler
Handles iOS, Android, and mobile application requirements
"""

from .base_handler import BaseDomainHandler
from typing import Dict, List, Any

class MobileAppDomainHandler(BaseDomainHandler):
    """Mobile Application domain handler"""
    
    def get_domain_name(self) -> str:
        return 'mobile_app'
    
    def get_detection_keywords(self) -> List[str]:
        return [
            'mobile', 'app', 'ios', 'android', 'smartphone', 'tablet',
            'react native', 'flutter', 'swift', 'kotlin', 'mobile app',
            'push notification', 'offline', 'touch', 'gesture', 'camera'
        ]
    
    def get_priority_score(self) -> int:
        return 4  # High priority - specific platform requirements
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()
        
        # Platform Support
        if any(term in content_lower for term in ['ios', 'android', 'mobile', 'app']):
            requirements.append({
                'title': 'Cross-Platform Mobile App Development (iOS/Android)',
                'priority': 'high',
                'category': 'functional'
            })
        
        # User Authentication
        if any(term in content_lower for term in ['login', 'auth', 'user', 'account']):
            requirements.append({
                'title': 'Mobile User Authentication and Profile Management',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Offline Functionality
        if any(term in content_lower for term in ['offline', 'cache', 'sync', 'local storage']):
            requirements.append({
                'title': 'Offline Data Storage and Synchronization',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Push Notifications
        if any(term in content_lower for term in ['notification', 'push', 'alert', 'message']):
            requirements.append({
                'title': 'Push Notification System and Messaging',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Camera/Media Integration
        if any(term in content_lower for term in ['camera', 'photo', 'video', 'media', 'image']):
            requirements.append({
                'title': 'Camera Integration and Media Capture System',
                'priority': 'medium',
                'category': 'functional'
            })
        
        # Touch Interface
        if any(term in content_lower for term in ['touch', 'gesture', 'swipe', 'tap', 'pinch']):
            requirements.append({
                'title': 'Touch-Optimized User Interface with Gesture Support',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Performance Optimization
        requirements.append({
            'title': 'Mobile Performance Optimization and Battery Efficiency',
            'priority': 'medium',
            'category': 'non-functional'
        })
        
        return requirements
    
    def extract_stakeholders(self, content: str) -> List[str]:
        """Extract mobile app domain stakeholders"""
        stakeholders = ['Mobile Users', 'UI/UX Designers', 'Mobile Developers', 'Development Team']
        content_lower = content.lower()
        
        if any(term in content_lower for term in ['ios', 'iphone', 'ipad']):
            stakeholders.append('iOS Users')
        if any(term in content_lower for term in ['android', 'google play']):
            stakeholders.append('Android Users')
        if any(term in content_lower for term in ['testing', 'qa']):
            stakeholders.append('Mobile QA Testers')
        if any(term in content_lower for term in ['store', 'publish', 'deployment']):
            stakeholders.append('App Store Managers')
            
        return stakeholders
