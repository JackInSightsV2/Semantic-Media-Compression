#!/usr/bin/env python3
"""
Master Test Runner for Core Technical Testing Framework
Provides CLI interface with argparse supporting --test {01,02,03,04,all}, 
--budget override, --models selection, --report generation, --dry-run
"""

import os
import sys
import json
import time
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Add framework to path
sys.path.append(str(Path(__file__).parent / "01-core-technical"))

from framework.data.config_loader import load_config
from framework.data.result_storage import ResultStorage
from framework.reporting.report_generator import ReportGenerator

# Import individual test runners
from scripts.run_test_01 import Test01Runner
from scripts.run_test_02 import Test02Runner
from scripts.run_test_03 import Test03Runner
from scripts.run_test_04 import Test04Runner

@dataclass
class TestExecutionSummary:
    """Summary of test execution results"""
    test_id: str
    status: str  # 'success', 'failed', 'skipped'
    execution_time: float
    cost: float
    error_message: Optional[str] = None
    results_path: Optional[str] = None

@dataclass
class MasterTestResults:
    """Results from master test execution"""
    execution_timestamp: str
    total_execution_time: float
    total_cost: float
    budget_limit: float
    tests_executed: List[TestExecutionSummary]
    overall_status: str
    configuration_used: Dict[str, Any]

