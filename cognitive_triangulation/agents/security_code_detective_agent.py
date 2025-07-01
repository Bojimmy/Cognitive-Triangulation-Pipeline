#!/usr/bin/env python3
"""
Enhanced Security Code Detective Agent with MCP Integration
The ultimate security + bug hunter for multi-language codebases

Combines:
- Your cognitive triangulation patterns
- AI IDE Integration MCP (static analysis tools)
- GitHub MCP (vulnerability databases)
- Multi-language security expertise

Languages supported: Python, Java, CSS, HTML
Focus: Security vulnerabilities + Critical bugs
"""
import ast
import re
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
import time
from pathlib import Path

# Import base detective
import sys
sys.path.append('/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation/cognitive_triangulation/agents')
from code_quality_detective_agent import CodeQualityDetectiveAgent, CodeIssue

@dataclass
class SecurityFinding:
    """Enhanced security finding with MCP context"""
    severity: str  # 'critical', 'high', 'medium', 'low'
    finding_type: str  # 'security', 'bug', 'vulnerability', 'cve'
    language: str  # 'python', 'java', 'css', 'html'
    line_number: int
    description: str
    code_snippet: str
    fix_suggestion: str
    confidence: float
    source: str  # 'cognitive_pattern', 'ide_static', 'github_vuln', 'triangulated'
    cve_id: Optional[str] = None
    severity_score: int = 0  # 0-10 scale

