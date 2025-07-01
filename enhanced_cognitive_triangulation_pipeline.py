#!/usr/bin/env python3
"""
Enhanced Cognitive Triangulation Pipeline with Security Integration
Batch security analysis across multiple files with MCP tools
"""
import sys
import os
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Any

# Add paths
sys.path.append('/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation/cognitive_triangulation/agents')
sys.path.append('/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation/agent_performance_test')
sys.path.append('/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation/domain_plugins')

# Import enhanced agents
from security_code_detective_agent import SecurityCodeDetectiveAgent
from code_quality_detective_agent import CodeQualityDetectiveAgent

# Import domain detection system
from domain_plugins.registry import DomainRegistry
from domain_plugin_creator_agent import IntelligentDomainPluginCreator

class EnhancedCognitiveTriangulationPipeline:
    """
    Complete cognitive triangulation pipeline with security focus
    
    Pipeline Flow:
    1. Industry Domain Detection & Plugin Management
    2. File Discovery & Language Detection
    3. Security Analysis (SecurityCodeDetective + MCP tools)
    4. Quality Analysis (CodeQualityDetective) 
    5. Triangulated Confidence Scoring
    6. Comprehensive Risk Assessment
    """
    
    def __init__(self):
        # Initialize agents
        self.security_detective = SecurityCodeDetectiveAgent()
        self.quality_detective = CodeQualityDetectiveAgent()
        
        # Initialize domain detection system
        self.domain_registry = DomainRegistry()
        self.plugin_creator = IntelligentDomainPluginCreator()
        
        # Configuration
        self.domain_confidence_threshold = 0.7  # Higher threshold for better domain matching
        
        self.supported_extensions = {'.py', '.java', '.css', '.html', '.js', '.jsx', '.ts', '.tsx', '.json'}
        self.metrics = {
            'files_analyzed': 0,
            'security_issues_found': 0,
            'quality_issues_found': 0,
            'total_processing_time': 0.0,
            'high_risk_files': [],
            'secure_files': [],
            'detected_industry': None,
            'industry_confidence': 0.0,
            'plugin_created': False,
            'created_plugin_name': None
        }
        
        print("🧠 Enhanced Cognitive Triangulation Pipeline Initialized!")
        print(f"   🏭 Domain Detection: {len(self.domain_registry.list_domains())} industries loaded")
        print(f"   🤖 Plugin Creator: LLM-backed (confidence threshold: {self.domain_confidence_threshold})")
        print(f"   🔒 Security Detective: Ready")
        print(f"   🔍 Quality Detective: Ready")
        print(f"   📁 Supported Files: {', '.join(self.supported_extensions)}")
    
    async def analyze_project(self, project_path: str, include_security=True, include_quality=True):
        """Analyze entire project with cognitive triangulation"""
        
        print(f"\n🚀 ENHANCED COGNITIVE TRIANGULATION ANALYSIS")
        print(f"=" * 70)
        print(f"📁 Project: {project_path}")
        print(f"🔒 Security Analysis: {'✅ Enabled' if include_security else '❌ Disabled'}")
        print(f"🔍 Quality Analysis: {'✅ Enabled' if include_quality else '❌ Disabled'}")
        
        start_time = time.time()
        
        # Step 1: Discover files
        files = self._discover_analyzable_files(project_path)
        print(f"\n📊 Step 1: File Discovery")
        print(f"   📁 Found {len(files)} analyzable files")
        
        # Step 2: Industry Domain Detection
        print(f"\n🏭 Step 2: Industry Domain Detection")
        industry_domain, confidence = await self._detect_project_industry(files)
        self.metrics['detected_industry'] = industry_domain
        self.metrics['industry_confidence'] = confidence
        print(f"   🎯 Detected Industry: {industry_domain} (confidence: {confidence:.2f})")
        
        # Step 3: Batch analysis
        print(f"\n🔄 Step 3: Batch Analysis")
        analysis_results = []
        
        for i, file_path in enumerate(files, 1):
            print(f"   Analyzing {i}/{len(files)}: {Path(file_path).name}")
            
            file_result = await self._analyze_single_file(
                file_path, include_security, include_quality
            )
            analysis_results.append(file_result)
            
            # Update metrics
            self.metrics['files_analyzed'] += 1
            if file_result.get('security_score', 100) < 70:
                self.metrics['high_risk_files'].append(file_path)
            elif file_result.get('security_score', 100) == 100:
                self.metrics['secure_files'].append(file_path)
        
        # Step 4: Aggregate and report
        print(f"\n📊 Step 4: Project Aggregation")
        project_report = self._generate_project_security_report(analysis_results, project_path)
        
        # Update final metrics
        total_time = time.time() - start_time
        self.metrics['total_processing_time'] = total_time
        
        # Step 5: Display comprehensive results
        self._display_project_results(project_report)
        
        return project_report
    
    def _discover_analyzable_files(self, project_path: str) -> List[str]:
        """Discover files for analysis"""
        files = []
        
        # Skip common directories
        skip_dirs = {'__pycache__', '.git', 'node_modules', '.venv', 'venv', 'build', 'dist'}
        
        for root, dirs, filenames in os.walk(project_path):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for filename in filenames:
                file_path = Path(root) / filename
                
                if file_path.suffix.lower() in self.supported_extensions:
                    if file_path.stat().st_size < 5 * 1024 * 1024:  # < 5MB
                        files.append(str(file_path))
        
        return sorted(files)
    
    async def _analyze_single_file(self, file_path: str, include_security: bool, include_quality: bool) -> Dict[str, Any]:
        """Analyze single file with both detectives"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                'file_path': file_path,
                'error': str(e),
                'security_score': 0,
                'quality_score': 0
            }
        
        result = {
            'file_path': file_path,
            'file_size': len(content),
            'lines_of_code': len(content.splitlines())
        }
        
        # Security analysis
        if include_security:
            security_result = await self._run_security_analysis(file_path, content)
            result.update({
                'security_score': security_result.get('security_score', 100),
                'security_issues': security_result.get('total_findings', 0),
                'risk_level': security_result.get('risk_level', 'LOW'),
                'critical_security_issues': security_result.get('critical_findings', [])
            })
            self.metrics['security_issues_found'] += security_result.get('total_findings', 0)
        
        # Quality analysis
        if include_quality:
            quality_result = await self._run_quality_analysis(file_path, content)
            result.update({
                'quality_score': quality_result.get('quality_score', 100),
                'quality_issues': quality_result.get('total_issues', 0),
                'maintainability_issues': quality_result.get('issues', [])
            })
            self.metrics['quality_issues_found'] += quality_result.get('total_issues', 0)
        
        # Triangulated overall score
        if include_security and include_quality:
            result['overall_score'] = (result['security_score'] + result['quality_score']) / 2
        elif include_security:
            result['overall_score'] = result['security_score']
        elif include_quality:
            result['overall_score'] = result['quality_score']
        
        return result
    
    async def _run_security_analysis(self, file_path: str, content: str) -> Dict[str, Any]:
        """Run security analysis with SecurityCodeDetective"""
        
        import html
        escaped_content = html.escape(content)
        
        xml_input = f'''<code_analysis_request>
            <file_path>{file_path}</file_path>
            <file_content>{escaped_content}</file_content>
            <language>python</language>
        </code_analysis_request>'''
        
        result_xml = self.security_detective.process(xml_input)
        
        # Parse XML result
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(result_xml)
            summary = root.find('summary')
            
            if summary is not None:
                return {
                    'total_findings': int(summary.find('total_findings').text),
                    'security_score': int(summary.find('security_score').text),
                    'risk_level': summary.find('risk_level').text,
                    'critical_findings': [
                        {
                            'line': int(f.find('line').text),
                            'description': f.find('description').text,
                            'fix': f.find('fix').text
                        }
                        for f in root.findall('.//critical_findings/finding')
                    ]
                }
        except Exception as e:
            print(f"   ⚠️ Security analysis parsing error: {e}")
        
        return {'total_findings': 0, 'security_score': 100, 'risk_level': 'LOW'}
    
    async def _run_quality_analysis(self, file_path: str, content: str) -> Dict[str, Any]:
        """Run quality analysis with CodeQualityDetective"""
        
        import html
        escaped_content = html.escape(content)
        
        xml_input = f'''<code_analysis_request>
            <file_path>{file_path}</file_path>
            <file_content>{escaped_content}</file_content>
            <language>python</language>
        </code_analysis_request>'''
        
        result_xml = self.quality_detective.process(xml_input)
        
        # Parse XML result
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(result_xml)
            summary = root.find('summary')
            
            if summary is not None:
                return {
                    'total_issues': int(summary.find('total_issues').text),
                    'quality_score': int(summary.find('quality_score').text),
                    'issues': [
                        {
                            'line': int(i.find('line_number').text),
                            'description': i.find('description').text,
                            'fix': i.find('fix_suggestion').text
                        }
                        for i in root.findall('.//top_issues/issue')[:5]  # Top 5
                    ]
                }
        except Exception as e:
            print(f"   ⚠️ Quality analysis parsing error: {e}")
        
        return {'total_issues': 0, 'quality_score': 100}
    
    def _generate_project_security_report(self, analysis_results: List[Dict], project_path: str) -> Dict[str, Any]:
        """Generate comprehensive project security report"""
        
        total_files = len(analysis_results)
        total_security_issues = sum(r.get('security_issues', 0) for r in analysis_results)
        total_quality_issues = sum(r.get('quality_issues', 0) for r in analysis_results)
        
        avg_security_score = sum(r.get('security_score', 100) for r in analysis_results) / total_files if total_files > 0 else 100
        avg_quality_score = sum(r.get('quality_score', 100) for r in analysis_results) / total_files if total_files > 0 else 100
        avg_overall_score = sum(r.get('overall_score', 100) for r in analysis_results) / total_files
        
        # Risk categorization
        high_risk_files = [r for r in analysis_results if r.get('security_score', 100) < 50]
        medium_risk_files = [r for r in analysis_results if 50 <= r.get('security_score', 100) < 80]
        low_risk_files = [r for r in analysis_results if r.get('security_score', 100) >= 80]
        
        return {
            'project_path': project_path,
            'analysis_summary': {
                'total_files': total_files,
                'total_security_issues': total_security_issues,
                'total_quality_issues': total_quality_issues,
                'avg_security_score': round(avg_security_score, 1),
                'avg_quality_score': round(avg_quality_score, 1),
                'avg_overall_score': round(avg_overall_score, 1)
            },
            'risk_breakdown': {
                'high_risk': len(high_risk_files),
                'medium_risk': len(medium_risk_files),
                'low_risk': len(low_risk_files)
            },
            'top_security_issues': [
                r for r in analysis_results 
                if r.get('critical_security_issues') 
                and len(r.get('critical_security_issues', [])) > 0
            ][:10],
            'analysis_results': analysis_results,
            'metrics': self.metrics
        }
    
    def _display_project_results(self, report: Dict[str, Any]):
        """Display comprehensive project results"""
        
        summary = report['analysis_summary']
        risk = report['risk_breakdown']
        
        print(f"\n" + "=" * 70)
        print(f"🎉 ENHANCED COGNITIVE TRIANGULATION COMPLETE!")
        print(f"=" * 70)
        
        print(f"\n📊 PROJECT ANALYSIS SUMMARY:")
        print(f"   📁 Files Analyzed: {summary['total_files']}")
        print(f"   🔒 Security Issues: {summary['total_security_issues']}")
        print(f"   🔍 Quality Issues: {summary['total_quality_issues']}")
        print(f"   🏆 Average Security Score: {summary['avg_security_score']}/100")
        print(f"   🏆 Average Quality Score: {summary['avg_quality_score']}/100")
        print(f"   🏆 Overall Project Score: {summary['avg_overall_score']}/100")
        
        print(f"\n🚨 RISK BREAKDOWN:")
        print(f"   🔴 High Risk Files: {risk['high_risk']}")
        print(f"   🟡 Medium Risk Files: {risk['medium_risk']}")
        print(f"   🟢 Low Risk Files: {risk['low_risk']}")
        
        if report['top_security_issues']:
            print(f"\n🚨 TOP SECURITY CONCERNS:")
            for i, issue_file in enumerate(report['top_security_issues'][:5], 1):
                file_name = Path(issue_file['file_path']).name
                security_score = issue_file.get('security_score', 100)
                issues_count = len(issue_file.get('critical_security_issues', []))
                print(f"   {i}. {file_name} (Score: {security_score}/100, {issues_count} critical issues)")
        
        print(f"\n⏱️ Performance Metrics:")
        print(f"   🕐 Total Time: {self.metrics['total_processing_time']:.2f} seconds")
        print(f"   ⚡ Files/Second: {self.metrics['files_analyzed'] / self.metrics['total_processing_time']:.1f}")
        print(f"   🔒 Secure Files: {len(self.metrics['secure_files'])}")
        print(f"   ⚠️ High Risk Files: {len(self.metrics['high_risk_files'])}")
        
        print(f"\n🏭 Domain Intelligence:")
        print(f"   🎯 Detected Industry: {self.metrics['detected_industry']} (confidence: {self.metrics['industry_confidence']:.2f})")
        if self.metrics['plugin_created']:
            print(f"   🤖 Created Plugin: {self.metrics['created_plugin_name']} (LLM-generated)")
        else:
            print(f"   🔄 Plugin Creation: Not needed (existing plugins sufficient)")

    async def _detect_project_industry(self, file_paths: List[str]) -> tuple:
        """Detect project industry domain from file contents with intelligent plugin creation"""
        try:
            # Step 1: Aggregate content from key files for domain detection
            content_for_detection = ""
            
            # Sample up to 10 files to avoid overwhelming the detection
            sample_files = file_paths[:10] if len(file_paths) > 10 else file_paths
            
            for file_path in sample_files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        # Read first 1000 chars from each file
                        file_content = f.read(1000)
                        content_for_detection += f"\n{file_content}"
                except Exception as e:
                    print(f"      ⚠️ Could not read {Path(file_path).name}: {e}")
                    continue
            
            if not content_for_detection.strip():
                return 'general', 0.0
                
            # Step 2: Use domain registry to detect industry
            industry, confidence = self.domain_registry.detect_domain(content_for_detection)
            print(f"   📊 Initial Detection: {industry} (confidence: {confidence:.2f})")
            
            # Step 3: Check if confidence is below threshold - trigger plugin creator
            if confidence < self.domain_confidence_threshold:
                print(f"   🤖 Confidence {confidence:.2f} < {self.domain_confidence_threshold} - Triggering LLM Plugin Creator...")
                
                try:
                    # Use the IntelligentDomainPluginCreator to analyze and potentially create a new plugin
                    creation_result = await self.plugin_creator.analyze_and_create_if_needed(
                        content_for_detection, 
                        domain_hint=industry
                    )
                    
                    if creation_result['success']:
                        if creation_result.get('action') == 'new_domain_created':
                            print(f"   ✅ Created new domain plugin: {creation_result['domain_name']}")
                            self.metrics['plugin_created'] = True
                            self.metrics['created_plugin_name'] = creation_result['domain_name']
                            
                            # Reload domain registry to include new plugin
                            self.domain_registry = DomainRegistry()
                            
                            # Re-detect with new plugin
                            new_industry, new_confidence = self.domain_registry.detect_domain(content_for_detection)
                            print(f"   🔄 Re-detection with new plugin: {new_industry} (confidence: {new_confidence:.2f})")
                            return new_industry, new_confidence
                            
                        elif creation_result.get('action') == 'existing_domain_used':
                            print(f"   ℹ️ Using existing domain: {creation_result['domain_name']}")
                            return creation_result['domain_name'], creation_result['confidence']
                    else:
                        print(f"   ⚠️ Plugin creation failed: {creation_result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    print(f"   ❌ Plugin creator error: {e}")
            
            # Return original detection if plugin creation wasn't needed or failed
            return industry, confidence
                
        except Exception as e:
            print(f"      ❌ Industry detection failed: {e}")
            return 'general', 0.0

async def main():
    """Test the enhanced cognitive triangulation pipeline"""
    
    pipeline = EnhancedCognitiveTriangulationPipeline()
    
    # Get target project from command line or use default
    import sys
    target_project = sys.argv[1] if len(sys.argv) > 1 else '/Users/bobdallavia/MediVault'
    
    print(f"🎯 Testing Enhanced Cognitive Triangulation on: {target_project}")
    
    report = await pipeline.analyze_project(
        target_project, 
        include_security=True, 
        include_quality=True
    )
    
    print(f"\n🎉 Enhanced Cognitive Triangulation Analysis Complete!")

if __name__ == "__main__":
    asyncio.run(main())