class TestController:
    """Main test controller orchestrating execution with progress monitoring, 
    cost tracking, and real-time status updates"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize test controller"""
        self.config = load_config(config_path)
        self.result_storage = ResultStorage()
        self.report_generator = ReportGenerator()
        
        # Cost tracking
        self.total_cost = 0.0
        self.cost_lock = threading.Lock()
        
        # Test runners
        self.test_runners = {
            '01': Test01Runner,
            '02': Test02Runner,
            '03': Test03Runner,
            '04': Test04Runner
        }
        
        # Setup logging
        self._setup_logging()
        
        # Execution state
        self.execution_start_time = None
        self.current_tests = {}
        
    def _setup_logging(self):
        """Setup logging for test controller"""
        log_dir = Path("TESTS/01-core-technical/results")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"master_test_runner_{int(time.time())}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def validate_setup(self) -> bool:
        """Validate setup without running tests (dry-run mode)"""
        self.logger.info("🔍 Validating test setup...")
        
        validation_results = {
            'configuration': False,
            'api_keys': False,
            'video_files': False,
            'ground_truth_data': False,
            'estimated_costs': {}
        }
        
        try:
            # Validate configuration
            self.logger.info("Checking configuration...")
            if self.config:
                validation_results['configuration'] = True
                self.logger.info("✅ Configuration loaded successfully")
            else:
                self.logger.error("❌ Configuration failed to load")
                return False
            
            # Validate API keys
            self.logger.info("Checking API keys...")
            api_keys_present = []
            if hasattr(self.config, 'openai_api_key') and self.config.openai_api_key:
                api_keys_present.append('OpenAI')
            if hasattr(self.config, 'anthropic_api_key') and self.config.anthropic_api_key:
                api_keys_present.append('Anthropic')
            if hasattr(self.config, 'elevenlabs_api_key') and self.config.elevenlabs_api_key:
                api_keys_present.append('ElevenLabs')
            
            if api_keys_present:
                validation_results['api_keys'] = True
                self.logger.info(f"✅ API keys available: {', '.join(api_keys_present)}")
            else:
                self.logger.warning("⚠️  No API keys configured - some tests may fail")
            
            # Validate video files
            self.logger.info("Checking video files...")
            video_folder = Path(getattr(self.config, 'video_folder', 'video'))
            if video_folder.exists():
                video_files = list(video_folder.glob('*.mp4')) + list(video_folder.glob('*.avi'))
                if video_files:
                    validation_results['video_files'] = True
                    self.logger.info(f"✅ Found {len(video_files)} video files")
                else:
                    self.logger.warning("⚠️  No video files found in video folder")
            else:
                self.logger.warning(f"⚠️  Video folder not found: {video_folder}")
            
            # Validate ground truth data
            self.logger.info("Checking ground truth data...")
            ground_truth_dir = Path("TESTS/01-core-technical/test-data/ground-truth")
            if ground_truth_dir.exists():
                validation_results['ground_truth_data'] = True
                self.logger.info("✅ Ground truth data directory exists")
            else:
                self.logger.warning("⚠️  Ground truth data directory not found")
            
            # Estimate costs
            self.logger.info("Estimating test costs...")
            cost_estimates = self._estimate_test_costs()
            validation_results['estimated_costs'] = cost_estimates
            
            total_estimated_cost = sum(cost_estimates.values())
            self.logger.info(f"💰 Total estimated cost: £{total_estimated_cost:.2f}")
            
            for test_id, cost in cost_estimates.items():
                self.logger.info(f"  - Test {test_id}: £{cost:.2f}")
            
            # Overall validation result
            critical_validations = [
                validation_results['configuration'],
                validation_results['api_keys']
            ]
            
            if all(critical_validations):
                self.logger.info("✅ Setup validation PASSED - ready to run tests")
                return True
            else:
                self.logger.error("❌ Setup validation FAILED - check configuration")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Setup validation failed with error: {e}")
            return False
    
    def _estimate_test_costs(self) -> Dict[str, float]:
        """Estimate costs for each test"""
        # Cost estimates based on test specifications
        return {
            '01': 30.0,  # £20 GPT-4 + £10 Claude for 5 videos
            '02': 25.0,  # JSON generation costs
            '03': 50.0,  # Content regeneration costs
            '04': 40.0   # Code extraction and regeneration costs
        }
    
    def execute_test_suite(self, test_ids: List[str], budget_limit: float, 
                          models_to_test: Optional[List[str]] = None,
                          parallel: bool = False) -> MasterTestResults:
        """
        Execute specified test suite with progress monitoring and cost tracking
        
        Args:
            test_ids: List of test IDs to execute ('01', '02', '03', '04')
            budget_limit: Maximum budget for all tests
            models_to_test: Optional list of models to test
            parallel: Whether to run tests in parallel (where safe)
            
        Returns:
            MasterTestResults: Comprehensive execution results
        """
        self.execution_start_time = time.time()
        self.total_cost = 0.0
        
        self.logger.info("🚀 Starting test suite execution...")
        self.logger.info(f"Tests to execute: {', '.join(test_ids)}")
        self.logger.info(f"Budget limit: £{budget_limit:.2f}")
        if models_to_test:
            self.logger.info(f"Models to test: {', '.join(models_to_test)}")
        
        # Initialize results
        results = MasterTestResults(
            execution_timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            total_execution_time=0.0,
            total_cost=0.0,
            budget_limit=budget_limit,
            tests_executed=[],
            overall_status='running',
            configuration_used=self._get_config_summary()
        )
        
        try:
            if parallel and len(test_ids) > 1:
                # Execute tests in parallel (with dependencies handled)
                test_summaries = self._execute_tests_parallel(
                    test_ids, budget_limit, models_to_test
                )
            else:
                # Execute tests sequentially
                test_summaries = self._execute_tests_sequential(
                    test_ids, budget_limit, models_to_test
                )
            
            results.tests_executed = test_summaries
            results.total_execution_time = time.time() - self.execution_start_time
            results.total_cost = self.total_cost
            
            # Determine overall status
            failed_tests = [t for t in test_summaries if t.status == 'failed']
            if failed_tests:
                results.overall_status = 'partial_success' if len(failed_tests) < len(test_summaries) else 'failed'
            else:
                results.overall_status = 'success'
            
            # Store master results
            self._store_master_results(results)
            
            self.logger.info("✅ Test suite execution completed")
            self._print_execution_summary(results)
            
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Test suite execution failed: {e}")
            results.overall_status = 'failed'
            results.total_execution_time = time.time() - self.execution_start_time
            results.total_cost = self.total_cost
            raise
    
    def _execute_tests_sequential(self, test_ids: List[str], budget_limit: float,
                                models_to_test: Optional[List[str]]) -> List[TestExecutionSummary]:
        """Execute tests sequentially with dependency handling"""
        test_summaries = []
        remaining_budget = budget_limit
        
        for test_id in test_ids:
            if remaining_budget <= 0:
                self.logger.warning(f"⚠️  Budget exhausted, skipping Test {test_id}")
                test_summaries.append(TestExecutionSummary(
                    test_id=test_id,
                    status='skipped',
                    execution_time=0.0,
                    cost=0.0,
                    error_message='Budget exhausted'
                ))
                continue
            
            try:
                self.logger.info(f"🔄 Executing Test {test_id}...")
                
                # Check dependencies
                if not self._check_test_dependencies(test_id, test_summaries):
                    self.logger.warning(f"⚠️  Dependencies not met for Test {test_id}, skipping")
                    test_summaries.append(TestExecutionSummary(
                        test_id=test_id,
                        status='skipped',
                        execution_time=0.0,
                        cost=0.0,
                        error_message='Dependencies not met'
                    ))
                    continue
                
                # Execute test
                summary = self._execute_single_test(
                    test_id, remaining_budget, models_to_test
                )
                test_summaries.append(summary)
                
                # Update budget and cost tracking
                with self.cost_lock:
                    self.total_cost += summary.cost
                    remaining_budget -= summary.cost
                
                if summary.status == 'success':
                    self.logger.info(f"✅ Test {test_id} completed successfully")
                else:
                    self.logger.error(f"❌ Test {test_id} failed: {summary.error_message}")
                
            except Exception as e:
                self.logger.error(f"❌ Test {test_id} execution failed: {e}")
                test_summaries.append(TestExecutionSummary(
                    test_id=test_id,
                    status='failed',
                    execution_time=0.0,
                    cost=0.0,
                    error_message=str(e)
                ))
        
        return test_summaries
    
    def _execute_tests_parallel(self, test_ids: List[str], budget_limit: float,
                              models_to_test: Optional[List[str]]) -> List[TestExecutionSummary]:
        """Execute tests in parallel where dependencies allow"""
        # For now, implement sequential execution with rate limiting
        # True parallel execution would require careful dependency management
        self.logger.info("🔄 Parallel execution requested - using sequential with rate limiting")
        return self._execute_tests_sequential(test_ids, budget_limit, models_to_test)
    
    def _check_test_dependencies(self, test_id: str, completed_tests: List[TestExecutionSummary]) -> bool:
        """Check if test dependencies are satisfied"""
        dependencies = {
            '01': [],  # No dependencies
            '02': ['01'],  # Requires Test 01 results
            '03': ['02'],  # Requires Test 02 results
            '04': []   # No dependencies
        }
        
        required_deps = dependencies.get(test_id, [])
        if not required_deps:
            return True
        
        completed_test_ids = [
            t.test_id for t in completed_tests 
            if t.status == 'success'
        ]
        
        return all(dep in completed_test_ids for dep in required_deps)
    
    def _execute_single_test(self, test_id: str, budget_limit: float,
                           models_to_test: Optional[List[str]]) -> TestExecutionSummary:
        """Execute a single test and return summary"""
        start_time = time.time()
        
        try:
            # Get test runner class
            runner_class = self.test_runners.get(test_id)
            if not runner_class:
                raise ValueError(f"Unknown test ID: {test_id}")
            
            # Initialize runner
            runner = runner_class()
            
            # Execute test based on type
            if test_id == '01':
                results = runner.run_test(
                    budget_limit=budget_limit,
                    models_to_test=models_to_test
                )
            elif test_id == '02':
                results = runner.run_test(
                    budget_limit=budget_limit,
                    models_to_test=models_to_test
                )
            elif test_id == '03':
                results = runner.run_test(
                    budget_limit=budget_limit,
                    models_to_test=models_to_test
                )
            elif test_id == '04':
                results = runner.run_test(
                    budget_limit=budget_limit,
                    models_to_test=models_to_test
                )
            else:
                raise ValueError(f"Unsupported test ID: {test_id}")
            
            execution_time = time.time() - start_time
            
            # Extract cost from results
            cost = 0.0
            if hasattr(results, 'cost_summary') and results.cost_summary:
                cost = results.cost_summary.get('total', 0.0)
            
            # Determine results path
            results_path = f"TESTS/01-core-technical/results/{self._get_test_results_dir(test_id)}/"
            
            return TestExecutionSummary(
                test_id=test_id,
                status='success',
                execution_time=execution_time,
                cost=cost,
                results_path=results_path
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestExecutionSummary(
                test_id=test_id,
                status='failed',
                execution_time=execution_time,
                cost=0.0,
                error_message=str(e)
            )
    
    def _get_test_results_dir(self, test_id: str) -> str:
        """Get results directory name for test ID"""
        dirs = {
            '01': 'semantic-extraction',
            '02': 'json-generation',
            '03': 'content-regeneration',
            '04': 'code-extraction'
        }
        return dirs.get(test_id, f'test-{test_id}')
    
    def _get_config_summary(self) -> Dict[str, Any]:
        """Get configuration summary for results"""
        return {
            'video_folder': getattr(self.config, 'video_folder', 'video'),
            'total_budget': getattr(self.config, 'total_budget', 200.0),
            'per_test_budget': getattr(self.config, 'per_test_budget', 50.0),
            'api_keys_configured': {
                'openai': bool(getattr(self.config, 'openai_api_key', None)),
                'anthropic': bool(getattr(self.config, 'anthropic_api_key', None)),
                'elevenlabs': bool(getattr(self.config, 'elevenlabs_api_key', None))
            }
        }
    
    def _store_master_results(self, results: MasterTestResults):
        """Store master test execution results"""
        try:
            results_path = Path("TESTS/01-core-technical/results/master_execution_results.json")
            results_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(results_path, 'w') as f:
                json.dump(asdict(results), f, indent=2, default=str)
            
            self.logger.info(f"Master results stored: {results_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to store master results: {e}")
    
    def _print_execution_summary(self, results: MasterTestResults):
        """Print execution summary to console"""
        print("\n" + "="*60)
        print("TEST SUITE EXECUTION SUMMARY")
        print("="*60)
        print(f"Execution Time: {results.total_execution_time:.2f} seconds")
        print(f"Total Cost: £{results.total_cost:.2f}")
        print(f"Budget Limit: £{results.budget_limit:.2f}")
        print(f"Budget Utilization: {(results.total_cost/results.budget_limit)*100:.1f}%")
        print(f"Overall Status: {results.overall_status.upper()}")
        print()
        
        print("Individual Test Results:")
        print("-" * 40)
        for test in results.tests_executed:
            status_icon = "✅" if test.status == 'success' else "❌" if test.status == 'failed' else "⏭️"
            print(f"{status_icon} Test {test.test_id}: {test.status.upper()}")
            print(f"   Time: {test.execution_time:.2f}s, Cost: £{test.cost:.2f}")
            if test.error_message:
                print(f"   Error: {test.error_message}")
            if test.results_path:
                print(f"   Results: {test.results_path}")
            print()
        
        print("="*60)
    
    def generate_comprehensive_report(self, include_visualizations: bool = True):
        """Generate comprehensive report across all test results"""
        try:
            self.logger.info("📊 Generating comprehensive report...")
            
            # Generate report using report generator
            report_path = self.report_generator.generate_comprehensive_report(
                include_visualizations=include_visualizations
            )
            
            self.logger.info(f"✅ Comprehensive report generated: {report_path}")
            print(f"\n📊 Comprehensive report available at: {report_path}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to generate comprehensive report: {e}")


def main():
    """Main CLI interface for master test runner"""
    parser = argparse.ArgumentParser(
        description="Master Test Runner for Core Technical Testing Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py --test all --budget 150
  python run_tests.py --test 01 02 --models gpt4_vision claude_sonnet
  python run_tests.py --dry-run
  python run_tests.py --test 03 --budget 60 --report
        """
    )
    
    parser.add_argument(
        "--test", 
        nargs="+",
        choices=["01", "02", "03", "04", "all"],
        default=["all"],
        help="Which tests to run (default: all)"
    )
    
    parser.add_argument(
        "--budget", 
        type=float, 
        help="Override budget limit for test execution"
    )
    
    parser.add_argument(
        "--models", 
        nargs="+",
        help="Specific models to test (varies by test)"
    )
    
    parser.add_argument(
        "--report", 
        action="store_true",
        help="Generate comprehensive report after execution"
    )
    
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Validate setup without running tests"
    )
    
    parser.add_argument(
        "--parallel", 
        action="store_true",
        help="Run tests in parallel where possible"
    )
    
    parser.add_argument(
        "--config", 
        type=str,
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Set up logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize test controller
        controller = TestController(config_path=args.config)
        
        # Handle dry run
        if args.dry_run:
            print("🔍 Running setup validation (dry-run mode)...")
            if controller.validate_setup():
                print("✅ Setup validation passed - ready to run tests")
                sys.exit(0)
            else:
                print("❌ Setup validation failed - check configuration")
                sys.exit(1)
        
        # Determine tests to run
        test_ids = args.test
        if "all" in test_ids:
            test_ids = ["01", "02", "03", "04"]
        
        # Determine budget
        budget_limit = args.budget
        if budget_limit is None:
            # Use default budget from config or fallback
            budget_limit = getattr(controller.config, 'total_budget', 200.0)
        
        # Validate setup before execution
        print("🔍 Validating setup before execution...")
        if not controller.validate_setup():
            print("❌ Setup validation failed - cannot proceed")
            sys.exit(1)
        
        # Execute test suite
        print(f"\n🚀 Starting test execution...")
        results = controller.execute_test_suite(
            test_ids=test_ids,
            budget_limit=budget_limit,
            models_to_test=args.models,
            parallel=args.parallel
        )
        
        # Generate report if requested
        if args.report:
            controller.generate_comprehensive_report()
        
        # Exit with appropriate code
        if results.overall_status == 'success':
            print("\n🎉 All tests completed successfully!")
            sys.exit(0)
        elif results.overall_status == 'partial_success':
            print("\n⚠️  Some tests failed - check results for details")
            sys.exit(1)
        else:
            print("\n❌ Test execution failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Test execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Test execution failed with error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()