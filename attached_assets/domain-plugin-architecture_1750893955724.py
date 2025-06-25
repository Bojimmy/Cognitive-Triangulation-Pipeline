#!/usr/bin/env python3
"""
X-Agent Domain Plugin Architecture
Scalable system for adding new business domains without modifying core code
"""

import json
import os
import importlib
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import re

# =============================================================================
# 1. DOMAIN PLUGIN BASE CLASS
# =============================================================================

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
        """Calculate confidence that content belongs to this domain (0.0-1.0)"""
        content_lower = content.lower()
        keyword_matches = sum(1 for keyword in self.keywords if keyword in content_lower)
        max_possible = len(self.keywords)
        return min(keyword_matches / max(max_possible * 0.3, 1), 1.0)  # Need 30% keyword match
    
    def extract_stakeholders(self, content: str) -> List[str]:
        """Extract domain-specific stakeholders"""
        return ['End Users', 'Development Team']  # Default stakeholders
    
    def get_cross_cutting_requirements(self, content: str) -> List[Dict[str, Any]]:
        """Extract cross-cutting concerns (security, performance, etc.)"""
        requirements = []
        content_lower = content.lower()
        
        # Security
        if any(term in content_lower for term in ['security', 'auth', 'encrypt', 'secure']):
            requirements.append({
                'title': 'Security Framework and Data Protection Implementation',
                'priority': 'high',
                'category': 'security'
            })
        
        # Performance
        if any(term in content_lower for term in ['performance', 'scalability', 'uptime']) or re.search(r'\d+%\s*uptime', content_lower):
            requirements.append({
                'title': 'Performance Optimization and Scalability Implementation',
                'priority': 'high', 
                'category': 'performance'
            })
        
        # Compliance
        if any(term in content_lower for term in ['compliance', 'gdpr', 'hipaa', 'privacy']):
            requirements.append({
                'title': 'Regulatory Compliance and Privacy Protection',
                'priority': 'high',
                'category': 'compliance'
            })
        
        return requirements

# =============================================================================
# 2. DOMAIN PLUGIN IMPLEMENTATIONS
# =============================================================================

class CustomerSupportDomainHandler(BaseDomainHandler):
    """Customer Support domain handler"""
    
    def get_domain_name(self) -> str:
        return 'customer_support'
    
    def get_detection_keywords(self) -> List[str]:
        return ['support', 'ticket', 'helpdesk', 'customer service', 'agent', 'escalation', 'call center']
    
    def get_priority_score(self) -> int:
        return 3  # High specificity
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()
        
        if any(term in content_lower for term in ['ticket', 'support', 'helpdesk']):
            requirements.append({
                'title': 'Intelligent Ticket Management and Routing System',
                'priority': 'high',
                'category': 'functional'
            })
        
        if any(term in content_lower for term in ['agent', 'staff', 'representative']):
            requirements.append({
                'title': 'Support Agent Dashboard and Workload Management',
                'priority': 'high',
                'category': 'functional'
            })
        
        if any(term in content_lower for term in ['escalation', 'priority', 'urgent']):
            requirements.append({
                'title': 'Automated Escalation and Priority Management System',
                'priority': 'high',
                'category': 'functional'
            })
        
        if any(term in content_lower for term in ['salesforce', 'crm', 'integration']):
            requirements.append({
                'title': 'CRM Integration and Customer Data Synchronization',
                'priority': 'high',
                'category': 'functional'
            })
        
        if any(term in content_lower for term in ['phone', 'call', 'telephony']):
            requirements.append({
                'title': 'Telephony System Integration and Call Management',
                'priority': 'high',
                'category': 'functional'
            })
        
        # Volume-based requirements
        volume_match = re.search(r'(\d+,?\d*)\s*(?:monthly|per month|tickets)', content_lower)
        if volume_match:
            volume = volume_match.group(1)
            requirements.append({
                'title': f'High-Volume Ticket Processing ({volume} monthly capacity)',
                'priority': 'high',
                'category': 'non-functional'
            })
        
        return requirements
    
    def extract_stakeholders(self, content: str) -> List[str]:
        stakeholders = ['Support Agents', 'Customers', 'Management']
        content_lower = content.lower()
        
        if 'enterprise' in content_lower or 'business' in content_lower:
            stakeholders.append('Business Stakeholders')
        if 'developer' in content_lower:
            stakeholders.append('Development Team')
        
        return stakeholders


