#!/usr/bin/env python3
"""
ULTIMATE PROJECT NECROMANCER
The complete dead project revival system with all MCP integrations

Combines:
1. Cognitive Triangulation (your patterns)
2. GitHub MCP (community solutions) 
3. Context7 MCP (current documentation & examples)

This is the definitive solution for reviving dead projects!
"""
import asyncio
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import all our specialized systems
import sys
sys.path.append('/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation')

from dead_project_revival_detective import ProjectRevivalDetective, ProjectDeathCause
from real_github_mcp_client import RealGitHubMCPClient
from context7_documentation_revival import EnhancedDeadProjectRevivalWithDocs

class UltimateProjectNecromancer:
    """
    The Ultimate Project Necromancer
    
    Triple-powered revival system:
    🧠 Cognitive Triangulation - Find death patterns
    🐙 GitHub MCP - Get community solutions  
    📚 Context7 MCP - Get current documentation & examples
    
    Perfect for projects killed by:
    - LLM going off the rails with outdated info
    - Breaking changes in libraries
    - Outdated tutorials and examples
    - Version conflicts and API changes
    """
    
    def __init__(self, github_token: Optional[str] = None):
        print("💀 ULTIMATE PROJECT NECROMANCER")
        print("=" * 70)
        print("🎯 Mission: Bring dead projects back to life")
        print("🔧 Method: Triple-powered cognitive triangulation")
        
        # Initialize all three systems
        self.cognitive_detective = ProjectRevivalDetective()
        self.github_mcp = RealGitHubMCPClient()  
        self.context7_docs = EnhancedDeadProjectRevivalWithDocs()
        
        self.system_status = {
            'cognitive': True,  # Always available
            'github_mcp': False,
            'context7_mcp': False
        }
        
        self.revival_stats = {
            'projects_revived': 0,
            'average_success_rate': 0.0,
            'total_fixes_generated': 0
        }
    
    async def initialize_necromancer(self):
        """Initialize all MCP connections"""
        print("\n🔄 Initializing Project Necromancer systems...")
        
        # Initialize GitHub MCP
        github_connected = await self.github_mcp.initialize()
        self.system_status['github_mcp'] = github_connected
        
        # Initialize Context7 MCP
        context7_connected = await self.context7_docs.initialize()
        self.system_status['context7_mcp'] = context7_connected
        
        # Display system status
        print(f"\n📊 NECROMANCER SYSTEM STATUS:")
        print(f"   🧠 Cognitive Triangulation: ✅ ONLINE")
        print(f"   🐙 GitHub MCP: {'✅ CONNECTED' if github_connected else '⚠️ SIMULATED'}")
        print(f"   📚 Context7 MCP: {'✅ CONNECTED' if context7_connected else '⚠️ SIMULATED'}")
        
        power_level = sum(self.system_status.values())
        print(f"\n⚡ NECROMANCER POWER LEVEL: {power_level}/3")
        
        if power_level == 3:
            print("🔥 MAXIMUM POWER: All systems operational!")
        elif power_level == 2:
            print("⚡ HIGH POWER: Most systems operational!")
        else:
            print("🔋 BASIC POWER: Core system operational!")
        
        return power_level >= 1  # Need at least cognitive system
    
    async def revive_dead_project(self, project_path: str, 
                                deep_analysis: bool = True,
                                generate_fixes: bool = True,
                                create_scripts: bool = True) -> Dict[str, Any]:
        """
        MAIN NECROMANCER METHOD
        
        Complete project revival with triple-powered analysis
        """
        
        print(f"\n💀 ULTIMATE PROJECT NECROMANCER ENGAGED")
        print(f"=" * 80)
        print(f"📁 Target: {project_path}")
        print(f"⚡ Power Level: {sum(self.system_status.values())}/3")
        print(f"🎯 Mission: Diagnose and revive dead project")
        
        if not Path(project_path).exists():
            return {'error': 'Project path not found', 'revival_status': 'FAILED'}
        
        revival_start_time = time.time()
        
        # ============================================
        # PHASE 1: COGNITIVE TRIANGULATION ANALYSIS
        # ============================================
        print(f"\n🧠 PHASE 1: COGNITIVE TRIANGULATION ANALYSIS")
        print("-" * 60)
        print("🔍 Scanning for project death signatures...")
        
        cognitive_diagnosis = await self.cognitive_detective.diagnose_dead_project(project_path)
        death_causes = cognitive_diagnosis['death_causes']
        
        print(f"☠️ Cognitive analysis complete: {len(death_causes)} death causes identified")
        
        # ============================================
        # PHASE 2: GITHUB COMMUNITY INTELLIGENCE  
        # ============================================
        github_solutions = {}
        repository_analysis = {}
        if self.system_status['github_mcp']:
            print(f"\n🐙 PHASE 2: GITHUB COMMUNITY INTELLIGENCE")
            print("-" * 60)
            print("🔍 Analyzing repository and searching community solutions...")
            
            # Analyze the repository if it's a Git repo
            repository_analysis = await self.github_mcp.analyze_project_repository(project_path)
            
            # Search for community solutions
            github_solutions = await self.get_enhanced_solutions_batch(death_causes)
            community_solutions_count = sum(len(solutions) for solutions in github_solutions.values())
            print(f"📚 GitHub analysis complete: {community_solutions_count} community solutions found")
            
            if repository_analysis.get('has_github_remote'):
                repo = repository_analysis['repository']
                print(f"📊 Repository: {repo['owner']}/{repo['repo']}")
                languages = repository_analysis.get('languages', {})
                if languages:
                    top_lang = max(languages.items(), key=lambda x: x[1])[0]
                    print(f"🔧 Primary language: {top_lang}")
        else:
            print(f"\n🐙 PHASE 2: GITHUB MCP (SIMULATED)")
            print("⚠️ Running in simulation mode")
        
        # ============================================
        # PHASE 3: CONTEXT7 DOCUMENTATION REVIVAL
        # ============================================
        documentation_fixes = {}
        if self.system_status['context7_mcp']:
            print(f"\n📚 PHASE 3: CONTEXT7 DOCUMENTATION REVIVAL")
            print("-" * 60)
            print("📖 Fetching current documentation and examples...")
            
            documentation_fixes = await self.context7_docs.get_documentation_based_fixes(
                project_path, death_causes
            )
            
            libraries_detected = len(documentation_fixes.get('library_analysis', {}))
            doc_fixes_count = len(documentation_fixes.get('documentation_fixes', {}))
            print(f"📚 Context7 analysis complete: {libraries_detected} libraries, {doc_fixes_count} doc fixes")
        else:
            print(f"\n📚 PHASE 3: CONTEXT7 MCP (SIMULATED)")
            print("⚠️ Running in simulation mode")
        
        # ============================================
        # PHASE 4: TRIPLE-POWERED TRIANGULATION
        # ============================================
        print(f"\n🔺 PHASE 4: TRIPLE-POWERED TRIANGULATION")
        print("-" * 60)
        print("🧮 Combining cognitive + community + documentation intelligence...")
        
        triangulated_plan = await self._create_ultimate_revival_plan(
            cognitive_diagnosis, github_solutions, documentation_fixes, repository_analysis
        )
        
        # ============================================
        # PHASE 5: EXECUTABLE REVIVAL GENERATION
        # ============================================
        executable_revival = {}
        if generate_fixes:
            print(f"\n🔧 PHASE 5: EXECUTABLE REVIVAL GENERATION")
            print("-" * 60)
            print("⚙️ Generating executable fixes and scripts...")
            
            executable_revival = await self._generate_ultimate_fixes(
                triangulated_plan, documentation_fixes, create_scripts
            )
            
            fixes_generated = len(executable_revival.get('fix_scripts', [])) + \
                            len(executable_revival.get('config_updates', [])) + \
                            len(executable_revival.get('dependency_commands', []))
            print(f"🛠️ Revival generation complete: {fixes_generated} executable fixes created")
        
        # ============================================
        # FINAL NECROMANCER ASSESSMENT
        # ============================================
        total_time = time.time() - revival_start_time
        
        final_assessment = await self._generate_final_necromancer_assessment(
            cognitive_diagnosis, github_solutions, documentation_fixes, 
            triangulated_plan, executable_revival, total_time, repository_analysis
        )
        
        # Display ultimate results
        self._display_ultimate_necromancer_results(final_assessment)
        
        # Update necromancer stats
        self.revival_stats['projects_revived'] += 1
        self.revival_stats['total_fixes_generated'] += len(executable_revival.get('fix_scripts', []))
        
        return final_assessment
    
    async def get_enhanced_solutions_batch(self, death_causes: List[ProjectDeathCause]) -> Dict[str, Any]:
        """Enhanced batch solution gathering from GitHub using real MCP client"""
        
        if not self.system_status['github_mcp']:
            return {}
        
        # Use real GitHub MCP to search for similar issues
        solutions = await self.github_mcp.search_similar_issues(death_causes, limit=10)
        
        return solutions
    
    async def _create_ultimate_revival_plan(self, cognitive_diagnosis: Dict, 
                                          github_solutions: Dict, 
                                          documentation_fixes: Dict,
                                          repository_analysis: Dict = None) -> Dict[str, Any]:
        """Create the ultimate revival plan using all three intelligence sources"""
        
        print("🧠 Triangulating intelligence from all sources...")
        
        # Start with cognitive diagnosis
        base_plan = cognitive_diagnosis['revival_plan']
        base_causes = cognitive_diagnosis['death_causes']
        
        # Enhance with GitHub community solutions
        community_enhanced_solutions = []
        for cause in base_causes:
            github_sols = github_solutions.get(cause.issue_type, [])
            
            enhanced_solution = {
                'death_cause': cause,
                'cognitive_confidence': cause.confidence,
                'github_solutions': github_sols,
                'community_boost': 0.1 if github_sols else 0,
                'documentation_available': False,
                'final_confidence': cause.confidence
            }
            
            # Check if Context7 has documentation for this issue
            if documentation_fixes:
                doc_fixes = documentation_fixes.get('documentation_fixes', {})
                if any(cause.category.lower() in fix_type.lower() for fix_type in doc_fixes.keys()):
                    enhanced_solution['documentation_available'] = True
                    enhanced_solution['documentation_boost'] = 0.15
                    enhanced_solution['final_confidence'] += 0.15
            
            # Apply community boost
            enhanced_solution['final_confidence'] += enhanced_solution['community_boost']
            enhanced_solution['final_confidence'] = min(enhanced_solution['final_confidence'], 1.0)
            
            community_enhanced_solutions.append(enhanced_solution)
        
        # Create ultimate categorization
        ultimate_quick_wins = [sol for sol in community_enhanced_solutions 
                              if self._is_ultimate_quick_win(sol)]
        
        ultimate_critical_fixes = [sol for sol in community_enhanced_solutions 
                                  if sol['final_confidence'] > 0.8 and sol not in ultimate_quick_wins]
        
        ultimate_documentation_fixes = [sol for sol in community_enhanced_solutions 
                                       if sol['documentation_available']]
        
        # Calculate ultimate revival probability
        ultimate_probability = self._calculate_ultimate_revival_probability(
            community_enhanced_solutions, github_solutions, documentation_fixes
        )
        
        ultimate_plan = {
            'necromancer_power_level': sum(self.system_status.values()),
            'total_enhanced_solutions': len(community_enhanced_solutions),
            'ultimate_quick_wins': ultimate_quick_wins,
            'ultimate_critical_fixes': ultimate_critical_fixes,
            'ultimate_documentation_fixes': ultimate_documentation_fixes,
            'ultimate_revival_probability': ultimate_probability,
            'estimated_revival_time': self._calculate_ultimate_time_estimate(community_enhanced_solutions),
            'intelligence_sources_used': [k for k, v in self.system_status.items() if v],
            'necromancer_recommendations': self._generate_necromancer_recommendations(
                ultimate_quick_wins, ultimate_critical_fixes, ultimate_documentation_fixes
            )
        }
        
        print(f"✅ Ultimate triangulation complete:")
        print(f"   ⚡ Ultimate Quick Wins: {len(ultimate_quick_wins)}")
        print(f"   🔧 Ultimate Critical Fixes: {len(ultimate_critical_fixes)}")  
        print(f"   📚 Documentation-Enhanced: {len(ultimate_documentation_fixes)}")
        print(f"   🎯 Ultimate Revival Probability: {ultimate_probability['overall']*100:.1f}%")
        
        return ultimate_plan
    
    async def _generate_ultimate_fixes(self, triangulated_plan: Dict, 
                                     documentation_fixes: Dict, 
                                     create_scripts: bool) -> Dict[str, Any]:
        """Generate ultimate executable fixes combining all intelligence sources"""
        
        ultimate_fixes = {
            'fix_scripts': [],
            'config_updates': [],
            'dependency_commands': [],
            'documentation_examples': [],
            'migration_guides': [],
            'testing_commands': []
        }
        
        # Generate scripts for ultimate quick wins
        for quick_win in triangulated_plan['ultimate_quick_wins'][:5]:
            cause = quick_win['death_cause']
            
            if 'port' in cause.issue_type.lower():
                ultimate_fixes['fix_scripts'].append({
                    'name': 'ultimate_port_fix.sh',
                    'description': 'Ultimate port conflict resolution',
                    'intelligence_sources': ['cognitive', 'github'],
                    'script': self._generate_ultimate_port_fix_script(quick_win),
                    'execution_time': '30 seconds',
                    'success_probability': quick_win['final_confidence']
                })
            
            elif 'dependency' in cause.issue_type.lower():
                ultimate_fixes['dependency_commands'].append({
                    'name': 'ultimate_dependency_fix',
                    'description': 'Ultimate dependency resolution with current docs',
                    'intelligence_sources': ['cognitive', 'context7'],
                    'commands': self._generate_ultimate_dependency_commands(quick_win, documentation_fixes),
                    'execution_time': '2-5 minutes',
                    'success_probability': quick_win['final_confidence']
                })
        
        # Add Context7 documentation examples
        if documentation_fixes and 'updated_code_examples' in documentation_fixes:
            for example_type, examples in documentation_fixes['updated_code_examples'].items():
                ultimate_fixes['documentation_examples'].append({
                    'type': example_type,
                    'source': 'context7_current_docs',
                    'examples': examples,
                    'description': f'Current documentation examples for {example_type}'
                })
        
        # Add migration guides if version conflicts detected
        if documentation_fixes and 'version_migration_needed' in documentation_fixes:
            for migration in documentation_fixes['version_migration_needed']:
                ultimate_fixes['migration_guides'].append({
                    'library': migration['library'],
                    'from_version': migration['current_version'],
                    'recommended_action': migration['recommended_action'],
                    'source': 'context7_migration_docs'
                })
        
        # Generate ultimate configuration updates
        ultimate_fixes['config_updates'].append({
            'file': '.env.ultimate',
            'description': 'Ultimate environment configuration with current best practices',
            'intelligence_sources': ['cognitive', 'github', 'context7'],
            'content': self._generate_ultimate_env_config(documentation_fixes)
        })
        
        # Generate testing commands
        ultimate_fixes['testing_commands'] = [
            'npm test || python -m pytest',
            'npm run build || python setup.py build',  
            'npm start || python app.py',
            'echo "Ultimate fix verification complete!"'
        ]
        
        return ultimate_fixes
    
    def _is_ultimate_quick_win(self, enhanced_solution: Dict) -> bool:
        """Determine if this is an ultimate quick win"""
        cause = enhanced_solution['death_cause']
        
        quick_win_indicators = [
            'port' in cause.issue_type.lower(),
            'missing dependency' in cause.issue_type.lower(),
            'indent' in cause.issue_type.lower(),
            'json' in cause.issue_type.lower(),
            enhanced_solution['final_confidence'] > 0.9,
            enhanced_solution['github_solutions'] and enhanced_solution['documentation_available']
        ]
        
        return any(quick_win_indicators)
    
    def _calculate_ultimate_revival_probability(self, enhanced_solutions: List, 
                                              github_solutions: Dict, 
                                              documentation_fixes: Dict) -> Dict[str, Any]:
        """Calculate ultimate revival probability using all intelligence sources"""
        
        base_prob = 0.5  # Start neutral
        
        # Boost for high-confidence solutions
        high_confidence_count = len([sol for sol in enhanced_solutions if sol['final_confidence'] > 0.8])
        confidence_boost = min(high_confidence_count * 0.08, 0.4)
        
        # Boost for community solutions available
        community_boost = min(len(github_solutions) * 0.05, 0.25)
        
        # Boost for documentation availability
        doc_boost = 0.2 if documentation_fixes and documentation_fixes.get('library_analysis') else 0
        
        # Penalty for project killers
        project_killers = len([sol for sol in enhanced_solutions 
                              if sol['death_cause'].severity == 'project_killer'])
        killer_penalty = project_killers * 0.15
        
        ultimate_probability = max(0.1, min(0.95, 
            base_prob + confidence_boost + community_boost + doc_boost - killer_penalty
        ))
        
        return {
            'overall': ultimate_probability,
            'confidence_boost': confidence_boost,
            'community_boost': community_boost,
            'documentation_boost': doc_boost,
            'killer_penalty': killer_penalty,
            'assessment': self._get_ultimate_probability_assessment(ultimate_probability)
        }
    
    def _calculate_ultimate_time_estimate(self, enhanced_solutions: List) -> Dict[str, float]:
        """Calculate ultimate time estimate for revival"""
        
        total_hours = 0
        quick_win_hours = 0
        
        for solution in enhanced_solutions:
            cause = solution['death_cause']
            
            if self._is_ultimate_quick_win(solution):
                time_needed = 0.25  # 15 minutes
                quick_win_hours += time_needed
            elif cause.severity == 'project_killer':
                time_needed = 2.0 if solution['final_confidence'] > 0.8 else 4.0
            elif cause.severity == 'major':
                time_needed = 1.0 if solution['final_confidence'] > 0.8 else 2.0
            else:
                time_needed = 0.5
            
            total_hours += time_needed
        
        return {
            'total_hours': total_hours,
            'quick_wins_hours': quick_win_hours,
            'critical_hours': total_hours - quick_win_hours,
            'sessions_needed': max(1, total_hours // 4),  # 4-hour sessions
            'estimated_days': max(1, total_hours // 8)     # 8-hour days
        }
    
    def _generate_necromancer_recommendations(self, quick_wins: List, 
                                            critical_fixes: List, 
                                            doc_fixes: List) -> List[str]:
        """Generate ultimate necromancer recommendations"""
        
        recommendations = []
        
        if quick_wins:
            recommendations.append(f"🚀 IMMEDIATE ACTION: Execute {len(quick_wins)} ultimate quick wins first (high success probability)")
        
        if doc_fixes:
            recommendations.append(f"📚 DOCUMENTATION ADVANTAGE: {len(doc_fixes)} issues have current documentation examples - use them!")
        
        if critical_fixes:
            recommendations.append(f"🔧 SYSTEMATIC APPROACH: Work through {len(critical_fixes)} critical fixes methodically")
        
        recommendations.extend([
            "🧪 TEST INCREMENTALLY: Verify each fix before moving to the next",
            "📊 TRACK PROGRESS: Document what works for future project revivals",
            "🔄 ITERATE: Some fixes may reveal additional issues - that's normal",
            "🎯 FOCUS: Don't try to fix everything at once - prioritize by impact"
        ])
        
        return recommendations
    
    def _generate_ultimate_port_fix_script(self, quick_win: Dict) -> str:
        """Generate ultimate port fix script"""
        return '''#!/bin/bash
# Ultimate Port Conflict Fix - Necromancer Generated
echo "🔧 Ultimate port conflict resolution starting..."

# Kill common development ports
for port in 3000 8000 5000 4000 8080; do
    pid=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        echo "   Killing process $pid on port $port"
        kill -9 $pid 2>/dev/null
    fi
done

# Verify ports are free
echo "🔍 Verifying ports are available..."
for port in 3000 8000 5000; do
    if ! lsof -i:$port >/dev/null 2>&1; then
        echo "   ✅ Port $port is now available"
    else
        echo "   ⚠️ Port $port still in use"
    fi
done

echo "🎉 Ultimate port fix complete!"'''
    
    def _generate_ultimate_dependency_commands(self, quick_win: Dict, doc_fixes: Dict) -> List[str]:
        """Generate ultimate dependency installation commands"""
        
        commands = [
            "echo '🔧 Ultimate dependency resolution starting...'",
            "# Clear package caches",
            "npm cache clean --force 2>/dev/null || echo 'No npm cache to clear'",
            "pip cache purge 2>/dev/null || echo 'No pip cache to clear'",
            "",
            "# Install dependencies with current best practices",
            "if [ -f 'package.json' ]; then",
            "    echo '📦 Installing Node.js dependencies...'", 
            "    npm ci || npm install",
            "fi",
            "",
            "if [ -f 'requirements.txt' ]; then",
            "    echo '🐍 Installing Python dependencies...'",
            "    pip install -r requirements.txt",
            "fi",
            "",
            "echo '🎉 Ultimate dependency installation complete!'"
        ]
        
        return commands
    
    def _generate_ultimate_env_config(self, doc_fixes: Dict) -> str:
        """Generate ultimate environment configuration"""
        
        config = '''# Ultimate Environment Configuration
# Generated by Project Necromancer with current best practices

# === API KEYS & SECRETS ===
# Replace with your actual values
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
JWT_SECRET=your_super_secret_jwt_key_change_this
SESSION_SECRET=your_session_secret_change_this

# === DATABASE CONFIGURATION ===
DATABASE_URL=sqlite:///./necromancer_revived.db
REDIS_URL=redis://localhost:6379

# === SERVER CONFIGURATION ===
# Dynamic port assignment
PORT=${PORT:-3000}
NODE_ENV=development
DEBUG=true

# === SECURITY SETTINGS ===
CORS_ORIGIN=http://localhost:3000,http://localhost:3001
SECURE_COOKIES=false
TRUST_PROXY=false

# === PERFORMANCE SETTINGS ===
CACHE_TTL=3600
MAX_REQUEST_SIZE=10mb
RATE_LIMIT_WINDOW=900000
RATE_LIMIT_MAX=100

# === FEATURE FLAGS ===
ENABLE_ANALYTICS=false
ENABLE_LOGGING=true
ENABLE_METRICS=false

# Project revived by Ultimate Project Necromancer 💀🚀
'''
        
        return config
    
    def _get_ultimate_probability_assessment(self, probability: float) -> str:
        """Get ultimate probability assessment"""
        
        if probability > 0.85:
            return "🔥 EXCELLENT - Necromancer expects high success rate"
        elif probability > 0.7:
            return "🚀 VERY GOOD - Strong revival probability with current intelligence"
        elif probability > 0.55:
            return "⚡ GOOD - Solid revival chances with systematic approach"
        elif probability > 0.4:
            return "🔋 MODERATE - Challenging but achievable with patience"
        else:
            return "💀 DIFFICULT - Major issues detected, consider phased approach"
    
    async def _generate_final_necromancer_assessment(self, cognitive_diagnosis: Dict,
                                                   github_solutions: Dict,
                                                   documentation_fixes: Dict,
                                                   triangulated_plan: Dict,
                                                   executable_revival: Dict,
                                                   total_time: float,
                                                   repository_analysis: Dict = None) -> Dict[str, Any]:
        """Generate the final necromancer assessment"""
        
        return {
            'project_path': cognitive_diagnosis['project_path'],
            'necromancer_metadata': {
                'analysis_time': total_time,
                'power_level': triangulated_plan['necromancer_power_level'],
                'intelligence_sources': triangulated_plan['intelligence_sources_used'],
                'necromancer_version': '1.0.0-ultimate'
            },
            'cognitive_analysis': cognitive_diagnosis,
            'github_intelligence': github_solutions,
            'repository_analysis': repository_analysis or {},
            'context7_documentation': documentation_fixes,
            'ultimate_revival_plan': triangulated_plan,
            'executable_revival_kit': executable_revival,
            'final_assessment': {
                'revival_probability': triangulated_plan['ultimate_revival_probability'],
                'estimated_time': triangulated_plan['estimated_revival_time'],
                'necromancer_recommendations': triangulated_plan['necromancer_recommendations'],
                'success_factors': self._identify_ultimate_success_factors(triangulated_plan),
                'risk_factors': self._identify_ultimate_risk_factors(triangulated_plan),
                'next_actions': self._generate_immediate_next_actions(triangulated_plan)
            }
        }
    
    def _identify_ultimate_success_factors(self, plan: Dict) -> List[str]:
        """Identify ultimate success factors"""
        
        factors = []
        
        if plan['ultimate_quick_wins']:
            factors.append(f"{len(plan['ultimate_quick_wins'])} ultimate quick wins with high success probability")
        
        if plan['necromancer_power_level'] >= 2:
            factors.append(f"Multiple intelligence sources active (power level {plan['necromancer_power_level']}/3)")
        
        if plan['ultimate_documentation_fixes']:
            factors.append(f"{len(plan['ultimate_documentation_fixes'])} issues have current documentation")
        
        high_confidence = len([fix for fix in plan['ultimate_critical_fixes'] 
                              if fix['final_confidence'] > 0.8])
        if high_confidence > 0:
            factors.append(f"{high_confidence} critical fixes have high confidence scores")
        
        return factors
    
    def _identify_ultimate_risk_factors(self, plan: Dict) -> List[str]:
        """Identify ultimate risk factors"""
        
        factors = []
        
        project_killers = len([fix for fix in plan['ultimate_critical_fixes'] 
                              if fix['death_cause'].severity == 'project_killer'])
        if project_killers > 3:
            factors.append(f"{project_killers} project-killing issues detected")
        
        if plan['estimated_revival_time']['total_hours'] > 20:
            factors.append(f"Large time investment required: {plan['estimated_revival_time']['total_hours']:.1f} hours")
        
        if plan['necromancer_power_level'] < 2:
            factors.append("Limited intelligence sources - consider enabling MCP connections")
        
        low_confidence = len([fix for fix in plan['ultimate_critical_fixes'] 
                             if fix['final_confidence'] < 0.6])
        if low_confidence > 0:
            factors.append(f"{low_confidence} issues have uncertain solutions")
        
        return factors
    
    def _generate_immediate_next_actions(self, plan: Dict) -> List[str]:
        """Generate immediate next action recommendations"""
        
        actions = []
        
        if plan['ultimate_quick_wins']:
            actions.append("🚀 Execute ultimate quick wins first for immediate progress")
        
        actions.extend([
            "📚 Review Context7 documentation examples before coding",
            "🐙 Reference GitHub community solutions when stuck", 
            "🧪 Test each fix individually before moving to next",
            "📊 Document successful fixes for future reference"
        ])
        
        if plan['estimated_revival_time']['sessions_needed'] > 1:
            actions.append(f"⏰ Plan {int(plan['estimated_revival_time']['sessions_needed'])} focused work sessions")
        
        return actions
    
    def _display_ultimate_necromancer_results(self, assessment: Dict):
        """Display the ultimate necromancer results"""
        
        print(f"\n" + "=" * 80)
        print(f"💀 ULTIMATE PROJECT NECROMANCER ASSESSMENT COMPLETE")
        print(f"=" * 80)
        
        metadata = assessment['necromancer_metadata']
        final = assessment['final_assessment']
        plan = assessment['ultimate_revival_plan']
        
        # Necromancer header
        print(f"\n⚡ NECROMANCER STATUS:")
        print(f"   🔋 Power Level: {metadata['power_level']}/3")
        print(f"   🧠 Intelligence Sources: {', '.join(metadata['intelligence_sources'])}")
        print(f"   ⏱️ Analysis Time: {metadata['analysis_time']:.2f} seconds")
        print(f"   🏷️ Version: {metadata['necromancer_version']}")
        
        # Ultimate assessment
        prob = final['revival_probability']
        print(f"\n🎯 ULTIMATE REVIVAL ASSESSMENT:")
        prob_emoji = "🔥" if prob['overall'] > 0.7 else "⚡" if prob['overall'] > 0.4 else "💀"
        print(f"   {prob_emoji} Revival Probability: {prob['overall']*100:.1f}%")
        print(f"   📊 Assessment: {prob['assessment']}")
        
        # Time estimates
        time_est = final['estimated_time']
        print(f"\n⏰ REVIVAL TIME ESTIMATES:")
        print(f"   ⚡ Quick Wins: {time_est['quick_wins_hours']:.1f} hours")
        print(f"   🔧 Critical Fixes: {time_est['critical_hours']:.1f} hours")
        print(f"   📅 Total Time: {time_est['total_hours']:.1f} hours ({time_est['estimated_days']:.1f} days)")
        print(f"   🎯 Work Sessions: {int(time_est['sessions_needed'])} sessions recommended")
        
        # Ultimate plan summary
        print(f"\n🚀 ULTIMATE REVIVAL PLAN:")
        print(f"   ⚡ Ultimate Quick Wins: {len(plan['ultimate_quick_wins'])}")
        print(f"   🔧 Critical Fixes: {len(plan['ultimate_critical_fixes'])}")
        print(f"   📚 Documentation-Enhanced: {len(plan['ultimate_documentation_fixes'])}")
        
        # Success factors
        if final['success_factors']:
            print(f"\n✅ SUCCESS FACTORS:")
            for factor in final['success_factors']:
                print(f"   • {factor}")
        
        # Risk factors
        if final['risk_factors']:
            print(f"\n⚠️ RISK FACTORS:")
            for risk in final['risk_factors']:
                print(f"   • {risk}")
        
        # Necromancer recommendations
        print(f"\n💡 NECROMANCER RECOMMENDATIONS:")
        for i, rec in enumerate(final['necromancer_recommendations'], 1):
            print(f"   {i}. {rec}")
        
        # Immediate actions
        print(f"\n🎯 IMMEDIATE NEXT ACTIONS:")
        for i, action in enumerate(final['next_actions'], 1):
            print(f"   {i}. {action}")
        
        # Necromancer signature
        print(f"\n💀 PROJECT NECROMANCER ASSESSMENT COMPLETE")
        print(f"🚀 Ready to bring this project back from the dead!")
        print(f"⚡ May the power of cognitive triangulation be with you!")

# Ultimate test function
async def test_ultimate_necromancer():
    """Test the Ultimate Project Necromancer"""
    
    print("💀 TESTING ULTIMATE PROJECT NECROMANCER")
    print("=" * 70)
    
    # Initialize the ultimate system
    necromancer = UltimateProjectNecromancer()
    
    # Initialize all systems
    system_ready = await necromancer.initialize_necromancer()
    
    if system_ready:
        # Test on Bob's complex X-Agent pipeline for full GitHub intelligence test
        test_project = '/Users/bobdallavia/X-Agent-Pipeline'
        
        print(f"\n🎯 ULTIMATE NECROMANCER TEST TARGET:")
        print(f"📁 Project: {test_project}")
        print(f"🔬 Method: Triple-powered cognitive triangulation")
        
        # Run ultimate revival analysis
        assessment = await necromancer.revive_dead_project(
            test_project,
            deep_analysis=True,
            generate_fixes=True, 
            create_scripts=True
        )
        
        print(f"\n🎉 ULTIMATE NECROMANCER TEST COMPLETE!")
        print(f"💀 The necromancer has spoken - project revival assessment delivered!")
    
    else:
        print("❌ Ultimate Necromancer failed to initialize")

if __name__ == "__main__":
    asyncio.run(test_ultimate_necromancer())
