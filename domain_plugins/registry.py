
#!/usr/bin/env python3
"""
Domain Registry for Managing Domain Handlers
"""

import os
import importlib
from typing import Dict, Optional, Tuple
from .base_handler import BaseDomainHandler

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
        try:
            from .customer_support_handler import CustomerSupportDomainHandler
            from .fitness_app_handler import FitnessAppDomainHandler
            from .traffic_management_handler import TrafficManagementDomainHandler
            from .real_estate_handler import RealEstateDomainHandler
            from .healthcare_handler import HealthcareDomainHandler
            from .mobile_app_handler import MobileAppDomainHandler
            from .ecommerce_handler import EcommerceDomainHandler
            from .fintech_handler import FintechDomainHandler
            from .visual_workflow_handler import VisualWorkflowDomainHandler
            from .enterprise_handler import EnterpriseDomainHandler
            from .beekeeping_handler import BeekeepingDomainHandler
            from .restaurant_management_handler import RestaurantManagementDomainHandler
            from .gaming_studio_management_handler import GamingStudioManagementDomainHandler
            
            default_handlers = [
                CustomerSupportDomainHandler(),
                FitnessAppDomainHandler(),
                TrafficManagementDomainHandler(),
                RealEstateDomainHandler(),
                HealthcareDomainHandler(),
                MobileAppDomainHandler(),
                EcommerceDomainHandler(),
                FintechDomainHandler(),
                VisualWorkflowDomainHandler(),
                EnterpriseDomainHandler(),
                BeekeepingDomainHandler(),
                RestaurantManagementDomainHandler(),
                GamingStudioManagementDomainHandler(),
            ]
            
            for handler in default_handlers:
                self.register_handler(handler)
                
        except ImportError as e:
            print(f"Warning: Could not load default handlers: {e}")
    
    def detect_domain(self, content: str) -> Tuple[str, float]:
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
    
    def list_domains(self) -> list:
        """List all available domains"""
        return list(self.handlers.keys())

class DomainPluginLoader:
    """Loads domain plugins from external files"""
    
    def __init__(self, plugin_dir: str = "domain_plugins"):
        self.plugin_dir = plugin_dir
    
    def load_plugins(self, registry: DomainRegistry):
        """Load all plugins from plugin directory"""
        if not os.path.exists(self.plugin_dir):
            return
            
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('_handler.py') and not filename.startswith('base_'):
                module_name = filename[:-3]  # Remove .py
                try:
                    module = importlib.import_module(f"{self.plugin_dir}.{module_name}")
                    
                    # Look for handler class in module
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and 
                            issubclass(attr, BaseDomainHandler) and 
                            attr != BaseDomainHandler):
                            
                            handler_instance = attr()
                            registry.register_handler(handler_instance)
                            print(f"✅ Loaded domain plugin: {handler_instance.domain_name}")
                            break
                            
                except Exception as e:
                    print(f"❌ Failed to load plugin {module_name}: {e}")