class FitnessAppDomainHandler(BaseDomainHandler):
    """Fitness/Health App domain handler"""
    
    def get_domain_name(self) -> str:
        return 'fitness_app'
    
    def get_detection_keywords(self) -> List[str]:
        return ['fitness', 'workout', 'nutrition', 'health', 'wellness', 'exercise', 'trainer', 'wearable']
    
    def get_priority_score(self) -> int:
        return 4  # Very specific domain
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()
        
        if any(term in content_lower for term in ['workout', 'exercise', 'fitness']):
            requirements.append({
                'title': 'Comprehensive Workout Tracking and Exercise Logging System',
                'priority': 'high',
                'category': 'functional'
            })
        
        if any(term in content_lower for term in ['nutrition', 'food', 'meal', 'calorie']):
            requirements.append({
                'title': 'Nutrition Tracking with Barcode Scanning and Food Database',
                'priority': 'high',
                'category': 'functional'
            })
        
        if any(term in content_lower for term in ['apple watch', 'fitbit', 'wearable']):
            requirements.append({
                'title': 'Wearable Device Integration (Apple Watch, Fitbit, Heart Rate Monitors)',
                'priority': 'high',
                'category': 'functional'
            })
        
        if any(term in content_lower for term in ['trainer', 'coach', 'personal']):
            requirements.append({
                'title': 'Personal Trainer Management and Coaching Platform',
                'priority': 'high',
                'category': 'functional'
            })
        
        if any(term in content_lower for term in ['mobile', 'app', 'ios', 'android']):
            requirements.append({
                'title': 'Cross-Platform Mobile Application with Offline Sync',
                'priority': 'high',
                'category': 'functional'
            })
        
        if any(term in content_lower for term in ['social', 'community', 'friend']):
            requirements.append({
                'title': 'Social Features and Community Platform with Challenges',
                'priority': 'medium',
                'category': 'functional'
            })
        
        return requirements


class EcommerceDomainHandler(BaseDomainHandler):
    """E-commerce domain handler"""
    
    def get_domain_name(self) -> str:
        return 'ecommerce'
    
    def get_detection_keywords(self) -> List[str]:
        return ['ecommerce', 'e-commerce', 'shopping', 'cart', 'product', 'payment', 'checkout', 'marketplace']
    
    def get_priority_score(self) -> int:
        return 3
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()
        
        if any(term in content_lower for term in ['product', 'catalog', 'inventory']):
            requirements.append({
                'title': 'Product Catalog and Inventory Management System',
                'priority': 'high',
                'category': 'functional'
            })
        
        if any(term in content_lower for term in ['cart', 'shopping', 'checkout']):
            requirements.append({
                'title': 'Shopping Cart and Checkout Process Implementation',
                'priority': 'high',
                'category': 'functional'
            })
        
        if any(term in content_lower for term in ['payment', 'stripe', 'paypal']):
            requirements.append({
                'title': 'Payment Processing and Transaction Management',
                'priority': 'high',
                'category': 'functional'
            })
        
        if any(term in content_lower for term in ['vendor', 'seller', 'marketplace']):
            requirements.append({
                'title': 'Vendor Management and Marketplace Platform',
                'priority': 'medium',
                'category': 'functional'
            })
        
        return requirements

# =============================================================================
# 3. DOMAIN REGISTRY AND MANAGER
# =============================================================================

