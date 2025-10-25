"""
Visualization engine for semantic compression testing framework.

This module provides comprehensive data visualization capabilities using matplotlib
for creating charts, graphs, and dashboards to analyze test results and performance trends.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server environments

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import base64
from io import BytesIO
import pandas as pd


class VisualizationEngine:
    """
    Creates various visualizations for semantic compression testing results.
    """
    
    def __init__(self):
        """Initialize the visualization engine with styling."""
        # Set style for better-looking plots
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Configure matplotlib for better rendering
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
        
    def create_accuracy_trends_chart(self, accuracy_data: Dict[str, List[Dict[str, Any]]]) -> str:
        """
        Create line chart showing accuracy trends over time by model.
        
        Args:
            accuracy_data: Dictionary with model names as keys and list of 
                         {timestamp, accuracy} dictionaries as values
                         
        Returns:
            Base64 encoded PNG image string
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(accuracy_data)))
        
        for i, (model_name, data_points) in enumerate(accuracy_data.items()):
            if not data_points:
                continue
                
            # Sort by timestamp
            data_points = sorted(data_points, key=lambda x: x['timestamp'])
            
            timestamps = [point['timestamp'] for point in data_points]
            accuracies = [point['accuracy'] for point in data_points]
            
            ax.plot(timestamps, accuracies, 
                   marker='o', linewidth=2, markersize=6,
                   label=model_name.replace('_', ' ').title(),
                   color=colors[i])
        
        ax.set_title('Accuracy Trends Over Time by Model', fontsize=16, fontweight='bold')
        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('Accuracy Score (0-10)', fontsize=12)
        ax.set_ylim(0, 10)
        ax.grid(True, alpha=0.3)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
        plt.xticks(rotation=45)
        
        # Add target line
        ax.axhline(y=7.5, color='red', linestyle='--', alpha=0.7, label='Target (7.5)')
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_cost_analysis_chart(self, cost_data: Dict[str, float]) -> str:
        """
        Create pie chart and bar chart for cost analysis by test type.
        
        Args:
            cost_data: Dictionary with test types as keys and costs as values
            
        Returns:
            Base64 encoded PNG image string
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        test_types = list(cost_data.keys())
        costs = list(cost_data.values())
        total_cost = sum(costs)
        
        # Pie chart
        colors = plt.cm.Set3(np.linspace(0, 1, len(test_types)))
        wedges, texts, autotexts = ax1.pie(costs, labels=[t.replace('_', ' ').title() for t in test_types], 
                                          autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('Cost Distribution by Test Type', fontsize=14, fontweight='bold')
        
        # Bar chart with cost per test type
        bars = ax2.bar(range(len(test_types)), costs, color=colors)
        ax2.set_title('Cost Breakdown by Test Type', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Test Type', fontsize=12)
        ax2.set_ylabel('Cost ($)', fontsize=12)
        ax2.set_xticks(range(len(test_types)))
        ax2.set_xticklabels([t.replace('_', ' ').title() for t in test_types], rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, cost in zip(bars, costs):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'${cost:.2f}', ha='center', va='bottom', fontweight='bold')
        
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_model_comparison_chart(self, model_data: Dict[str, Dict[str, List[float]]]) -> str:
        """
        Create radar chart comparing model performance across different metrics.
        
        Args:
            model_data: Dictionary with model names as keys and performance data as values
            
        Returns:
            Base64 encoded PNG image string
        """
        fig, ax = plt.subplots(figsize=(12, 10), subplot_kw=dict(projection='polar'))
        
        # Calculate average scores for each model
        model_averages = {}
        for model_name, data in model_data.items():
            avg_accuracy = np.mean(data['scores']) if data['scores'] else 0
            avg_cost = np.mean(data['costs']) if data['costs'] else 0
            
            # Normalize cost (invert so lower cost = higher score)
            max_cost = max([np.mean(d['costs']) if d['costs'] else 0 for d in model_data.values()])
            normalized_cost = (max_cost - avg_cost) / max_cost * 10 if max_cost > 0 else 5
            
            model_averages[model_name] = {
                'accuracy': avg_accuracy,
                'cost_efficiency': normalized_cost,
                'reliability': min(avg_accuracy, 8),  # Placeholder for reliability metric
                'speed': 7  # Placeholder for speed metric
            }
        
        # Set up radar chart
        categories = ['Accuracy', 'Cost Efficiency', 'Reliability', 'Speed']
        N = len(categories)
        
        # Compute angle for each category
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Complete the circle
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(model_averages)))
        
        for i, (model_name, metrics) in enumerate(model_averages.items()):
            values = [metrics['accuracy'], metrics['cost_efficiency'], 
                     metrics['reliability'], metrics['speed']]
            values += values[:1]  # Complete the circle
            
            ax.plot(angles, values, 'o-', linewidth=2, 
                   label=model_name.replace('_', ' ').title(), color=colors[i])
            ax.fill(angles, values, alpha=0.25, color=colors[i])
        
        # Customize the chart
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 10)
        ax.set_title('Model Performance Comparison\n(Radar Chart)', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        ax.grid(True)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_quality_heatmap(self, quality_data: Dict[str, Dict[str, float]]) -> str:
        """
        Create heatmap showing quality metrics across different test types.
        
        Args:
            quality_data: Dictionary with test types as keys and quality metrics as values
            
        Returns:
            Base64 encoded PNG image string
        """
        if not quality_data:
            # Create empty heatmap if no data
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, 'No quality data available', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=16)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            return self._fig_to_base64(fig)
        
        # Prepare data for heatmap
        test_types = list(quality_data.keys())
        metrics = ['character_consistency', 'scene_coherence', 'cultural_accuracy', 'overall_score']
        
        # Create matrix
        data_matrix = []
        for test_type in test_types:
            row = []
            for metric in metrics:
                value = quality_data[test_type].get(metric, 0)
                row.append(value)
            data_matrix.append(row)
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(12, 8))
        
        im = ax.imshow(data_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
        
        # Set ticks and labels
        ax.set_xticks(np.arange(len(metrics)))
        ax.set_yticks(np.arange(len(test_types)))
        ax.set_xticklabels([m.replace('_', ' ').title() for m in metrics])
        ax.set_yticklabels([t.replace('_', ' ').title() for t in test_types])
        
        # Rotate the tick labels and set their alignment
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Add colorbar
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel('Quality Score (%)', rotation=-90, va="bottom")
        
        # Add text annotations
        for i in range(len(test_types)):
            for j in range(len(metrics)):
                text = ax.text(j, i, f'{data_matrix[i][j]:.1f}%',
                             ha="center", va="center", color="black", fontweight='bold')
        
        ax.set_title('Quality Metrics Heatmap by Test Type', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_budget_utilization_chart(self, budget_data: Dict[str, Dict[str, float]]) -> str:
        """
        Create stacked bar chart showing budget utilization by test type and model.
        
        Args:
            budget_data: Dictionary with test types and their budget breakdown by model
            
        Returns:
            Base64 encoded PNG image string
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        
        test_types = list(budget_data.keys())
        all_models = set()
        for test_data in budget_data.values():
            all_models.update(test_data.keys())
        all_models = sorted(list(all_models))
        
        # Prepare data for stacked bar chart
        bottom = np.zeros(len(test_types))
        colors = plt.cm.Set3(np.linspace(0, 1, len(all_models)))
        
        for i, model in enumerate(all_models):
            values = []
            for test_type in test_types:
                values.append(budget_data[test_type].get(model, 0))
            
            ax.bar(test_types, values, bottom=bottom, 
                  label=model.replace('_', ' ').title(), color=colors[i])
            bottom += values
        
        ax.set_title('Budget Utilization by Test Type and Model', fontsize=16, fontweight='bold')
        ax.set_xlabel('Test Type', fontsize=12)
        ax.set_ylabel('Cost ($)', fontsize=12)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Rotate x-axis labels
        plt.xticks(rotation=45, ha='right')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_cultural_adaptation_chart(self, cultural_data: Dict[str, Dict[str, float]]) -> str:
        """
        Create grouped bar chart showing cultural adaptation success rates.
        
        Args:
            cultural_data: Dictionary with cultures as keys and approval ratings as values
            
        Returns:
            Base64 encoded PNG image string
        """
        if not cultural_data:
            # Create placeholder chart if no data
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, 'No cultural adaptation data available', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=16)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            return self._fig_to_base64(fig)
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        cultures = list(cultural_data.keys())
        metrics = list(next(iter(cultural_data.values())).keys())
        
        x = np.arange(len(cultures))
        width = 0.8 / len(metrics)
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(metrics)))
        
        for i, metric in enumerate(metrics):
            values = [cultural_data[culture].get(metric, 0) for culture in cultures]
            offset = (i - len(metrics)/2 + 0.5) * width
            bars = ax.bar(x + offset, values, width, 
                         label=metric.replace('_', ' ').title(), color=colors[i])
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{value:.1f}%', ha='center', va='bottom', fontsize=9)
        
        ax.set_title('Cultural Adaptation Success Rates', fontsize=16, fontweight='bold')
        ax.set_xlabel('Target Culture', fontsize=12)
        ax.set_ylabel('Approval Rating (%)', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(cultures)
        ax.legend()
        ax.set_ylim(0, 100)
        
        # Add target line
        ax.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='Target (70%)')
        
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_character_consistency_trends(self, consistency_data: Dict[str, List[Dict[str, Any]]]) -> str:
        """
        Create line chart showing character consistency trends across test cycles.
        
        Args:
            consistency_data: Dictionary with test IDs and consistency measurements over time
            
        Returns:
            Base64 encoded PNG image string
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(consistency_data)))
        
        for i, (test_id, data_points) in enumerate(consistency_data.items()):
            if not data_points:
                continue
                
            cycles = [point.get('cycle', i) for i, point in enumerate(data_points)]
            consistency_scores = [point.get('consistency', 0) for point in data_points]
            
            ax.plot(cycles, consistency_scores, 
                   marker='o', linewidth=2, markersize=6,
                   label=f'Test {test_id}', color=colors[i])
        
        ax.set_title('Character Consistency Across Regeneration Cycles', fontsize=16, fontweight='bold')
        ax.set_xlabel('Regeneration Cycle', fontsize=12)
        ax.set_ylabel('Character Consistency (%)', fontsize=12)
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Add target line
        ax.axhline(y=80, color='red', linestyle='--', alpha=0.7, label='Target (80%)')
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_semantic_completeness_distribution(self, completeness_data: List[float]) -> str:
        """
        Create histogram showing distribution of semantic completeness scores.
        
        Args:
            completeness_data: List of semantic completeness percentages
            
        Returns:
            Base64 encoded PNG image string
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Histogram
        ax1.hist(completeness_data, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_title('Semantic Completeness Distribution', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Completeness (%)', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.axvline(x=85, color='red', linestyle='--', alpha=0.7, label='Target (85%)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Box plot
        ax2.boxplot(completeness_data, vert=True, patch_artist=True,
                   boxprops=dict(facecolor='lightblue', alpha=0.7))
        ax2.set_title('Semantic Completeness Box Plot', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Completeness (%)', fontsize=12)
        ax2.axhline(y=85, color='red', linestyle='--', alpha=0.7, label='Target (85%)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Add statistics
        mean_val = np.mean(completeness_data)
        median_val = np.median(completeness_data)
        std_val = np.std(completeness_data)
        
        stats_text = f'Mean: {mean_val:.1f}%\nMedian: {median_val:.1f}%\nStd: {std_val:.1f}%'
        ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_compression_ratio_analysis(self, compression_data: Dict[str, List[float]]) -> str:
        """
        Create chart analyzing compression ratios achieved by different methods.
        
        Args:
            compression_data: Dictionary with compression methods and their achieved ratios
            
        Returns:
            Base64 encoded PNG image string
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        methods = list(compression_data.keys())
        ratios_data = list(compression_data.values())
        
        # Create violin plot
        parts = ax.violinplot(ratios_data, positions=range(len(methods)), showmeans=True, showmedians=True)
        
        # Customize violin plot colors
        colors = plt.cm.Set3(np.linspace(0, 1, len(methods)))
        for pc, color in zip(parts['bodies'], colors):
            pc.set_facecolor(color)
            pc.set_alpha(0.7)
        
        ax.set_title('Compression Ratio Analysis by Method', fontsize=16, fontweight='bold')
        ax.set_xlabel('Compression Method', fontsize=12)
        ax.set_ylabel('Compression Ratio', fontsize=12)
        ax.set_xticks(range(len(methods)))
        ax.set_xticklabels([m.replace('_', ' ').title() for m in methods])
        
        # Add target line
        ax.axhline(y=500, color='red', linestyle='--', alpha=0.7, label='Target (500:1)')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _fig_to_base64(self, fig) -> str:
        """
        Convert matplotlib figure to base64 encoded string.
        
        Args:
            fig: Matplotlib figure object
            
        Returns:
            Base64 encoded PNG image string
        """
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close(fig)  # Close figure to free memory
        
        graphic = base64.b64encode(image_png)
        return graphic.decode('utf-8')
    
    def create_dashboard_summary(self, 
                               accuracy_data: Dict[str, List[Dict[str, Any]]],
                               cost_data: Dict[str, float],
                               quality_data: Dict[str, Dict[str, float]]) -> str:
        """
        Create a comprehensive dashboard with multiple charts in one figure.
        
        Args:
            accuracy_data: Accuracy trends data
            cost_data: Cost analysis data
            quality_data: Quality metrics data
            
        Returns:
            Base64 encoded PNG image string
        """
        fig = plt.figure(figsize=(20, 12))
        
        # Create subplots
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
        
        # Accuracy trends (top left)
        ax1 = fig.add_subplot(gs[0, 0])
        if accuracy_data:
            for model_name, data_points in accuracy_data.items():
                if data_points:
                    timestamps = [point['timestamp'] for point in data_points]
                    accuracies = [point['accuracy'] for point in data_points]
                    ax1.plot(timestamps, accuracies, marker='o', label=model_name.replace('_', ' ').title())
        ax1.set_title('Accuracy Trends', fontweight='bold')
        ax1.set_ylabel('Accuracy Score')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Cost analysis (top middle)
        ax2 = fig.add_subplot(gs[0, 1])
        if cost_data:
            test_types = list(cost_data.keys())
            costs = list(cost_data.values())
            ax2.pie(costs, labels=[t.replace('_', ' ').title() for t in test_types], autopct='%1.1f%%')
        ax2.set_title('Cost Distribution', fontweight='bold')
        
        # Quality heatmap (top right)
        ax3 = fig.add_subplot(gs[0, 2])
        if quality_data:
            test_types = list(quality_data.keys())
            metrics = ['character_consistency', 'scene_coherence', 'cultural_accuracy', 'overall_score']
            data_matrix = []
            for test_type in test_types:
                row = [quality_data[test_type].get(metric, 0) for metric in metrics]
                data_matrix.append(row)
            
            im = ax3.imshow(data_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
            ax3.set_xticks(range(len(metrics)))
            ax3.set_yticks(range(len(test_types)))
            ax3.set_xticklabels([m.replace('_', ' ').title() for m in metrics], rotation=45)
            ax3.set_yticklabels([t.replace('_', ' ').title() for t in test_types])
        ax3.set_title('Quality Metrics', fontweight='bold')
        
        # Summary statistics (bottom span)
        ax4 = fig.add_subplot(gs[1, :])
        ax4.axis('off')
        
        # Calculate summary statistics
        total_cost = sum(cost_data.values()) if cost_data else 0
        avg_accuracy = 0
        if accuracy_data:
            all_accuracies = []
            for data_points in accuracy_data.values():
                all_accuracies.extend([point['accuracy'] for point in data_points])
            avg_accuracy = np.mean(all_accuracies) if all_accuracies else 0
        
        summary_text = f"""
        DASHBOARD SUMMARY
        
        Total Cost: ${total_cost:.2f}
        Average Accuracy: {avg_accuracy:.1f}/10
        Test Types Analyzed: {len(cost_data) if cost_data else 0}
        Models Compared: {len(accuracy_data) if accuracy_data else 0}
        
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        ax4.text(0.5, 0.5, summary_text, ha='center', va='center', 
                fontsize=14, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.suptitle('Semantic Compression Testing Dashboard', fontsize=20, fontweight='bold')
        return self._fig_to_base64(fig)