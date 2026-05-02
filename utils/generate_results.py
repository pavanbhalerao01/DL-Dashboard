"""
Generate mock results for deep learning models trained on Retina dataset
"""
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, roc_curve, auc
import json
import os
from pathlib import Path

# Configuration
OPTIMIZERS = ['Adam', 'RMSprop', 'SGD']
LEARNING_RATES = [0.01, 0.001, 0.0001]
ALGORITHMS = [
    'CNN',
    'CNN + Augmentation',
    'ResNet50',
    'ResNet50 (Unfroze)',
    'VGG16',
    'VGG16 (Unfroze)',
    'AlexNet',
    'AlexNet (Unfroze)',
]

def generate_mock_metrics(base_accuracy=0.85):
    """Generate realistic mock metrics with variations"""
    # Add some randomness to make results realistic
    accuracy = np.random.normal(base_accuracy, 0.05)
    accuracy = np.clip(accuracy, 0.65, 0.99)
    
    precision = accuracy - np.random.uniform(0, 0.05)
    recall = accuracy - np.random.uniform(0, 0.05)
    f1 = 2 * (precision * recall) / (precision + recall + 1e-10)
    
    return {
        'accuracy': round(float(accuracy), 4),
        'precision': round(float(np.clip(precision, 0, 1)), 4),
        'recall': round(float(np.clip(recall, 0, 1)), 4),
        'f1': round(float(np.clip(f1, 0, 1)), 4),
    }

def generate_confusion_matrix(accuracy=0.85, num_classes=5):
    """Generate realistic confusion matrix"""
    # Create a base confusion matrix with high diagonal values
    cm = np.zeros((num_classes, num_classes))
    
    # Fill diagonal (correct predictions)
    for i in range(num_classes):
        cm[i, i] = int(100 * accuracy / num_classes * 5)
    
    # Add some misclassifications
    for i in range(num_classes):
        for j in range(num_classes):
            if i != j:
                cm[i, j] = np.random.randint(5, 20)
    
    # Normalize
    cm = cm.astype('float')
    cm = cm / cm.sum(axis=1, keepdims=True)
    return cm

def create_results_database():
    """Create a comprehensive results database"""
    results = {}
    
    for algo in ALGORITHMS:
        results[algo] = {}
        
        # Determine base accuracy based on algorithm
        base_acc = {
            'CNN': 0.82,
            'CNN + Augmentation': 0.87,
            'ResNet50': 0.89,
            'ResNet50 (Unfroze)': 0.91,
            'VGG16': 0.88,
            'VGG16 (Unfroze)': 0.90,
            'AlexNet': 0.80,
            'AlexNet (Unfroze)': 0.85,
        }.get(algo, 0.85)
        
        for opt in OPTIMIZERS:
            results[algo][opt] = {}
            for lr in LEARNING_RATES:
                # Higher learning rates might have slightly different results
                lr_factor = 1 - abs(np.log10(lr) + 2) * 0.02  # Small variation
                adjusted_acc = base_acc * lr_factor
                
                # Optimizer impact
                opt_factor = {
                    'Adam': 1.0,
                    'RMSprop': 0.98,
                    'SGD': 0.95,
                }.get(opt, 0.95)
                
                final_acc = adjusted_acc * opt_factor
                
                key = f"lr_{lr}"
                results[algo][opt][key] = {
                    **generate_mock_metrics(final_acc),
                    'optimizer': opt,
                    'learning_rate': lr,
                    'algorithm': algo,
                    'confusion_matrix': generate_confusion_matrix(final_acc).tolist(),
                }
    
    return results

BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results"

def save_results(results, filepath=None):
    """Save results to JSON file"""
    if filepath is None:
        filepath = RESULTS_DIR / "all_results.json"
    filepath = Path(filepath)
    os.makedirs(filepath.parent, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {filepath}")
    return filepath

def create_comparison_dataframe(results):
    """Create a pandas DataFrame for easy comparison"""
    data = []
    
    for algo, opt_dict in results.items():
        for opt, lr_dict in opt_dict.items():
            for lr_key, metrics in lr_dict.items():
                data.append({
                    'Algorithm': algo,
                    'Optimizer': opt,
                    'Learning Rate': metrics['learning_rate'],
                    'Accuracy': metrics['accuracy'],
                    'Precision': metrics['precision'],
                    'Recall': metrics['recall'],
                    'F1-Score': metrics['f1'],
                })
    
    df = pd.DataFrame(data)
    return df

def save_summary_stats(df, filepath=None):
    """Save summary statistics for dashboards"""
    if filepath is None:
        filepath = RESULTS_DIR / "summary_stats.json"
    filepath = Path(filepath)
    os.makedirs(filepath.parent, exist_ok=True)
    best_config = df.loc[df['Accuracy'].idxmax()].to_dict()
    summary_stats = {
        'Total Configurations': int(len(df)),
        'Total Algorithms': int(df['Algorithm'].nunique()),
        'Total Optimizers': int(df['Optimizer'].nunique()),
        'Total Learning Rates': int(df['Learning Rate'].nunique()),
        'Mean Accuracy': float(df['Accuracy'].mean()),
        'Best Accuracy': float(df['Accuracy'].max()),
        'Best Configuration': best_config,
    }
    with open(filepath, 'w') as f:
        json.dump(summary_stats, f, indent=2)
    print(f"Summary stats saved to {filepath}")
    return filepath

if __name__ == "__main__":
    print("Generating mock results for Retina dataset...")
    results = create_results_database()
    save_results(results)
    
    df = create_comparison_dataframe(results)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(RESULTS_DIR / "comparison.csv", index=False)
    print("Comparison CSV saved!")
    save_summary_stats(df)
    print("\nResults Summary:")
    print(df.groupby('Algorithm')[['Accuracy', 'Precision', 'Recall', 'F1-Score']].mean().round(4))
