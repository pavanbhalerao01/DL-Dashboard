"""
Create visualizations for deep learning model results
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay
import json
import os

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)

def load_results(filepath='d:\\VS Code\\Python\\DL\\results\\all_results.json'):
    """Load results from JSON"""
    with open(filepath, 'r') as f:
        return json.load(f)

def load_comparison_df(filepath='d:\\VS Code\\Python\\DL\\results\\comparison.csv'):
    """Load comparison dataframe"""
    return pd.read_csv(filepath)

def plot_accuracy_by_algorithm(df, save_path='d:\\VS Code\\Python\\DL\\results\\accuracy_by_algo.png'):
    """Plot accuracy comparison by algorithm"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    algo_accuracy = df.groupby('Algorithm')['Accuracy'].mean().sort_values(ascending=False)
    colors = plt.cm.viridis(np.linspace(0, 1, len(algo_accuracy)))
    
    bars = ax.bar(range(len(algo_accuracy)), algo_accuracy.values, color=colors, edgecolor='black', linewidth=1.5)
    ax.set_xticks(range(len(algo_accuracy)))
    ax.set_xticklabels(algo_accuracy.index, rotation=45, ha='right')
    ax.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
    ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
    ax.set_title('Average Accuracy by Algorithm', fontsize=14, fontweight='bold')
    ax.set_ylim([0.7, 0.95])
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    return save_path

def plot_optimizer_comparison(df, save_path='d:\\VS Code\\Python\\DL\\results\\optimizer_comparison.png'):
    """Plot optimizer comparison"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    opt_data = df.groupby('Optimizer')[['Accuracy', 'Precision', 'Recall', 'F1-Score']].mean()
    
    x = np.arange(len(opt_data.index))
    width = 0.2
    
    for i, metric in enumerate(['Accuracy', 'Precision', 'Recall', 'F1-Score']):
        ax.bar(x + i*width, opt_data[metric], width, label=metric, edgecolor='black', linewidth=1)
    
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(opt_data.index)
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_xlabel('Optimizer', fontsize=12, fontweight='bold')
    ax.set_title('Optimizer Performance Comparison', fontsize=14, fontweight='bold')
    ax.legend()
    ax.set_ylim([0.7, 1.0])
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    return save_path

def plot_learning_rate_impact(df, save_path='d:\\VS Code\\Python\\DL\\results\\lr_impact.png'):
    """Plot learning rate impact"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    lr_data = df.groupby('Learning Rate')[['Accuracy', 'Precision', 'Recall', 'F1-Score']].mean()
    
    x = np.arange(len(lr_data.index))
    width = 0.2
    
    for i, metric in enumerate(['Accuracy', 'Precision', 'Recall', 'F1-Score']):
        ax.bar(x + i*width, lr_data[metric], width, label=metric, edgecolor='black', linewidth=1)
    
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels([f'{lr:.4f}' for lr in lr_data.index])
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_xlabel('Learning Rate', fontsize=12, fontweight='bold')
    ax.set_title('Learning Rate Impact on Performance', fontsize=14, fontweight='bold')
    ax.legend()
    ax.set_ylim([0.7, 1.0])
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    return save_path

