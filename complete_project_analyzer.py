#!/usr/bin/env python3
"""
Complete Project Cognitive Triangulation System
Full folder analysis with cleanup capabilities for reviewing old projects

Features:
- Scans entire project directories
- Analyzes all relevant files
- Identifies cleanup opportunities  
- Provides comprehensive project insights
- Generates actionable recommendations
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
class FileAnalysis:
    """Results from analyzing a single file"""
    path: str
    size: int
    lines: int
    pois: int
    relationships: int
    patterns: int
    confidence: float
    processing_time_ms: float
    file_type: str
    
@dataclass
class CleanupRecommendation:
    """Recommendation for cleaning up a file/directory"""
    path: str
    reason: str
    action: str  # 'delete', 'archive', 'review'
    priority: str  # 'high', 'medium', 'low'
    size_saved: int

class ProjectCleanupAgent:
    """
    Agent specialized in identifying cleanup opportunities in projects
    """
    
    def __init__(self):
        self.cleanup_patterns = {
            # Files that are commonly safe to remove
            'safe_to_remove': {
                '__pycache__', '.pyc', '.pyo', '.pyd',
                'node_modules', '.DS_Store', 'Thumbs.db',
                '.git/logs', 'npm-debug.log', 'yarn-error.log',
                '.pytest_cache', '.coverage', 'htmlcov',
                '*.tmp', '*.temp', '*.bak', '*.backup'
            },
            
            # Files that might be outdated/unused
            'review_for_removal': {
                'TODO.txt', 'NOTES.txt', 'scratch.py', 'test_temp.py',
                'debug.py', 'temp.py', 'old_', 'backup_', 'copy_of_'
            },
            
            # Large files that might need attention
            'large_file_threshold': 10 * 1024 * 1024,  # 10MB
            
            # Empty directories
            'remove_empty_dirs': True
        }
    
    def analyze_cleanup_opportunities(self, project_path: str) -> List[CleanupRecommendation]:
        """
        Analyze project for cleanup opportunities
        """
        recommendations = []
        project_path = Path(project_path)
        
        print(f"🧹 Scanning for cleanup opportunities in: {project_path}")
        
        # Scan all files and directories
        for root, dirs, files in os.walk(project_path):
            root_path = Path(root)
            
            # Check for safe-to-remove patterns
            for file in files:
                file_path = root_path / file
                relative_path = file_path.relative_to(project_path)
                
                # Check if file matches cleanup patterns
                cleanup_reason = self._should_cleanup_file(file_path, file)
                if cleanup_reason:
                    file_size = file_path.stat().st_size if file_path.exists() else 0
                    recommendations.append(CleanupRecommendation(
                        path=str(relative_path),
                        reason=cleanup_reason['reason'],
                        action=cleanup_reason['action'],
                        priority=cleanup_reason['priority'],
                        size_saved=file_size
                    ))
            
            # Check for empty directories
            if self.cleanup_patterns['remove_empty_dirs']:
                if not files and not dirs:  # Empty directory
                    relative_path = root_path.relative_to(project_path)
                    if str(relative_path) != '.':  # Don't remove root
                        recommendations.append(CleanupRecommendation(
                            path=str(relative_path),
                            reason="Empty directory",
                            action='delete',
                            priority='low',
                            size_saved=0
                        ))
        
        return recommendations
    
    def _should_cleanup_file(self, file_path: Path, filename: str) -> Dict[str, str] | None:
        """
        Determine if a file should be cleaned up
        """
        # Check safe-to-remove patterns
        for pattern in self.cleanup_patterns['safe_to_remove']:
            if pattern in filename or filename.endswith(pattern.replace('*', '')):
                return {
                    'reason': f"Build artifact or cache file ({pattern})",
                    'action': 'delete',
                    'priority': 'high'
                }
        
        # Check review patterns
        for pattern in self.cleanup_patterns['review_for_removal']:
            if pattern in filename.lower():
                return {
                    'reason': f"Potentially outdated file ({pattern})",
                    'action': 'review',
                    'priority': 'medium'
                }
        
        # Check file size
        if file_path.exists():
            file_size = file_path.stat().st_size
            if file_size > self.cleanup_patterns['large_file_threshold']:
                return {
                    'reason': f"Large file ({file_size / 1024 / 1024:.1f}MB)",
                    'action': 'review',
                    'priority': 'medium'
                }
        
        # Check for duplicate files (simple name-based check)
        if 'copy' in filename.lower() or 'backup' in filename.lower():
            return {
                'reason': "Potential duplicate or backup file",
                'action': 'review',
                'priority': 'low'
            }
        
        return None

class CompleteProjectAnalyzer:
    """
    Complete project analysis system with cognitive triangulation
    """
    
    def __init__(self):
        self.cleanup_agent = ProjectCleanupAgent()
        self.supported_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
            '.rb', '.go', '.rs', '.php', '.cs', '.swift', '.kt', '.scala',
            '.r', '.m', '.mm', '.sql', '.sh', '.bash', '.ps1', '.md', '.json',
            '.xml', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf'
        }
        
        # Try to load available agents
        self.agents_available = self._load_agents()
    
    def _load_agents(self) -> Dict[str, Any]:
        """Load available analysis agents"""
        agents = {}
        
        try:
            from colocated_plugin_agent import CoLocatedPluginCodeScoutAgent
            agents['code_scout'] = CoLocatedPluginCodeScoutAgent()
            print("✅ CodeScout agent loaded")
        except ImportError:
            print("⚠️ CodeScout agent not available")
        
        try:
            from relationship_detector_agent import RelationshipDetectorAgent
            from context_analyzer_agent import ContextAnalyzerAgent  
            from confidence_aggregator_agent import ConfidenceAggregatorAgent
            agents['relationship_detector'] = RelationshipDetectorAgent()
            agents['context_analyzer'] = ContextAnalyzerAgent()
            agents['confidence_aggregator'] = ConfidenceAggregatorAgent()
            print("✅ Triangulation agents loaded")
        except ImportError:
            print("⚠️ Some triangulation agents not available")
        
        return agents
    
    async def analyze_complete_project(self, project_path: str, include_cleanup: bool = True) -> Dict[str, Any]:
        """
        Perform complete cognitive triangulation analysis of entire project
        """
        start_time = time.time()
        project_path = Path(project_path)
        
        print(f"🧠 COMPLETE PROJECT COGNITIVE TRIANGULATION")
        print(f"=" * 60)
        print(f"📁 Project: {project_path}")
        print(f"🧹 Cleanup Analysis: {'Enabled' if include_cleanup else 'Disabled'}")
        print()
        
        # Step 1: Discover all files
        print("🔍 STEP 1: Project Discovery")
        print("-" * 40)
        
        files_to_analyze = self._discover_files(project_path)
        print(f"📊 Discovered {len(files_to_analyze)} analyzable files")
        
        # Step 2: Analyze each file
        print(f"\n🚀 STEP 2: File Analysis")
        print("-" * 40)
        
        file_analyses = []
        total_processing_time = 0
        
        for i, file_path in enumerate(files_to_analyze, 1):
            print(f"   Analyzing {i}/{len(files_to_analyze)}: {file_path.name}")
            
            try:
                analysis = await self._analyze_single_file(file_path)
                file_analyses.append(analysis)
                total_processing_time += analysis.processing_time_ms
            except Exception as e:
                print(f"   ⚠️ Error analyzing {file_path}: {e}")
        
        # Step 3: Cleanup analysis
        cleanup_recommendations = []
        if include_cleanup:
            print(f"\n🧹 STEP 3: Cleanup Analysis")
            print("-" * 40)
            cleanup_recommendations = self.cleanup_agent.analyze_cleanup_opportunities(project_path)
            print(f"🎯 Found {len(cleanup_recommendations)} cleanup opportunities")
        
        # Step 4: Aggregate project insights
        print(f"\n📊 STEP 4: Project Aggregation")
        print("-" * 40)
        
        project_insights = self._aggregate_project_insights(file_analyses, cleanup_recommendations)
        
        total_time = time.time() - start_time
        project_insights['analysis_metadata'] = {
            'total_time_seconds': total_time,
            'total_processing_time_ms': total_processing_time,
            'files_analyzed': len(file_analyses),
            'cleanup_opportunities': len(cleanup_recommendations),
            'analysis_date': datetime.now().isoformat()
        }
        
        # Step 5: Generate report
        self._generate_project_report(project_insights, project_path)
        
        return project_insights
    
    def _discover_files(self, project_path: Path) -> List[Path]:
        """
        Discover all analyzable files in the project
        """
        files = []
        
        # Skip common directories we don't want to analyze
        skip_dirs = {
            '__pycache__', '.git', 'node_modules', '.venv', 'venv', 
            '.pytest_cache', 'htmlcov', '.coverage', 'dist', 'build',
            '.next', '.nuxt', 'target', 'bin', 'obj'
        }
        
        for root, dirs, filenames in os.walk(project_path):
            # Remove skip directories from dirs to prevent walking into them
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for filename in filenames:
                file_path = Path(root) / filename
                
                # Check if file has supported extension
                if file_path.suffix.lower() in self.supported_extensions:
                    # Additional filters
                    if not filename.startswith('.') and file_path.stat().st_size < 10 * 1024 * 1024:  # < 10MB
                        files.append(file_path)
        
        return sorted(files)
    
    async def _analyze_single_file(self, file_path: Path) -> FileAnalysis:
        """
        Analyze a single file using available agents
        """
        start_time = time.time()
        
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, PermissionError):
            # Skip binary or inaccessible files
            return FileAnalysis(
                path=str(file_path),
                size=file_path.stat().st_size,
                lines=0,
                pois=0,
                relationships=0,
                patterns=0,
                confidence=0.0,
                processing_time_ms=0.0,
                file_type='unreadable'
            )
        
        file_size = len(content)
        line_count = len(content.splitlines())
        file_type = file_path.suffix.lower()
        
        pois = relationships = patterns = 0
        confidence = 0.0
        
        # Use CodeScout if available
        if 'code_scout' in self.agents_available:
            try:
                scout_input = f'''<code_analysis_request>
                    <file_path>{file_path.name}</file_path>
                    <file_content>{content}</file_content>
                    <language>{self._detect_language(file_path)}</language>
                    <analysis_depth>standard</analysis_depth>
                </code_analysis_request>'''
                
                scout_result = self.agents_available['code_scout'].process(scout_input)
                
                # Quick parse of results
                import xml.etree.ElementTree as ET
                try:
                    scout_root = ET.fromstring(scout_result)
                    pois = len(scout_root.findall('.//poi'))
                    confidence = 85.0  # Default confidence for successful analysis
                except ET.ParseError:
                    pass
                    
            except Exception as e:
                pass  # Continue with manual analysis
        
        # Manual analysis if agents not available
        if pois == 0:
            pois = self._count_basic_pois(content, file_type)
            relationships = self._estimate_relationships(content)
            patterns = self._detect_basic_patterns(content)
            confidence = 70.0
        
        processing_time = (time.time() - start_time) * 1000
        
        return FileAnalysis(
            path=str(file_path),
            size=file_size,
            lines=line_count,
            pois=pois,
            relationships=relationships,
            patterns=patterns,
            confidence=confidence,
            processing_time_ms=processing_time,
            file_type=file_type
        )
    
    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        ext_to_lang = {
            '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
            '.java': 'java', '.cpp': 'cpp', '.c': 'c', '.h': 'c',
            '.rb': 'ruby', '.go': 'go', '.rs': 'rust', '.php': 'php',
            '.cs': 'csharp', '.swift': 'swift', '.kt': 'kotlin',
            '.md': 'markdown', '.json': 'json', '.xml': 'xml',
            '.yaml': 'yaml', '.yml': 'yaml'
        }
        return ext_to_lang.get(file_path.suffix.lower(), 'text')
    
    def _count_basic_pois(self, content: str, file_type: str) -> int:
        """Basic POI counting for when agents aren't available"""
        poi_count = 0
        
        if file_type == '.py':
            poi_count += content.count('def ')
            poi_count += content.count('class ')
            poi_count += content.count('import ')
            poi_count += content.count('from ')
        elif file_type in ['.js', '.ts']:
            poi_count += content.count('function ')
            poi_count += content.count('class ')
            poi_count += content.count('const ')
            poi_count += content.count('let ')
        elif file_type == '.java':
            poi_count += content.count('public ')
            poi_count += content.count('private ')
            poi_count += content.count('class ')
            poi_count += content.count('interface ')
        
        return poi_count
    
    def _estimate_relationships(self, content: str) -> int:
        """Estimate relationship count"""
        # Simple heuristic based on common relationship indicators
        relationships = 0
        relationships += content.count('import')
        relationships += content.count('extends')
        relationships += content.count('implements')
        relationships += content.count('new ')
        relationships += content.count('.')  # Method calls, property access
        return min(relationships // 10, 50)  # Cap and normalize
    
    def _detect_basic_patterns(self, content: str) -> int:
        """Detect basic design patterns"""
        patterns = 0
        pattern_indicators = [
            'factory', 'builder', 'singleton', 'observer', 'strategy',
            'decorator', 'adapter', 'facade', 'proxy', 'template',
            'mvc', 'mvp', 'mvvm', 'repository', 'service'
        ]
        
        content_lower = content.lower()
        for pattern in pattern_indicators:
            if pattern in content_lower:
                patterns += 1
        
        return patterns
    
    def _aggregate_project_insights(self, file_analyses: List[FileAnalysis], 
                                   cleanup_recommendations: List[CleanupRecommendation]) -> Dict[str, Any]:
        """
        Aggregate insights across the entire project
        """
        if not file_analyses:
            return {'error': 'No files analyzed'}
        
        # Calculate totals
        total_files = len(file_analyses)
        total_size = sum(f.size for f in file_analyses)
        total_lines = sum(f.lines for f in file_analyses)
        total_pois = sum(f.pois for f in file_analyses)
        total_relationships = sum(f.relationships for f in file_analyses)
        total_patterns = sum(f.patterns for f in file_analyses)
        avg_confidence = sum(f.confidence for f in file_analyses) / total_files
        total_processing_time = sum(f.processing_time_ms for f in file_analyses)
        
        # Analyze file types
        file_types = {}
        for analysis in file_analyses:
            file_type = analysis.file_type
            if file_type not in file_types:
                file_types[file_type] = {'count': 0, 'size': 0, 'lines': 0}
            file_types[file_type]['count'] += 1
            file_types[file_type]['size'] += analysis.size
            file_types[file_type]['lines'] += analysis.lines
        
        # Top files by various metrics
        largest_files = sorted(file_analyses, key=lambda f: f.size, reverse=True)[:10]
        most_complex_files = sorted(file_analyses, key=lambda f: f.pois, reverse=True)[:10]
        
        # Cleanup insights
        cleanup_stats = {
            'total_opportunities': len(cleanup_recommendations),
            'high_priority': len([r for r in cleanup_recommendations if r.priority == 'high']),
            'potential_space_saved': sum(r.size_saved for r in cleanup_recommendations),
            'actions': {}
        }
        
        for rec in cleanup_recommendations:
            action = rec.action
            if action not in cleanup_stats['actions']:
                cleanup_stats['actions'][action] = 0
            cleanup_stats['actions'][action] += 1
        
        return {
            'project_summary': {
                'total_files': total_files,
                'total_size_bytes': total_size,
                'total_lines': total_lines,
                'total_pois': total_pois,
                'total_relationships': total_relationships,
                'total_patterns': total_patterns,
                'average_confidence': avg_confidence,
                'total_processing_time_ms': total_processing_time
            },
            'file_type_breakdown': file_types,
            'top_files': {
                'largest': [{'path': f.path, 'size': f.size} for f in largest_files[:5]],
                'most_complex': [{'path': f.path, 'pois': f.pois} for f in most_complex_files[:5]]
            },
            'cleanup_analysis': cleanup_stats,
            'cleanup_recommendations': cleanup_recommendations,
            'detailed_analyses': file_analyses
        }
    
    def _generate_project_report(self, insights: Dict[str, Any], project_path: Path):
        """
        Generate and display comprehensive project report
        """
        print(f"\n" + "=" * 80)
        print(f"🎉 COMPLETE PROJECT ANALYSIS REPORT")
        print(f"=" * 80)
        
        summary = insights['project_summary']
        
        print(f"\n📊 PROJECT SUMMARY:")
        print(f"   📁 Files Analyzed: {summary['total_files']}")
        print(f"   📏 Total Size: {summary['total_size_bytes'] / 1024:.1f} KB")
        print(f"   📝 Total Lines: {summary['total_lines']:,}")
        print(f"   🎯 POIs Found: {summary['total_pois']}")
        print(f"   🔗 Relationships: {summary['total_relationships']}")
        print(f"   🎨 Patterns: {summary['total_patterns']}")
        print(f"   📊 Avg Confidence: {summary['average_confidence']:.1f}%")
        print(f"   ⚡ Processing Time: {summary['total_processing_time_ms']:.1f}ms")
        
        print(f"\n📁 FILE TYPE BREAKDOWN:")
        for file_type, stats in insights['file_type_breakdown'].items():
            print(f"   {file_type}: {stats['count']} files, {stats['lines']} lines")
        
        print(f"\n🏆 TOP FILES:")
        print("   📏 Largest Files:")
        for file_info in insights['top_files']['largest']:
            print(f"      • {Path(file_info['path']).name} ({file_info['size']:,} bytes)")
        
        print("   🧠 Most Complex Files:")
        for file_info in insights['top_files']['most_complex']:
            print(f"      • {Path(file_info['path']).name} ({file_info['pois']} POIs)")
        
        cleanup = insights['cleanup_analysis']
        if cleanup['total_opportunities'] > 0:
            print(f"\n🧹 CLEANUP OPPORTUNITIES:")
            print(f"   🎯 Total Opportunities: {cleanup['total_opportunities']}")
            print(f"   🚨 High Priority: {cleanup['high_priority']}")
            print(f"   💾 Potential Space Saved: {cleanup['potential_space_saved'] / 1024:.1f} KB")
            
            print("   📋 Actions Recommended:")
            for action, count in cleanup['actions'].items():
                print(f"      • {action.title()}: {count} items")
            
            print(f"\n🧹 TOP CLEANUP RECOMMENDATIONS:")
            high_priority = [r for r in insights['cleanup_recommendations'] if r.priority == 'high'][:5]
            for rec in high_priority:
                print(f"      • {rec.action.upper()}: {rec.path} ({rec.reason})")
        
        print(f"\n🎯 PROJECT HEALTH ASSESSMENT:")
        health_score = self._calculate_health_score(insights)
        print(f"   🏥 Overall Health: {health_score}%")
        
        if health_score >= 80:
            print("   ✅ Excellent project structure and cleanliness!")
        elif health_score >= 60:
            print("   👍 Good project, minor cleanup recommended")
        else:
            print("   ⚠️ Project needs attention - cleanup and refactoring recommended")
    
    def _calculate_health_score(self, insights: Dict[str, Any]) -> int:
        """Calculate overall project health score"""
        score = 100
        
        # Deduct points for cleanup issues
        cleanup = insights['cleanup_analysis']
        if cleanup['total_opportunities'] > 0:
            score -= min(cleanup['high_priority'] * 5, 30)  # Max 30 points deduction
            score -= min(cleanup['total_opportunities'] * 2, 20)  # Max 20 points deduction
        
        # Bonus for good structure
        summary = insights['project_summary']
        if summary['average_confidence'] > 80:
            score += 5
        
        return max(score, 0)

async def main():
    """Main entry point for complete project analysis"""
    
    # Check for command line argument or use default
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
    else:
        target_path = '/Users/bobdallavia/X-Agent-Pipeline'  # Bob's original X-Agent folder
    
    analyzer = CompleteProjectAnalyzer()
    
    print("🚀 Starting Complete Project Cognitive Triangulation Analysis...")
    print()
    
    insights = await analyzer.analyze_complete_project(target_path, include_cleanup=True)
    
    print(f"\n🎉 Analysis completed successfully!")
    print(f"📊 Analyzed {insights['project_summary']['total_files']} files")
    print(f"🧹 Found {insights['cleanup_analysis']['total_opportunities']} cleanup opportunities")

if __name__ == "__main__":
    asyncio.run(main())
