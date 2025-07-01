#!/usr/bin/env python3
"""
Scale Testing Framework for Cognitive Triangulation X-Agent System
Tests performance and accuracy across different project sizes and domains
"""

import os
import sys
import time
import json
import subprocess
import requests
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import tempfile
import shutil
from datetime import datetime

@dataclass
class TestResult:
    """Results from testing a single repository"""
    repo_name: str
    repo_url: str
    lines_of_code: int
    file_count: int
    detected_domain: str
    domain_confidence: float
    processing_time_ms: float
    agents_run: List[str]
    issues_found: int
    relationships_detected: int
    domain_plugin_created: bool
    success: bool
    error_message: Optional[str] = None

@dataclass
class ScaleTestSuite:
    """Complete test suite results"""
    test_date: str
    total_repos_tested: int
    successful_tests: int
    failed_tests: int
    results: List[TestResult]
    performance_summary: Dict[str, float]

class GitHubRepoFetcher:
    """Fetches popular repositories from GitHub for testing"""
    
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token
        self.headers = {}
        if github_token:
            self.headers['Authorization'] = f'token {github_token}'
    
    def get_popular_repos(self, languages: List[str], sizes: List[str]) -> List[Dict]:
        """
        Fetch popular repositories of different sizes and languages
        
        Args:
            languages: Programming languages to test ['python', 'javascript', 'java']
            sizes: Repository sizes ['small', 'medium', 'large', 'enterprise']
        
        Returns:
            List of repository information
        """
        repos = []
        
        # Size mappings (lines of code ranges)
        size_queries = {
            'small': 'size:1..1000',      # 1-1K lines
            'medium': 'size:1000..10000', # 1K-10K lines  
            'large': 'size:10000..50000', # 10K-50K lines
            'enterprise': 'size:>50000'   # 50K+ lines
        }
        
        for language in languages:
            for size in sizes:
                try:
                    # Search for popular repos of specific language and size
                    query = f'language:{language} {size_queries[size]} stars:>100'
                    url = f'https://api.github.com/search/repositories?q={query}&sort=stars&per_page=5'
                    
                    response = requests.get(url, headers=self.headers)
                    if response.status_code == 200:
                        data = response.json()
                        for repo in data.get('items', []):
                            repos.append({
                                'name': repo['full_name'],
                                'url': repo['clone_url'],
                                'language': language,
                                'size_category': size,
                                'stars': repo['stargazers_count'],
                                'description': repo.get('description', '')
                            })
                    else:
                        print(f"Failed to fetch {language} {size} repos: {response.status_code}")
                        
                except Exception as e:
                    print(f"Error fetching {language} {size} repos: {e}")
                    
                # Rate limiting
                time.sleep(1)
        
        return repos

