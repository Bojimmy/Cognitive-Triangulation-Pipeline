#!/usr/bin/env python3
"""
Complete Dead Project Revival System
The ultimate "Project Necromancer" with full GitHub MCP + Context7 MCP integration

This system combines:
1. Cognitive Triangulation Patterns (your approach)
2. GitHub MCP (solutions from community)
3. Context7 MCP (architectural analysis)

Perfect for reviving abandoned projects that died from LLM going off the rails!
"""
import asyncio
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Import our specialized components
import sys
sys.path.append('/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation')

from dead_project_revival_detective import ProjectRevivalDetective, ProjectDeathCause
from github_mcp_integration import EnhancedProjectRevivalWithGitHub, GitHubSolution
from context7_mcp_integration import EnhancedProjectRevivalWithContext7, ArchitecturalIssue

@dataclass
class RevivalSolution:
    """Complete solution for reviving a dead project"""
    issue_description: str
    solution_source: str  # 'cognitive', 'github', 'context7', 'triangulated'
    confidence: float
    estimated_time: str
    steps: List[str]
    github_solutions: List[GitHubSolution]
    architectural_fixes: List[str]
    quick_win: bool = False

class CompleteDeadProjectRevivalSystem:
    """
    The Ultimate Project Necromancer
    
    Combines cognitive triangulation, GitHub community solutions,
    and architectural analysis to diagnose and revive dead projects
    """
    
    def __init__(self, github_token: Optional[str] = None):
        # Initialize all three analysis systems
        self.cognitive_detective = ProjectRevivalDetective()
        self.github_integration = EnhancedProjectRevivalWithGitHub(github_token)
        self.context7_integration = EnhancedProjectRevivalWithContext7()
        
        self.system_ready = False
        self.revival_stats = {
            'projects_analyzed': 0,
            'projects_revived': 0,
            'average_revival_time': 0,
            'success_rate': 0.0
        }
        
        print("💀 COMPLETE DEAD PROJECT REVIVAL SYSTEM")
        print("=" * 60)
        print("🧠 Cognitive Triangulation Detective: Ready")
        print("🐙 GitHub MCP Integration: Initializing...")
        print("🧠 Context7 MCP Integration: Initializing...")
    
    async def initialize_system(self):
        """Initialize all MCP connections"""
        print("\n🔄 Initializing MCP connections...")
        
        # Initialize GitHub MCP
        github_connected = await self.github_integration.initialize()
        
        # Initialize Context7 MCP  
        context7_connected = await self.context7_integration.initialize()
        
        self.system_ready = github_connected and context7_connected
        
        if self.system_ready:
            print("✅ All systems connected and ready!")
        else:
            print("⚠️ Some systems running in simulation mode")
        
        print(f"🎯 System Status: {'FULLY OPERATIONAL' if self.system_ready else 'SIMULATION MODE'}")
        
        return self.system_ready
    
    async def diagnose_and_revive_project(self, project_path: str, 
                                        generate_fixes: bool = True,
                                        create_revival_plan: bool = True) -> Dict[str, Any]:
        """
        Complete project diagnosis and revival plan generation
        
        This is the main method that orchestrates all three analysis systems
        """
        
        print(f"\n💀 COMPLETE PROJECT REVIVAL ANALYSIS")
        print(f"=" * 80)
        print(f"📁 Target Project: {project_path}")
        print(f"🎯 Mission: Diagnose death causes and create revival plan")
        
        if not Path(project_path).exists():
            return {'error': 'Project path does not exist', 'status': 'failed'}
        
        start_time = time.time()
        
        # Phase 1: Cognitive Triangulation Analysis (your approach)
        print(f"\n🧠 PHASE 1: COGNITIVE TRIANGULATION ANALYSIS")
        print("-" * 50)
        cognitive_diagnosis = await self.cognitive_detective.diagnose_dead_project(project_path)
        
        # Phase 2: GitHub Community Solutions
        print(f"\n🐙 PHASE 2: GITHUB COMMUNITY SOLUTIONS")
        print("-" * 50)
        github_solutions = await self._get_github_solutions(cognitive_diagnosis['death_causes'])
        
        # Phase 3: Architectural Analysis
        print(f"\n🏗️ PHASE 3: ARCHITECTURAL ANALYSIS")
        print("-" * 50)
        architectural_issues = await self.context7_integration.get_architectural_issues(project_path)
        
        # Phase 4: Triangulated Revival Plan
        print(f"\n🎯 PHASE 4: TRIANGULATED REVIVAL PLAN")
        print("-" * 50)
        revival_plan = self._create_triangulated_revival_plan(
            cognitive_diagnosis, github_solutions, architectural_issues
        )
        
        # Phase 5: Generate executable fixes (if requested)
        executable_fixes = {}
        if generate_fixes:
            print(f"\n🔧 PHASE 5: GENERATING EXECUTABLE FIXES")
            print("-" * 50)
            executable_fixes = await self._generate_executable_fixes(revival_plan)
        
        # Compile comprehensive results
        total_time = time.time() - start_time
        
        complete_diagnosis = {
            'project_path': project_path,
            'analysis_metadata': {
                'total_analysis_time': total_time,
                'analysis_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'system_mode': 'full' if self.system_ready else 'simulation',
                'phases_completed': 5 if generate_fixes else 4
            },
            'cognitive_analysis': cognitive_diagnosis,
            'github_solutions': github_solutions,
            'architectural_issues': [asdict(issue) for issue in architectural_issues],
            'triangulated_revival_plan': revival_plan,
            'executable_fixes': executable_fixes,
            'revival_probability': self._calculate_enhanced_revival_probability(
                cognitive_diagnosis, github_solutions, architectural_issues
            ),
            'system_recommendations': self._generate_system_recommendations(revival_plan)
        }
        
        # Display comprehensive results
        self._display_complete_diagnosis(complete_diagnosis)
        
        # Update stats
        self.revival_stats['projects_analyzed'] += 1
        
        return complete_diagnosis
    
    async def _get_github_solutions(self, death_causes: List[ProjectDeathCause]) -> Dict[str, List[GitHubSolution]]:
        """Get GitHub community solutions for each death cause"""
        
        github_solutions = {}
        
        print("🔍 Searching GitHub for community solutions...")
        
        for cause in death_causes[:10]:  # Top 10 most critical issues
            print(f"   📍 Searching: {cause.issue_type}")
            
            solutions = await self.github_integration.get_enhanced_solutions(cause)
            
            if solutions:
                github_solutions[cause.issue_type] = solutions
                print(f"      ✅ Found {len(solutions)} solutions")
            else:
                print(f"      ⚠️ No GitHub solutions found")
        
        total_solutions = sum(len(sols) for sols in github_solutions.values())
        print(f"\n📊 GitHub Analysis Complete: {total_solutions} community solutions found")
        
        return github_solutions
    
    def _create_triangulated_revival_plan(self, 
                                        cognitive_diagnosis: Dict,
                                        github_solutions: Dict,
                                        architectural_issues: List[ArchitecturalIssue]) -> Dict[str, Any]:
        """Create triangulated revival plan using all three analysis sources"""
        
        print("🧮 Triangulating solutions from all sources...")
        
        # Combine all issues and solutions
        revival_solutions = []
        
        # Process cognitive detection issues
        for cause in cognitive_diagnosis['death_causes']:
            github_sols = github_solutions.get(cause.issue_type, [])
            
            solution = RevivalSolution(
                issue_description=cause.description,
                solution_source='cognitive' if not github_sols else 'triangulated',
                confidence=cause.confidence,
                estimated_time=self._estimate_fix_time(cause),
                steps=cause.revival_steps,
                github_solutions=github_sols,
                architectural_fixes=[],
                quick_win=any(keyword in cause.issue_type.lower() 
                            for keyword in ['port', 'missing', 'indent', 'json'])
            )
            
            # Boost confidence if GitHub confirms the issue
            if github_sols:
                solution.confidence = min(solution.confidence + 0.1, 1.0)
            
            revival_solutions.append(solution)
        
        # Add architectural issues
        for arch_issue in architectural_issues:
            solution = RevivalSolution(
                issue_description=arch_issue.description,
                solution_source='context7',
                confidence=arch_issue.confidence,
                estimated_time=self._estimate_architectural_fix_time(arch_issue),
                steps=arch_issue.refactoring_suggestions,
                github_solutions=[],
                architectural_fixes=arch_issue.refactoring_suggestions,
                quick_win=False  # Architectural fixes are rarely quick
            )
            revival_solutions.append(solution)
        
        # Sort by priority: quick wins first, then by confidence
        revival_solutions.sort(key=lambda x: (not x.quick_win, -x.confidence))
        
        # Create phased revival plan
        revival_plan = {
            'total_solutions': len(revival_solutions),
            'quick_wins': [sol for sol in revival_solutions if sol.quick_win],
            'critical_fixes': [sol for sol in revival_solutions 
                             if not sol.quick_win and sol.confidence > 0.8],
            'architectural_improvements': [sol for sol in revival_solutions 
                                         if sol.solution_source == 'context7'],
            'estimated_total_time': sum(self._parse_time_estimate(sol.estimated_time) 
                                      for sol in revival_solutions),
            'success_factors': self._identify_success_factors(revival_solutions),
            'risk_factors': self._identify_risk_factors(revival_solutions)
        }
        
        print(f"✅ Triangulated plan created:")
        print(f"   ⚡ Quick wins: {len(revival_plan['quick_wins'])}")
        print(f"   🔧 Critical fixes: {len(revival_plan['critical_fixes'])}")
        print(f"   🏗️ Architectural: {len(revival_plan['architectural_improvements'])}")
        print(f"   ⏰ Total time: {revival_plan['estimated_total_time']:.1f} hours")
        
        return revival_plan
    
    async def _generate_executable_fixes(self, revival_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Generate actual executable fixes for the most critical issues"""
        
        print("🔧 Generating executable fixes for critical issues...")
        
        executable_fixes = {
            'quick_fix_scripts': [],
            'configuration_updates': [],
            'dependency_commands': [],
            'manual_steps': []
        }
        
        # Generate quick fix scripts
        for quick_win in revival_plan['quick_wins'][:5]:  # Top 5 quick wins
            if 'port' in quick_win.issue_description.lower():
                executable_fixes['quick_fix_scripts'].append({
                    'name': 'fix_port_conflict.sh',
                    'description': 'Kill processes using conflicting ports',
                    'script': '''#!/bin/bash
# Kill processes using common development ports
echo "Checking for port conflicts..."
lsof -ti:3000 | xargs kill -9 2>/dev/null || echo "Port 3000 is free"
lsof -ti:8000 | xargs kill -9 2>/dev/null || echo "Port 8000 is free"
lsof -ti:5000 | xargs kill -9 2>/dev/null || echo "Port 5000 is free"
echo "Port conflicts resolved!"''',
                    'execution_time': '30 seconds'
                })
            
            elif 'missing dependency' in quick_win.issue_description.lower():
                executable_fixes['dependency_commands'].append({
                    'name': 'install_missing_dependencies',
                    'description': 'Install common missing dependencies',
                    'commands': [
                        'pip install -r requirements.txt',
                        'npm install',
                        'pip install python-dotenv flask requests'
                    ],
                    'execution_time': '2-5 minutes'
                })
            
            elif 'indent' in quick_win.issue_description.lower():
                executable_fixes['quick_fix_scripts'].append({
                    'name': 'fix_python_indentation.py',
                    'description': 'Auto-fix Python indentation issues',
                    'script': '''#!/usr/bin/env python3
import autopep8
import glob

print("Fixing Python indentation issues...")
for py_file in glob.glob("**/*.py", recursive=True):
    if "__pycache__" not in py_file:
        try:
            with open(py_file, 'r') as f:
                original = f.read()
            
            fixed = autopep8.fix_code(original, options={'aggressive': 1})
            
            with open(py_file, 'w') as f:
                f.write(fixed)
            
            print(f"Fixed: {py_file}")
        except Exception as e:
            print(f"Could not fix {py_file}: {e}")

print("Indentation fixes complete!")''',
                    'execution_time': '1-2 minutes'
                })
        
        # Generate configuration updates
        executable_fixes['configuration_updates'].append({
            'file': '.env.example',
            'description': 'Template for environment variables',
            'content': '''# Environment Configuration
# Copy this file to .env and fill in your values

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Database
DATABASE_URL=sqlite:///./database.db
REDIS_URL=redis://localhost:6379

# Server Configuration
PORT=3000
DEBUG=true
NODE_ENV=development

# Security
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here
'''
        })
        
        print(f"✅ Generated {len(executable_fixes['quick_fix_scripts'])} executable scripts")
        print(f"✅ Generated {len(executable_fixes['dependency_commands'])} dependency fixes")
        print(f"✅ Generated {len(executable_fixes['configuration_updates'])} config templates")
        
        return executable_fixes
    
    def _calculate_enhanced_revival_probability(self, 
                                              cognitive_diagnosis: Dict,
                                              github_solutions: Dict,
                                              architectural_issues: List) -> Dict[str, Any]:
        """Calculate enhanced revival probability using all data sources"""
        
        base_probability = cognitive_diagnosis['success_probability']['overall']
        
        # Boost probability based on GitHub solutions available
        github_boost = min(len(github_solutions) * 0.05, 0.2)  # Max 20% boost
        
        # Reduce probability for architectural issues
        arch_penalty = len(architectural_issues) * 0.03  # 3% per architectural issue
        
        # Final probability
        enhanced_probability = max(0.1, min(0.95, base_probability + github_boost - arch_penalty))
        
        return {
            'overall_probability': enhanced_probability,
            'base_cognitive_score': base_probability,
            'github_solutions_boost': github_boost,
            'architectural_penalty': arch_penalty,
            'confidence_level': 'high' if enhanced_probability > 0.7 else 
                              'medium' if enhanced_probability > 0.4 else 'low',
            'reasoning': self._get_probability_reasoning(enhanced_probability, github_solutions, architectural_issues)
        }
    
    def _generate_system_recommendations(self, revival_plan: Dict) -> List[str]:
        """Generate high-level system recommendations"""
        
        recommendations = []
        
        quick_wins = len(revival_plan['quick_wins'])
        critical_fixes = len(revival_plan['critical_fixes'])
        
        if quick_wins > 0:
            recommendations.append(f"🚀 START HERE: You have {quick_wins} quick wins that can be fixed in under 30 minutes each")
        
        if critical_fixes > 5:
            recommendations.append("⚠️ This project has significant issues. Consider gradual revival over several sessions")
        elif critical_fixes > 0:
            recommendations.append(f"🔧 Focus on the {critical_fixes} critical fixes after completing quick wins")
        
        if revival_plan['estimated_total_time'] > 40:
            recommendations.append("⏰ Large time investment required. Consider breaking revival into phases")
        elif revival_plan['estimated_total_time'] < 8:
            recommendations.append("⚡ This project can likely be revived in a single work session!")
        
        if len(revival_plan['architectural_improvements']) > 0:
            recommendations.append("🏗️ Consider architectural improvements for long-term maintainability")
        
        recommendations.append("📚 Use GitHub solutions as references - the community has solved similar issues")
        recommendations.append("🧪 Test each fix incrementally to avoid introducing new issues")
        
        return recommendations
    
    def _estimate_fix_time(self, cause: ProjectDeathCause) -> str:
        """Estimate time to fix a specific death cause"""
        
        if cause.severity == 'project_killer':
            return "2-4 hours"
        elif cause.severity == 'major':
            return "1-2 hours"
        else:
            return "15-30 minutes"
    
    def _estimate_architectural_fix_time(self, issue: ArchitecturalIssue) -> str:
        """Estimate time to fix architectural issues"""
        
        if issue.severity == 'critical':
            return "8-16 hours"
        elif issue.severity == 'major':
            return "4-8 hours"
        else:
            return "1-2 hours"
    
    def _parse_time_estimate(self, time_str: str) -> float:
        """Parse time estimate string to hours"""
        
        if 'minutes' in time_str:
            return 0.5  # Assume 30 minutes average
        elif 'hour' in time_str:
            # Extract first number
            import re
            numbers = re.findall(r'\d+', time_str)
            return float(numbers[0]) if numbers else 1.0
        else:
            return 1.0  # Default 1 hour
    
    def _identify_success_factors(self, solutions: List[RevivalSolution]) -> List[str]:
        """Identify factors that increase revival success probability"""
        
        factors = []
        
        quick_win_count = len([s for s in solutions if s.quick_win])
        if quick_win_count > 0:
            factors.append(f"{quick_win_count} quick wins available for immediate progress")
        
        github_solutions = sum(len(s.github_solutions) for s in solutions)
        if github_solutions > 0:
            factors.append(f"{github_solutions} community solutions available as references")
        
        high_confidence = len([s for s in solutions if s.confidence > 0.8])
        if high_confidence > 0:
            factors.append(f"{high_confidence} issues have high-confidence solutions")
        
        return factors
    
    def _identify_risk_factors(self, solutions: List[RevivalSolution]) -> List[str]:
        """Identify factors that could complicate revival"""
        
        factors = []
        
        architectural_count = len([s for s in solutions if s.solution_source == 'context7'])
        if architectural_count > 3:
            factors.append(f"{architectural_count} architectural issues may require significant refactoring")
        
        no_github_solutions = len([s for s in solutions if not s.github_solutions and s.solution_source != 'context7'])
        if no_github_solutions > 5:
            factors.append(f"{no_github_solutions} issues have no community solutions available")
        
        total_time = sum(self._parse_time_estimate(s.estimated_time) for s in solutions)
        if total_time > 40:
            factors.append(f"Estimated {total_time:.1f} hours required - large time investment")
        
        return factors
    
    def _get_probability_reasoning(self, probability: float, github_solutions: Dict, architectural_issues: List) -> str:
        """Get human-readable reasoning for probability score"""
        
        if probability > 0.8:
            return "High success probability - mostly fixable issues with community solutions available"
        elif probability > 0.6:
            return "Good success probability - some challenges but definitely achievable"
        elif probability > 0.4:
            return "Moderate success probability - significant effort required but possible"
        else:
            return "Challenging revival - major structural issues present"
    
    def _display_complete_diagnosis(self, diagnosis: Dict[str, Any]):
        """Display comprehensive diagnosis results"""
        
        print(f"\n" + "=" * 80)
        print(f"💀 COMPLETE PROJECT REVIVAL DIAGNOSIS")
        print(f"=" * 80)
        
        metadata = diagnosis['analysis_metadata']
        cognitive = diagnosis['cognitive_analysis']
        revival_plan = diagnosis['triangulated_revival_plan']
        probability = diagnosis['revival_probability']
        
        # Header information
        print(f"\n📊 ANALYSIS SUMMARY:")
        print(f"   ⏱️ Total Analysis Time: {metadata['total_analysis_time']:.2f} seconds")
        print(f"   🔧 System Mode: {metadata['system_mode'].upper()}")
        print(f"   📅 Analysis Date: {metadata['analysis_date']}")
        
        # Enhanced probability assessment
        print(f"\n🎯 REVIVAL PROBABILITY ASSESSMENT:")
        prob_emoji = "🟢" if probability['overall_probability'] > 0.7 else "🟡" if probability['overall_probability'] > 0.4 else "🔴"
        print(f"   {prob_emoji} Overall Probability: {probability['overall_probability']*100:.1f}%")
        print(f"   🎨 Confidence Level: {probability['confidence_level'].upper()}")
        print(f"   📝 Assessment: {probability['reasoning']}")
        
        # Revival plan summary
        print(f"\n🚀 TRIANGULATED REVIVAL PLAN:")
        print(f"   ⚡ Quick Wins: {len(revival_plan['quick_wins'])} issues (start here!)")
        print(f"   🔧 Critical Fixes: {len(revival_plan['critical_fixes'])} issues")
        print(f"   🏗️ Architectural: {len(revival_plan['architectural_improvements'])} issues")
        print(f"   ⏰ Total Estimated Time: {revival_plan['estimated_total_time']:.1f} hours")
        
        # System recommendations
        print(f"\n💡 SYSTEM RECOMMENDATIONS:")
        for i, rec in enumerate(diagnosis['system_recommendations'], 1):
            print(f"   {i}. {rec}")
        
        # Success and risk factors
        if revival_plan['success_factors']:
            print(f"\n✅ SUCCESS FACTORS:")
            for factor in revival_plan['success_factors']:
                print(f"   • {factor}")
        
        if revival_plan['risk_factors']:
            print(f"\n⚠️ RISK FACTORS:")
            for risk in revival_plan['risk_factors']:
                print(f"   • {risk}")
        
        # GitHub solutions summary
        github_count = sum(len(sols) for sols in diagnosis['github_solutions'].values())
        if github_count > 0:
            print(f"\n🐙 GITHUB COMMUNITY SOLUTIONS:")
            print(f"   📚 {github_count} community solutions found")
            print(f"   🎯 Use these as references and starting points")
        
        # Next steps
        print(f"\n🎯 RECOMMENDED NEXT STEPS:")
        print(f"   1. 🚀 Start with quick wins to build momentum")
        print(f"   2. 🔧 Work through critical fixes systematically")
        print(f"   3. 🧪 Test each fix before moving to the next")
        print(f"   4. 📚 Reference GitHub solutions when stuck")
        print(f"   5. 🏗️ Address architectural issues for long-term health")
        
        print(f"\n🎉 PROJECT REVIVAL DIAGNOSIS COMPLETE!")
        print(f"💀 Ready to bring this project back to life? Let's go! 🚀")

# Example usage - Test the complete system
async def test_complete_revival_system():
    """Test the complete dead project revival system"""
    
    # Initialize the complete system
    revival_system = CompleteDeadProjectRevivalSystem()
    
    # Initialize all MCP connections
    await revival_system.initialize_system()
    
    # Test on Bob's X-Agent pipeline
    test_project = '/Users/bobdallavia/X-Agent-Pipeline'
    
    print(f"\n🧪 TESTING COMPLETE REVIVAL SYSTEM")
    print(f"📁 Target: {test_project}")
    print(f"🎯 Demonstrating full cognitive triangulation + MCP integration")
    
    # Run complete diagnosis
    diagnosis = await revival_system.diagnose_and_revive_project(
        test_project,
        generate_fixes=True,
        create_revival_plan=True
    )
    
    print(f"\n✅ COMPLETE SYSTEM TEST FINISHED!")
    print(f"🎯 System is ready for real dead project revival missions!")
    
    return diagnosis

if __name__ == "__main__":
    asyncio.run(test_complete_revival_system())
