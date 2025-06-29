#!/usr/bin/env python3
"""
REAL GITHUB MCP CLIENT
Direct integration with GitHub CLI for Project Necromancer

Uses your existing 'gh' authentication for real repository analysis,
issue tracking, and community solution gathering.
"""

import asyncio
import json
import subprocess
import re
from typing import Dict, List, Any, Optional
from pathlib import Path

class RealGitHubMCPClient:
    """
    Real GitHub MCP Client using authenticated GitHub CLI
    
    Features:
    🔍 Repository analysis and file inspection
    📊 Issue and PR analysis for similar problems
    🧠 Community solution patterns extraction
    🚀 Automated workflow suggestions
    """
    
    def __init__(self):
        self.authenticated = False
        self.user_info = {}
        
    async def initialize(self) -> bool:
        """Initialize and verify GitHub CLI authentication"""
        try:
            # Check authentication status
            result = subprocess.run(['gh', 'auth', 'status'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.authenticated = True
                
                # Get user info
                user_result = subprocess.run(['gh', 'api', 'user'], 
                                           capture_output=True, text=True)
                if user_result.returncode == 0:
                    self.user_info = json.loads(user_result.stdout)
                
                print(f"🐙 GitHub MCP: Connected as {self.user_info.get('login', 'unknown')}")
                return True
            else:
                print(f"❌ GitHub MCP: Authentication failed")
                return False
                
        except Exception as e:
            print(f"❌ GitHub MCP: Error during initialization: {e}")
            return False
    
    async def analyze_project_repository(self, project_path: str) -> Dict[str, Any]:
        """Analyze if the project is a Git repository and get GitHub info"""
        
        if not self.authenticated:
            return {'error': 'Not authenticated with GitHub'}
            
        try:
            # Check if it's a git repository
            git_check = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                                     cwd=project_path, capture_output=True)
            
            if git_check.returncode != 0:
                return {'is_git_repo': False, 'message': 'Not a Git repository'}
            
            # Get remote origin URL
            remote_result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                         cwd=project_path, capture_output=True, text=True)
            
            if remote_result.returncode != 0:
                return {'is_git_repo': True, 'has_github_remote': False}
            
            # Parse GitHub repository info
            remote_url = remote_result.stdout.strip()
            repo_info = self._parse_github_url(remote_url)
            
            if repo_info:
                # Get repository details from GitHub API
                api_result = subprocess.run([
                    'gh', 'api', f'repos/{repo_info["owner"]}/{repo_info["repo"]}'
                ], capture_output=True, text=True)
                
                if api_result.returncode == 0:
                    repo_data = json.loads(api_result.stdout)
                    return {
                        'is_git_repo': True,
                        'has_github_remote': True,
                        'repository': repo_info,
                        'github_data': repo_data,
                        'languages': await self._get_repository_languages(repo_info),
                        'recent_activity': await self._get_recent_commits(project_path)
                    }
            
            return {'is_git_repo': True, 'has_github_remote': False, 
                   'remote_url': remote_url}
            
        except Exception as e:
            return {'error': f'Repository analysis failed: {e}'}
    
    async def search_similar_issues(self, death_causes: List, limit: int = 10) -> Dict[str, List]:
        """Search GitHub for similar issues and solutions"""
        
        if not self.authenticated:
            return {'error': 'Not authenticated with GitHub'}
        
        solutions_by_cause = {}
        
        for cause in death_causes[:5]:  # Top 5 death causes
            issue_type = cause.issue_type.lower()
            search_terms = self._generate_search_terms(cause)
            
            solutions = []
            for term in search_terms[:3]:  # Top 3 search terms
                try:
                    # Search GitHub issues
                    search_result = subprocess.run([
                        'gh', 'search', 'issues', 
                        f'{term} state:closed', 
                        '--limit', '5',
                        '--json', 'title,url,state,repository,body'
                    ], capture_output=True, text=True, timeout=30)
                    
                    if search_result.returncode == 0:
                        issues = json.loads(search_result.stdout)
                        
                        for issue in issues:
                            solution = await self._extract_solution_from_issue(issue, cause)
                            if solution:
                                solutions.append(solution)
                    
                except subprocess.TimeoutExpired:
                    print(f"⚠️ Search timeout for term: {term}")
                except Exception as e:
                    print(f"⚠️ Search error for {term}: {e}")
            
            if solutions:
                solutions_by_cause[issue_type] = solutions
        
        return solutions_by_cause
    
    async def get_repository_community_patterns(self, repo_owner: str, repo_name: str) -> Dict[str, Any]:
        """Analyze repository for common issue patterns and solutions"""
        
        if not self.authenticated:
            return {'error': 'Not authenticated with GitHub'}
        
        try:
            # Get repository issues
            issues_result = subprocess.run([
                'gh', 'api', f'repos/{repo_owner}/{repo_name}/issues',
                '--jq', '.[] | {title, state, labels: [.labels[].name], body}'
            ], capture_output=True, text=True, timeout=30)
            
            # Get pull requests
            prs_result = subprocess.run([
                'gh', 'api', f'repos/{repo_owner}/{repo_name}/pulls',
                '--jq', '.[] | {title, state, body}'
            ], capture_output=True, text=True, timeout=30)
            
            patterns = {
                'common_issues': [],
                'frequent_fixes': [],
                'dependency_updates': [],
                'configuration_changes': []
            }
            
            if issues_result.returncode == 0:
                patterns['common_issues'] = self._analyze_issue_patterns(issues_result.stdout)
            
            if prs_result.returncode == 0:
                patterns['frequent_fixes'] = self._analyze_pr_patterns(prs_result.stdout)
            
            return patterns
            
        except Exception as e:
            return {'error': f'Community pattern analysis failed: {e}'}
    
    async def suggest_automated_fixes(self, project_path: str, death_causes: List) -> List[Dict]:
        """Suggest automated fixes using GitHub Actions or scripts"""
        
        suggestions = []
        
        for cause in death_causes:
            if 'dependency' in cause.issue_type.lower():
                suggestions.append({
                    'type': 'github_action',
                    'name': 'Automated Dependency Update',
                    'description': 'Set up Dependabot for automatic dependency updates',
                    'action_file': self._generate_dependabot_config(),
                    'priority': 'high'
                })
            
            elif 'port' in cause.issue_type.lower():
                suggestions.append({
                    'type': 'script',
                    'name': 'Port Management Script',
                    'description': 'Automated port conflict resolution',
                    'script_content': self._generate_port_management_script(),
                    'priority': 'medium'
                })
            
            elif 'test' in cause.issue_type.lower():
                suggestions.append({
                    'type': 'github_action',
                    'name': 'CI/CD Pipeline',
                    'description': 'Automated testing and deployment',
                    'action_file': self._generate_ci_workflow(),
                    'priority': 'high'
                })
        
        return suggestions
    
    def _parse_github_url(self, url: str) -> Optional[Dict[str, str]]:
        """Parse GitHub repository URL to extract owner and repo name"""
        
        patterns = [
            r'github\.com[:/]([^/]+)/([^/\.]+)',  # SSH or HTTPS
            r'github\.com/([^/]+)/([^/\.]+)'      # HTTPS without .git
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return {
                    'owner': match.group(1),
                    'repo': match.group(2)
                }
        
        return None
    
    async def _get_repository_languages(self, repo_info: Dict) -> Dict[str, Any]:
        """Get programming languages used in the repository"""
        try:
            result = subprocess.run([
                'gh', 'api', f'repos/{repo_info["owner"]}/{repo_info["repo"]}/languages'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            
        except Exception:
            pass
        
        return {}
    
    async def _get_recent_commits(self, project_path: str) -> List[Dict]:
        """Get recent commit activity"""
        try:
            result = subprocess.run([
                'git', 'log', '--oneline', '--max-count=10'
            ], cwd=project_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                commits = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split(' ', 1)
                        commits.append({
                            'hash': parts[0],
                            'message': parts[1] if len(parts) > 1 else ''
                        })
                return commits
                
        except Exception:
            pass
        
        return []
    
    def _generate_search_terms(self, cause) -> List[str]:
        """Generate effective search terms for GitHub issue search"""
        
        base_terms = []
        
        # Add specific issue type terms
        if 'port' in cause.issue_type.lower():
            base_terms.extend([
                'port already in use EADDRINUSE',
                'address already in use error',
                'kill process port conflict'
            ])
        elif 'dependency' in cause.issue_type.lower():
            base_terms.extend([
                'missing dependency import error',
                'module not found install',
                'package installation failed'
            ])
        elif 'indentation' in cause.issue_type.lower():
            base_terms.extend([
                'python indentation error tabs spaces',
                'indentationerror expected',
                'python formatting autopep8'
            ])
        elif 'json' in cause.issue_type.lower():
            base_terms.extend([
                'invalid json syntax error',
                'json decode error malformed',
                'json parsing failed'
            ])
        else:
            # Generic search based on issue type
            base_terms.append(cause.issue_type.replace('_', ' '))
        
        return base_terms
    
    async def _extract_solution_from_issue(self, issue: Dict, cause) -> Optional[Dict]:
        """Extract solution information from a GitHub issue"""
        
        title = issue.get('title', '').lower()
        body = issue.get('body', '').lower()
        
        # Look for solution indicators
        solution_indicators = [
            'solved', 'fixed', 'resolved', 'workaround', 
            'solution', 'fix', 'install', 'npm install', 'pip install'
        ]
        
        if any(indicator in body for indicator in solution_indicators):
            return {
                'title': issue.get('title', ''),
                'url': issue.get('url', ''),
                'repository': issue.get('repository', {}).get('nameWithOwner', ''),
                'relevance_score': self._calculate_relevance(issue, cause),
                'solution_type': self._identify_solution_type(body),
                'quick_summary': self._extract_solution_summary(body)
            }
        
        return None
    
    def _calculate_relevance(self, issue: Dict, cause) -> float:
        """Calculate how relevant this issue is to the death cause"""
        
        title = issue.get('title', '').lower()
        body = issue.get('body', '').lower()
        cause_type = cause.issue_type.lower()
        
        relevance = 0.0
        
        # Exact term matches
        if cause_type in title:
            relevance += 0.5
        if cause_type in body:
            relevance += 0.3
        
        # Keyword matches
        keywords = cause_type.split('_')
        for keyword in keywords:
            if keyword in title:
                relevance += 0.2
            if keyword in body:
                relevance += 0.1
        
        return min(relevance, 1.0)
    
    def _identify_solution_type(self, body: str) -> str:
        """Identify the type of solution from issue body"""
        
        if 'npm install' in body or 'yarn add' in body:
            return 'dependency_installation'
        elif 'pip install' in body:
            return 'python_dependency'
        elif 'kill -9' in body or 'killall' in body:
            return 'process_management'
        elif 'config' in body or '.env' in body:
            return 'configuration'
        elif 'update' in body or 'upgrade' in body:
            return 'version_update'
        else:
            return 'general_fix'
    
    def _extract_solution_summary(self, body: str) -> str:
        """Extract a quick summary of the solution"""
        
        # Look for common solution patterns
        sentences = body.split('.')
        
        for sentence in sentences:
            if any(word in sentence.lower() for word in ['fixed', 'solved', 'install', 'run']):
                return sentence.strip()[:100] + '...'
        
        return body[:100] + '...' if body else 'See issue for details'
    
    def _analyze_issue_patterns(self, issues_json: str) -> List[str]:
        """Analyze common patterns in repository issues"""
        
        patterns = []
        
        try:
            lines = issues_json.strip().split('\n')
            titles = []
            
            for line in lines:
                if line.strip():
                    issue = json.loads(line)
                    titles.append(issue.get('title', '').lower())
            
            # Find common keywords
            word_count = {}
            for title in titles:
                words = title.split()
                for word in words:
                    if len(word) > 3:  # Skip short words
                        word_count[word] = word_count.get(word, 0) + 1
            
            # Get most common patterns
            sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
            patterns = [f"{word} ({count} occurrences)" for word, count in sorted_words[:5]]
            
        except Exception:
            patterns = ['Unable to analyze issue patterns']
        
        return patterns
    
    def _analyze_pr_patterns(self, prs_json: str) -> List[str]:
        """Analyze common patterns in repository pull requests"""
        
        patterns = []
        
        try:
            lines = prs_json.strip().split('\n')
            pr_types = []
            
            for line in lines:
                if line.strip():
                    pr = json.loads(line)
                    title = pr.get('title', '').lower()
                    
                    if 'fix' in title:
                        pr_types.append('Bug fixes')
                    elif 'update' in title or 'upgrade' in title:
                        pr_types.append('Dependency updates')
                    elif 'add' in title:
                        pr_types.append('Feature additions')
                    elif 'refactor' in title:
                        pr_types.append('Code refactoring')
            
            # Count PR types
            type_count = {}
            for pr_type in pr_types:
                type_count[pr_type] = type_count.get(pr_type, 0) + 1
            
            patterns = [f"{pr_type}: {count}" for pr_type, count in type_count.items()]
            
        except Exception:
            patterns = ['Unable to analyze PR patterns']
        
        return patterns
    
    def _generate_dependabot_config(self) -> str:
        """Generate Dependabot configuration for automated dependency updates"""
        
        return '''# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
'''
    
    def _generate_port_management_script(self) -> str:
        """Generate script for managing port conflicts"""
        
        return '''#!/bin/bash
# Port Conflict Resolution Script
# Generated by GitHub MCP

echo "🔧 Resolving port conflicts..."

# Common development ports
PORTS=(3000 8000 5000 4000 8080 3001)

for PORT in "${PORTS[@]}"; do
    PID=$(lsof -ti:$PORT 2>/dev/null)
    if [ ! -z "$PID" ]; then
        echo "  Killing process $PID on port $PORT"
        kill -9 $PID 2>/dev/null
    fi
done

echo "✅ Port conflicts resolved!"
'''
    
    def _generate_ci_workflow(self) -> str:
        """Generate basic CI/CD workflow"""
        
        return '''# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm test
    
    - name: Build project
      run: npm run build
'''

# Test function
async def test_real_github_mcp():
    """Test the real GitHub MCP client"""
    
    print("🐙 TESTING REAL GITHUB MCP CLIENT")
    print("=" * 50)
    
    client = RealGitHubMCPClient()
    
    # Initialize
    connected = await client.initialize()
    
    if connected:
        print(f"✅ Connected to GitHub as: {client.user_info.get('login')}")
        
        # Test repository analysis
        repo_analysis = await client.analyze_project_repository('/Users/bobdallavia/X-Agent-Pipeline')
        print(f"\n📊 Repository Analysis:")
        print(f"   Git Repo: {repo_analysis.get('is_git_repo', False)}")
        print(f"   GitHub Remote: {repo_analysis.get('has_github_remote', False)}")
        
        if repo_analysis.get('repository'):
            repo = repo_analysis['repository']
            print(f"   Repository: {repo['owner']}/{repo['repo']}")
    else:
        print("❌ Failed to connect to GitHub")

if __name__ == "__main__":
    asyncio.run(test_real_github_mcp())
