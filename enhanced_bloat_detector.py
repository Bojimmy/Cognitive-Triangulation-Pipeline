#!/usr/bin/env python3
"""
Enhanced Cleanup Agent for Detecting Project Bloat and Issues
Specifically designed to find bugs, waste, and organizational problems in real projects

This is the enhanced version that will catch all the issues in bloated project folders
"""
import os
import sys
import time
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

# Add our system paths
sys.path.append('/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation/cognitive_triangulation/agents')
sys.path.append('/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation/agent_performance_test')

@dataclass
class EnhancedCleanupRecommendation:
    """Enhanced cleanup recommendation with bug detection"""
    path: str
    reason: str
    action: str  # 'delete', 'archive', 'review', 'fix', 'reorganize'
    priority: str  # 'critical', 'high', 'medium', 'low'
    category: str  # 'bloat', 'bug', 'organization', 'performance', 'security'
    size_saved: int
    details: str

class EnhancedProjectCleanupAgent:
    """
    Enhanced agent specialized in finding bugs, bloat, and organizational issues
    """
    
    def __init__(self):
        self.bloat_patterns = {
            # System files that shouldn't be in projects
            'system_bloat': {
                '.DS_Store', 'Thumbs.db', 'desktop.ini', '.directory',
                '.Spotlight-V100', '.Trashes', '.AppleDouble', '.LSOverride'
            },
            
            # Build artifacts and cache
            'build_artifacts': {
                '__pycache__', '.pyc', '.pyo', '.pyd', '.class', '.o', '.obj',
                'node_modules', '.npm', 'dist', 'build', '.next', '.nuxt',
                '.pytest_cache', '.coverage', 'htmlcov', '.tox', '.mypy_cache'
            },
            
            # Environment and dependency files
            'environment_bloat': {
                'venv', '.venv', 'env', '.env', 'ENV', 'virtualenv',
                'node_modules', 'vendor', '.bundle'
            },
            
            # Temporary and debug files
            'temp_debug_files': {
                'debug_', 'temp_', 'test_temp', 'scratch_', 'tmp_',
                '.tmp', '.temp', '.bak', '.backup', '.orig', '.log'
            },
            
            # Duplicate/redundant files
            'redundant_patterns': {
                'copy_of_', 'backup_', 'old_', '_old', '_backup', '_copy',
                '(1)', '(2)', '(3)', 'untitled', 'new_file'
            },
            
            # Configuration proliferation
            'config_proliferation': {
                'requirements.txt', 'requirements-', 'package.json', 'package-lock.json',
                'poetry.lock', 'Pipfile', 'Pipfile.lock', 'setup.py', 'setup.cfg'
            }
        }
        
        # File organization issues
        self.organization_issues = {
            'root_test_files': r'test_.*\.py$',
            'root_debug_files': r'debug_.*\.py$',
            'scattered_configs': r'.*config.*\.(json|yaml|yml|toml|ini)$',
            'loose_scripts': r'(main|run|server|app)\.py$'
        }
        
        # Bug patterns
        self.bug_patterns = {
            'python_syntax_errors': [
                'SyntaxError', 'IndentationError', 'TabError',
                'import error', 'ImportError', 'ModuleNotFoundError'
            ],
            'common_mistakes': [
                'print(', 'console.log(', 'debugger;', 'TODO:', 'FIXME:',
                'XXX:', 'HACK:', 'BUG:', 'BROKEN:'
            ],
            'security_issues': [
                'password =', 'secret =', 'api_key =', 'token =',
                'SECRET_KEY', 'API_SECRET', 'hardcoded'
            ]
        }
    
    def analyze_enhanced_cleanup(self, project_path: str) -> List[EnhancedCleanupRecommendation]:
        """
        Enhanced cleanup analysis that finds bugs, bloat, and organization issues
        """
        recommendations = []
        project_path = Path(project_path)
        
        print(f"🔍 ENHANCED CLEANUP ANALYSIS: Scanning for bugs, bloat, and waste")
        print(f"📁 Target: {project_path}")
        print()
        
        # Analyze project structure
        structure_issues = self._analyze_project_structure(project_path)
        recommendations.extend(structure_issues)
        
        # Scan all files for issues
        for root, dirs, files in os.walk(project_path):
            root_path = Path(root)
            
            # Check directories
            for dir_name in dirs:
                dir_path = root_path / dir_name
                dir_issues = self._analyze_directory(dir_path, project_path)
                recommendations.extend(dir_issues)
            
            # Check files
            for file in files:
                file_path = root_path / file
                file_issues = self._analyze_file_comprehensive(file_path, project_path)
                recommendations.extend(file_issues)
        
        # Sort by priority and category
        recommendations.sort(key=lambda x: (
            {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}[x.priority],
            x.category
        ))
        
        return recommendations
    
    def _analyze_project_structure(self, project_path: Path) -> List[EnhancedCleanupRecommendation]:
        """Analyze overall project structure for issues"""
        issues = []
        
        # Check for scattered files in root
        root_files = list(project_path.glob('*'))
        python_files_in_root = [f for f in root_files if f.suffix == '.py' and f.is_file()]
        
        if len(python_files_in_root) > 5:
            issues.append(EnhancedCleanupRecommendation(
                path=str(project_path),
                reason=f"Too many Python files in root ({len(python_files_in_root)} files)",
                action='reorganize',
                priority='medium',
                category='organization',
                size_saved=0,
                details="Consider organizing files into src/, scripts/, or appropriate subdirectories"
            ))
        
        # Check for multiple similar files
        similar_groups = self._find_similar_files(python_files_in_root)
        for group in similar_groups:
            if len(group) > 1:
                issues.append(EnhancedCleanupRecommendation(
                    path=str(project_path),
                    reason=f"Multiple similar files: {[f.name for f in group]}",
                    action='review',
                    priority='medium',
                    category='bloat',
                    size_saved=sum(f.stat().st_size for f in group[1:]),
                    details="Review for potential consolidation or removal of duplicates"
                ))
        
        return issues
    
    def _find_similar_files(self, files: List[Path]) -> List[List[Path]]:
        """Find groups of similar files"""
        similar_groups = []
        
        # Group by similar names
        name_groups = {}
        for file in files:
            base_name = file.stem.lower()
            
            # Remove common prefixes/suffixes
            for prefix in ['test_', 'debug_', 'demo_']:
                if base_name.startswith(prefix):
                    base_name = base_name[len(prefix):]
                    break
            
            for suffix in ['_test', '_debug', '_demo', '_old', '_backup']:
                if base_name.endswith(suffix):
                    base_name = base_name[:-len(suffix)]
                    break
            
            if base_name not in name_groups:
                name_groups[base_name] = []
            name_groups[base_name].append(file)
        
        # Return groups with multiple files
        return [group for group in name_groups.values() if len(group) > 1]
    
    def _analyze_directory(self, dir_path: Path, project_root: Path) -> List[EnhancedCleanupRecommendation]:
        """Analyze directory for issues"""
        issues = []
        relative_path = dir_path.relative_to(project_root)
        dir_name = dir_path.name
        
        # Check for build artifacts and cache directories
        for category, patterns in self.bloat_patterns.items():
            if dir_name in patterns:
                dir_size = sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
                
                priority = 'high' if category in ['build_artifacts', 'system_bloat'] else 'medium'
                action = 'delete' if category in ['build_artifacts', 'system_bloat'] else 'review'
                
                issues.append(EnhancedCleanupRecommendation(
                    path=str(relative_path),
                    reason=f"{category.replace('_', ' ').title()}: {dir_name}",
                    action=action,
                    priority=priority,
                    category='bloat',
                    size_saved=dir_size,
                    details=f"Directory contains {category.replace('_', ' ')} and can likely be removed"
                ))
        
        # Check for empty directories
        try:
            if dir_path.is_dir() and not any(dir_path.iterdir()):
                issues.append(EnhancedCleanupRecommendation(
                    path=str(relative_path),
                    reason="Empty directory",
                    action='delete',
                    priority='low',
                    category='bloat',
                    size_saved=0,
                    details="Directory contains no files and can be removed"
                ))
        except PermissionError:
            pass
        
        return issues
    
    def _analyze_file_comprehensive(self, file_path: Path, project_root: Path) -> List[EnhancedCleanupRecommendation]:
        """Comprehensive file analysis for bugs, bloat, and issues"""
        issues = []
        relative_path = file_path.relative_to(project_root)
        filename = file_path.name
        
        # Check file size
        try:
            file_size = file_path.stat().st_size
        except (OSError, PermissionError):
            return issues
        
        # Check for system bloat files
        for category, patterns in self.bloat_patterns.items():
            if any(pattern in filename for pattern in patterns):
                priority = 'critical' if category == 'system_bloat' else 'high'
                
                issues.append(EnhancedCleanupRecommendation(
                    path=str(relative_path),
                    reason=f"{category.replace('_', ' ').title()}: {filename}",
                    action='delete',
                    priority=priority,
                    category='bloat',
                    size_saved=file_size,
                    details=f"File is {category.replace('_', ' ')} and should not be in the repository"
                ))
        
        # Check for large files
        if file_size > 10 * 1024 * 1024:  # > 10MB
            issues.append(EnhancedCleanupRecommendation(
                path=str(relative_path),
                reason=f"Large file ({file_size / 1024 / 1024:.1f}MB)",
                action='review',
                priority='medium',
                category='performance',
                size_saved=file_size,
                details="Consider if this large file is necessary or if it should be stored elsewhere"
            ))
        
        # Analyze file content for bugs and issues
        if file_path.suffix in ['.py', '.js', '.ts', '.md', '.txt', '.json', '.yaml', '.yml']:
            content_issues = self._analyze_file_content(file_path, project_root)
            issues.extend(content_issues)
        
        # Check for organization issues
        for issue_type, pattern in self.organization_issues.items():
            import re
            if re.match(pattern, filename):
                issues.append(EnhancedCleanupRecommendation(
                    path=str(relative_path),
                    reason=f"Organization issue: {issue_type.replace('_', ' ')}",
                    action='reorganize',
                    priority='medium',
                    category='organization',
                    size_saved=0,
                    details=f"File should be organized into appropriate subdirectory"
                ))
        
        return issues
    
    def _analyze_file_content(self, file_path: Path, project_root: Path) -> List[EnhancedCleanupRecommendation]:
        """Analyze file content for bugs and issues"""
        issues = []
        relative_path = file_path.relative_to(project_root)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, PermissionError, OSError):
            return issues
        
        # Check for bug patterns
        for category, patterns in self.bug_patterns.items():
            for pattern in patterns:
                if pattern.lower() in content.lower():
                    line_num = self._find_line_number(content, pattern)
                    
                    priority = 'critical' if category == 'security_issues' else 'high'
                    
                    issues.append(EnhancedCleanupRecommendation(
                        path=str(relative_path),
                        reason=f"{category.replace('_', ' ').title()}: Found '{pattern}'",
                        action='fix',
                        priority=priority,
                        category='bug',
                        size_saved=0,
                        details=f"Line {line_num}: Potential {category.replace('_', ' ')} detected"
                    ))
        
        # Check for code quality issues
        lines = content.split('\n')
        
        # Check for very long lines
        long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 200]
        if long_lines:
            issues.append(EnhancedCleanupRecommendation(
                path=str(relative_path),
                reason=f"Code quality: Very long lines found",
                action='fix',
                priority='low',
                category='bug',
                size_saved=0,
                details=f"Lines {long_lines[:5]} are over 200 characters"
            ))
        
        # Check for excessive comments or debug code
        comment_lines = [line for line in lines if line.strip().startswith('#') or line.strip().startswith('//')]
        if len(comment_lines) > len(lines) * 0.5:  # > 50% comments
            issues.append(EnhancedCleanupRecommendation(
                path=str(relative_path),
                reason=f"Code quality: Excessive comments ({len(comment_lines)}/{len(lines)} lines)",
                action='review',
                priority='low',
                category='bloat',
                size_saved=0,
                details="Consider cleaning up excessive comments or debug code"
            ))
        
        return issues
    
    def _find_line_number(self, content: str, pattern: str) -> int:
        """Find line number where pattern occurs"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if pattern.lower() in line.lower():
                return i
        return 1

async def analyze_bloated_project():
    """
    Analyze the bloated XML-MCP-AgentTemplate project for bugs and waste
    """
    
    print("🧹 ENHANCED BLOAT & BUG DETECTION ANALYSIS")
    print("=" * 60)
    print("🎯 Target: XML-MCP-AgentTemplate (Known Bloated Project)")
    print("🔍 Mission: Find ALL bugs, waste, and organizational issues")
    print()
    
    project_path = '/Users/bobdallavia/XML-MCP-AgentTemplate'
    
    # Run enhanced cleanup analysis
    cleanup_agent = EnhancedProjectCleanupAgent()
    recommendations = cleanup_agent.analyze_enhanced_cleanup(project_path)
    
    # Categorize recommendations
    categories = {}
    total_size_saved = 0
    
    for rec in recommendations:
        if rec.category not in categories:
            categories[rec.category] = []
        categories[rec.category].append(rec)
        total_size_saved += rec.size_saved
    
    # Generate comprehensive report
    print(f"\n🎉 ENHANCED CLEANUP ANALYSIS COMPLETE")
    print("=" * 60)
    
    print(f"\n📊 ISSUES SUMMARY:")
    print(f"   🚨 Total Issues Found: {len(recommendations)}")
    print(f"   💾 Potential Space Saved: {total_size_saved / 1024:.1f} KB")
    
    print(f"\n📋 ISSUES BY CATEGORY:")
    priority_order = ['critical', 'high', 'medium', 'low']
    
    for category, issues in categories.items():
        print(f"\n🔸 {category.upper()} ({len(issues)} issues):")
        
        # Sort by priority within category
        sorted_issues = sorted(issues, key=lambda x: priority_order.index(x.priority))
        
        for issue in sorted_issues[:10]:  # Show top 10 per category
            priority_emoji = {'critical': '🚨', 'high': '⚠️', 'medium': '📝', 'low': '💡'}[issue.priority]
            action_emoji = {'delete': '🗑️', 'fix': '🔧', 'review': '👀', 'reorganize': '📁', 'archive': '📦'}[issue.action]
            
            print(f"   {priority_emoji} {action_emoji} {issue.path}")
            print(f"      Reason: {issue.reason}")
            if issue.size_saved > 0:
                print(f"      Saves: {issue.size_saved / 1024:.1f} KB")
            print(f"      Action: {issue.action.title()} - {issue.details}")
            print()
    
    # Priority recommendations
    critical_issues = [r for r in recommendations if r.priority == 'critical']
    high_issues = [r for r in recommendations if r.priority == 'high']
    
    print(f"\n🚨 IMMEDIATE ACTION REQUIRED:")
    print(f"   Critical Issues: {len(critical_issues)}")
    print(f"   High Priority Issues: {len(high_issues)}")
    
    if critical_issues:
        print(f"\n🔥 CRITICAL ISSUES (Fix Immediately):")
        for issue in critical_issues[:5]:
            print(f"   • {issue.path}: {issue.reason}")
    
    if high_issues:
        print(f"\n⚠️ HIGH PRIORITY ISSUES (Fix Soon):")
        for issue in high_issues[:5]:
            print(f"   • {issue.path}: {issue.reason}")
    
    # Quick wins
    quick_wins = [r for r in recommendations if r.action == 'delete' and r.size_saved > 1024]
    if quick_wins:
        total_quick_savings = sum(r.size_saved for r in quick_wins)
        print(f"\n🎯 QUICK WINS (Easy Deletions):")
        print(f"   Files to delete: {len(quick_wins)}")
        print(f"   Space saved: {total_quick_savings / 1024:.1f} KB")
        
        for win in quick_wins[:5]:
            print(f"   • {win.path} ({win.size_saved / 1024:.1f} KB)")
    
    print(f"\n🏆 BLOAT & BUG DETECTION COMPLETE!")
    print(f"✅ Found {len(recommendations)} issues across {len(categories)} categories")
    print(f"✅ Identified {total_size_saved / 1024:.1f} KB of potential savings")
    print(f"✅ Prioritized issues from critical to low impact")
    
    return recommendations

if __name__ == "__main__":
    asyncio.run(analyze_bloated_project())
