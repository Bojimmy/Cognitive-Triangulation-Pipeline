# 📝 LOGGING INSTRUCTIONS FOR JIM

## 🔍 Where to Find the Logs

The system logs are now configured to save to the `logs/` directory with detailed output.

## 🧪 How to Test with Full Logging

### Option 1: Run the Test Script (Recommended)
```bash
cd /Users/bobdallavia/X-Agent-Pipeline
python3 test_for_jim.py
```

This will:
- ✅ Enable full file logging
- ✅ Test the gaming studio domain (complex content)
- ✅ Create detailed log files in `logs/` directory
- ✅ Show you exactly where the logs are saved

### Option 2: Run Any System with Logging
```python
# Add this to the top of any Python file
from logging_config import setup_logging
logger = setup_logging(enable_file_logging=True)

# Then run your normal code - logs will be saved automatically
```

## 📁 Log Files Created

After running the test, check the `logs/` directory for:

1. **`x_agent_pipeline_YYYYMMDD_HHMMSS.log`** - Main system log (all messages)
2. **`plugin_creator_YYYYMMDD_HHMMSS.log`** - Plugin creator specific logs
3. **`errors_YYYYMMDD_HHMMSS.log`** - Error messages only

## 🔍 What You'll See in the Logs

The logs will show:
- Dynamic model selection logic
- Function calling requests and responses
- Domain detection confidence scores
- Plugin creation steps
- Cost optimization decisions
- Fallback logic when API unavailable

## 📊 Example Log Output

```
2025-06-27 16:30:15 | domain_plugin_creator_agent | INFO | [Plugin Creator] Content complexity: 0.750, selected model: claude-3-opus-20240229
2025-06-27 16:30:16 | domain_plugin_creator_agent | INFO | [Plugin Creator] Claude analyzed new domain via function call: gaming_studio_management  
2025-06-27 16:30:18 | domain_plugin_creator_agent | INFO | [Plugin Creator] Claude generated domain handler (2847 chars)
```

## 🚀 Quick Start

1. Run: `python3 test_for_jim.py`
2. Check: `logs/` directory for output files
3. Open the log files to see detailed system behavior

## 💡 Debug Mode

For even more detailed logs:
```python
from logging_config import enable_debug_logging
logger = enable_debug_logging()
```

This will show DEBUG level messages for maximum detail.