class DomainRegistry:
    """Registry for managing domain handlers"""
    
    def __init__(self):
        self.handlers: Dict[str, BaseDomainHandler] = {}
        self.load_default_handlers()
    
    def register_handler(self, handler: BaseDomainHandler):
        """Register a domain handler"""
        self.handlers[handler.domain_name] = handler
    
    def load_default_handlers(self):
        """Load built-in domain handlers"""
        default_handlers = [
            CustomerSupportDomainHandler(),
            FitnessAppDomainHandler(),
            EcommerceDomainHandler(),
            # Add more default handlers here
        ]
        
        for handler in default_handlers:
            self.register_handler(handler)
    
    def detect_domain(self, content: str) -> tuple[str, float]:
        """Detect the best domain for content"""
        best_domain = 'general'
        best_confidence = 0.0
        
        for domain_name, handler in self.handlers.items():
            confidence = handler.detect_domain_confidence(content)
            # Weight by priority score
            weighted_confidence = confidence * (handler.priority_score / 5.0)
            
            if weighted_confidence > best_confidence:
                best_confidence = weighted_confidence
                best_domain = domain_name
        
        return best_domain, best_confidence
    
    def get_handler(self, domain: str) -> Optional[BaseDomainHandler]:
        """Get handler for specific domain"""
        return self.handlers.get(domain)
    
    def list_domains(self) -> List[str]:
        """List all available domains"""
        return list(self.handlers.keys())

# =============================================================================
# 4. DOMAIN PLUGIN LOADER (FOR EXTERNAL PLUGINS)
# =============================================================================

class DomainPluginLoader:
    """Loads domain plugins from external files"""
    
    def __init__(self, plugin_directory: str = "domain_plugins"):
        self.plugin_directory = plugin_directory
        self.ensure_plugin_directory()
    
    def ensure_plugin_directory(self):
        """Create plugin directory if it doesn't exist"""
        if not os.path.exists(self.plugin_directory):
            os.makedirs(self.plugin_directory)
    
    def load_plugins(self, registry: DomainRegistry):
        """Load all plugins from plugin directory"""
        if not os.path.exists(self.plugin_directory):
            return
        
        for filename in os.listdir(self.plugin_directory):
            if filename.endswith('.py') and not filename.startswith('__'):
                self.load_plugin(filename[:-3], registry)
    
    def load_plugin(self, module_name: str, registry: DomainRegistry):
        """Load a specific plugin module"""
        try:
            module_path = f"{self.plugin_directory}.{module_name}"
            module = importlib.import_module(module_path)
            
            # Look for handler classes
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, BaseDomainHandler) and 
                    attr != BaseDomainHandler):
                    
                    handler = attr()
                    registry.register_handler(handler)
                    print(f"Loaded domain plugin: {handler.domain_name}")
        
        except Exception as e:
            print(f"Failed to load plugin {module_name}: {e}")

# =============================================================================
# 5. CONFIGURATION-DRIVEN DOMAIN DETECTION
# =============================================================================

class ConfigurableDomainHandler(BaseDomainHandler):
    """Domain handler that loads configuration from JSON/YAML"""
    
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.domain_config = json.load(f)
        super().__init__(self.domain_config)
    
    def get_domain_name(self) -> str:
        return self.domain_config['domain_name']
    
    def get_detection_keywords(self) -> List[str]:
        return self.domain_config['keywords']
    
    def get_priority_score(self) -> int:
        return self.domain_config.get('priority', 1)
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()
        
        for req_config in self.domain_config['requirements']:
            keywords = req_config['keywords']
            if any(keyword in content_lower for keyword in keywords):
                requirements.append({
                    'title': req_config['title'],
                    'priority': req_config.get('priority', 'medium'),
                    'category': req_config.get('category', 'functional')
                })
        
        return requirements

# =============================================================================
# 6. UPDATED PRODUCT MANAGER AGENT
# =============================================================================

