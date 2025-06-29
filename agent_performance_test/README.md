# Agent Performance Testing Framework

## 🎯 Test Objective
Compare different X-Agent implementation approaches for code analysis performance and output quality.

## 🧪 Test Setup

### Test Implementations:
1. **EmbeddedAgent** - All logic built into agent
2. **CoLocatedPluginAgent** - Agent + co-located domain plugin  
3. **OriginalStyleAgent** - Based on working main.py pattern

### Test File:
- `sample_code.py` - A real Python file with various code structures
- Contains: classes, functions, imports, inheritance, method calls

### Metrics:
1. **Performance**: Execution time (milliseconds)
2. **Output Quality**: POI detection accuracy
3. **Maintainability**: Code organization and readability

## 📊 Expected Results Format

```json
{
  "test_run": "2025-06-29",
  "implementations": {
    "embedded": {
      "execution_time_ms": 0,
      "pois_detected": 0,
      "functions_found": [],
      "classes_found": [],
      "imports_found": [],
      "relationships_found": []
    },
    "co_located_plugin": {
      "execution_time_ms": 0,
      "pois_detected": 0,
      "functions_found": [],
      "classes_found": [],
      "imports_found": [],
      "relationships_found": []
    },
    "original_style": {
      "execution_time_ms": 0,
      "pois_detected": 0,
      "functions_found": [],
      "classes_found": [],
      "imports_found": [],
      "relationships_found": []
    }
  }
}
```

## 🚀 Usage

```bash
python test_runner.py
```

This will analyze the sample code with all three agent implementations and output a comparison report.
