
#!/usr/bin/env python3
"""
Fitness App Domain Handler
Extracted from main.py ProductManagerXAgent
"""

import re
from .base_handler import BaseDomainHandler
from typing import Dict, List, Any

class FitnessAppDomainHandler(BaseDomainHandler):
    """Fitness/Health App domain handler"""
    
    def get_domain_name(self) -> str:
        return 'fitness_app'
    
    def get_detection_keywords(self) -> List[str]:
        return ['fitness', 'workout', 'nutrition', 'health', 'wellness', 'exercise', 'trainer', 'meal', 'calorie', 'step', 'wearable', 'fitbit', 'apple watch', 'strava']
    
    def get_priority_score(self) -> int:
        return 4  # Very specific domain
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()

        # Core fitness tracking
        if any(term in content_lower for term in ['workout', 'exercise', 'fitness', 'training']):
            requirements.append({
                'title': 'Comprehensive Workout Tracking and Exercise Logging System',
                'priority': 'high',
                'category': 'functional'
            })

        # Nutrition tracking
        if any(term in content_lower for term in ['nutrition', 'food', 'meal', 'calorie', 'diet', 'eating']):
            requirements.append({
                'title': 'Nutrition Tracking with Barcode Scanning and Food Database',
                'priority': 'high',
                'category': 'functional'
            })

        # Wearable device integration
        if any(term in content_lower for term in ['apple watch', 'fitbit', 'wearable', 'smartwatch', 'heart rate']):
            requirements.append({
                'title': 'Wearable Device Integration (Apple Watch, Fitbit, Heart Rate Monitors)',
                'priority': 'high',
                'category': 'functional'
            })

        # Trainer/coaching features
        if any(term in content_lower for term in ['trainer', 'coach', 'personal', 'professional', 'instructor']):
            requirements.append({
                'title': 'Personal Trainer Management and Coaching Platform',
                'priority': 'high',
                'category': 'functional'
            })

        # Social and community features
        if any(term in content_lower for term in ['social', 'community', 'friend', 'share', 'challenge', 'leaderboard']):
            requirements.append({
                'title': 'Social Features and Community Platform with Challenges',
                'priority': 'medium',
                'category': 'functional'
            })

        # Third-party integrations
        if any(term in content_lower for term in ['strava', 'myfitnesspal', 'apple health', 'google fit', 'integration']):
            requirements.append({
                'title': 'Third-Party Fitness App Integration (Strava, Apple Health, Google Fit)',
                'priority': 'medium',
                'category': 'functional'
            })

        # Mobile app essentials
        if any(term in content_lower for term in ['mobile', 'app', 'ios', 'android']):
            requirements.append({
                'title': 'Cross-Platform Mobile Application with Offline Sync',
                'priority': 'high',
                'category': 'functional'
            })

        # Progress tracking and analytics
        if any(term in content_lower for term in ['progress', 'goal', 'achievement', 'analytics', 'report']):
            requirements.append({
                'title': 'Progress Tracking and Goal Achievement Analytics',
                'priority': 'medium',
                'category': 'functional'
            })

        # User scaling
        user_scale_match = re.search(r'(\d+(?:,\d+)*)\s*(?:to|-)?\s*(\d+(?:,\d+)*)\s*(?:users|customers)', content_lower)
        if user_scale_match:
            min_users = user_scale_match.group(1)
            max_users = user_scale_match.group(2) if user_scale_match.group(2) else min_users
            requirements.append({
                'title': f'Scalable Architecture for {min_users} to {max_users} Users',
                'priority': 'high',
                'category': 'non-functional'
            })

        return requirements

    def extract_stakeholders(self, content: str) -> List[str]:
        stakeholders = ['Fitness Enthusiasts', 'Personal Trainers', 'Health Professionals']
        content_lower = content.lower()
        
        if 'social' in content_lower or 'community' in content_lower:
            stakeholders.append('Community Members')
        if 'premium' in content_lower or 'subscription' in content_lower:
            stakeholders.append('Premium Subscribers')
        
        return stakeholders
