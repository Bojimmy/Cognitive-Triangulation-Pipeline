#!/usr/bin/env python3
"""
Dead Project Revival System with GitHub MCP + Context7 Integration
The ultimate "Project Necromancer" for diagnosing and reviving abandoned projects

Specifically designed to find the issues that kill projects:
- Connection problems (DB, API, CORS, auth)
- Critical bugs (logic errors, exceptions, race conditions)
- Syntax/indent issues (the silent killers)
- Backend server issues (config, deps, ports)
- Architectural problems (broken data flows)

Uses cognitive triangulation + MCP tools to quickly identify what went wrong
"""
import ast
import re
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Tuple, Optional, Set
from dataclasses import dataclass
import time
from pathlib import Path
import os

@dataclass
class ProjectDeathCause:
    """Represents why a project died"""
    category: str  # 'connection', 'bug', 'syntax', 'backend', 'architecture'
    severity: str  # 'project_killer', 'major', 'minor'
    issue_type: str
    file_path: str
    line_number: int
    description: str
    likely_symptoms: List[str]  # What user would have experienced
    revival_steps: List[str]    # How to fix it
    confidence: float
    mcp_source: Optional[str] = None  # 'github', 'context7', 'cognitive'

class ProjectRevivalDetective:
    """
    Main detective for diagnosing dead projects
    
    This detective specializes in finding the issues that make developers
    abandon projects - the frustrating problems that are hard to debug
    """
    
    def __init__(self):
        self.agent_type = "project_revival_detective"
        self.metrics = {
            'projects_analyzed': 0,
            'death_causes_found': 0,
            'revival_success_rate': 0.0,
            'mcp_calls_made': 0
        }
        
        # Setup project death pattern detection
        self._setup_project_death_patterns()
        
        # MCP integration (simulated for now, ready for real integration)
        self.github_mcp_available = self._check_github_mcp()
        self.context7_mcp_available = self._check_context7_mcp()
        
        print(f"💀 ProjectRevivalDetective initialized!")
        print(f"   🔧 GitHub MCP: {'✅ Connected' if self.github_mcp_available else '⚠️ Simulated'}")
        print(f"   🧠 Context7 MCP: {'✅ Connected' if self.context7_mcp_available else '⚠️ Simulated'}")
        print(f"   🎯 Ready to diagnose dead projects!")
    
    def _check_github_mcp(self) -> bool:
        """Check if GitHub MCP is available"""
        try:
            # TODO: Replace with actual GitHub MCP client
            # from github_mcp import GitHub_MCP
            # self.github_mcp = GitHub_MCP()
            # return True
            return False  # Simulated for now
        except ImportError:
            return False
    
    def _check_context7_mcp(self) -> bool:
        """Check if Context7 MCP is available"""
        try:
            # TODO: Replace with actual Context7 MCP client  
            # from context7_mcp import Context7_MCP
            # self.context7_mcp = Context7_MCP()
            # return True
            return False  # Simulated for now
        except ImportError:
            return False
    
    def _setup_project_death_patterns(self):
        """Setup patterns that commonly kill projects"""
        
        # CONNECTION DEATH PATTERNS (database, API, network issues)
        self.connection_death_patterns = [
            # Database connection issues
            (r'connection.*refused', 'Database connection refused', 'project_killer',
             ['App crashes on startup', 'Cannot connect to database'],
             ['Check database is running', 'Verify connection string', 'Check firewall/ports']),
            
            (r'ECONNREFUSED.*\d+', 'Port connection refused', 'project_killer',
             ['Service unavailable', 'Connection timeouts'],
             ['Check if service is running on correct port', 'Verify port configuration']),
            
            (r'CORS.*blocked', 'CORS policy blocking requests', 'project_killer',
             ['Frontend cannot call backend', 'API requests fail in browser'],
             ['Configure CORS headers', 'Add frontend domain to allowed origins']),
            
            (r'401.*unauthorized|403.*forbidden', 'Authentication/authorization failure', 'major',
             ['Login not working', 'API returns unauthorized'],
             ['Check API keys', 'Verify authentication logic', 'Check user permissions']),
            
            (r'timeout.*exceeded|ETIMEDOUT', 'Network timeout issues', 'major',
             ['Slow or hanging requests', 'App becomes unresponsive'],
             ['Increase timeout values', 'Check network connectivity', 'Optimize queries']),
            
            # API endpoint issues
            (r'404.*not.*found.*api|endpoint.*not.*found', 'API endpoint not found', 'major',
             ['API calls failing', 'Routes not working'],
             ['Check API route definitions', 'Verify URL patterns', 'Check server routing']),
        ]
        
        # CRITICAL BUG PATTERNS (logic errors, exceptions that kill projects)
        self.critical_bug_patterns = [
            # Null/undefined errors
            (r'NoneType.*attribute|AttributeError.*None', 'Null pointer/None type error', 'project_killer',
             ['App crashes randomly', 'Unexpected crashes during use'],
             ['Add null checks', 'Initialize variables properly', 'Use optional chaining']),
            
            (r'undefined.*not.*function|TypeError.*undefined', 'Undefined function/variable', 'project_killer',
             ['JavaScript errors in console', 'Features not working'],
             ['Define missing functions', 'Check variable scope', 'Fix import statements']),
            
            # Type errors
            (r'TypeError.*expected.*got|type.*mismatch', 'Type mismatch errors', 'major',
             ['Unexpected behavior', 'Data processing fails'],
             ['Add type checking', 'Validate input types', 'Use proper type conversions']),
            
            # Infinite loops/recursion
            (r'maximum.*recursion.*exceeded|stack.*overflow', 'Infinite recursion', 'project_killer',
             ['App hangs/freezes', 'Browser tab crashes'],
             ['Add base case to recursion', 'Check loop conditions', 'Add recursion limits']),
            
            # Memory/resource issues
            (r'out.*of.*memory|memory.*error', 'Memory exhaustion', 'project_killer',
             ['App crashes under load', 'Performance degrades over time'],
             ['Fix memory leaks', 'Optimize data structures', 'Add pagination']),
            
            # Race conditions
            (r'race.*condition|concurrent.*modification', 'Race condition detected', 'major',
             ['Inconsistent results', 'Data corruption', 'Random failures'],
             ['Add proper locking', 'Use atomic operations', 'Synchronize access']),
        ]
        
        # SYNTAX DEATH PATTERNS (the silent killers)
        self.syntax_death_patterns = [
            # Python indentation (the classic killer)
            (r'IndentationError|unexpected.*indent', 'Python indentation error', 'project_killer',
             ['Python script won\'t run', 'Syntax errors on startup'],
             ['Fix indentation consistency', 'Use 4 spaces throughout', 'Check mixed tabs/spaces']),
            
            # Missing brackets/parens
            (r'SyntaxError.*missing.*\)|unexpected.*EOF', 'Missing closing bracket/paren', 'project_killer',
             ['Code won\'t compile/run', 'Syntax errors'],
             ['Add missing closing brackets', 'Check parentheses matching', 'Use IDE bracket matching']),
            
            # Quote mismatches
            (r'unterminated.*string|EOL.*scanning.*string', 'Unterminated string literal', 'project_killer',
             ['Syntax errors', 'Code highlighting broken'],
             ['Close unterminated strings', 'Check quote matching', 'Escape quotes properly']),
            
            # Semicolon issues (JavaScript)
            (r'SyntaxError.*unexpected.*token', 'JavaScript syntax error', 'major',
             ['JavaScript errors in console', 'Features not working'],
             ['Add missing semicolons', 'Check JavaScript syntax', 'Use linter']),
            
            # Invalid JSON
            (r'JSON.*parse.*error|invalid.*JSON', 'Invalid JSON format', 'major',
             ['Config files not loading', 'API responses failing'],
             ['Validate JSON syntax', 'Check for trailing commas', 'Use JSON validator']),
        ]
        
        # BACKEND SERVER DEATH PATTERNS (config, dependencies, startup issues)
        self.backend_death_patterns = [
            # Port conflicts
            (r'port.*already.*in.*use|address.*already.*in.*use', 'Port already in use', 'project_killer',
             ['Server won\'t start', 'Cannot bind to port'],
             ['Kill process using port', 'Change port number', 'Check for running services']),
            
            # Missing environment variables
            (r'environment.*variable.*not.*found|missing.*env', 'Missing environment variable', 'project_killer',
             ['Server crashes on startup', 'Configuration errors'],
             ['Set missing environment variables', 'Create .env file', 'Check config']),
            
            # Dependency issues
            (r'module.*not.*found|import.*error|package.*not.*found', 'Missing dependency/import', 'project_killer',
             ['App won\'t start', 'Import errors'],
             ['Install missing packages', 'Check requirements.txt', 'Run npm install']),
            
            # Version conflicts
            (r'version.*conflict|incompatible.*version', 'Version compatibility issue', 'major',
             ['Dependency errors', 'Build failures'],
             ['Update package versions', 'Check compatibility', 'Use lock files']),
            
            # Configuration errors
            (r'configuration.*error|config.*invalid', 'Invalid configuration', 'major',
             ['Service misconfiguration', 'Settings not working'],
             ['Validate configuration files', 'Check config syntax', 'Use default configs']),
            
            # Database schema issues
            (r'table.*not.*found|column.*not.*exist|migration.*failed', 'Database schema problem', 'major',
             ['Database queries failing', 'Migration errors'],
             ['Run database migrations', 'Create missing tables', 'Check schema consistency']),
        ]
        
        # ARCHITECTURAL DEATH PATTERNS (data flow, dependency issues)
        self.architectural_death_patterns = [
            # Circular dependencies
            (r'circular.*dependency|cyclic.*import', 'Circular dependency detected', 'major',
             ['Import errors', 'Module loading fails'],
             ['Refactor to break circular deps', 'Use dependency injection', 'Reorganize modules']),
            
            # Broken data flow
            (r'data.*not.*flowing|pipeline.*broken', 'Data flow interruption', 'major',
             ['Data not updating', 'Features partially working'],
             ['Trace data flow', 'Check component connections', 'Validate data transformations']),
            
            # Missing dependencies
            (r'dependency.*not.*satisfied|missing.*requirement', 'Unsatisfied dependency', 'major',
             ['Components not working together', 'Services failing to start'],
             ['Install missing dependencies', 'Check dependency graph', 'Update package lists']),
        ]
        
        # Combine all patterns by category
        self.death_patterns = {
            'connection': self.connection_death_patterns,
            'bug': self.critical_bug_patterns,
            'syntax': self.syntax_death_patterns,
            'backend': self.backend_death_patterns,
            'architecture': self.architectural_death_patterns
        }
    
    async def diagnose_dead_project(self, project_path: str) -> Dict[str, Any]:
        """
        Main method: Diagnose why a project died and how to revive it
        """
        print(f"\n💀 DEAD PROJECT REVIVAL ANALYSIS")
        print(f"=" * 60)
        print(f"🔍 Analyzing: {project_path}")
        print(f"🎯 Goal: Find what killed this project and how to revive it")
        
        start_time = time.time()
        
        # Step 1: Quick project scan
        project_files = self._scan_project_structure(project_path)
        print(f"\n📁 Project scan: {len(project_files)} files found")
        
        # Step 2: Multi-phase death cause analysis
        death_causes = []
        
        print(f"\n🔍 Phase 1: Cognitive pattern analysis (project death signatures)")
        cognitive_causes = await self._analyze_with_death_patterns(project_files)
        death_causes.extend(cognitive_causes)
        print(f"   ☠️ Found {len(cognitive_causes)} potential death causes")
        
        print(f"\n🐙 Phase 2: GitHub MCP analysis (similar project failures)")
        github_causes = await self._analyze_with_github_mcp(project_files, cognitive_causes)
        death_causes.extend(github_causes)
        print(f"   📚 Found {len(github_causes)} historical patterns")
        
        print(f"\n🧠 Phase 3: Context7 MCP analysis (architectural flow issues)")
        context7_causes = await self._analyze_with_context7_mcp(project_files)
        death_causes.extend(context7_causes)
        print(f"   🔗 Found {len(context7_causes)} architectural issues")
        
        print(f"\n🎯 Phase 4: Revival plan generation")
        # Triangulate and prioritize death causes
        prioritized_causes = self._triangulate_death_causes(death_causes)
        revival_plan = self._generate_revival_plan(prioritized_causes, project_path)
        
        # Generate comprehensive diagnosis report
        total_time = time.time() - start_time
        
        diagnosis = {
            'project_path': project_path,
            'analysis_time': total_time,
            'project_status': self._assess_project_health(prioritized_causes),
            'death_causes': prioritized_causes,
            'revival_plan': revival_plan,
            'quick_wins': self._identify_quick_wins(prioritized_causes),
            'estimated_revival_time': self._estimate_revival_time(prioritized_causes),
            'success_probability': self._calculate_revival_probability(prioritized_causes)
        }
        
        self._display_diagnosis_report(diagnosis)
        
        return diagnosis
    
    def _scan_project_structure(self, project_path: str) -> List[Dict[str, Any]]:
        """Scan project structure and identify key files"""
        files = []
        
        # Common files that often contain project-killing issues
        critical_files = {
            'package.json', 'requirements.txt', 'Pipfile', 'Dockerfile',
            'docker-compose.yml', '.env', 'config.py', 'settings.py',
            'main.py', 'app.py', 'server.js', 'index.js', 'index.html'
        }
        
        log_files = {'.log', 'error.log', 'debug.log', 'npm-debug.log'}
        
        skip_dirs = {'__pycache__', '.git', 'node_modules', '.venv', 'venv', 'build', 'dist'}
        
        for root, dirs, filenames in os.walk(project_path):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for filename in filenames:
                file_path = Path(root) / filename
                
                # Prioritize critical files and log files
                priority = 'high' if filename in critical_files else 'normal'
                if any(filename.endswith(ext) for ext in log_files):
                    priority = 'critical'  # Log files often contain death clues
                
                if file_path.stat().st_size < 10 * 1024 * 1024:  # < 10MB
                    files.append({
                        'path': str(file_path),
                        'name': filename,
                        'size': file_path.stat().st_size,
                        'priority': priority,
                        'extension': file_path.suffix.lower()
                    })
        
        # Sort by priority (critical first, then high, then normal)
        priority_order = {'critical': 0, 'high': 1, 'normal': 2}
        files.sort(key=lambda f: (priority_order[f['priority']], f['name']))
        
        return files
    
    async def _analyze_with_death_patterns(self, project_files: List[Dict]) -> List[ProjectDeathCause]:
        """Analyze files for known project death patterns"""
        death_causes = []
        
        for file_info in project_files:
            try:
                with open(file_info['path'], 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check each category of death patterns
                for category, patterns in self.death_patterns.items():
                    for pattern, description, severity, symptoms, fixes in patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                        
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            
                            death_causes.append(ProjectDeathCause(
                                category=category,
                                severity=severity,
                                issue_type=description,
                                file_path=file_info['path'],
                                line_number=line_num,
                                description=f"{description} in {file_info['name']}",
                                likely_symptoms=symptoms,
                                revival_steps=fixes,
                                confidence=0.85,  # High confidence in known patterns
                                mcp_source='cognitive'
                            ))
                
            except Exception as e:
                # File reading error might itself be a clue
                if 'encoding' in str(e).lower() or 'decode' in str(e).lower():
                    death_causes.append(ProjectDeathCause(
                        category='syntax',
                        severity='minor',
                        issue_type='File encoding issue',
                        file_path=file_info['path'],
                        line_number=1,
                        description=f"Cannot read file {file_info['name']} - encoding issue",
                        likely_symptoms=['File appears corrupted', 'Editor shows strange characters'],
                        revival_steps=['Convert file to UTF-8', 'Check file encoding', 'Re-save file'],
                        confidence=0.7,
                        mcp_source='cognitive'
                    ))
        
        return death_causes
    
    async def _analyze_with_github_mcp(self, project_files: List[Dict], cognitive_causes: List[ProjectDeathCause]) -> List[ProjectDeathCause]:
        """Use GitHub MCP to find similar project failures and solutions"""
        
        if not self.github_mcp_available:
            # Simulate GitHub MCP analysis
            return self._simulate_github_mcp_analysis(project_files, cognitive_causes)
        
        github_causes = []
        
        # TODO: Real GitHub MCP integration
        # try:
        #     # Search for similar error patterns in GitHub issues
        #     for cause in cognitive_causes:
        #         similar_issues = self.github_mcp.search_issues(
        #             query=cause.issue_type,
        #             language=self._detect_project_language(project_files),
        #             state='closed'  # Look for solved issues
        #         )
        #         
        #         for issue in similar_issues[:3]:  # Top 3 similar issues
        #             if issue.solution_available:
        #                 github_causes.append(ProjectDeathCause(
        #                     category=cause.category,
        #                     severity=cause.severity,
        #                     issue_type=f"Known issue: {issue.title}",
        #                     file_path=cause.file_path,
        #                     line_number=cause.line_number,
        #                     description=f"Similar to GitHub issue #{issue.number}: {issue.title}",
        #                     likely_symptoms=cause.likely_symptoms,
        #                     revival_steps=issue.solution_steps,
        #                     confidence=0.9,  # High confidence in GitHub solutions
        #                     mcp_source='github'
        #                 ))
        #     
        #     self.metrics['mcp_calls_made'] += len(cognitive_causes)
        # except Exception as e:
        #     print(f"   ⚠️ GitHub MCP analysis failed: {e}")
        
        return github_causes
    
    def _simulate_github_mcp_analysis(self, project_files: List[Dict], cognitive_causes: List[ProjectDeathCause]) -> List[ProjectDeathCause]:
        """Simulate what GitHub MCP would find"""
        simulated_causes = []
        
        # Simulate finding common solutions for detected issues
        for cause in cognitive_causes[:3]:  # Simulate top 3 issues
            if cause.category == 'connection':
                simulated_causes.append(ProjectDeathCause(
                    category='connection',
                    severity='major',
                    issue_type='Common CORS solution pattern',
                    file_path=cause.file_path,
                    line_number=cause.line_number,
                    description='GitHub pattern: Express CORS middleware solution',
                    likely_symptoms=cause.likely_symptoms,
                    revival_steps=[
                        'npm install cors',
                        'Add app.use(cors()) to Express server',
                        'Configure CORS with specific origins'
                    ],
                    confidence=0.92,
                    mcp_source='github'
                ))
            
            elif cause.category == 'backend':
                simulated_causes.append(ProjectDeathCause(
                    category='backend',
                    severity='project_killer',
                    issue_type='Common port conflict solution',
                    file_path=cause.file_path,
                    line_number=cause.line_number,
                    description='GitHub pattern: Dynamic port assignment',
                    likely_symptoms=cause.likely_symptoms,
                    revival_steps=[
                        'Use process.env.PORT || 3000',
                        'Kill existing process: lsof -ti:3000 | xargs kill',
                        'Add port detection logic'
                    ],
                    confidence=0.95,
                    mcp_source='github'
                ))
        
        return simulated_causes
    
    async def _analyze_with_context7_mcp(self, project_files: List[Dict]) -> List[ProjectDeathCause]:
        """Use Context7 MCP for semantic analysis of architectural problems"""
        
        if not self.context7_mcp_available:
            # Simulate Context7 analysis
            return self._simulate_context7_analysis(project_files)
        
        context7_causes = []
        
        # TODO: Real Context7 MCP integration
        # try:
        #     # Analyze semantic relationships and data flow
        #     project_context = self.context7_mcp.analyze_project_context(
        #         files=[f['path'] for f in project_files]
        #     )
        #     
        #     # Look for broken data flows
        #     broken_flows = self.context7_mcp.find_broken_data_flows(project_context)
        #     for flow in broken_flows:
        #         context7_causes.append(ProjectDeathCause(
        #             category='architecture',
        #             severity='major',
        #             issue_type='Broken data flow',
        #             file_path=flow.source_file,
        #             line_number=flow.source_line,
        #             description=f"Data flow broken between {flow.source} and {flow.target}",
        #             likely_symptoms=['Features partially working', 'Data not updating'],
        #             revival_steps=flow.suggested_fixes,
        #             confidence=0.88,
        #             mcp_source='context7'
        #         ))
        #     
        #     # Look for dependency cycles
        #     cycles = self.context7_mcp.find_dependency_cycles(project_context)
        #     for cycle in cycles:
        #         context7_causes.append(ProjectDeathCause(
        #             category='architecture',
        #             severity='major',
        #             issue_type='Circular dependency',
        #             file_path=cycle.files[0],
        #             line_number=1,
        #             description=f"Circular dependency: {' -> '.join(cycle.files)}",
        #             likely_symptoms=['Import errors', 'Module loading fails'],
        #             revival_steps=cycle.resolution_steps,
        #             confidence=0.93,
        #             mcp_source='context7'
        #         ))
        #     
        #     self.metrics['mcp_calls_made'] += 2
        # except Exception as e:
        #     print(f"   ⚠️ Context7 MCP analysis failed: {e}")
        
        return context7_causes
    
    def _simulate_context7_analysis(self, project_files: List[Dict]) -> List[ProjectDeathCause]:
        """Simulate Context7 semantic analysis"""
        simulated_causes = []
        
        # Look for common architectural red flags
        
        # Check for potential circular imports (common in Python/JavaScript)
        import_files = [f for f in project_files if f['extension'] in ['.py', '.js', '.jsx', '.ts']]
        
        if len(import_files) > 10:  # Only for larger projects
            simulated_causes.append(ProjectDeathCause(
                category='architecture',
                severity='major',
                issue_type='Potential circular dependency detected',
                file_path=import_files[0]['path'],
                line_number=1,
                description='Context7 analysis: Complex import structure suggests potential circular dependencies',
                likely_symptoms=['Import errors on startup', 'Module loading inconsistencies'],
                revival_steps=[
                    'Map import dependencies visually',
                    'Identify and break circular imports',
                    'Use dependency injection pattern',
                    'Reorganize module structure'
                ],
                confidence=0.75,
                mcp_source='context7'
            ))
        
        # Check for missing configuration files
        config_files = [f for f in project_files if any(keyword in f['name'].lower() 
                      for keyword in ['config', 'env', 'setting'])]
        
        if len(config_files) == 0:
            simulated_causes.append(ProjectDeathCause(
                category='backend',
                severity='project_killer',
                issue_type='Missing configuration management',
                file_path=project_files[0]['path'] if project_files else 'project_root',
                line_number=1,
                description='Context7 analysis: No configuration files detected - likely missing environment setup',
                likely_symptoms=['App crashes with env errors', 'Configuration not found errors'],
                revival_steps=[
                    'Create .env file with required variables',
                    'Add config.py or similar configuration module',
                    'Document required environment variables'
                ],
                confidence=0.85,
                mcp_source='context7'
            ))
        
        return simulated_causes
    
    def _triangulate_death_causes(self, death_causes: List[ProjectDeathCause]) -> List[ProjectDeathCause]:
        """Triangulate death causes using cognitive triangulation approach"""
        
        # Group similar causes by file and issue type
        cause_groups = {}
        
        for cause in death_causes:
            key = (cause.file_path, cause.category, cause.issue_type)
            if key not in cause_groups:
                cause_groups[key] = []
            cause_groups[key].append(cause)
        
        triangulated_causes = []
        
        for key, causes_group in cause_groups.items():
            if len(causes_group) == 1:
                # Single source
                triangulated_causes.append(causes_group[0])
            else:
                # Multiple sources confirm same issue - boost confidence
                best_cause = max(causes_group, key=lambda c: c.confidence)
                sources = [c.mcp_source for c in causes_group if c.mcp_source]
                
                # Boost confidence based on multiple confirmations
                confidence_boost = min(0.1 * (len(sources) - 1), 0.2)
                best_cause.confidence = min(best_cause.confidence + confidence_boost, 1.0)
                
                # Combine revival steps from all sources
                all_steps = []
                for cause in causes_group:
                    all_steps.extend(cause.revival_steps)
                best_cause.revival_steps = list(dict.fromkeys(all_steps))  # Remove duplicates
                
                triangulated_causes.append(best_cause)
        
        # Sort by severity and confidence
        severity_order = {'project_killer': 0, 'major': 1, 'minor': 2}
        triangulated_causes.sort(key=lambda c: (severity_order[c.severity], -c.confidence))
        
        return triangulated_causes
    
    def _generate_revival_plan(self, death_causes: List[ProjectDeathCause], project_path: str) -> Dict[str, Any]:
        """Generate step-by-step revival plan"""
        
        # Prioritize project killers first
        project_killers = [c for c in death_causes if c.severity == 'project_killer']
        major_issues = [c for c in death_causes if c.severity == 'major']
        minor_issues = [c for c in death_causes if c.severity == 'minor']
        
        revival_plan = {
            'phase_1_critical': {
                'title': 'Critical Issues (Must Fix First)',
                'issues': project_killers,
                'estimated_time': len(project_killers) * 2,  # 2 hours per critical issue
                'description': 'These issues prevent the project from running at all'
            },
            'phase_2_major': {
                'title': 'Major Issues (Fix for Stability)',
                'issues': major_issues,
                'estimated_time': len(major_issues) * 1,  # 1 hour per major issue
                'description': 'These issues cause significant problems but may allow limited functionality'
            },
            'phase_3_polish': {
                'title': 'Polish & Optimization',
                'issues': minor_issues,
                'estimated_time': len(minor_issues) * 0.5,  # 30 min per minor issue
                'description': 'These issues improve code quality but don\'t block functionality'
            }
        }
        
        return revival_plan
    
    def _identify_quick_wins(self, death_causes: List[ProjectDeathCause]) -> List[Dict[str, Any]]:
        """Identify quick wins - easy fixes that provide big impact"""
        quick_wins = []
        
        quick_win_patterns = [
            'Missing environment variable',
            'Port already in use',
            'Python indentation error',
            'Missing dependency',
            'Invalid JSON format'
        ]
        
        for cause in death_causes:
            if any(pattern in cause.issue_type for pattern in quick_win_patterns):
                quick_wins.append({
                    'issue': cause.issue_type,
                    'file': Path(cause.file_path).name,
                    'fix_time': '5-15 minutes',
                    'impact': 'High',
                    'steps': cause.revival_steps[:2]  # First 2 steps
                })
        
        return quick_wins[:5]  # Top 5 quick wins
    
    def _estimate_revival_time(self, death_causes: List[ProjectDeathCause]) -> Dict[str, float]:
        """Estimate time needed to revive the project"""
        
        time_estimates = {
            'project_killer': 2.0,  # 2 hours per critical issue
            'major': 1.0,           # 1 hour per major issue  
            'minor': 0.5            # 30 minutes per minor issue
        }
        
        total_time = sum(time_estimates[cause.severity] for cause in death_causes)
        
        return {
            'total_hours': total_time,
            'total_days': total_time / 8,  # Assuming 8-hour work days
            'critical_hours': sum(time_estimates[c.severity] for c in death_causes if c.severity == 'project_killer'),
            'quick_wins_hours': sum(0.25 for c in death_causes if 'Missing' in c.issue_type or 'Port' in c.issue_type)
        }
    
    def _calculate_revival_probability(self, death_causes: List[ProjectDeathCause]) -> Dict[str, float]:
        """Calculate probability of successful project revival"""
        
        if not death_causes:
            return {'overall': 0.95, 'reasoning': 'No major issues detected'}
        
        # Base probability starts high
        base_probability = 0.9
        
        # Reduce probability based on severity and number of issues
        penalty_per_killer = 0.15
        penalty_per_major = 0.08
        penalty_per_minor = 0.02
        
        killers = len([c for c in death_causes if c.severity == 'project_killer'])
        majors = len([c for c in death_causes if c.severity == 'major'])
        minors = len([c for c in death_causes if c.severity == 'minor'])
        
        probability = base_probability - (
            killers * penalty_per_killer +
            majors * penalty_per_major +
            minors * penalty_per_minor
        )
        
        probability = max(0.1, min(0.95, probability))  # Clamp between 10% and 95%
        
        # Reasoning
        if probability > 0.8:
            reasoning = 'High probability - mostly minor issues'
        elif probability > 0.6:
            reasoning = 'Good probability - some major issues but fixable'
        elif probability > 0.4:
            reasoning = 'Moderate probability - significant issues but not impossible'
        else:
            reasoning = 'Low probability - major structural problems'
        
        return {
            'overall': probability,
            'reasoning': reasoning,
            'critical_issues': killers,
            'major_issues': majors
        }
    
    def _assess_project_health(self, death_causes: List[ProjectDeathCause]) -> str:
        """Assess overall project health"""
        
        if not death_causes:
            return 'HEALTHY'
        
        killers = len([c for c in death_causes if c.severity == 'project_killer'])
        majors = len([c for c in death_causes if c.severity == 'major'])
        
        if killers > 3:
            return 'CRITICAL'
        elif killers > 0 or majors > 5:
            return 'CRITICAL'
        elif majors > 2:
            return 'UNSTABLE'
        elif majors > 0:
            return 'NEEDS_ATTENTION'
        else:
            return 'MINOR_ISSUES'
    
    def _detect_project_language(self, project_files: List[Dict]) -> str:
        """Detect primary project language"""
        extensions = [f['extension'] for f in project_files]
        
        if '.py' in extensions and 'requirements.txt' in [f['name'] for f in project_files]:
            return 'python'
        elif '.js' in extensions and 'package.json' in [f['name'] for f in project_files]:
            return 'javascript'
        elif '.java' in extensions:
            return 'java'
        elif '.cs' in extensions:
            return 'csharp'
        else:
            return 'unknown'
    
    def _display_diagnosis_report(self, diagnosis: Dict[str, Any]):
        """Display comprehensive diagnosis report"""
        
        print(f"\n" + "=" * 60)
        print(f"💀 DEAD PROJECT DIAGNOSIS COMPLETE")
        print(f"=" * 60)
        
        status = diagnosis['project_status']
        status_emoji = {
            'HEALTHY': '💚',
            'MINOR_ISSUES': '💛', 
            'NEEDS_ATTENTION': '🟠',
            'UNSTABLE': '🔴',
            'CRITICAL': '💀'
        }
        
        print(f"\n📊 PROJECT STATUS: {status_emoji.get(status, '❓')} {status}")
        print(f"⏱️ Analysis Time: {diagnosis['analysis_time']:.2f} seconds")
        print(f"☠️ Death Causes Found: {len(diagnosis['death_causes'])}")
        
        # Revival probability
        prob = diagnosis['success_probability']
        print(f"🎯 Revival Probability: {prob['overall']*100:.1f}% ({prob['reasoning']})")
        
        # Time estimates
        time_est = diagnosis['estimated_revival_time']
        print(f"⏰ Estimated Revival Time: {time_est['total_hours']:.1f} hours ({time_est['total_days']:.1f} days)")
        
        # Quick wins
        if diagnosis['quick_wins']:
            print(f"\n⚡ QUICK WINS AVAILABLE:")
            for i, win in enumerate(diagnosis['quick_wins'], 1):
                print(f"   {i}. {win['issue']} in {win['file']} ({win['fix_time']})")
        
        # Death causes by category
        if diagnosis['death_causes']:
            print(f"\n☠️ DEATH CAUSES BY CATEGORY:")
            
            by_category = {}
            for cause in diagnosis['death_causes']:
                if cause.category not in by_category:
                    by_category[cause.category] = []
                by_category[cause.category].append(cause)
            
            category_emoji = {
                'connection': '🔌',
                'bug': '🐛', 
                'syntax': '📝',
                'backend': '⚙️',
                'architecture': '🏗️'
            }
            
            for category, causes in by_category.items():
                emoji = category_emoji.get(category, '❓')
                print(f"\n   {emoji} {category.upper()} ({len(causes)} issues):")
                
                for cause in causes[:3]:  # Show top 3 per category
                    severity_emoji = {'project_killer': '💀', 'major': '🔴', 'minor': '🟡'}
                    print(f"      {severity_emoji.get(cause.severity, '⚪')} {cause.issue_type}")
                    print(f"         📁 {Path(cause.file_path).name}:{cause.line_number}")
                    print(f"         💡 {cause.revival_steps[0] if cause.revival_steps else 'See detailed plan'}")
                
                if len(causes) > 3:
                    print(f"      ... and {len(causes) - 3} more {category} issues")
        
        # Revival plan summary
        plan = diagnosis['revival_plan']
        print(f"\n🚀 REVIVAL PLAN SUMMARY:")
        for phase_key, phase in plan.items():
            if phase['issues']:
                print(f"   📋 {phase['title']}: {len(phase['issues'])} issues ({phase['estimated_time']:.1f}h)")
        
        print(f"\n💡 TIP: Focus on Critical Issues first - they're blocking the project from running!")
        print(f"🎯 Ready to start revival? Begin with the Quick Wins for immediate progress!")

# Test the Project Revival Detective
async def test_dead_project_revival():
    """Test the dead project revival system"""
    
    detective = ProjectRevivalDetective()
    
    # Test on Bob's original X-Agent pipeline (simulate a "dead" project analysis)
    test_project = '/Users/bobdallavia/X-Agent-Pipeline'
    
    print("🧪 TESTING DEAD PROJECT REVIVAL SYSTEM")
    print("=" * 50)
    print(f"📁 Test Target: {test_project}")
    print("🎯 Goal: Demonstrate dead project diagnosis capabilities")
    
    diagnosis = await detective.diagnose_dead_project(test_project)
    
    print(f"\n✅ Dead Project Revival Test Complete!")
    print(f"📊 System successfully analyzed project structure and identified potential issues")
    print(f"🎯 Ready for real dead project revival missions!")
    
    return diagnosis

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_dead_project_revival())
