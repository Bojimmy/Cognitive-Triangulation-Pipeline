#!/usr/bin/env python3
"""
Code Quality Detective Agent
Specialized X-Agent for finding bugs, code smells, and quality issues

Unlike structural analysis agents, this detective looks for:
- Logic errors and potential bugs
- Error handling problems  
- Performance anti-patterns
- Maintainability issues
- Security vulnerabilities
"""
import ast
import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import time

@dataclass
class CodeIssue:
    """Represents a detected code quality issue"""
    severity: str  # 'critical', 'high', 'medium', 'low'
    issue_type: str  # 'bug', 'security', 'performance', 'maintainability'
    line_number: int
    description: str
    code_snippet: str
    fix_suggestion: str
    confidence: float

class CodeQualityDetectiveAgent:
    """
    X-Agent specialized in detecting code quality issues and bugs
    
    This detective uses multiple detection strategies:
    1. AST-based analysis for logical issues
    2. Pattern matching for common anti-patterns
    3. Complexity analysis for maintainability
    4. Security pattern detection
    """
    
    def __init__(self):
        self.agent_type = "code_quality_detective"
        self.metrics = {'total_time': 0.0, 'issues_found': 0}
        
        # Initialize detection patterns
        self._setup_detection_patterns()
    
    def _setup_detection_patterns(self):
        """Setup patterns for different types of code issues"""
        
        # Bug-prone patterns
        self.bug_patterns = [
            (r'except\s*:', 'Bare except clause catches all exceptions', 'high'),
            (r'eval\s*\(', 'Use of eval() is dangerous', 'critical'),
            (r'exec\s*\(', 'Use of exec() is dangerous', 'critical'),
            (r'import\s+\*', 'Wildcard imports can cause namespace pollution', 'medium'),
            (r'==\s*None', 'Use "is None" instead of "== None"', 'medium'),
            (r'!=\s*None', 'Use "is not None" instead of "!= None"', 'medium'),
            (r'time\.sleep\(\d+\)', 'Long sleep statements can cause blocking', 'medium'),
        ]
        
        # Performance anti-patterns
        self.performance_patterns = [
            (r'\.append\(.+\)\s*$.*for.*in', 'Consider list comprehension instead of append in loop', 'low'),
            (r'len\(.+\)\s*==\s*0', 'Use "not sequence" instead of "len(sequence) == 0"', 'low'),
            (r'len\(.+\)\s*>\s*0', 'Use "sequence" instead of "len(sequence) > 0"', 'low'),
        ]
        
        # Security patterns
        self.security_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password detected', 'critical'),
            (r'api_key\s*=\s*["\'][^"\']+["\']', 'Hardcoded API key detected', 'critical'),
            (r'secret\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret detected', 'critical'),
            (r'subprocess\.call\(.+shell=True', 'Shell injection vulnerability', 'high'),
        ]
    
    def process(self, input_xml: str) -> str:
        """Main processing method for the X-Agent"""
        start_time = time.time()
        
        try:
            # Parse input XML
            root = ET.fromstring(input_xml)
            
            # Extract code content
            code_content = self._extract_code_content(root)
            file_path = root.find('.//file_path')
            file_path_str = file_path.text if file_path is not None else "unknown"
            
            # Run comprehensive code quality analysis
            issues = self._detect_code_issues(code_content, file_path_str)
            
            # Generate quality report
            result = self._generate_quality_report(issues, file_path_str, code_content)
            
            # Update metrics
            processing_time = time.time() - start_time
            self.metrics['total_time'] += processing_time
            self.metrics['issues_found'] += len(issues)
            
            return self._generate_xml_output(result)
            
        except Exception as e:
            return self._generate_error_xml(str(e))
    
    def _extract_code_content(self, root: ET.Element) -> str:
        """Extract code content from XML input"""
        content_elem = root.find('.//file_content')
        if content_elem is None:
            content_elem = root.find('.//content')
        if content_elem is None:
            content_elem = root.find('.//code')
        
        if content_elem is not None:
            content = content_elem.text or ""
            # Unescape HTML entities if present
            import html
            return html.unescape(content)
        else:
            return ""
    
    def _detect_code_issues(self, code_content: str, file_path: str) -> List[CodeIssue]:
        """Main detection method - runs all quality checks"""
        issues = []
        
        # 1. AST-based analysis for structural issues
        issues.extend(self._analyze_ast_issues(code_content))
        
        # 2. Pattern-based detection for common problems
        issues.extend(self._detect_pattern_issues(code_content))
        
        # 3. Complexity analysis
        issues.extend(self._analyze_complexity_issues(code_content))
        
        # 4. Error handling analysis
        issues.extend(self._analyze_error_handling(code_content))
        
        # 5. Import and dependency analysis
        issues.extend(self._analyze_imports(code_content))
        
        # Sort by severity and confidence
        issues.sort(key=lambda x: (
            {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}[x.severity], 
            x.confidence
        ), reverse=True)
        
        return issues
    
    def _analyze_ast_issues(self, code_content: str) -> List[CodeIssue]:
        """Use AST to find structural and logical issues"""
        issues = []
        
        try:
            tree = ast.parse(code_content)
            
            for node in ast.walk(tree):
                # Detect unreachable code after return
                if isinstance(node, ast.FunctionDef):
                    issues.extend(self._check_unreachable_code(node))
                
                # Detect unused variables
                if isinstance(node, ast.Assign):
                    issues.extend(self._check_unused_assignments(node, tree))
                
                # Detect too many nested levels
                if isinstance(node, (ast.If, ast.For, ast.While)):
                    issues.extend(self._check_nesting_depth(node))
                
                # Detect missing return statements
                if isinstance(node, ast.FunctionDef):
                    issues.extend(self._check_missing_returns(node))
        
        except SyntaxError as e:
            issues.append(CodeIssue(
                severity='critical',
                issue_type='bug',
                line_number=e.lineno or 0,
                description=f'Syntax Error: {str(e)}',
                code_snippet=str(e.text) if e.text else '',
                fix_suggestion='Fix the syntax error',
                confidence=1.0
            ))
        
        return issues
    
    def _detect_pattern_issues(self, code_content: str) -> List[CodeIssue]:
        """Detect issues using regex patterns"""
        issues = []
        lines = code_content.split('\n')
        
        # Check all pattern categories
        all_patterns = [
            (self.bug_patterns, 'bug'),
            (self.performance_patterns, 'performance'), 
            (self.security_patterns, 'security')
        ]
        
        for patterns, issue_type in all_patterns:
            for pattern, description, severity in patterns:
                for line_num, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append(CodeIssue(
                            severity=severity,
                            issue_type=issue_type,
                            line_number=line_num,
                            description=description,
                            code_snippet=line.strip(),
                            fix_suggestion=self._get_fix_suggestion(pattern, description),
                            confidence=0.8
                        ))
        
        return issues
    
    def _analyze_complexity_issues(self, code_content: str) -> List[CodeIssue]:
        """Analyze code complexity issues"""
        issues = []
        lines = code_content.split('\n')
        
        # Check for overly long functions
        current_function = None
        function_start = 0
        function_lines = 0
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('def '):
                if current_function and function_lines > 50:
                    issues.append(CodeIssue(
                        severity='medium',
                        issue_type='maintainability',
                        line_number=function_start,
                        description=f'Function "{current_function}" is too long ({function_lines} lines)',
                        code_snippet=f'def {current_function}...',
                        fix_suggestion='Consider breaking this function into smaller functions',
                        confidence=0.9
                    ))
                
                current_function = line.split('def ')[1].split('(')[0]
                function_start = line_num
                function_lines = 1
            elif current_function:
                function_lines += 1
        
        # Check final function
        if current_function and function_lines > 50:
            issues.append(CodeIssue(
                severity='medium',
                issue_type='maintainability',
                line_number=function_start,
                description=f'Function "{current_function}" is too long ({function_lines} lines)',
                code_snippet=f'def {current_function}...',
                fix_suggestion='Consider breaking this function into smaller functions',
                confidence=0.9
            ))
        
        return issues
    
    def _analyze_error_handling(self, code_content: str) -> List[CodeIssue]:
        """Analyze error handling patterns"""
        issues = []
        lines = code_content.split('\n')
        
        in_try_block = False
        try_line = 0
        has_except = False
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('try:'):
                in_try_block = True
                try_line = line_num
                has_except = False
            
            elif stripped.startswith('except') and in_try_block:
                has_except = True
                
                # Check for bare except
                if stripped == 'except:':
                    issues.append(CodeIssue(
                        severity='high',
                        issue_type='bug',
                        line_number=line_num,
                        description='Bare except clause catches all exceptions',
                        code_snippet=stripped,
                        fix_suggestion='Specify the exception type: except SpecificException:',
                        confidence=1.0
                    ))
            
            elif (stripped.startswith('def ') or stripped.startswith('class ')) and in_try_block:
                if not has_except:
                    issues.append(CodeIssue(
                        severity='medium',
                        issue_type='bug',
                        line_number=try_line,
                        description='Try block without except clause',
                        code_snippet='try: ... (no except)',
                        fix_suggestion='Add appropriate except clause',
                        confidence=0.9
                    ))
                in_try_block = False
        
        return issues
    
    def _analyze_imports(self, code_content: str) -> List[CodeIssue]:
        """Analyze import statements for issues"""
        issues = []
        lines = code_content.split('\n')
        
        imported_modules = set()
        used_modules = set()
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Track imports
            if stripped.startswith('import ') or stripped.startswith('from '):
                if '*' in stripped:
                    issues.append(CodeIssue(
                        severity='medium',
                        issue_type='maintainability',
                        line_number=line_num,
                        description='Wildcard import detected',
                        code_snippet=stripped,
                        fix_suggestion='Import specific items instead of using *',
                        confidence=0.9
                    ))
                
                # Extract module name
                if stripped.startswith('import '):
                    module = stripped.split('import ')[1].split()[0].split('.')[0]
                    imported_modules.add(module)
                elif stripped.startswith('from ') and ' import ' in stripped:
                    module = stripped.split('from ')[1].split(' import')[0].split('.')[0]
                    imported_modules.add(module)
        
        return issues
    
    def _check_unreachable_code(self, func_node: ast.FunctionDef) -> List[CodeIssue]:
        """Check for unreachable code after return statements"""
        issues = []
        
        for i, stmt in enumerate(func_node.body[:-1]):  # All but last statement
            if isinstance(stmt, ast.Return):
                next_stmt = func_node.body[i + 1]
                issues.append(CodeIssue(
                    severity='medium',
                    issue_type='bug',
                    line_number=next_stmt.lineno,
                    description='Unreachable code after return statement',
                    code_snippet='Code after return',
                    fix_suggestion='Remove unreachable code or restructure logic',
                    confidence=0.95
                ))
        
        return issues
    
    def _check_unused_assignments(self, assign_node: ast.Assign, tree: ast.AST) -> List[CodeIssue]:
        """Check for potentially unused variable assignments"""
        # This is a simplified check - full implementation would need scope analysis
        return []
    
    def _check_nesting_depth(self, node: ast.stmt) -> List[CodeIssue]:
        """Check for excessive nesting depth"""
        def count_nesting(node, depth=0):
            max_depth = depth
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.With)):
                    child_depth = count_nesting(child, depth + 1)
                    max_depth = max(max_depth, child_depth)
            return max_depth
        
        depth = count_nesting(node)
        if depth > 4:
            return [CodeIssue(
                severity='medium',
                issue_type='maintainability',
                line_number=node.lineno,
                description=f'Excessive nesting depth: {depth} levels',
                code_snippet='Deep nesting detected',
                fix_suggestion='Consider extracting nested logic into functions',
                confidence=0.8
            )]
        
        return []
    
    def _check_missing_returns(self, func_node: ast.FunctionDef) -> List[CodeIssue]:
        """Check for functions that might be missing return statements"""
        has_return = any(isinstance(stmt, ast.Return) for stmt in ast.walk(func_node))
        
        # If function has no return and is not a simple setter/procedure
        if not has_return and len(func_node.body) > 3:
            return [CodeIssue(
                severity='low',
                issue_type='maintainability',
                line_number=func_node.lineno,
                description=f'Function "{func_node.name}" has no return statement',
                code_snippet=f'def {func_node.name}...',
                fix_suggestion='Consider adding explicit return statement or documenting if intentional',
                confidence=0.6
            )]
        
        return []
    
    def _get_fix_suggestion(self, pattern: str, description: str) -> str:
        """Generate fix suggestions based on the detected pattern"""
        fix_map = {
            'except\\s*:': 'Replace with "except SpecificException:" to catch specific errors',
            'eval\\s*\\(': 'Use ast.literal_eval() for safe evaluation or redesign without eval',
            'exec\\s*\\(': 'Redesign code to avoid exec() - consider function dispatch or other patterns',
            '==\\s*None': 'Replace "== None" with "is None"',
            '!=\\s*None': 'Replace "!= None" with "is not None"',
            'len\\(.+\\)\\s*==\\s*0': 'Use "not sequence" instead of "len(sequence) == 0"',
            'password.*=': 'Move sensitive data to environment variables or secure config',
        }
        
        for pattern_key, suggestion in fix_map.items():
            if pattern_key in pattern:
                return suggestion
        
        return 'Review and fix this issue'
    
    def _generate_quality_report(self, issues: List[CodeIssue], file_path: str, code_content: str) -> Dict[str, Any]:
        """Generate comprehensive quality report"""
        
        # Categorize issues
        by_severity = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        by_type = {'bug': 0, 'security': 0, 'performance': 0, 'maintainability': 0}
        
        for issue in issues:
            by_severity[issue.severity] += 1
            by_type[issue.issue_type] += 1
        
        # Calculate quality score
        total_lines = len(code_content.split('\n'))
        quality_score = max(0, 100 - (
            by_severity['critical'] * 20 +
            by_severity['high'] * 10 +
            by_severity['medium'] * 5 +
            by_severity['low'] * 1
        ))
        
        return {
            'file_path': file_path,
            'total_issues': len(issues),
            'quality_score': quality_score,
            'issues_by_severity': by_severity,
            'issues_by_type': by_type,
            'issues': [
                {
                    'severity': issue.severity,
                    'type': issue.issue_type,
                    'line': issue.line_number,
                    'description': issue.description,
                    'code': issue.code_snippet,
                    'fix': issue.fix_suggestion,
                    'confidence': issue.confidence
                }
                for issue in issues[:10]  # Top 10 issues
            ],
            'total_lines': total_lines,
            'issues_per_100_lines': round((len(issues) / total_lines) * 100, 2) if total_lines > 0 else 0
        }
    
    def _generate_xml_output(self, result: Dict[str, Any]) -> str:
        """Generate XML output for next agent in pipeline"""
        root = ET.Element("code_quality_analysis")
        
        # Summary
        summary = ET.SubElement(root, "summary")
        ET.SubElement(summary, "file_path").text = result['file_path']
        ET.SubElement(summary, "total_issues").text = str(result['total_issues'])
        ET.SubElement(summary, "quality_score").text = str(result['quality_score'])
        ET.SubElement(summary, "total_lines").text = str(result['total_lines'])
        ET.SubElement(summary, "issues_per_100_lines").text = str(result['issues_per_100_lines'])
        
        # Issues by severity
        severity_elem = ET.SubElement(root, "issues_by_severity")
        for severity, count in result['issues_by_severity'].items():
            ET.SubElement(severity_elem, severity).text = str(count)
        
        # Issues by type
        type_elem = ET.SubElement(root, "issues_by_type")
        for issue_type, count in result['issues_by_type'].items():
            ET.SubElement(type_elem, issue_type).text = str(count)
        
        # Top issues
        issues_elem = ET.SubElement(root, "top_issues")
        for issue in result['issues']:
            issue_elem = ET.SubElement(issues_elem, "issue")
            ET.SubElement(issue_elem, "severity").text = issue['severity']
            ET.SubElement(issue_elem, "type").text = issue['type']
            ET.SubElement(issue_elem, "line_number").text = str(issue['line'])
            ET.SubElement(issue_elem, "description").text = issue['description']
            ET.SubElement(issue_elem, "code_snippet").text = issue['code']
            ET.SubElement(issue_elem, "fix_suggestion").text = issue['fix']
            ET.SubElement(issue_elem, "confidence").text = str(issue['confidence'])
        
        return ET.tostring(root, encoding='unicode')
    
    def _generate_error_xml(self, error_message: str) -> str:
        """Generate error XML response"""
        root = ET.Element("code_quality_analysis")
        error_elem = ET.SubElement(root, "error")
        error_elem.text = error_message
        return ET.tostring(root, encoding='unicode')

if __name__ == "__main__":
    # Test the detective on a sample
    detective = CodeQualityDetectiveAgent()
    
    test_input = '''<code_analysis_request>
        <file_path>test.py</file_path>
        <file_content>
def broken_function():
    try:
        password = "hardcoded123"
        result = eval(user_input)
        if result == None:
            return
        print("unreachable code")
    except:
        pass
    
def very_long_function():
    # This would be a 100+ line function in reality
    pass
        </file_content>
    </code_analysis_request>'''
    
    result = detective.process(test_input)
    print("🔍 CODE QUALITY DETECTIVE TEST RESULT:")
    print(result)
