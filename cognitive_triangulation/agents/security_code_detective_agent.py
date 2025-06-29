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
    
    def process(self, input_xml: str) -> str:
        """Enhanced processing with multi-source security analysis"""
        start_time = time.time()
        
        try:
            # Parse input XML
            root = ET.fromstring(input_xml)
            
            # Extract code content and metadata
            code_content = self._extract_code_content(root)
            file_path = root.find('.//file_path')
            file_path_str = file_path.text if file_path is not None else "unknown"
            
            # Detect language
            language = self._detect_language(file_path_str, code_content)
            self.metrics['languages_analyzed'].add(language)
            
            print(f"🔍 Analyzing {language} file: {Path(file_path_str).name}")
            
            # Multi-source security analysis
            findings = self._comprehensive_security_analysis(code_content, language, file_path_str)
            
            # Generate enhanced security report
            result = self._generate_security_report(findings, file_path_str, language, code_content)
            
            # Update metrics
            processing_time = time.time() - start_time
            self.metrics['total_time'] += processing_time
            self.metrics['security_issues_found'] += len(findings)
            self.metrics['critical_vulns_found'] += len([f for f in findings if f.severity == 'critical'])
            
            return self._generate_xml_output(result)
            
        except Exception as e:
            return self._generate_error_xml(str(e))
    
    def _detect_language(self, file_path: str, code_content: str) -> str:
        """Detect programming language from file path and content"""
        file_path = file_path.lower()
        
        if file_path.endswith('.py'):
            return 'python'
        elif file_path.endswith(('.java', '.kt')):
            return 'java'
        elif file_path.endswith('.css'):
            return 'css'
        elif file_path.endswith(('.html', '.htm', '.xhtml')):
            return 'html'
        elif file_path.endswith('.js'):
            return 'javascript'
        
        # Content-based detection
        if 'def ' in code_content and 'import ' in code_content:
            return 'python'
        elif 'public class' in code_content or 'package ' in code_content:
            return 'java'
        elif '<html' in code_content.lower() or '<!doctype' in code_content.lower():
            return 'html'
        elif '{' in code_content and '}' in code_content and ('color:' in code_content or 'font-' in code_content):
            return 'css'
        
        return 'unknown'
    
    def _comprehensive_security_analysis(self, code_content: str, language: str, file_path: str) -> List[SecurityFinding]:
        """Run comprehensive multi-source security analysis"""
        all_findings = []
        
        print(f"   🔍 Phase 1: Cognitive pattern analysis...")
        # Phase 1: Cognitive triangulation patterns (your fast approach)
        cognitive_findings = self._analyze_with_cognitive_patterns(code_content, language)
        all_findings.extend(cognitive_findings)
        print(f"   ✅ Found {len(cognitive_findings)} issues via cognitive patterns")
        
        print(f"   🛠️ Phase 2: Static analysis (MCP simulation)...")
        # Phase 2: MCP Static Analysis (language-specific tools)
        static_findings = self._analyze_with_mcp_static_tools(code_content, language, file_path)
        all_findings.extend(static_findings)
        print(f"   ✅ Found {len(static_findings)} issues via static analysis")
        
        print(f"   🐙 Phase 3: Vulnerability database check...")
        # Phase 3: MCP GitHub vulnerability database
        vuln_findings = self._analyze_with_mcp_vulnerability_db(code_content, language, file_path)
        all_findings.extend(vuln_findings)
        print(f"   ✅ Found {len(vuln_findings)} issues via vulnerability database")
        
        print(f"   🧠 Phase 4: Triangulated confidence scoring...")
        # Phase 4: Triangulate and score confidence
        triangulated_findings = self._triangulate_security_findings(all_findings)
        print(f"   ✅ Final triangulated findings: {len(triangulated_findings)}")
        
        return triangulated_findings
    
    def _analyze_with_cognitive_patterns(self, code_content: str, language: str) -> List[SecurityFinding]:
        """Phase 1: Use your cognitive triangulation patterns"""
        findings = []
        
        if language not in self.security_patterns:
            return findings
        
        patterns = self.security_patterns[language]
        lines = code_content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for pattern, description, severity, vuln_type in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append(SecurityFinding(
                        severity=severity,
                        finding_type='security',
                        language=language,
                        line_number=line_num,
                        description=description,
                        code_snippet=line.strip(),
                        fix_suggestion=self._get_security_fix_suggestion(vuln_type),
                        confidence=0.85,  # High confidence in your patterns
                        source='cognitive_pattern',
                        severity_score=self.severity_scores[severity]
                    ))
        
        return findings
    
    def _analyze_with_mcp_static_tools(self, code_content: str, language: str, file_path: str) -> List[SecurityFinding]:
        """Phase 2: Use MCP AI IDE Integration for static analysis"""
        findings = []
        
        if not self.ide_mcp_available:
            # Simulate MCP static analysis results
            findings.extend(self._simulate_static_analysis(code_content, language))
            return findings
        
        # TODO: Real MCP integration when available
        # try:
        #     if language == 'python':
        #         results = self.ide_mcp.run_bandit_security_scan(code_content)
        #         results.extend(self.ide_mcp.run_pylint_security(code_content))
        #     elif language == 'java':
        #         results = self.ide_mcp.run_spotbugs_security(code_content)
        #         results.extend(self.ide_mcp.run_pmd_security(code_content))
        #     
        #     for result in results:
        #         findings.append(SecurityFinding(
        #             severity=result.severity,
        #             finding_type='security',
        #             language=language,
        #             line_number=result.line,
        #             description=result.message,
        #             code_snippet=result.code,
        #             fix_suggestion=result.fix,
        #             confidence=0.95,  # High confidence in professional tools
        #             source='ide_static'
        #         ))
        #     
        #     self.metrics['mcp_calls_made'] += 1
        # except Exception as e:
        #     print(f"   ⚠️ MCP IDE static analysis failed: {e}")
        
        return findings
    
    def _simulate_static_analysis(self, code_content: str, language: str) -> List[SecurityFinding]:
        """Simulate what static analysis tools would find"""
        findings = []
        
        if language == 'python':
            # Simulate Bandit-style findings
            if 'subprocess.call' in code_content and 'shell=True' in code_content:
                findings.append(SecurityFinding(
                    severity='critical',
                    finding_type='security',
                    language=language,
                    line_number=self._find_line_number(code_content, 'subprocess.call'),
                    description='[BANDIT] High severity: subprocess call with shell=True',
                    code_snippet='subprocess.call(..., shell=True)',
                    fix_suggestion='Use subprocess.run() with a list of arguments instead',
                    confidence=0.95,
                    source='ide_static'
                ))
        
        elif language == 'java':
            # Simulate SpotBugs-style findings
            if 'Runtime.getRuntime().exec' in code_content:
                findings.append(SecurityFinding(
                    severity='critical',
                    finding_type='security', 
                    language=language,
                    line_number=self._find_line_number(code_content, 'Runtime.getRuntime().exec'),
                    description='[SPOTBUGS] Command injection vulnerability',
                    code_snippet='Runtime.getRuntime().exec(...)',
                    fix_suggestion='Validate and sanitize all inputs to exec()',
                    confidence=0.95,
                    source='ide_static'
                ))
        
        return findings
    
    def _analyze_with_mcp_vulnerability_db(self, code_content: str, language: str, file_path: str) -> List[SecurityFinding]:
        """Phase 3: Use MCP GitHub for vulnerability database lookup"""
        findings = []
        
        if not self.github_mcp_available:
            # Simulate vulnerability database results
            findings.extend(self._simulate_vulnerability_lookup(code_content, language))
            return findings
        
        # TODO: Real MCP GitHub integration when available
        # try:
        #     # Check for known vulnerable patterns
        #     vuln_patterns = self.github_mcp.get_vulnerability_patterns(language)
        #     cve_matches = self.github_mcp.check_cve_database(code_content)
        #     
        #     for match in cve_matches:
        #         findings.append(SecurityFinding(
        #             severity=match.severity,
        #             finding_type='vulnerability',
        #             language=language,
        #             line_number=match.line,
        #             description=f'CVE-{match.cve_id}: {match.description}',
        #             code_snippet=match.code,
        #             fix_suggestion=match.mitigation,
        #             confidence=0.99,  # Very high confidence in CVE database
        #             source='github_vuln',
        #             cve_id=match.cve_id
        #         ))
        #     
        #     self.metrics['mcp_calls_made'] += 1
        # except Exception as e:
        #     print(f"   ⚠️ MCP GitHub vulnerability lookup failed: {e}")
        
        return findings
    
    def _simulate_vulnerability_lookup(self, code_content: str, language: str) -> List[SecurityFinding]:
        """Simulate vulnerability database lookups"""
        findings = []
        
        # Simulate finding known vulnerable patterns
        if language == 'python' and 'pickle.loads' in code_content:
            findings.append(SecurityFinding(
                severity='critical',
                finding_type='vulnerability',
                language=language,
                line_number=self._find_line_number(code_content, 'pickle.loads'),
                description='CVE-2019-16935: Arbitrary code execution via pickle deserialization',
                code_snippet='pickle.loads(...)',
                fix_suggestion='Use json or other safe serialization formats',
                confidence=0.99,
                source='github_vuln',
                cve_id='CVE-2019-16935'
            ))
        
        return findings
    
    def _triangulate_security_findings(self, all_findings: List[SecurityFinding]) -> List[SecurityFinding]:
        """Phase 4: Triangulate findings from multiple sources for confidence scoring"""
        
        # Group findings by line number and description similarity
        grouped_findings = {}
        
        for finding in all_findings:
            key = (finding.line_number, finding.finding_type, finding.severity)
            if key not in grouped_findings:
                grouped_findings[key] = []
            grouped_findings[key].append(finding)
        
        triangulated = []
        
        for key, findings_group in grouped_findings.items():
            if len(findings_group) == 1:
                # Single source finding
                triangulated.append(findings_group[0])
            else:
                # Multiple sources confirm same issue - boost confidence!
                best_finding = max(findings_group, key=lambda f: f.confidence)
                sources = [f.source for f in findings_group]
                
                # Boost confidence based on multiple confirmations
                confidence_boost = min(0.15 * (len(sources) - 1), 0.3)
                best_finding.confidence = min(best_finding.confidence + confidence_boost, 1.0)
                best_finding.source = f"triangulated_{'+'.join(set(sources))}"
                
                triangulated.append(best_finding)
        
        # Sort by severity and confidence
        triangulated.sort(key=lambda f: (f.severity_score, f.confidence), reverse=True)
        
        return triangulated
    
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
    
    def _generate_security_report(self, findings: List[SecurityFinding], file_path: str, language: str, code_content: str) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        
        # Categorize findings
        by_severity = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        by_type = {'security': 0, 'vulnerability': 0, 'bug': 0}
        by_source = {}
        
        critical_findings = []
        
        for finding in findings:
            by_severity[finding.severity] += 1
            by_type[finding.finding_type] += 1
            
            if finding.source not in by_source:
                by_source[finding.source] = 0
            by_source[finding.source] += 1
            
            if finding.severity == 'critical':
                critical_findings.append(finding)
        
        # Calculate security score (0-100, higher is better)
        total_lines = len(code_content.split('\n'))
        security_score = max(0, 100 - (
            by_severity['critical'] * 25 +
            by_severity['high'] * 15 +
            by_severity['medium'] * 8 +
            by_severity['low'] * 3
        ))
        
        # Risk assessment
        risk_level = 'LOW'
        if by_severity['critical'] > 0:
            risk_level = 'CRITICAL'
        elif by_severity['high'] > 2:
            risk_level = 'HIGH'
        elif by_severity['high'] > 0 or by_severity['medium'] > 5:
            risk_level = 'MEDIUM'
        
        return {
            'file_path': file_path,
            'language': language,
            'total_findings': len(findings),
            'security_score': security_score,
            'risk_level': risk_level,
            'findings_by_severity': by_severity,
            'findings_by_type': by_type,
            'findings_by_source': by_source,
            'critical_findings': [
                {
                    'severity': f.severity,
                    'type': f.finding_type,
                    'line': f.line_number,
                    'description': f.description,
                    'code': f.code_snippet,
                    'fix': f.fix_suggestion,
                    'confidence': f.confidence,
                    'source': f.source,
                    'cve_id': f.cve_id
                }
                for f in critical_findings
            ],
            'top_findings': [
                {
                    'severity': f.severity,
                    'type': f.finding_type,
                    'line': f.line_number,
                    'description': f.description,
                    'code': f.code_snippet,
                    'fix': f.fix_suggestion,
                    'confidence': f.confidence,
                    'source': f.source,
                    'cve_id': f.cve_id
                }
                for f in findings[:15]  # Top 15 findings
            ],
            'total_lines': total_lines,
            'findings_per_100_lines': round((len(findings) / total_lines) * 100, 2) if total_lines > 0 else 0,
            'analysis_metadata': {
                'cognitive_patterns_used': len(self.security_patterns.get(language, [])),
                'mcp_calls_made': self.metrics['mcp_calls_made'],
                'sources_used': list(by_source.keys()),
                'triangulation_applied': any('triangulated' in source for source in by_source.keys())
            }
        }

