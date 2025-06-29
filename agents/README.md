# X-Agent Pipeline - Agents Architecture

## 📁 Folder Structure

```
agents/
├── __init__.py                  # Package initialization
├── agent_template.py            # Template for creating new agents
├── integration_example.py       # How to add agents to main pipeline
├── core/                        # Core pipeline agents (future)
│   ├── analyst_agent.py        # Document analysis
│   ├── product_manager_agent.py # Requirements extraction  
│   └── task_manager_agent.py   # Task breakdown
└── specialized/                 # Domain-specific agents
    ├── customer_service_agent.py # Customer support workflows
    ├── healthcare_agent.py      # Medical domain processing
    └── ecommerce_agent.py       # E-commerce workflows
```

## 🚀 Creating New Agents

### Step 1: Copy the Template
```bash
cp agents/agent_template.py agents/specialized/your_agent.py
```

### Step 2: Implement Your Logic
1. Inherit from `BaseXAgent`
2. Implement `_process_intelligence()` - Your agent's core logic
3. Implement `_generate_xml()` - Output format for next agent
4. Add any specialized methods your agent needs

### Step 3: Integration
```python
# In main.py
from agents.specialized.your_agent import YourXAgent

class XAgentPipeline:
    def __init__(self):
        self.your_agent = YourXAgent()
```

## 🎯 Agent Design Principles

1. **Single Responsibility** - Each agent does one thing excellently
2. **XML Communication** - Agents communicate via structured XML
3. **Performance Tracking** - Built-in timing metrics
4. **Error Handling** - Robust error management
5. **Testability** - Easy to test individual agents

## 📊 Agent Performance

- **Target Processing Time**: < 10ms per agent
- **XML Processing**: Built-in lxml parsing
- **Memory Efficient**: Minimal resource usage
- **Scalable**: Can handle multiple concurrent requests

## 🔧 Current Status

**Embedded in main.py (Legacy):**
- AnalystXAgent
- ProductManagerXAgent  
- TaskManagerXAgent
- POScrumMasterXAgent

**Separate Files:**
- DocumentFormatterXAgent (root level)
- DomainPluginCreatorXAgent (root level)

**New Architecture (Future):**
- All new agents in agents/ folder
- Organized by category (core/specialized)
- Template-based development
- Easy integration pattern

## 🎉 Benefits

✅ **Better Organization** - Clear folder structure
✅ **Easier Testing** - Individual agent testing  
✅ **Reusable Agents** - Agents can be used in multiple workflows
✅ **Team Collaboration** - Different developers can work on different agents
✅ **Cleaner main.py** - Reduced complexity in main pipeline file
✅ **Plugin Architecture** - Easy to add/remove agents
