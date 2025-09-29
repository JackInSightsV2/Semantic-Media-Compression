#!/usr/bin/env python3
"""
Test Controller for orchestrating test execution with progress monitoring,
cost tracking against budgets, and real-time status updates
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import threading

from .data.config_loader import load_config
from .data.result_storage import ResultStorage
from .reporting.report_generator import ReportGenerator

@dataclass
class TestProgress:
    """Progress tracking for test execution"""
    test_id: str
    status: str  # 'pending', 'running', 'completed', 'failed'
    progress_percentage: float
    current_step: str
    estimated_time_remaining: float
    cost_so_far: float

class TestController:
    """
    Test controller class orchestrating execution with progress monitoring,
    cost tracking against budgets, real-time status updates
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize test controller"""
        self.config = load_config(config_path)
        self.result_storage = ResultStorage()
        self.report_generator = ReportGenerator()
        
        # Progress tracking
        self.test_progress = {}
        self.progress_lock = threading.Lock()
        
        # Cost tracking
        self.total_cost = 0.0
        self.cost_breakdown = {}
        self.cost_lock = threading.Lock()
        
        # Setup logging
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging for test controller"""
        log_dir = Path("TESTS/01-core-technical/results")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"test_controller_{int(time.time())}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_all_tests(self, budget: Optional[float] = None, 
                     models: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run all tests in sequence"""
        test_ids = ['01', '02', '03', '04']
        return self.run_tests(test_ids, budget, models)
    
    def run_single_test(self, test_id: str, budget: Optional[float] = None,
                       models: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run a single test"""
        return self.run_tests([test_id], budget, models)
    
    def run_tests(self, test_ids: List[str], budget: Optional[float] = None,
                 models: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run specified tests with monitoring and cost tracking"""
        start_time = time.time()
        
        # Set budget
        if budget is None:
            budget = getattr(self.config, 'total_budget', 200.0)
        
        self.logger.info(f"Starting test execution: {test_ids}")
        self.logger.info(f"Budget limit: £{budget:.2f}")
        
        # Initialize progress tracking
        for test_id in test_ids:
            with self.progress_lock:
                self.test_progress[test_id] = TestProgress(
                    test_id=test_id,
                    status='pending',
                    progress_percentage=0.0,
                    current_step='Initializing',
                    estimated_time_remaining=0.0,
                    cost_so_far=0.0
                )
        
        results = {
            'execution_timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'test_results': {},
            'total_cost': 0.0,
            'total_time': 0.0,
            'budget_limit': budget,
            'overall_status': 'success'
        }
        
        try:
            # Execute tests sequentially
            for test_id in test_ids:
                if self.total_cost >= budget:
                    self.logger.warning(f"Budget limit reached, skipping Test {test_id}")
                    self._update_test_progress(test_id, 'skipped', 100.0, 'Budget exceeded')
                    continue
                
                self.logger.info(f"Executing Test {test_id}...")
                self._update_test_progress(test_id, 'running', 0.0, 'Starting test')
                
                try:
                    # Execute individual test
                    test_result = self._execute_test(test_id, budget - self.total_cost, models)
                    results['test_results'][test_id] = test_result
                    
                    # Update cost tracking
                    test_cost = test_result.get('cost', 0.0)
                    with self.cost_lock:
                        self.total_cost += test_cost
                        self.cost_breakdown[test_id] = test_cost
                    
                    self._update_test_progress(test_id, 'completed', 100.0, 'Test completed', test_cost)
                    self.logger.info(f"Test {test_id} completed. Cost: £{test_cost:.2f}")
                    
                except Exception as e:
                    self.logger.error(f"Test {test_id} failed: {e}")
                    results['test_results'][test_id] = {'error': str(e)}
                    self._update_test_progress(test_id, 'failed', 100.0, f'Failed: {str(e)}')
                    results['overall_status'] = 'partial_failure'
            
            # Finalize results
            results['total_cost'] = self.total_cost
            results['total_time'] = time.time() - start_time
            results['cost_breakdown'] = self.cost_breakdown
            
            # Store results
            self._store_execution_results(results)
            
            self.logger.info(f"Test execution completed. Total cost: £{self.total_cost:.2f}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Test execution failed: {e}")
            results['overall_status'] = 'failed'
            results['error'] = str(e)
            return results
    
    def _execute_test(self, test_id: str, budget_limit: float, 
                     models: Optional[List[str]]) -> Dict[str, Any]:
        """Execute a single test with progress monitoring"""
        # This would import and run the specific test
        # For now, return mock results
        
        self._update_test_progress(test_id, 'running', 25.0, 'Loading test data')
        time.sleep(1)  # Simulate work
        
        self._update_test_progress(test_id, 'running', 50.0, 'Processing with AI models')
        time.sleep(2)  # Simulate work
        
        self._update_test_progress(test_id, 'running', 75.0, 'Validating results')
        time.sleep(1)  # Simulate work
        
        # Mock test result
        return {
            'test_id': test_id,
            'status': 'success',
            'cost': min(budget_limit * 0.5, 25.0),  # Use up to 50% of budget or £25
            'execution_time': 4.0,
            'results_summary': f'Test {test_id} completed successfully'
        }
    
    def _update_test_progress(self, test_id: str, status: str, progress: float,
                            current_step: str, cost: float = 0.0):
        """Update progress for a specific test"""
        with self.progress_lock:
            if test_id in self.test_progress:
                self.test_progress[test_id].status = status
                self.test_progress[test_id].progress_percentage = progress
                self.test_progress[test_id].current_step = current_step
                self.test_progress[test_id].cost_so_far = cost
    
    def get_progress_status(self) -> Dict[str, TestProgress]:
        """Get current progress status for all tests"""
        with self.progress_lock:
            return self.test_progress.copy()
    
    def monitor_progress(self) -> None:
        """Monitor and display progress in real-time"""
        while True:
            progress_status = self.get_progress_status()
            
            # Clear screen and display progress
            os.system('cls' if os.name == 'nt' else 'clear')
            print("="*60)
            print("TEST EXECUTION PROGRESS")
            print("="*60)
            
            for test_id, progress in progress_status.items():
                status_icon = {
                    'pending': '⏳',
                    'running': '🔄',
                    'completed': '✅',
                    'failed': '❌',
                    'skipped': '⏭️'
                }.get(progress.status, '❓')
                
                print(f"{status_icon} Test {test_id}: {progress.status.upper()}")
                print(f"   Progress: {progress.progress_percentage:.1f}%")
                print(f"   Step: {progress.current_step}")
                print(f"   Cost: £{progress.cost_so_far:.2f}")
                print()
            
            print(f"Total Cost: £{self.total_cost:.2f}")
            print("="*60)
            
            # Check if all tests are done
            all_done = all(
                p.status in ['completed', 'failed', 'skipped'] 
                for p in progress_status.values()
            )
            
            if all_done:
                break
            
            time.sleep(2)  # Update every 2 seconds
    
    def validate_setup(self) -> bool:
        """Validate test setup and configuration"""
        try:
            self.logger.info("Validating test setup...")
            
            # Check configuration
            if not self.config:
                self.logger.error("Configuration not loaded")
                return False
            
            # Check API keys
            api_keys_present = []
            if hasattr(self.config, 'openai_api_key') and self.config.openai_api_key:
                api_keys_present.append('OpenAI')
            if hasattr(self.config, 'anthropic_api_key') and self.config.anthropic_api_key:
                api_keys_present.append('Anthropic')
            
            if not api_keys_present:
                self.logger.warning("No API keys configured")
                return False
            
            # Check video folder
            video_folder = Path(getattr(self.config, 'video_folder', 'video'))
            if not video_folder.exists():
                self.logger.warning(f"Video folder not found: {video_folder}")
            
            self.logger.info("Setup validation completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Setup validation failed: {e}")
            return False
    
    def _store_execution_results(self, results: Dict[str, Any]):
        """Store execution results"""
        try:
            results_path = Path("TESTS/01-core-technical/results/execution_summary.json")
            results_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(results_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            self.logger.info(f"Execution results stored: {results_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to store execution results: {e}")
    
    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive report across all test results"""
        try:
            self.logger.info("Generating comprehensive report...")
            
            # Use report generator to create comprehensive report
            report_path = self.report_generator.generate_comprehensive_report()
            
            self.logger.info(f"Comprehensive report generated: {report_path}")
            return report_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate comprehensive report: {e}")
            return ""