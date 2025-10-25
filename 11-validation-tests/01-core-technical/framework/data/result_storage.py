"""
Results storage and historical tracking system for semantic compression testing framework.

This module handles storing test results, maintaining historical data, and providing
analysis capabilities for model performance trends and regression detection.
"""

import os
import json
import csv
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import asdict
import pandas as pd

from . import (
    TestSummary,
    SemanticExtractionResult,
    JSONGenerationResult,
    ContentRegenerationResult,
    CodeExtractionResult,
    QualityMetrics
)


class StorageError(Exception):
    """Raised when storage operations fail."""
    pass


class ResultStorage:
    """
    Manages storage and retrieval of test results with historical tracking capabilities.
    """
    
    def __init__(self, tests_root: Optional[str] = None):
        """
        Initialize the result storage system.
        
        Args:
            tests_root: Path to TESTS directory. If None, auto-detects.
        """
        if tests_root is None:
            # Auto-detect TESTS directory
            current_dir = Path(__file__).parent
            while current_dir.parent != current_dir:
                tests_dir = current_dir / "TESTS"
                if tests_dir.exists():
                    self.tests_root = tests_dir
                    break
                current_dir = current_dir.parent
            else:
                # Fallback: assume we're in TESTS/01-core-technical/framework/data
                self.tests_root = Path(__file__).parent.parent.parent.parent
        else:
            self.tests_root = Path(tests_root)
        
        self.results_dir = self.tests_root / "01-core-technical" / "results"
        self.historical_dir = self.results_dir / "historical"
        
        # Result type directories
        self.result_dirs = {
            'semantic_extraction': self.results_dir / "semantic-extraction",
            'json_generation': self.results_dir / "json-generation",
            'content_regeneration': self.results_dir / "content-regeneration",
            'code_extraction': self.results_dir / "code-extraction"
        }
        
        # Ensure directories exist
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        directories = list(self.result_dirs.values()) + [
            self.historical_dir,
            self.historical_dir / "trends",
            self.historical_dir / "exports"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def store_results(self, test_type: str, results: Union[List[Any], Any], 
                     test_id: Optional[str] = None) -> str:
        """
        Store test results in results/{test-type}/ with timestamp-based filenames.
        
        Args:
            test_type: Type of test ('semantic_extraction', 'json_generation', etc.)
            results: Test results to store (single result or list of results)
            test_id: Optional test ID for filename
            
        Returns:
            Path to stored results file
            
        Raises:
            StorageError: If storage fails
        """
        if test_type not in self.result_dirs:
            raise StorageError(f"Unknown test type: {test_type}")
        
        # Ensure results is a list
        if not isinstance(results, list):
            results = [results]
        
        # Generate timestamp-based filename
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        
        if test_id:
            filename = f"{test_id}_{timestamp_str}.json"
        else:
            filename = f"results_{timestamp_str}.json"
        
        result_file = self.result_dirs[test_type] / filename
        
        try:
            # Convert dataclass objects to dictionaries
            serializable_results = []
            for result in results:
                if hasattr(result, '__dict__'):
                    # Handle dataclass objects
                    result_dict = asdict(result)
                    # Convert datetime objects to ISO strings
                    result_dict = self._serialize_datetime_objects(result_dict)
                    serializable_results.append(result_dict)
                else:
                    serializable_results.append(result)
            
            # Store as JSON
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'test_type': test_type,
                    'timestamp': timestamp.isoformat(),
                    'test_id': test_id,
                    'result_count': len(serializable_results),
                    'results': serializable_results
                }, f, indent=2, ensure_ascii=False)
            
            # Update historical tracking
            self._update_historical_tracking(test_type, serializable_results, timestamp)
            
            return str(result_file)
            
        except Exception as e:
            raise StorageError(f"Failed to store results: {e}")
    
    def _serialize_datetime_objects(self, obj: Any) -> Any:
        """
        Recursively convert datetime objects to ISO strings for JSON serialization.
        
        Args:
            obj: Object that may contain datetime objects
            
        Returns:
            Object with datetime objects converted to strings
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {key: self._serialize_datetime_objects(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_datetime_objects(item) for item in obj]
        else:
            return obj
    
    def _update_historical_tracking(self, test_type: str, results: List[Dict[str, Any]], 
                                  timestamp: datetime) -> None:
        """
        Update historical tracking data for model performance trends.
        
        Args:
            test_type: Type of test
            results: Test results
            timestamp: Timestamp of results
        """
        historical_file = self.historical_dir / f"{test_type}_history.json"
        
        # Load existing historical data
        historical_data = []
        if historical_file.exists():
            try:
                with open(historical_file, 'r', encoding='utf-8') as f:
                    historical_data = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load historical data: {e}")
        
        # Extract key metrics from results
        for result in results:
            historical_entry = {
                'timestamp': timestamp.isoformat(),
                'test_type': test_type,
                'model_name': result.get('model_name', 'unknown'),
                'test_id': result.get('test_id', 'unknown')
            }
            
            # Extract type-specific metrics
            if test_type == 'semantic_extraction':
                historical_entry.update({
                    'accuracy_score': result.get('accuracy_score', 0.0),
                    'processing_time': result.get('processing_time', 0.0),
                    'cost': result.get('cost', 0.0)
                })
            elif test_type == 'json_generation':
                historical_entry.update({
                    'schema_compliance': result.get('schema_compliance', False),
                    'semantic_completeness': result.get('semantic_completeness', 0.0),
                    'compression_ratio': result.get('compression_ratio', 0.0)
                })
            elif test_type == 'content_regeneration':
                quality_metrics = result.get('quality_metrics', {})
                historical_entry.update({
                    'character_consistency': quality_metrics.get('character_consistency', 0.0),
                    'scene_coherence': quality_metrics.get('scene_coherence', 0.0),
                    'cultural_accuracy': quality_metrics.get('cultural_accuracy', 0.0),
                    'overall_score': quality_metrics.get('overall_score', 0.0),
                    'generation_time': result.get('generation_time', 0.0),
                    'cost': result.get('cost', 0.0)
                })
            elif test_type == 'code_extraction':
                historical_entry.update({
                    'business_logic_preservation': result.get('business_logic_preservation', 0.0),
                    'architectural_pattern_fidelity': result.get('architectural_pattern_fidelity', 0.0),
                    'processing_time': result.get('processing_time', 0.0),
                    'cost': result.get('cost', 0.0)
                })
                
                # Add functional equivalence scores
                func_equiv_scores = result.get('functional_equivalence_scores', {})
                for lang, score in func_equiv_scores.items():
                    historical_entry[f'equivalence_{lang}'] = score
            
            historical_data.append(historical_entry)
        
        # Save updated historical data
        try:
            with open(historical_file, 'w', encoding='utf-8') as f:
                json.dump(historical_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not update historical data: {e}")
    
    def get_historical_data(self, test_type: str, 
                          date_range: Optional[Tuple[datetime, datetime]] = None,
                          model_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve historical test results with filtering options.
        
        Args:
            test_type: Type of test to retrieve
            date_range: Optional tuple of (start_date, end_date) for filtering
            model_filter: Optional model name to filter by
            
        Returns:
            List of historical test results
            
        Raises:
            StorageError: If retrieval fails
        """
        historical_file = self.historical_dir / f"{test_type}_history.json"
        
        if not historical_file.exists():
            return []
        
        try:
            with open(historical_file, 'r', encoding='utf-8') as f:
                historical_data = json.load(f)
            
            # Apply filters
            filtered_data = historical_data
            
            if date_range:
                start_date, end_date = date_range
                filtered_data = [
                    entry for entry in filtered_data
                    if start_date <= datetime.fromisoformat(entry['timestamp']) <= end_date
                ]
            
            if model_filter:
                filtered_data = [
                    entry for entry in filtered_data
                    if entry.get('model_name') == model_filter
                ]
            
            return filtered_data
            
        except Exception as e:
            raise StorageError(f"Failed to retrieve historical data: {e}")
    
    def detect_performance_regression(self, test_type: str, model_name: str,
                                    lookback_days: int = 30) -> Dict[str, Any]:
        """
        Detect performance regression by comparing recent results with historical baseline.
        
        Args:
            test_type: Type of test to analyze
            model_name: Model to analyze
            lookback_days: Number of days to look back for comparison
            
        Returns:
            Dictionary with regression analysis results
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_days)
        
        # Get recent data
        recent_data = self.get_historical_data(
            test_type, 
            date_range=(start_date, end_date),
            model_filter=model_name
        )
        
        # Get baseline data (previous period)
        baseline_start = start_date - timedelta(days=lookback_days)
        baseline_data = self.get_historical_data(
            test_type,
            date_range=(baseline_start, start_date),
            model_filter=model_name
        )
        
        if not recent_data or not baseline_data:
            return {
                'regression_detected': False,
                'reason': 'Insufficient data for comparison',
                'recent_count': len(recent_data),
                'baseline_count': len(baseline_data)
            }
        
        # Calculate metrics for comparison
        regression_analysis = {
            'regression_detected': False,
            'metrics_comparison': {},
            'recent_period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
                'sample_count': len(recent_data)
            },
            'baseline_period': {
                'start': baseline_start.isoformat(),
                'end': start_date.isoformat(),
                'sample_count': len(baseline_data)
            }
        }
        
        # Define metrics to compare based on test type
        metrics_to_compare = self._get_regression_metrics(test_type)
        
        for metric in metrics_to_compare:
            recent_values = [entry.get(metric, 0) for entry in recent_data if metric in entry]
            baseline_values = [entry.get(metric, 0) for entry in baseline_data if metric in entry]
            
            if recent_values and baseline_values:
                recent_avg = sum(recent_values) / len(recent_values)
                baseline_avg = sum(baseline_values) / len(baseline_values)
                
                # Calculate percentage change
                if baseline_avg != 0:
                    change_percent = ((recent_avg - baseline_avg) / baseline_avg) * 100
                else:
                    change_percent = 0
                
                # Determine if this indicates regression (depends on metric)
                is_regression = self._is_metric_regression(metric, change_percent)
                
                regression_analysis['metrics_comparison'][metric] = {
                    'recent_average': recent_avg,
                    'baseline_average': baseline_avg,
                    'change_percent': change_percent,
                    'is_regression': is_regression
                }
                
                if is_regression:
                    regression_analysis['regression_detected'] = True
        
        return regression_analysis
    
    def _get_regression_metrics(self, test_type: str) -> List[str]:
        """
        Get list of metrics to monitor for regression based on test type.
        
        Args:
            test_type: Type of test
            
        Returns:
            List of metric names to monitor
        """
        metrics_map = {
            'semantic_extraction': ['accuracy_score', 'processing_time', 'cost'],
            'json_generation': ['semantic_completeness', 'compression_ratio'],
            'content_regeneration': ['character_consistency', 'scene_coherence', 'cultural_accuracy', 'overall_score'],
            'code_extraction': ['business_logic_preservation', 'architectural_pattern_fidelity']
        }
        
        return metrics_map.get(test_type, [])
    
    def _is_metric_regression(self, metric: str, change_percent: float) -> bool:
        """
        Determine if a metric change indicates regression.
        
        Args:
            metric: Metric name
            change_percent: Percentage change (positive = increase, negative = decrease)
            
        Returns:
            True if change indicates regression
        """
        # Metrics where decrease is bad (higher is better)
        higher_is_better = [
            'accuracy_score', 'semantic_completeness', 'compression_ratio',
            'character_consistency', 'scene_coherence', 'cultural_accuracy',
            'overall_score', 'business_logic_preservation', 'architectural_pattern_fidelity'
        ]
        
        # Metrics where increase is bad (lower is better)
        lower_is_better = ['processing_time', 'cost', 'generation_time']
        
        # Define regression thresholds
        regression_threshold = 10.0  # 10% change threshold
        
        if metric in higher_is_better:
            return change_percent < -regression_threshold  # Significant decrease is bad
        elif metric in lower_is_better:
            return change_percent > regression_threshold   # Significant increase is bad
        else:
            return False  # Unknown metric, no regression detected
    
    def export_to_csv(self, test_type: str, output_file: Optional[str] = None,
                     date_range: Optional[Tuple[datetime, datetime]] = None) -> str:
        """
        Export historical data to CSV for external analysis.
        
        Args:
            test_type: Type of test to export
            output_file: Optional output filename
            date_range: Optional date range filter
            
        Returns:
            Path to exported CSV file
            
        Raises:
            StorageError: If export fails
        """
        historical_data = self.get_historical_data(test_type, date_range)
        
        if not historical_data:
            raise StorageError(f"No data available for export: {test_type}")
        
        # Generate output filename if not provided
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{test_type}_export_{timestamp}.csv"
        
        export_path = self.historical_dir / "exports" / output_file
        
        try:
            # Convert to DataFrame for easier CSV export
            df = pd.DataFrame(historical_data)
            
            # Ensure consistent column ordering
            column_order = ['timestamp', 'test_type', 'model_name', 'test_id']
            remaining_columns = [col for col in df.columns if col not in column_order]
            df = df[column_order + remaining_columns]
            
            # Export to CSV
            df.to_csv(export_path, index=False, encoding='utf-8')
            
            return str(export_path)
            
        except Exception as e:
            raise StorageError(f"Failed to export to CSV: {e}")
    
    def get_model_performance_summary(self, test_type: str, 
                                    days_back: int = 30) -> Dict[str, Dict[str, Any]]:
        """
        Get performance summary for all models in a test type.
        
        Args:
            test_type: Type of test to analyze
            days_back: Number of days to look back
            
        Returns:
            Dictionary mapping model names to performance summaries
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        historical_data = self.get_historical_data(test_type, (start_date, end_date))
        
        if not historical_data:
            return {}
        
        # Group by model
        model_data = {}
        for entry in historical_data:
            model_name = entry.get('model_name', 'unknown')
            if model_name not in model_data:
                model_data[model_name] = []
            model_data[model_name].append(entry)
        
        # Calculate summaries
        summaries = {}
        metrics_to_analyze = self._get_regression_metrics(test_type)
        
        for model_name, entries in model_data.items():
            summary = {
                'test_count': len(entries),
                'date_range': {
                    'start': start_date.isoformat(),
                    'end': end_date.isoformat()
                },
                'metrics': {}
            }
            
            for metric in metrics_to_analyze:
                values = [entry.get(metric, 0) for entry in entries if metric in entry]
                if values:
                    summary['metrics'][metric] = {
                        'average': sum(values) / len(values),
                        'min': min(values),
                        'max': max(values),
                        'count': len(values)
                    }
            
            summaries[model_name] = summary
        
        return summaries
    
    def cleanup_old_results(self, days_to_keep: int = 90) -> Dict[str, int]:
        """
        Clean up old result files to manage disk space.
        
        Args:
            days_to_keep: Number of days of results to keep
            
        Returns:
            Dictionary with cleanup statistics
        """
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cleanup_stats = {
            'files_removed': 0,
            'bytes_freed': 0,
            'errors': 0
        }
        
        for test_type, result_dir in self.result_dirs.items():
            if not result_dir.exists():
                continue
            
            for result_file in result_dir.iterdir():
                if not result_file.is_file() or result_file.suffix != '.json':
                    continue
                
                try:
                    # Check file modification time
                    file_mtime = datetime.fromtimestamp(result_file.stat().st_mtime)
                    
                    if file_mtime < cutoff_date:
                        file_size = result_file.stat().st_size
                        result_file.unlink()
                        cleanup_stats['files_removed'] += 1
                        cleanup_stats['bytes_freed'] += file_size
                        
                except Exception as e:
                    print(f"Warning: Could not remove old file {result_file}: {e}")
                    cleanup_stats['errors'] += 1
        
        return cleanup_stats