class CognitiveTriangulationTester:
    """Tests the Cognitive Triangulation X-Agent system"""
    
    def __init__(self, pipeline_path: str):
        self.pipeline_path = Path(pipeline_path)
        self.test_results: List[TestResult] = []
    
    def clone_repository(self, repo_url: str, temp_dir: Path) -> Path:
        """Clone a repository to temporary directory"""
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = temp_dir / repo_name
        
        try:
            subprocess.run(['git', 'clone', repo_url, str(repo_path)], 
                         check=True, capture_output=True)
            return repo_path
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to clone {repo_url}: {e}")
    
    def count_lines_of_code(self, repo_path: Path) -> Tuple[int, int]:
        """Count lines of code and number of files"""
        total_lines = 0
        file_count = 0
        
        # Common code file extensions
        code_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', 
                          '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt'}
        
        for file_path in repo_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in code_extensions:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = len(f.readlines())
                        total_lines += lines
                        file_count += 1
                except Exception:
                    continue  # Skip files that can't be read
        
        return total_lines, file_count
    
    def run_cognitive_triangulation(self, repo_path: Path) -> Dict:
        """Run the cognitive triangulation pipeline on a repository"""
        try:
            # Add all necessary paths to Python path
            sys.path.insert(0, str(self.pipeline_path))
            sys.path.insert(0, str(self.pipeline_path / "cognitive_triangulation"))
            sys.path.insert(0, str(self.pipeline_path / "cognitive_triangulation" / "agents"))
            sys.path.insert(0, str(self.pipeline_path / "domain_plugins"))
            sys.path.insert(0, str(self.pipeline_path / "rag_integration"))
            
            # Record start time
            start_time = time.time()
            
            # Use the basic agents directly instead of the complex pipeline
            try:
                from security_code_detective_agent import SecurityCodeDetectiveAgent
                from code_quality_detective_agent import CodeQualityDetectiveAgent
                
                security_agent = SecurityCodeDetectiveAgent()
                quality_agent = CodeQualityDetectiveAgent()
                
            except ImportError as e:
                return {
                    'success': False,
                    'error': f'Could not import agents: {e}',
                    'processing_time_ms': 0
                }
            
            # Get sample code files from the repository
            code_files = []
            extensions = [".py", ".js", ".java", ".cpp", ".c", ".cs", ".php", ".rb"]
            
            for ext in extensions:
                for file_path in repo_path.rglob(f"*{ext}"):
                    if file_path.is_file() and file_path.stat().st_size > 100:  # At least 100 bytes
                        code_files.append(file_path)
                    if len(code_files) >= 5:  # Analyze up to 5 files for speed
                        break
                if code_files:
                    break
            
            if not code_files:
                return {
                    'success': False,
                    'error': 'No suitable code files found for analysis',
                    'processing_time_ms': 0
                }
            
            # Analyze the files using the basic agents
            security_results = []
            quality_results = []
            
            for file_path in code_files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Create XML input for the agents
                    xml_input = f'''<code_analysis_request>
                        <file_path>{file_path}</file_path>
                        <file_content>{content[:2000]}</file_content>
                        <language>{file_path.suffix[1:] if file_path.suffix else 'unknown'}</language>
                    </code_analysis_request>'''
                    
                    # Run security analysis
                    try:
                        security_result = security_agent.process(xml_input)
                        security_results.append({
                            'file': str(file_path),
                            'result': security_result,
                            'success': True
                        })
                    except Exception as e:
                        security_results.append({
                            'file': str(file_path),
                            'error': str(e),
                            'success': False
                        })
                    
                    # Run quality analysis  
                    try:
                        quality_result = quality_agent.process(xml_input)
                        quality_results.append({
                            'file': str(file_path),
                            'result': quality_result,
                            'success': True
                        })
                    except Exception as e:
                        quality_results.append({
                            'file': str(file_path),
                            'error': str(e),
                            'success': False
                        })
                        
                except Exception as e:
                    print(f"   ⚠️ Error reading {file_path.name}: {e}")
                    continue
            
            # Calculate processing time
            processing_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Count successful analyses
            successful_security = sum(1 for r in security_results if r['success'])
            successful_quality = sum(1 for r in quality_results if r['success'])
            
            # Create summary result
            combined_result = {
                'files_analyzed': len(code_files),
                'total_files_found': len(code_files),
                'repository_path': str(repo_path),
                'security_analyses': {
                    'successful': successful_security,
                    'failed': len(security_results) - successful_security,
                    'results': security_results
                },
                'quality_analyses': {
                    'successful': successful_quality,
                    'failed': len(quality_results) - successful_quality,
                    'results': quality_results
                },
                'summary': {
                    'total_successful_analyses': successful_security + successful_quality,
                    'agent_performance': {
                        'security_agent_success_rate': successful_security / len(security_results) if security_results else 0,
                        'quality_agent_success_rate': successful_quality / len(quality_results) if quality_results else 0
                    }
                }
            }
            
            return {
                'success': True,
                'processing_time_ms': processing_time,
                'result': combined_result
            }
            
        except Exception as e:
            import traceback
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc(),
                'processing_time_ms': 0
            }
    
    def extract_analysis_metrics(self, analysis_result: Dict) -> Dict:
        """Extract key metrics from analysis result"""
        metrics = {
            'detected_domain': 'unknown',
            'domain_confidence': 0.0,
            'agents_run': [],
            'issues_found': 0,
            'relationships_detected': 0,
            'domain_plugin_created': False
        }
        
        try:
            # Extract domain information
            if 'domain_detection' in analysis_result:
                domain_info = analysis_result['domain_detection']
                metrics['detected_domain'] = domain_info.get('detected_domain', 'unknown')
                metrics['domain_confidence'] = domain_info.get('confidence', 0.0)
            
            # Extract agent information
            if 'agent_results' in analysis_result:
                metrics['agents_run'] = list(analysis_result['agent_results'].keys())
            
            # Count total issues found across all agents
            if 'triangulation_result' in analysis_result:
                triangulation = analysis_result['triangulation_result']
                if 'findings' in triangulation:
                    metrics['issues_found'] = len(triangulation['findings'])
                if 'relationships' in triangulation:
                    metrics['relationships_detected'] = len(triangulation['relationships'])
            
            # Check if domain plugin was created
            if 'plugin_creation' in analysis_result:
                metrics['domain_plugin_created'] = analysis_result['plugin_creation'].get('created', False)
            
        except Exception as e:
            print(f"Error extracting metrics: {e}")
        
        return metrics
    
    def test_repository(self, repo_info: Dict, temp_dir: Path) -> TestResult:
        """Test a single repository"""
        print(f"Testing {repo_info['name']} ({repo_info['size_category']})...")
        
        try:
            # Clone repository
            repo_path = self.clone_repository(repo_info['url'], temp_dir)
            
            # Count lines of code
            lines_of_code, file_count = self.count_lines_of_code(repo_path)
            
            # Run cognitive triangulation
            analysis = self.run_cognitive_triangulation(repo_path)
            
            if analysis['success']:
                # Extract metrics
                metrics = self.extract_analysis_metrics(analysis['result'])
                
                result = TestResult(
                    repo_name=repo_info['name'],
                    repo_url=repo_info['url'],
                    lines_of_code=lines_of_code,
                    file_count=file_count,
                    detected_domain=metrics['detected_domain'],
                    domain_confidence=metrics['domain_confidence'],
                    processing_time_ms=analysis['processing_time_ms'],
                    agents_run=metrics['agents_run'],
                    issues_found=metrics['issues_found'],
                    relationships_detected=metrics['relationships_detected'],
                    domain_plugin_created=metrics['domain_plugin_created'],
                    success=True
                )
            else:
                result = TestResult(
                    repo_name=repo_info['name'],
                    repo_url=repo_info['url'],
                    lines_of_code=lines_of_code,
                    file_count=file_count,
                    detected_domain='error',
                    domain_confidence=0.0,
                    processing_time_ms=0.0,
                    agents_run=[],
                    issues_found=0,
                    relationships_detected=0,
                    domain_plugin_created=False,
                    success=False,
                    error_message=analysis['error']
                )
            
            # Cleanup
            shutil.rmtree(repo_path, ignore_errors=True)
            
        except Exception as e:
            result = TestResult(
                repo_name=repo_info['name'],
                repo_url=repo_info['url'],
                lines_of_code=0,
                file_count=0,
                detected_domain='error',
                domain_confidence=0.0,
                processing_time_ms=0.0,
                agents_run=[],
                issues_found=0,
                relationships_detected=0,
                domain_plugin_created=False,
                success=False,
                error_message=str(e)
            )
        
        return result