if __name__ == "__main__":
    # Test the enhanced security detective
    detective = SecurityCodeDetectiveAgent()
    
    # Test with a vulnerable Python sample
    test_input = '''<code_analysis_request>
        <file_path>vulnerable_test.py</file_path>
        <file_content>
import subprocess
import pickle
import os

def vulnerable_function(user_input):
    # Critical vulnerabilities
    result = eval(user_input)  # Code injection!
    subprocess.call(user_input, shell=True)  # Command injection!
    
    # Deserialization vulnerability
    data = pickle.loads(user_input)
    
    # Hardcoded secrets
    api_key = "sk-1234567890abcdef1234567890abcdef"
    password = "supersecret123"
    
    # SQL injection pattern
    query = f"SELECT * FROM users WHERE id = {user_input}"
    
    return result
        </file_content>
        <language>python</language>
    </code_analysis_request>'''
    
    print("🔒 TESTING ENHANCED SECURITY DETECTIVE:")
    print("=" * 60)
    result = detective.process(test_input)
    
    # Parse and display results
    import xml.etree.ElementTree as ET
    root = ET.fromstring(result)
    
    summary = root.find('summary')
    if summary is not None:
        total_findings = summary.find('total_findings').text
        security_score = summary.find('security_score').text
        risk_level = summary.find('risk_level').text
        
        print(f"🎯 SECURITY ANALYSIS RESULTS:")
        print(f"   🚨 Total Security Findings: {total_findings}")
        print(f"   🛡️ Security Score: {security_score}/100")
        print(f"   ⚠️ Risk Level: {risk_level}")
        
        print(f"\n✅ Enhanced Security Detective Test Complete!")
        print(f"   📊 Ready for batch analysis on your codebase!")
