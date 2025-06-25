
# X-Agent Domain Plugin System

## Overview

The X-Agent Domain Plugin System allows you to add new business domains without modifying the core `main.py` file. Each domain is handled by a dedicated plugin that understands domain-specific requirements, stakeholders, and terminology.

## Quick Start: Adding a New Domain

### 1. Create Your Plugin File

Create a new file: `domain_plugins/your_domain_handler.py`

```python
#!/usr/bin/env python3
"""
Your Domain Handler
"""

from .base_handler import BaseDomainHandler
from typing import Dict, List, Any

class YourDomainHandler(BaseDomainHandler):
    """Your domain handler"""
    
    def get_domain_name(self) -> str:
        return 'your_domain'  # e.g., 'real_estate', 'education', 'gaming'
    
    def get_detection_keywords(self) -> List[str]:
        return ['keyword1', 'keyword2', 'keyword3']  # Domain-specific terms
    
    def get_priority_score(self) -> int:
        return 3  # 1-5, higher = more specific domain
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()
        
        # Add your domain-specific logic here
        if 'your_keyword' in content_lower:
            requirements.append({
                'title': 'Your Domain-Specific Requirement',
                'priority': 'high',  # 'high', 'medium', 'low'
                'category': 'functional'  # 'functional' or 'non-functional'
            })
        
        return requirements
    
    def extract_stakeholders(self, content: str) -> List[str]:
        return ['Domain Users', 'Domain Experts', 'Development Team']
```

### 2. Test Your Plugin

Restart the application. Your plugin will be automatically loaded and available.

## Plugin API Reference

### Required Methods

#### `get_domain_name() -> str`
Return the unique domain identifier (lowercase, underscore-separated).

#### `get_detection_keywords() -> List[str]`
Return keywords that identify this domain in user content.

#### `extract_requirements(content: str, context: Dict = None) -> List[Dict]`
Extract domain-specific requirements. Each requirement should have:
- `title`: Descriptive requirement title
- `priority`: 'high', 'medium', or 'low'
- `category`: 'functional' or 'non-functional'

### Optional Methods

#### `get_priority_score() -> int`
Return 1-5 priority score for domain conflicts (default: 1).

#### `extract_stakeholders(content: str) -> List[str]`
Return domain-specific stakeholders (default: ['End Users', 'Development Team']).

#### `get_cross_cutting_requirements(content: str) -> List[Dict]`
Add cross-cutting concerns like security, performance (uses base implementation by default).

## Example Domains

### Real Estate Plugin

```python
class RealEstateDomainHandler(BaseDomainHandler):
    def get_domain_name(self):
        return 'real_estate'
    
    def get_detection_keywords(self):
        return ['property', 'listing', 'mls', 'realtor', 'mortgage', 'rental', 'lease']
    
    def extract_requirements(self, content, context=None):
        requirements = []
        content_lower = content.lower()
        
        if any(term in content_lower for term in ['listing', 'property', 'mls']):
            requirements.append({
                'title': 'Property Listing Management System with MLS Integration',
                'priority': 'high',
                'category': 'functional'
            })
        
        if any(term in content_lower for term in ['search', 'filter', 'criteria']):
            requirements.append({
                'title': 'Advanced Property Search and Filtering System',
                'priority': 'high',
                'category': 'functional'
            })
        
        return requirements
```

## Plugin Loading

Plugins are automatically discovered and loaded from the `domain_plugins/` directory. The system:

1. Scans for `*_handler.py` files
2. Imports each module
3. Finds classes inheriting from `BaseDomainHandler`
4. Instantiates and registers them

## Best Practices

1. **Specific Keywords**: Use domain-specific terms that rarely appear in other contexts
2. **Meaningful Requirements**: Extract actionable, implementable requirements
3. **Appropriate Priority**: Use 'high' for core features, 'medium' for important features, 'low' for nice-to-have
4. **Clear Titles**: Make requirement titles descriptive and specific
5. **Domain Expertise**: Include stakeholders who understand the domain

## Debugging

Enable plugin debugging by setting environment variable:
```bash
export X_AGENT_DEBUG_PLUGINS=1
```

This will show plugin loading details and domain detection confidence scores.
