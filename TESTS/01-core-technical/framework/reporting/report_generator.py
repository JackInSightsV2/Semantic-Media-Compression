"""
Comprehensive report generation for semantic compression testing framework.

This module provides HTML report generation with embedded charts, test summaries,
failure analysis, and comparative model performance analysis.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import asdict
import base64
from io import BytesIO

from ..data import (
    TestSummary, SemanticExtractionResult, JSONGenerationResult,
    ContentRegenerationResult, CodeExtractionResult, QualityMetrics
)
from .visualizations import VisualizationEngine


class ReportGenerator:
    """
    Generates comprehensive HTML reports with embedded visualizations for
    semantic compression testing results.
    """
    
    def __init__(self, results_dir: str = "TESTS/01-core-technical/results"):
        """
        Initialize the report generator.
        
        Args:
            results_dir: Directory containing test results
        """
        self.results_dir = Path(results_dir)
        self.viz_engine = VisualizationEngine()
        
    def generate_comprehensive_report(self, 
                                    test_summaries: List[TestSummary],
                                    output_path: Optional[str] = None) -> str:
        """
        Generate a comprehensive HTML report with embedded charts.
        
        Args:
            test_summaries: List of test summaries to include in report
            output_path: Optional custom output path for the report
            
        Returns:
            Path to the generated HTML report
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.results_dir / f"comprehensive_report_{timestamp}.html"
        
        # Generate all visualizations
        charts = self._generate_all_charts(test_summaries)
        
        # Generate report sections
        executive_summary = self._generate_executive_summary(test_summaries)
        test_summary_section = self._generate_test_summary_section(test_summaries)
        model_comparison = self._generate_model_comparison(test_summaries)
        failure_analysis = self._generate_failure_analysis(test_summaries)
        cost_analysis = self._generate_cost_analysis(test_summaries)
        recommendations = self._generate_recommendations(test_summaries)
        
        # Generate complete HTML report
        html_content = self._generate_html_template(
            executive_summary=executive_summary,
            test_summary=test_summary_section,
            model_comparison=model_comparison,
            failure_analysis=failure_analysis,
            cost_analysis=cost_analysis,
            recommendations=recommendations,
            charts=charts
        )
        
        # Write report to file
        os.makedirs(output_path.parent, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return str(output_path)
    
    def _generate_all_charts(self, test_summaries: List[TestSummary]) -> Dict[str, str]:
        """Generate all charts and return as base64 encoded strings."""
        charts = {}
        
        # Accuracy trends chart
        accuracy_data = self._extract_accuracy_trends(test_summaries)
        if accuracy_data:
            charts['accuracy_trends'] = self.viz_engine.create_accuracy_trends_chart(accuracy_data)
        
        # Cost analysis chart
        cost_data = self._extract_cost_data(test_summaries)
        if cost_data:
            charts['cost_analysis'] = self.viz_engine.create_cost_analysis_chart(cost_data)
        
        # Model comparison chart
        model_data = self._extract_model_performance(test_summaries)
        if model_data:
            charts['model_comparison'] = self.viz_engine.create_model_comparison_chart(model_data)
        
        # Quality metrics heatmap
        quality_data = self._extract_quality_metrics(test_summaries)
        if quality_data:
            charts['quality_heatmap'] = self.viz_engine.create_quality_heatmap(quality_data)
        
        return charts
    
    def _generate_executive_summary(self, test_summaries: List[TestSummary]) -> str:
        """Generate executive summary section."""
        total_tests = sum(summary.total_test_cases for summary in test_summaries)
        total_passed = sum(summary.passed_cases for summary in test_summaries)
        total_cost = sum(sum(summary.cost_summary.values()) for summary in test_summaries)
        
        pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        # Calculate average scores across all tests
        all_scores = [summary.average_scores for summary in test_summaries if summary.average_scores]
        if all_scores:
            avg_character_consistency = sum(s.character_consistency for s in all_scores) / len(all_scores)
            avg_scene_coherence = sum(s.scene_coherence for s in all_scores) / len(all_scores)
            avg_cultural_accuracy = sum(s.cultural_accuracy for s in all_scores) / len(all_scores)
            avg_overall_score = sum(s.overall_score for s in all_scores) / len(all_scores)
        else:
            avg_character_consistency = avg_scene_coherence = avg_cultural_accuracy = avg_overall_score = 0
        
        return f"""
        <div class="executive-summary">
            <h2>Executive Summary</h2>
            <div class="summary-stats">
                <div class="stat-card">
                    <h3>Overall Pass Rate</h3>
                    <div class="stat-value {'success' if pass_rate >= 75 else 'warning' if pass_rate >= 50 else 'danger'}">{pass_rate:.1f}%</div>
                    <div class="stat-detail">{total_passed}/{total_tests} tests passed</div>
                </div>
                <div class="stat-card">
                    <h3>Total Cost</h3>
                    <div class="stat-value">${total_cost:.2f}</div>
                    <div class="stat-detail">Across all test runs</div>
                </div>
                <div class="stat-card">
                    <h3>Character Consistency</h3>
                    <div class="stat-value {'success' if avg_character_consistency >= 80 else 'warning' if avg_character_consistency >= 60 else 'danger'}">{avg_character_consistency:.1f}%</div>
                    <div class="stat-detail">Target: 80%+</div>
                </div>
                <div class="stat-card">
                    <h3>Overall Quality</h3>
                    <div class="stat-value {'success' if avg_overall_score >= 75 else 'warning' if avg_overall_score >= 60 else 'danger'}">{avg_overall_score:.1f}%</div>
                    <div class="stat-detail">Composite score</div>
                </div>
            </div>
        </div>
        """
    
    def _generate_test_summary_section(self, test_summaries: List[TestSummary]) -> str:
        """Generate detailed test summary section."""
        html = '<div class="test-summary"><h2>Test Summary by Category</h2>'
        
        # Group summaries by test type
        by_type = {}
        for summary in test_summaries:
            if summary.test_type not in by_type:
                by_type[summary.test_type] = []
            by_type[summary.test_type].append(summary)
        
        for test_type, summaries in by_type.items():
            total_cases = sum(s.total_test_cases for s in summaries)
            passed_cases = sum(s.passed_cases for s in summaries)
            total_cost = sum(sum(s.cost_summary.values()) for s in summaries)
            avg_execution_time = sum(s.execution_time for s in summaries) / len(summaries)
            
            pass_rate = (passed_cases / total_cases * 100) if total_cases > 0 else 0
            
            html += f"""
            <div class="test-type-summary">
                <h3>{test_type.replace('_', ' ').title()}</h3>
                <div class="test-metrics">
                    <span class="metric">Pass Rate: <strong>{pass_rate:.1f}%</strong></span>
                    <span class="metric">Cases: <strong>{passed_cases}/{total_cases}</strong></span>
                    <span class="metric">Cost: <strong>${total_cost:.2f}</strong></span>
                    <span class="metric">Avg Time: <strong>{avg_execution_time:.1f}s</strong></span>
                </div>
            </div>
            """
        
        html += '</div>'
        return html
    
    def _generate_model_comparison(self, test_summaries: List[TestSummary]) -> str:
        """Generate model performance comparison section."""
        model_performance = {}
        
        # Extract model performance data from detailed results
        for summary in test_summaries:
            for result in summary.detailed_results:
                model_name = getattr(result, 'model_name', 'unknown')
                if model_name not in model_performance:
                    model_performance[model_name] = {
                        'total_tests': 0,
                        'total_cost': 0,
                        'total_time': 0,
                        'accuracy_scores': [],
                        'quality_scores': []
                    }
                
                perf = model_performance[model_name]
                perf['total_tests'] += 1
                perf['total_cost'] += getattr(result, 'cost', 0)
                perf['total_time'] += getattr(result, 'processing_time', 0) or getattr(result, 'generation_time', 0)
                
                if hasattr(result, 'accuracy_score'):
                    perf['accuracy_scores'].append(result.accuracy_score)
                if hasattr(result, 'quality_metrics') and result.quality_metrics:
                    perf['quality_scores'].append(result.quality_metrics.overall_score)
        
        html = '<div class="model-comparison"><h2>Model Performance Comparison</h2>'
        html += '<div class="model-rankings">'
        
        # Rank models by performance
        ranked_models = []
        for model, data in model_performance.items():
            avg_accuracy = sum(data['accuracy_scores']) / len(data['accuracy_scores']) if data['accuracy_scores'] else 0
            avg_quality = sum(data['quality_scores']) / len(data['quality_scores']) if data['quality_scores'] else 0
            avg_cost_per_test = data['total_cost'] / data['total_tests'] if data['total_tests'] > 0 else 0
            avg_time_per_test = data['total_time'] / data['total_tests'] if data['total_tests'] > 0 else 0
            
            # Calculate composite score (higher is better)
            composite_score = (avg_accuracy * 0.4 + avg_quality * 0.4) - (avg_cost_per_test * 0.1) - (avg_time_per_test * 0.1)
            
            ranked_models.append({
                'name': model,
                'composite_score': composite_score,
                'avg_accuracy': avg_accuracy,
                'avg_quality': avg_quality,
                'avg_cost': avg_cost_per_test,
                'avg_time': avg_time_per_test,
                'total_tests': data['total_tests']
            })
        
        ranked_models.sort(key=lambda x: x['composite_score'], reverse=True)
        
        for i, model in enumerate(ranked_models, 1):
            html += f"""
            <div class="model-rank">
                <div class="rank-number">#{i}</div>
                <div class="model-details">
                    <h4>{model['name']}</h4>
                    <div class="model-metrics">
                        <span class="metric">Accuracy: {model['avg_accuracy']:.1f}/10</span>
                        <span class="metric">Quality: {model['avg_quality']:.1f}%</span>
                        <span class="metric">Cost/Test: ${model['avg_cost']:.2f}</span>
                        <span class="metric">Time/Test: {model['avg_time']:.1f}s</span>
                        <span class="metric">Tests: {model['total_tests']}</span>
                    </div>
                </div>
            </div>
            """
        
        html += '</div></div>'
        return html
    
    def _generate_failure_analysis(self, test_summaries: List[TestSummary]) -> str:
        """Generate detailed failure analysis section."""
        failures = []
        failure_patterns = {}
        
        for summary in test_summaries:
            if summary.failed_cases > 0:
                failure_rate = summary.failed_cases / summary.total_test_cases * 100
                failures.append({
                    'test_type': summary.test_type,
                    'failure_rate': failure_rate,
                    'failed_cases': summary.failed_cases,
                    'total_cases': summary.total_test_cases
                })
                
                # Analyze failure patterns from detailed results
                for result in summary.detailed_results:
                    if hasattr(result, 'accuracy_score') and result.accuracy_score < 5.0:
                        pattern = f"Low accuracy in {summary.test_type}"
                        failure_patterns[pattern] = failure_patterns.get(pattern, 0) + 1
                    
                    if hasattr(result, 'quality_metrics') and result.quality_metrics:
                        if result.quality_metrics.character_consistency < 80:
                            pattern = "Character consistency below target"
                            failure_patterns[pattern] = failure_patterns.get(pattern, 0) + 1
                        if result.quality_metrics.cultural_accuracy < 70:
                            pattern = "Cultural accuracy below target"
                            failure_patterns[pattern] = failure_patterns.get(pattern, 0) + 1
        
        html = '<div class="failure-analysis"><h2>Failure Analysis</h2>'
        
        if failures:
            html += '<h3>Failure Rates by Test Type</h3><div class="failure-rates">'
            for failure in sorted(failures, key=lambda x: x['failure_rate'], reverse=True):
                html += f"""
                <div class="failure-item">
                    <span class="test-type">{failure['test_type'].replace('_', ' ').title()}</span>
                    <span class="failure-rate {'danger' if failure['failure_rate'] > 25 else 'warning'}">{failure['failure_rate']:.1f}%</span>
                    <span class="failure-count">({failure['failed_cases']}/{failure['total_cases']})</span>
                </div>
                """
            html += '</div>'
        
        if failure_patterns:
            html += '<h3>Common Failure Patterns</h3><div class="failure-patterns">'
            for pattern, count in sorted(failure_patterns.items(), key=lambda x: x[1], reverse=True):
                html += f'<div class="pattern-item"><span class="pattern">{pattern}</span><span class="count">{count} occurrences</span></div>'
            html += '</div>'
        
        html += '</div>'
        return html
    
    def _generate_cost_analysis(self, test_summaries: List[TestSummary]) -> str:
        """Generate cost analysis section."""
        total_cost = sum(sum(summary.cost_summary.values()) for summary in test_summaries)
        
        # Cost breakdown by test type
        cost_by_type = {}
        for summary in test_summaries:
            cost_by_type[summary.test_type] = sum(summary.cost_summary.values())
        
        # Cost breakdown by model (from detailed results)
        cost_by_model = {}
        for summary in test_summaries:
            for result in summary.detailed_results:
                model_name = getattr(result, 'model_name', 'unknown')
                cost = getattr(result, 'cost', 0)
                cost_by_model[model_name] = cost_by_model.get(model_name, 0) + cost
        
        html = f"""
        <div class="cost-analysis">
            <h2>Cost Analysis</h2>
            <div class="total-cost">
                <h3>Total Cost: ${total_cost:.2f}</h3>
            </div>
            
            <div class="cost-breakdown">
                <h3>Cost by Test Type</h3>
                <div class="cost-items">
        """
        
        for test_type, cost in sorted(cost_by_type.items(), key=lambda x: x[1], reverse=True):
            percentage = (cost / total_cost * 100) if total_cost > 0 else 0
            html += f"""
            <div class="cost-item">
                <span class="item-name">{test_type.replace('_', ' ').title()}</span>
                <span class="item-cost">${cost:.2f}</span>
                <span class="item-percentage">({percentage:.1f}%)</span>
            </div>
            """
        
        html += '</div><h3>Cost by Model</h3><div class="cost-items">'
        
        for model, cost in sorted(cost_by_model.items(), key=lambda x: x[1], reverse=True):
            percentage = (cost / total_cost * 100) if total_cost > 0 else 0
            html += f"""
            <div class="cost-item">
                <span class="item-name">{model}</span>
                <span class="item-cost">${cost:.2f}</span>
                <span class="item-percentage">({percentage:.1f}%)</span>
            </div>
            """
        
        html += '</div></div></div>'
        return html
    
    def _generate_recommendations(self, test_summaries: List[TestSummary]) -> str:
        """Generate recommendations based on test results."""
        recommendations = []
        
        # Analyze overall performance
        total_tests = sum(s.total_test_cases for s in test_summaries)
        total_passed = sum(s.passed_cases for s in test_summaries)
        pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        if pass_rate < 75:
            recommendations.append({
                'type': 'performance',
                'priority': 'high',
                'title': 'Improve Overall Test Pass Rate',
                'description': f'Current pass rate of {pass_rate:.1f}% is below the recommended 75% threshold. Focus on addressing common failure patterns.'
            })
        
        # Analyze cost efficiency
        total_cost = sum(sum(s.cost_summary.values()) for s in test_summaries)
        if total_cost > 150:  # Assuming budget threshold
            recommendations.append({
                'type': 'cost',
                'priority': 'medium',
                'title': 'Optimize API Costs',
                'description': f'Total cost of ${total_cost:.2f} exceeds recommended budget. Consider using more cost-effective models for initial testing.'
            })
        
        # Analyze quality metrics
        all_scores = [s.average_scores for s in test_summaries if s.average_scores]
        if all_scores:
            avg_character_consistency = sum(s.character_consistency for s in all_scores) / len(all_scores)
            avg_cultural_accuracy = sum(s.cultural_accuracy for s in all_scores) / len(all_scores)
            
            if avg_character_consistency < 80:
                recommendations.append({
                    'type': 'quality',
                    'priority': 'high',
                    'title': 'Improve Character Consistency',
                    'description': f'Average character consistency of {avg_character_consistency:.1f}% is below the 80% target. Review character detection and tracking algorithms.'
                })
            
            if avg_cultural_accuracy < 70:
                recommendations.append({
                    'type': 'quality',
                    'priority': 'medium',
                    'title': 'Enhance Cultural Accuracy',
                    'description': f'Average cultural accuracy of {avg_cultural_accuracy:.1f}% is below the 70% target. Consider expanding cultural training data.'
                })
        
        html = '<div class="recommendations"><h2>Recommendations</h2>'
        
        if recommendations:
            for rec in recommendations:
                priority_class = f"priority-{rec['priority']}"
                html += f"""
                <div class="recommendation {priority_class}">
                    <div class="rec-header">
                        <span class="rec-type">{rec['type'].title()}</span>
                        <span class="rec-priority">{rec['priority'].title()} Priority</span>
                    </div>
                    <h4>{rec['title']}</h4>
                    <p>{rec['description']}</p>
                </div>
                """
        else:
            html += '<p class="no-recommendations">All metrics are within acceptable ranges. Continue monitoring performance trends.</p>'
        
        html += '</div>'
        return html
    
    def _extract_accuracy_trends(self, test_summaries: List[TestSummary]) -> Dict[str, Any]:
        """Extract accuracy trend data for visualization."""
        trends = {}
        for summary in test_summaries:
            for result in summary.detailed_results:
                if hasattr(result, 'accuracy_score') and hasattr(result, 'timestamp'):
                    model_name = getattr(result, 'model_name', 'unknown')
                    if model_name not in trends:
                        trends[model_name] = []
                    trends[model_name].append({
                        'timestamp': result.timestamp,
                        'accuracy': result.accuracy_score
                    })
        return trends
    
    def _extract_cost_data(self, test_summaries: List[TestSummary]) -> Dict[str, Any]:
        """Extract cost data for visualization."""
        cost_data = {}
        for summary in test_summaries:
            cost_data[summary.test_type] = sum(summary.cost_summary.values())
        return cost_data
    
    def _extract_model_performance(self, test_summaries: List[TestSummary]) -> Dict[str, Any]:
        """Extract model performance data for comparison."""
        performance = {}
        for summary in test_summaries:
            for result in summary.detailed_results:
                model_name = getattr(result, 'model_name', 'unknown')
                if model_name not in performance:
                    performance[model_name] = {'scores': [], 'costs': []}
                
                if hasattr(result, 'accuracy_score'):
                    performance[model_name]['scores'].append(result.accuracy_score)
                performance[model_name]['costs'].append(getattr(result, 'cost', 0))
        
        return performance
    
    def _extract_quality_metrics(self, test_summaries: List[TestSummary]) -> Dict[str, Any]:
        """Extract quality metrics for heatmap visualization."""
        metrics = {}
        for summary in test_summaries:
            if summary.average_scores:
                metrics[summary.test_type] = {
                    'character_consistency': summary.average_scores.character_consistency,
                    'scene_coherence': summary.average_scores.scene_coherence,
                    'cultural_accuracy': summary.average_scores.cultural_accuracy,
                    'overall_score': summary.average_scores.overall_score
                }
        return metrics
    
    def _generate_html_template(self, **sections) -> str:
        """Generate the complete HTML report template."""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Semantic Compression Testing Report</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Semantic Compression Testing Report</h1>
            <p class="report-date">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>
        
        {sections.get('executive_summary', '')}
        
        <div class="charts-section">
            <h2>Performance Visualizations</h2>
            {self._embed_charts(sections.get('charts', {}))}
        </div>
        
        {sections.get('test_summary', '')}
        {sections.get('model_comparison', '')}
        {sections.get('failure_analysis', '')}
        {sections.get('cost_analysis', '')}
        {sections.get('recommendations', '')}
        
        <footer>
            <p>Report generated by Semantic Compression Testing Framework</p>
        </footer>
    </div>
</body>
</html>
        """
    
    def _embed_charts(self, charts: Dict[str, str]) -> str:
        """Embed base64 encoded charts into HTML."""
        html = '<div class="charts-grid">'
        
        chart_titles = {
            'accuracy_trends': 'Accuracy Trends Over Time',
            'cost_analysis': 'Cost Analysis by Test Type',
            'model_comparison': 'Model Performance Comparison',
            'quality_heatmap': 'Quality Metrics Heatmap'
        }
        
        for chart_key, chart_data in charts.items():
            title = chart_titles.get(chart_key, chart_key.replace('_', ' ').title())
            html += f"""
            <div class="chart-container">
                <h3>{title}</h3>
                <img src="data:image/png;base64,{chart_data}" alt="{title}" class="chart-image">
            </div>
            """
        
        html += '</div>'
        return html
    
    def _get_css_styles(self) -> str:
        """Return CSS styles for the HTML report."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }
        
        header h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .report-date {
            color: #7f8c8d;
            font-style: italic;
        }
        
        .executive-summary {
            margin-bottom: 40px;
        }
        
        .summary-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #3498db;
        }
        
        .stat-card h3 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stat-value.success { color: #27ae60; }
        .stat-value.warning { color: #f39c12; }
        .stat-value.danger { color: #e74c3c; }
        
        .stat-detail {
            color: #7f8c8d;
            font-size: 0.9em;
        }
        
        .charts-section {
            margin: 40px 0;
        }
        
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-top: 20px;
        }
        
        .chart-container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .chart-container h3 {
            margin-bottom: 15px;
            color: #2c3e50;
        }
        
        .chart-image {
            width: 100%;
            height: auto;
            border-radius: 4px;
        }
        
        .test-summary, .model-comparison, .failure-analysis, .cost-analysis, .recommendations {
            margin: 40px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .test-type-summary {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 6px;
            border-left: 4px solid #3498db;
        }
        
        .test-metrics {
            margin-top: 10px;
        }
        
        .metric {
            display: inline-block;
            margin-right: 20px;
            color: #7f8c8d;
        }
        
        .model-rankings {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .model-rank {
            display: flex;
            align-items: center;
            background: white;
            padding: 15px;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .rank-number {
            font-size: 1.5em;
            font-weight: bold;
            color: #3498db;
            margin-right: 20px;
            min-width: 40px;
        }
        
        .model-details h4 {
            margin-bottom: 8px;
            color: #2c3e50;
        }
        
        .model-metrics .metric {
            margin-right: 15px;
            font-size: 0.9em;
        }
        
        .failure-rates, .failure-patterns, .cost-items {
            margin-top: 15px;
        }
        
        .failure-item, .pattern-item, .cost-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            margin: 5px 0;
            background: white;
            border-radius: 4px;
        }
        
        .failure-rate.danger { color: #e74c3c; font-weight: bold; }
        .failure-rate.warning { color: #f39c12; font-weight: bold; }
        
        .recommendation {
            background: white;
            padding: 20px;
            margin: 15px 0;
            border-radius: 6px;
            border-left: 4px solid #3498db;
        }
        
        .recommendation.priority-high { border-left-color: #e74c3c; }
        .recommendation.priority-medium { border-left-color: #f39c12; }
        .recommendation.priority-low { border-left-color: #27ae60; }
        
        .rec-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .rec-type { color: #7f8c8d; }
        .rec-priority { font-weight: bold; }
        
        .priority-high .rec-priority { color: #e74c3c; }
        .priority-medium .rec-priority { color: #f39c12; }
        .priority-low .rec-priority { color: #27ae60; }
        
        footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #7f8c8d;
        }
        
        @media (max-width: 768px) {
            .container { padding: 10px; }
            .summary-stats { grid-template-columns: 1fr; }
            .charts-grid { grid-template-columns: 1fr; }
            .model-rank { flex-direction: column; align-items: flex-start; }
            .rank-number { margin-bottom: 10px; }
        }
        """