class SecurityCodeDetectiveAgent(CodeQualityDetectiveAgent):
    """
    Enhanced X-Agent: Security-focused detective with MCP superpowers
    
    Architecture:
    1. Cognitive Triangulation (your patterns) - FAST
    2. MCP Static Analysis (language-specific) - THOROUGH  
    3. MCP Vulnerability Database (historical) - CONTEXT
    4. Triangulated Confidence Scoring - ACCURATE
    """
    
    def __init__(self):
        super().__init__()
        self.agent_type = "security_code_detective"
        
        # Enhanced metrics for security focus
        self.metrics.update({
            'security_issues_found': 0,
            'critical_vulns_found': 0,
            'mcp_calls_made': 0,
            'languages_analyzed': set()
        })
        
        # Initialize enhanced security patterns
        self._setup_enhanced_security_patterns()
        
        # MCP integration flags (will be True when MCPs are available)
        self.ide_mcp_available = self._check_ide_mcp()
        self.github_mcp_available = self._check_github_mcp()
        
        print(f"🔒 SecurityCodeDetective initialized!")
        print(f"   📊 Base patterns: {len(self.security_patterns)} security rules")
        print(f"   🔧 IDE MCP: {'✅ Available' if self.ide_mcp_available else '⚠️ Simulated'}")
        print(f"   🐙 GitHub MCP: {'✅ Available' if self.github_mcp_available else '⚠️ Simulated'}")
    
    def _check_ide_mcp(self) -> bool:
        """Check if AI IDE Integration MCP is available"""
        try:
            # TODO: Replace with actual MCP client when available
            # from ai_ide_integration_mcp import AI_IDE_MCP
            # self.ide_mcp = AI_IDE_MCP()
            # return True
            return False  # Simulated for now
        except ImportError:
            return False
    
    def _check_github_mcp(self) -> bool:
        """Check if GitHub MCP is available"""
        try:
            # TODO: Replace with actual MCP client when available
            # from github_mcp import GitHub_MCP
            # self.github_mcp = GitHub_MCP()
            # return True
            return False  # Simulated for now
        except ImportError:
            return False
    
    def _setup_enhanced_security_patterns(self):
        """Setup comprehensive multi-language security patterns"""
        
        # Python security vulnerabilities
        self.python_security_patterns = [
            # Code injection
            (r'exec\s*\(', 'Code injection via exec()', 'critical', 'CODE_INJECTION'),
            (r'eval\s*\(', 'Code injection via eval()', 'critical', 'CODE_INJECTION'),
            (r'compile\s*\(.*?\,.*?["\']exec["\']', 'Dynamic code compilation', 'high', 'CODE_INJECTION'),
            
            # Command injection  
            (r'subprocess\.call\(.*?shell\s*=\s*True', 'Command injection via subprocess', 'critical', 'COMMAND_INJECTION'),
            (r'os\.system\s*\(', 'Command injection via os.system', 'critical', 'COMMAND_INJECTION'),
            (r'os\.popen\s*\(', 'Command injection via os.popen', 'high', 'COMMAND_INJECTION'),
            
            # Deserialization
            (r'pickle\.loads?\s*\(', 'Unsafe deserialization with pickle', 'critical', 'DESERIALIZATION'),
            (r'yaml\.load\s*\((?!.*Loader)', 'Unsafe YAML deserialization', 'high', 'DESERIALIZATION'),
            (r'marshal\.loads?\s*\(', 'Unsafe marshal deserialization', 'high', 'DESERIALIZATION'),
            
            # SQL injection
            (r'["\'].*?%s.*?["\'].*?%.*?\(', 'Potential SQL injection with % formatting', 'high', 'SQL_INJECTION'),
            (r'f["\'].*?\{.*?\}.*?["\'].*?(execute|query)', 'Potential SQL injection with f-strings', 'high', 'SQL_INJECTION'),
            (r'\.format\(.*?\).*?(execute|query)', 'Potential SQL injection with .format()', 'medium', 'SQL_INJECTION'),
            
            # Cryptography issues
            (r'hashlib\.md5\s*\(', 'Weak hash algorithm MD5', 'medium', 'WEAK_CRYPTO'),
            (r'hashlib\.sha1\s*\(', 'Weak hash algorithm SHA1', 'medium', 'WEAK_CRYPTO'),
            (r'random\.random\s*\(', 'Non-cryptographic random for security', 'medium', 'WEAK_CRYPTO'),
            
            # Path traversal
            (r'open\s*\(.*?\+.*?\)', 'Potential path traversal in file open', 'medium', 'PATH_TRAVERSAL'),
            (r'os\.path\.join\s*\(.*?\+', 'Potential path traversal in path join', 'medium', 'PATH_TRAVERSAL'),
            
            # Hardcoded secrets
            (r'password\s*=\s*["\'][^"\']{8,}["\']', 'Hardcoded password detected', 'critical', 'HARDCODED_SECRET'),
            (r'api_?key\s*=\s*["\'][^"\']{20,}["\']', 'Hardcoded API key detected', 'critical', 'HARDCODED_SECRET'),
            (r'secret\s*=\s*["\'][^"\']{16,}["\']', 'Hardcoded secret detected', 'critical', 'HARDCODED_SECRET'),
            (r'token\s*=\s*["\'][^"\']{20,}["\']', 'Hardcoded token detected', 'critical', 'HARDCODED_SECRET'),
        ]
        
        # Java security vulnerabilities
        self.java_security_patterns = [
            # Code injection
            (r'Runtime\.getRuntime\(\)\.exec\s*\(', 'Command injection via Runtime.exec', 'critical', 'COMMAND_INJECTION'),
            (r'ProcessBuilder\s*\(.*?\)\.start', 'Potential command injection via ProcessBuilder', 'high', 'COMMAND_INJECTION'),
            
            # SQL injection
            (r'Statement\.execute\w*\s*\(\s*["\'].*?\+', 'SQL injection via string concatenation', 'critical', 'SQL_INJECTION'),
            (r'createStatement\(\)\.execute\w*\s*\([^?]*\+', 'SQL injection in Statement', 'critical', 'SQL_INJECTION'),
            
            # Deserialization
            (r'ObjectInputStream\.readObject\s*\(', 'Unsafe object deserialization', 'critical', 'DESERIALIZATION'),
            (r'XMLDecoder\.readObject\s*\(', 'Unsafe XML deserialization', 'high', 'DESERIALIZATION'),
            
            # XXE vulnerabilities
            (r'DocumentBuilderFactory\.newInstance\(\)(?!.*setFeature)', 'XXE vulnerability in XML parser', 'high', 'XXE'),
            (r'SAXParserFactory\.newInstance\(\)(?!.*setFeature)', 'XXE vulnerability in SAX parser', 'high', 'XXE'),
            
            # LDAP injection
            (r'new\s+InitialDirContext\s*\(.*?\+', 'LDAP injection vulnerability', 'high', 'LDAP_INJECTION'),
            
            # Weak crypto
            (r'Cipher\.getInstance\s*\(\s*["\']DES["\']', 'Weak encryption algorithm DES', 'high', 'WEAK_CRYPTO'),
            (r'MessageDigest\.getInstance\s*\(\s*["\']MD5["\']', 'Weak hash algorithm MD5', 'medium', 'WEAK_CRYPTO'),
        ]
        
        # CSS security issues
        self.css_security_patterns = [
            # CSS injection
            (r'expression\s*\(', 'CSS expression injection (IE)', 'high', 'CSS_INJECTION'),
            (r'javascript\s*:', 'JavaScript URL in CSS', 'high', 'CSS_INJECTION'),
            (r'data\s*:\s*text/html', 'HTML data URL in CSS', 'medium', 'CSS_INJECTION'),
            (r'@import\s+url\s*\(\s*["\']?https?://', 'External CSS import', 'low', 'EXTERNAL_RESOURCE'),
            
            # Content hijacking
            (r'content\s*:\s*attr\s*\(', 'Content attribute usage', 'low', 'CONTENT_HIJACK'),
        ]
        
        # HTML security issues
        self.html_security_patterns = [
            # XSS vectors
            (r'<script[^>]*>.*?</script>', 'Inline script tag', 'high', 'XSS'),
            (r'on\w+\s*=\s*["\'][^"\']*["\']', 'Inline event handler', 'medium', 'XSS'),
            (r'javascript\s*:', 'JavaScript URL', 'medium', 'XSS'),
            (r'data\s*:\s*text/html', 'HTML data URL', 'medium', 'XSS'),
            
            # Clickjacking
            (r'<iframe[^>]*src\s*=\s*["\']?https?://', 'External iframe', 'medium', 'CLICKJACKING'),
            
            # Content injection
            (r'\{\{.*?\}\}', 'Template injection pattern', 'medium', 'TEMPLATE_INJECTION'),
            (r'<%.*?%>', 'Server-side template pattern', 'medium', 'TEMPLATE_INJECTION'),
        ]
        
        # Combine all patterns by language
        self.security_patterns = {
            'python': self.python_security_patterns,
            'java': self.java_security_patterns,
            'css': self.css_security_patterns,
            'html': self.html_security_patterns
        }
        
        # CVE severity mapping
        self.severity_scores = {
            'critical': 9,
            'high': 7,
            'medium': 5,
            'low': 3
        }
    
    def _find_line_number(self, code_content: str, search_text: str) -> int:
        """Find line number of specific text in code"""
        lines = code_content.split('\n')
        for i, line in enumerate(lines, 1):
            if search_text in line:
                return i
        return 1
    
    def _get_security_fix_suggestion(self, vuln_type: str) -> str:
        """Get specific fix suggestions for vulnerability types"""
        fix_suggestions = {
            'CODE_INJECTION': 'Avoid dynamic code execution. Use ast.literal_eval() for safe evaluation or redesign without exec/eval',
            'COMMAND_INJECTION': 'Use subprocess.run() with argument lists instead of shell=True. Validate all inputs.',
            'DESERIALIZATION': 'Use safe serialization formats like JSON. If pickle needed, verify source and use signing.',
            'SQL_INJECTION': 'Use parameterized queries or prepared statements. Never concatenate user input into SQL.',
            'WEAK_CRYPTO': 'Use strong cryptographic algorithms: SHA-256+, AES, or modern libraries like cryptography',
            'PATH_TRAVERSAL': 'Validate file paths. Use os.path.realpath() and check against allowed directories.',
            'HARDCODED_SECRET': 'Move secrets to environment variables, key management systems, or encrypted config files',
            'XXE': 'Disable external entity processing in XML parsers. Use secure parser configurations.',
            'LDAP_INJECTION': 'Escape LDAP special characters in user input. Use parameterized LDAP queries.',
            'XSS': 'Escape output, use Content Security Policy, validate input, prefer textContent over innerHTML',
            'CLICKJACKING': 'Use X-Frame-Options header, validate iframe sources, implement CSP frame-ancestors',
            'CSS_INJECTION': 'Validate CSS input, use CSS sanitization libraries, avoid dynamic CSS generation'
        }
        
        return fix_suggestions.get(vuln_type, 'Review and fix this security issue according to best practices')