def plot_heatmap_accuracy(df, save_path='d:\\VS Code\\Python\\DL\\results\\accuracy_heatmap.png'):
    """Plot accuracy heatmap for algorithm vs optimizer"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    pivot_df = df.pivot_table(values='Accuracy', index='Algorithm', columns='Optimizer', aggfunc='mean')
    
    sns.heatmap(pivot_df, annot=True, fmt='.4f', cmap='RdYlGn', center=0.85, 
                cbar_kws={'label': 'Accuracy'}, ax=ax, linewidths=0.5, linecolor='gray')
    
    ax.set_title('Accuracy Heatmap: Algorithm vs Optimizer', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylabel('Algorithm', fontsize=12, fontweight='bold')
    ax.set_xlabel('Optimizer', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    return save_path

def plot_all_metrics_comparison(df, save_path='d:\\VS Code\\Python\\DL\\results\\all_metrics.png'):
    """Plot all metrics comparison"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('All Metrics Comparison by Algorithm', fontsize=16, fontweight='bold', y=1.00)
    
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    axes = axes.flatten()
    
    for idx, metric in enumerate(metrics):
        algo_metric = df.groupby('Algorithm')[metric].mean().sort_values(ascending=False)
        colors = plt.cm.viridis(np.linspace(0, 1, len(algo_metric)))
        
        bars = axes[idx].bar(range(len(algo_metric)), algo_metric.values, color=colors, 
                             edgecolor='black', linewidth=1)
        axes[idx].set_xticks(range(len(algo_metric)))
        axes[idx].set_xticklabels(algo_metric.index, rotation=45, ha='right', fontsize=9)
        axes[idx].set_ylabel(metric, fontsize=11, fontweight='bold')
        axes[idx].set_title(f'{metric} by Algorithm', fontsize=12, fontweight='bold')
        axes[idx].set_ylim([0.7, 1.0])
        
        for bar in bars:
            height = bar.get_height()
            axes[idx].text(bar.get_x() + bar.get_width()/2., height,
                          f'{height:.3f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    return save_path

def plot_confusion_matrix_samples(results, save_dir='d:\\VS Code\\Python\\DL\\results'):
    """Plot sample confusion matrices for best performing models"""
    os.makedirs(save_dir, exist_ok=True)
    
    df = load_comparison_df()
    
    # Get top 3 performing configurations
    top_configs = df.nlargest(3, 'Accuracy')
    
    for idx, (_, row) in enumerate(top_configs.iterrows()):
        algo = row['Algorithm']
        opt = row['Optimizer']
        lr = row['Learning Rate']
        
        # Load actual confusion matrix from results
        try:
            cm = results[algo][opt][f'lr_{lr}']['confusion_matrix']
            cm = np.array(cm)
            
            fig, ax = plt.subplots(figsize=(8, 6))
            im = ax.imshow(cm, cmap='Blues', aspect='auto')
            
            # Add labels
            class_names = ['Class 0', 'Class 1', 'Class 2', 'Class 3', 'Class 4']
            ax.set_xticks(range(len(class_names)))
            ax.set_yticks(range(len(class_names)))
            ax.set_xticklabels(class_names)
            ax.set_yticklabels(class_names)
            
            # Add text annotations
            for i in range(len(class_names)):
                for j in range(len(class_names)):
                    text = ax.text(j, i, f'{cm[i, j]:.2f}',
                                  ha="center", va="center", color="black", fontsize=10, fontweight='bold')
            
            ax.set_xlabel('Predicted Label', fontsize=12, fontweight='bold')
            ax.set_ylabel('True Label', fontsize=12, fontweight='bold')
            ax.set_title(f'Confusion Matrix: {algo}\n({opt}, LR={lr})', fontsize=12, fontweight='bold')
            
            plt.colorbar(im, ax=ax, label='Normalized Count')
            plt.tight_layout()
            plt.savefig(f'{save_dir}\\cm_{idx+1}_{algo.replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
            plt.close()
        except Exception as e:
            print(f"Error plotting confusion matrix for {algo}: {e}")

def plot_model_ranking(df, save_path='d:\\VS Code\\Python\\DL\\results\\model_ranking.png'):
    """Plot top performing models"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Calculate composite score
    df['Composite_Score'] = (df['Accuracy'] * 0.4 + df['Precision'] * 0.2 + 
                              df['Recall'] * 0.2 + df['F1-Score'] * 0.2)
    
    top_models = df.nlargest(15, 'Composite_Score').sort_values('Composite_Score', ascending=True)
    top_models['Config'] = (top_models['Algorithm'] + '\n' + 
                            top_models['Optimizer'] + '\n' + 
                            'LR: ' + top_models['Learning Rate'].astype(str))
    
    colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(top_models)))
    bars = ax.barh(range(len(top_models)), top_models['Composite_Score'].values, 
                   color=colors, edgecolor='black', linewidth=1.5)
    
    ax.set_yticks(range(len(top_models)))
    ax.set_yticklabels(top_models['Config'].values, fontsize=9)
    ax.set_xlabel('Composite Score', fontsize=12, fontweight='bold')
    ax.set_title('Top 15 Model Configurations', fontsize=14, fontweight='bold')
    ax.set_xlim([0.8, 0.95])
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.4f}', ha='left', va='center', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    return save_path

def create_all_visualizations():
    """Create all visualizations"""
    print("Loading results...")
    results = load_results()
    df = load_comparison_df()
    
    print("Creating visualizations...")
    viz_paths = {
        'accuracy_by_algo': plot_accuracy_by_algorithm(df),
        'optimizer_comparison': plot_optimizer_comparison(df),
        'lr_impact': plot_learning_rate_impact(df),
        'accuracy_heatmap': plot_heatmap_accuracy(df),
        'all_metrics': plot_all_metrics_comparison(df),
        'model_ranking': plot_model_ranking(df),
    }
    
    plot_confusion_matrix_samples(results)
    
    print("All visualizations created successfully!")
    for name, path in viz_paths.items():
        print(f"  ✓ {name}: {path}")
    
    return viz_paths

if __name__ == "__main__":
    create_all_visualizations()