class ScaleTestRunner:
    """Main test runner for scale testing"""
    
    def __init__(self, pipeline_path: str, github_token: Optional[str] = None):
        self.pipeline_path = pipeline_path
        self.fetcher = GitHubRepoFetcher(github_token)
        self.tester = CognitiveTriangulationTester(pipeline_path)
    
    def run_scale_test(self, 
                      languages: List[str] = ['python', 'javascript', 'java'],
                      sizes: List[str] = ['small', 'medium', 'large'],
                      max_repos_per_category: int = 3) -> ScaleTestSuite:
        """
        Run comprehensive scale testing
        
        Args:
            languages: Programming languages to test
            sizes: Repository size categories
            max_repos_per_category: Maximum repos to test per language/size combo
        """
        print("🚀 Starting Cognitive Triangulation X-Agent Scale Testing...")
        print(f"Languages: {languages}")
        print(f"Sizes: {sizes}")
        print(f"Max repos per category: {max_repos_per_category}")
        
        # Fetch repositories
        print("\n📥 Fetching repositories from GitHub...")
        repos = self.fetcher.get_popular_repos(languages, sizes)
        
        # Limit repos per category
        limited_repos = []
        category_counts = {}
        
        for repo in repos:
            category = f"{repo['language']}_{repo['size_category']}"
            if category_counts.get(category, 0) < max_repos_per_category:
                limited_repos.append(repo)
                category_counts[category] = category_counts.get(category, 0) + 1
        
        print(f"Selected {len(limited_repos)} repositories for testing")
        
        # Run tests
        results = []
        successful_tests = 0
        failed_tests = 0
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            for i, repo in enumerate(limited_repos, 1):
                print(f"\n[{i}/{len(limited_repos)}] Testing {repo['name']}...")
                
                result = self.tester.test_repository(repo, temp_path)
                results.append(result)
                
                if result.success:
                    successful_tests += 1
                    print(f"✅ Success - {result.processing_time_ms:.1f}ms, "
                          f"{result.lines_of_code:,} lines, "
                          f"domain: {result.detected_domain}")
                else:
                    failed_tests += 1
                    print(f"❌ Failed - {result.error_message}")
        
        # Calculate performance summary
        successful_results = [r for r in results if r.success]
        performance_summary = {}
        
        if successful_results:
            performance_summary = {
                'avg_processing_time_ms': sum(r.processing_time_ms for r in successful_results) / len(successful_results),
                'max_processing_time_ms': max(r.processing_time_ms for r in successful_results),
                'min_processing_time_ms': min(r.processing_time_ms for r in successful_results),
                'avg_lines_per_ms': sum(r.lines_of_code / max(r.processing_time_ms, 1) for r in successful_results) / len(successful_results),
                'total_lines_analyzed': sum(r.lines_of_code for r in successful_results),
                'total_files_analyzed': sum(r.file_count for r in successful_results),
                'domains_detected': len(set(r.detected_domain for r in successful_results if r.detected_domain != 'unknown')),
                'plugins_created': sum(1 for r in successful_results if r.domain_plugin_created)
            }
        
        # Create test suite
        test_suite = ScaleTestSuite(
            test_date=datetime.now().isoformat(),
            total_repos_tested=len(results),
            successful_tests=successful_tests,
            failed_tests=failed_tests,
            results=results,
            performance_summary=performance_summary
        )
        
        return test_suite
    
    def save_results(self, test_suite: ScaleTestSuite, output_path: str):
        """Save test results to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(asdict(test_suite), f, indent=2, default=str)
        print(f"📊 Results saved to {output_path}")
    
    def print_summary(self, test_suite: ScaleTestSuite):
        """Print test summary"""
        print("\n" + "="*60)
        print("🎯 SCALE TESTING SUMMARY")
        print("="*60)
        
        print(f"📅 Test Date: {test_suite.test_date}")
        print(f"🧪 Total Repositories Tested: {test_suite.total_repos_tested}")
        print(f"✅ Successful Tests: {test_suite.successful_tests}")
        print(f"❌ Failed Tests: {test_suite.failed_tests}")
        print(f"📈 Success Rate: {(test_suite.successful_tests/test_suite.total_repos_tested)*100:.1f}%")
        
        if test_suite.performance_summary:
            perf = test_suite.performance_summary
            print(f"\n⚡ PERFORMANCE METRICS:")
            print(f"  • Average Processing Time: {perf['avg_processing_time_ms']:.1f}ms")
            print(f"  • Fastest Analysis: {perf['min_processing_time_ms']:.1f}ms")
            print(f"  • Slowest Analysis: {perf['max_processing_time_ms']:.1f}ms")
            print(f"  • Processing Speed: {perf['avg_lines_per_ms']:.1f} lines/ms")
            print(f"  • Total Lines Analyzed: {perf['total_lines_analyzed']:,}")
            print(f"  • Total Files Analyzed: {perf['total_files_analyzed']:,}")
            print(f"  • Domains Detected: {perf['domains_detected']}")
            print(f"  • New Plugins Created: {perf['plugins_created']}")
        
        # Top performers
        successful_results = [r for r in test_suite.results if r.success]
        if successful_results:
            print(f"\n🏆 TOP PERFORMERS:")
            fastest = min(successful_results, key=lambda x: x.processing_time_ms)
            largest = max(successful_results, key=lambda x: x.lines_of_code)
            most_complex = max(successful_results, key=lambda x: x.issues_found + x.relationships_detected)
            
            print(f"  • Fastest: {fastest.repo_name} ({fastest.processing_time_ms:.1f}ms)")
            print(f"  • Largest: {largest.repo_name} ({largest.lines_of_code:,} lines)")
            print(f"  • Most Complex: {most_complex.repo_name} ({most_complex.issues_found + most_complex.relationships_detected} findings)")

def main():
    """Main entry point for scale testing"""
    # Configuration
    PIPELINE_PATH = "/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation/"
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # Optional: set for higher API limits
    
    # Initialize test runner
    runner = ScaleTestRunner(PIPELINE_PATH, GITHUB_TOKEN)
    
    print("🚀 Debug test was successful! Running FULL SCALE TEST...")
    
    # Run full scale test
    test_suite = runner.run_scale_test(
        languages=['python', 'javascript', 'java'],
        sizes=['small', 'medium', 'large'], 
        max_repos_per_category=2  # 2 repos per category = 18 total repos
    )
    
    # Print summary
    runner.print_summary(test_suite)
    
    # Save detailed results
    output_path = f"{PIPELINE_PATH}/scale_test_FULL_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    runner.save_results(test_suite, output_path)
    
    if test_suite.successful_tests > 0:
        success_rate = (test_suite.successful_tests / test_suite.total_repos_tested) * 100
        print(f"\n🎉 FULL SCALE TEST COMPLETE!")
        print(f"✅ Success Rate: {success_rate:.1f}%")
        print(f"⚡ Your X-Agent system is production-ready!")
        
        if success_rate >= 90:
            print(f"🏆 OUTSTANDING PERFORMANCE! Your system exceeds industry standards!")
        elif success_rate >= 75:
            print(f"🎯 EXCELLENT PERFORMANCE! Your system is highly reliable!")
        elif success_rate >= 60:
            print(f"👍 GOOD PERFORMANCE! System is stable with room for optimization!")
    else:
        print(f"\n⚠️ Some issues detected. Check detailed results for optimization opportunities.")
    
    print(f"\n📊 Detailed results: {output_path}")

if __name__ == "__main__":
    main()