class ProductManagerXAgent:
    """Simplified ProductManager that uses domain plugins"""
    
    def __init__(self):
        self.domain_registry = DomainRegistry()
        self.plugin_loader = DomainPluginLoader()
        self.plugin_loader.load_plugins(self.domain_registry)
    
    def extract_requirements(self, content: str) -> Dict[str, Any]:
        """Extract requirements using domain plugins"""
        
        # Detect domain
        domain, confidence = self.domain_registry.detect_domain(content)
        
        # Get domain handler
        handler = self.domain_registry.get_handler(domain)
        
        if handler:
            # Extract domain-specific requirements
            requirements = handler.extract_requirements(content)
            
            # Add cross-cutting requirements
            cross_cutting = handler.get_cross_cutting_requirements(content)
            requirements.extend(cross_cutting)
            
            # Extract stakeholders
            stakeholders = handler.extract_stakeholders(content)
        else:
            # Fallback to generic extraction
            requirements = self._extract_generic_requirements(content)
            stakeholders = ['End Users', 'Development Team']
        
        # Deduplicate and format
        formatted_requirements = self._format_requirements(requirements)
        
        return {
            'domain': domain,
            'confidence': confidence,
            'requirements': formatted_requirements,
            'stakeholders': stakeholders,
            'req_count': len(formatted_requirements)
        }
    
    def _extract_generic_requirements(self, content: str) -> List[Dict[str, Any]]:
        """Fallback generic requirement extraction"""
        return [
            {
                'title': 'Core System Architecture and Data Management',
                'priority': 'high',
                'category': 'functional'
            },
            {
                'title': 'User Interface and Experience Implementation',
                'priority': 'high', 
                'category': 'functional'
            },
            {
                'title': 'API Development and Integration Framework',
                'priority': 'medium',
                'category': 'functional'
            }
        ]
    
    def _format_requirements(self, requirements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format and deduplicate requirements"""
        seen_titles = set()
        formatted = []
        
        for i, req in enumerate(requirements[:8], 1):  # Limit to 8
            title = req['title']
            if title not in seen_titles:
                formatted.append({
                    'id': f"REQ-{i:03d}",
                    'title': title,
                    'priority': req.get('priority', 'medium')
                })
                seen_titles.add(title)
        
        return formatted

# =============================================================================
# 7. EXAMPLE CONFIGURATION FILE
# =============================================================================

def create_example_domain_config():
    """Create example domain configuration file"""
    healthcare_config = {
        "domain_name": "healthcare",
        "keywords": ["medical", "patient", "doctor", "hospital", "clinic", "healthcare", "hipaa"],
        "priority": 4,
        "requirements": [
            {
                "title": "Patient Management and Electronic Health Records System",
                "keywords": ["patient", "ehr", "medical record"],
                "priority": "high",
                "category": "functional"
            },
            {
                "title": "HIPAA Compliance and Medical Data Protection",
                "keywords": ["hipaa", "privacy", "medical data"],
                "priority": "high",
                "category": "compliance"
            },
            {
                "title": "Medical Staff Portal and Workflow Management",
                "keywords": ["doctor", "nurse", "staff", "workflow"],
                "priority": "high",
                "category": "functional"
            },
            {
                "title": "Appointment Scheduling and Patient Communication",
                "keywords": ["appointment", "schedule", "communication"],
                "priority": "medium",
                "category": "functional"
            }
        ]
    }
    
    os.makedirs("domain_configs", exist_ok=True)
    with open("domain_configs/healthcare.json", "w") as f:
        json.dump(healthcare_config, f, indent=2)

# =============================================================================
# 8. EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Create example config
    create_example_domain_config()
    
    # Initialize system
    pm_agent = ProductManagerXAgent()
    
    # Test with different domains
    test_docs = {
        "Customer Support": "We need a helpdesk system to manage 15000 monthly tickets with agent workload management and CRM integration",
        "Fitness App": "Building a wellness app with workout tracking, nutrition logging, and Apple Watch integration for health-conscious users",
        "E-commerce": "Marketplace platform with product catalog, shopping cart, payment processing, and vendor management features"
    }
    
    for doc_type, content in test_docs.items():
        print(f"\n=== {doc_type} Test ===")
        result = pm_agent.extract_requirements(content)
        print(f"Domain: {result['domain']} (confidence: {result['confidence']:.2f})")
        print(f"Requirements: {result['req_count']}")
        for req in result['requirements']:
            print(f"  - {req['id']}: {req['title']}")
    
    print(f"\nAvailable domains: {pm_agent.domain_registry.list_domains()}")
