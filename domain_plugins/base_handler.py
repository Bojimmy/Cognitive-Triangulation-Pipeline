#!/usr/bin/env python3
"""
Base Domain Handler for X-Agent Plugin Architecture
"""

import re
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class BaseDomainHandler(ABC):
    """Base class for all domain-specific requirement extractors"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.domain_name = self.get_domain_name()
        self.keywords = self.get_detection_keywords()
        self.priority_score = self.get_priority_score()

    @abstractmethod
    def get_domain_name(self) -> str:
        """Return the domain name (e.g., 'customer_support')"""
        pass

    @abstractmethod
    def get_detection_keywords(self) -> List[str]:
        """Return keywords that identify this domain"""
        pass

    @abstractmethod
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Extract domain-specific requirements from content"""
        pass

    def get_priority_score(self) -> int:
        """Return priority score for domain conflicts (higher = more specific)"""
        return 1

    def detect_domain_confidence(self, content: str) -> float:
        """Calculate confidence score for domain detection"""
        content_lower = content.lower()
        keywords = self.get_detection_keywords()

        # Count keyword matches with weight for multi-word phrases
        matches = 0
        for keyword in keywords:
            if keyword in content_lower:
                # Give higher weight to multi-word phrases
                weight = len(keyword.split()) if len(keyword.split()) > 1 else 1
                matches += weight

        # Calculate confidence based on matches relative to content length and keyword specificity
        total_possible_score = len(keywords) * 2  # Assume average 2-word phrases
        confidence = min(matches / max(total_possible_score * 0.2, 1), 1.0)

        return confidence

    def extract_stakeholders(self, content: str) -> List[str]:
        """Extract domain-specific stakeholders"""
        return ['End Users', 'Development Team']

    def get_cross_cutting_requirements(self, content: str) -> List[Dict[str, Any]]:
        """Extract cross-cutting concerns (security, performance, compliance)"""
        requirements = []
        content_lower = content.lower()

        # Security requirements
        if any(term in content_lower for term in ['security', 'cyber', 'encryption', 'auth', 'secure']):
            requirements.append({
                'title': 'Comprehensive Cybersecurity Framework and Data Protection',
                'priority': 'high',
                'category': 'non-functional'
            })

        # Performance requirements
        uptime_match = re.search(r'(\d+\.?\d*)%\s*uptime', content_lower)
        if uptime_match or any(term in content_lower for term in ['performance', 'scalability', 'reliability']):
            uptime_target = uptime_match.group(1) if uptime_match else "99.9"
            requirements.append({
                'title': f'System Reliability and Performance ({uptime_target}% uptime requirement)',
                'priority': 'high',
                'category': 'non-functional'
            })

        # Real-time processing
        if any(term in content_lower for term in ['real-time', 'realtime', 'instant', 'live']):
            requirements.append({
                'title': 'Real-Time Data Processing and Event Handling System',
                'priority': 'high',
                'category': 'non-functional'
            })

        return requirements