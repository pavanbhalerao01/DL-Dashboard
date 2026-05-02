"""
Streamlit Dashboard for Deep Learning Model Comparison on Retina Dataset
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import sys
from pathlib import Path

# Page Configuration
st.set_page_config(
    page_title="DL Model Comparison - Retina Dataset",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to match Google Colab style
st.markdown("""
    <style>
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f5f5f5;
        color: #000000;
    }
    .main {
        background-color: #ffffff;
    }
    .stMarkdown, .stText, .stCaption, .stDataFrame, .stTable {
        color: #000000;
    }
    h1, h2, h3 {
        color: #1a73e8;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 8px;
        color: white;
        margin: 10px 0;
    }
    .stMetric {
        background-color: #f9f9f9;
        padding: 10px;
        border-radius: 5px;
    }
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricDelta"] {
        color: #000000;
    }
    section[data-testid="stSidebar"] * {
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# Title with logo
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.markdown("🧠")
with col2:
    st.title("Deep Learning Model Comparison Dashboard")
    st.markdown("### Retina Dataset Analysis with Multiple Architectures, Optimizers & Learning Rates")

st.markdown("---")

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Load data
@st.cache_data
def load_data():
    results_path = BASE_DIR / "results"
    results_path.mkdir(parents=True, exist_ok=True)
    
    comparison_path = results_path / "comparison.csv"
    results_json_path = results_path / "all_results.json"
    summary_path = results_path / "summary_stats.json"
    
    if not (comparison_path.exists() and results_json_path.exists() and summary_path.exists()):
        from utils.generate_results import (
            create_results_database,
            create_comparison_dataframe,
            save_results,
            save_summary_stats,
        )
        
        results = create_results_database()
        save_results(results, results_json_path)
        df = create_comparison_dataframe(results)
        df.to_csv(comparison_path, index=False)
        save_summary_stats(df, summary_path)
    
    # Load comparison dataframe
    df = pd.read_csv(comparison_path)
    
    # Load results JSON
    with open(results_json_path, 'r') as f:
        results = json.load(f)
    
    # Load summary stats
    with open(summary_path, 'r') as f:
        summary = json.load(f)
    
    return df, results, summary

try:
    comparison_df, all_results, summary_stats = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Please run the data generation script first: `python utils/generate_results.py`")
    st.stop()

# Sidebar Navigation
with st.sidebar:
    st.markdown("## 🗂️ Navigation")
    page = st.radio("Select View:", [
        "📊 Overview",
        "🎯 Algorithm Comparison",
        "⚙️ Optimizer Analysis",
        "📈 Learning Rate Impact",
        "🔥 Top Configurations",
        "🗺️ Heatmaps",
        "🎲 Confusion Matrices",
        "📋 Detailed Results"
    ])
    
    st.markdown("---")
    st.markdown("## 📌 Filters")
    
    selected_algorithms = st.multiselect(
        "Select Algorithms:",
        options=sorted(comparison_df['Algorithm'].unique()),
        default=sorted(comparison_df['Algorithm'].unique())
    )
    
    selected_optimizers = st.multiselect(
        "Select Optimizers:",
        options=sorted(comparison_df['Optimizer'].unique()),
        default=sorted(comparison_df['Optimizer'].unique())
    )
    
    selected_lrs = st.multiselect(
        "Select Learning Rates:",
        options=sorted(comparison_df['Learning Rate'].unique()),
        default=sorted(comparison_df['Learning Rate'].unique())
    )
    
    # Apply filters
    filtered_df = comparison_df[
        (comparison_df['Algorithm'].isin(selected_algorithms)) &
        (comparison_df['Optimizer'].isin(selected_optimizers)) &
        (comparison_df['Learning Rate'].isin(selected_lrs))
    ]
    
    st.markdown("---")
    st.markdown(f"### 📊 Data Summary")
    st.metric("Configurations", len(filtered_df))
    st.metric("Algorithms", len(selected_algorithms))
    st.metric("Optimizers", len(selected_optimizers))

# PAGE 1: OVERVIEW
if page == "📊 Overview":
    st.markdown("## 📊 Overview Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📈 Mean Accuracy",
            f"{filtered_df['Accuracy'].mean():.4f}",
            f"{(filtered_df['Accuracy'].mean() - 0.80)*100:.2f}% vs baseline"
        )
    
    with col2:
        st.metric(
            "🏆 Best Accuracy",
            f"{filtered_df['Accuracy'].max():.4f}",
            filtered_df.loc[filtered_df['Accuracy'].idxmax(), 'Algorithm']
        )
    
    with col3:
        st.metric(
            "📊 Mean Precision",
            f"{filtered_df['Precision'].mean():.4f}",
            f"±{filtered_df['Precision'].std():.4f}"
        )
    
    with col4:
        st.metric(
            "🎯 Mean F1-Score",
            f"{filtered_df['F1-Score'].mean():.4f}",
            f"±{filtered_df['F1-Score'].std():.4f}"
        )
    
    st.markdown("---")
    
    # Performance by metric
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 5))
        metrics_summary = filtered_df[['Accuracy', 'Precision', 'Recall', 'F1-Score']].mean()
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        bars = ax.bar(metrics_summary.index, metrics_summary.values, color=colors, edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Score', fontsize=11, fontweight='bold')
        ax.set_title('Average Performance Metrics', fontsize=12, fontweight='bold')
        ax.set_ylim([0.7, 1.0])
        ax.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.4f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("### 📋 Top 5 Configurations")
        top_5 = filtered_df.nlargest(5, 'Accuracy')[['Algorithm', 'Optimizer', 'Learning Rate', 'Accuracy']]
        st.dataframe(top_5, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### 📊 Distribution of Accuracy")
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.hist(filtered_df['Accuracy'], bins=30, color='#1a73e8', edgecolor='black', alpha=0.7)
    ax.set_xlabel('Accuracy', fontsize=11, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
    ax.set_title('Distribution of Model Accuracies', fontsize=12, fontweight='bold')
    ax.axvline(filtered_df['Accuracy'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
    ax.axvline(filtered_df['Accuracy'].median(), color='green', linestyle='--', linewidth=2, label='Median')
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

# PAGE 2: ALGORITHM COMPARISON
elif page == "🎯 Algorithm Comparison":
    st.markdown("## 🎯 Algorithm Performance Comparison")
    
    # Algorithm metrics
    algo_stats = filtered_df.groupby('Algorithm')[['Accuracy', 'Precision', 'Recall', 'F1-Score']].agg(['mean', 'std', 'min', 'max'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        algo_accuracy = filtered_df.groupby('Algorithm')['Accuracy'].mean().sort_values(ascending=False)
        colors = plt.cm.viridis(np.linspace(0, 1, len(algo_accuracy)))
        bars = ax.bar(range(len(algo_accuracy)), algo_accuracy.values, color=colors, edgecolor='black', linewidth=1.5)
        ax.set_xticks(range(len(algo_accuracy)))
        ax.set_xticklabels(algo_accuracy.index, rotation=45, ha='right')
        ax.set_ylabel('Accuracy', fontsize=11, fontweight='bold')
        ax.set_title('Average Accuracy by Algorithm', fontsize=12, fontweight='bold')
        ax.set_ylim([0.7, 0.95])
        ax.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.4f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        algo_data = filtered_df.groupby('Algorithm')[['Accuracy', 'Precision', 'Recall', 'F1-Score']].mean()
        algo_data.plot(kind='bar', ax=ax, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'], edgecolor='black', linewidth=1)
        ax.set_ylabel('Score', fontsize=11, fontweight='bold')
        ax.set_xlabel('Algorithm', fontsize=11, fontweight='bold')
        ax.set_title('All Metrics by Algorithm', fontsize=12, fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.legend(['Accuracy', 'Precision', 'Recall', 'F1-Score'], loc='lower right')
        ax.set_ylim([0.7, 1.0])
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    st.markdown("---")
    st.markdown("### 📊 Algorithm Statistics")
    
    # Format the display
    for algo in sorted(filtered_df['Algorithm'].unique()):
        algo_data = filtered_df[filtered_df['Algorithm'] == algo]
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(f"{algo} - Accuracy", f"{algo_data['Accuracy'].mean():.4f}", 
                     f"σ={algo_data['Accuracy'].std():.4f}")
        with col2:
            st.metric(f"Precision", f"{algo_data['Precision'].mean():.4f}",
                     f"σ={algo_data['Precision'].std():.4f}")
        with col3:
            st.metric(f"Recall", f"{algo_data['Recall'].mean():.4f}",
                     f"σ={algo_data['Recall'].std():.4f}")
        with col4:
            st.metric(f"F1-Score", f"{algo_data['F1-Score'].mean():.4f}",
                     f"σ={algo_data['F1-Score'].std():.4f}")

# PAGE 3: OPTIMIZER ANALYSIS
elif page == "⚙️ Optimizer Analysis":
    st.markdown("## ⚙️ Optimizer Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        opt_data = filtered_df.groupby('Optimizer')[['Accuracy', 'Precision', 'Recall', 'F1-Score']].mean()
        x = np.arange(len(opt_data.index))
        width = 0.2
        colors_metrics = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        
        for i, (metric, color) in enumerate(zip(['Accuracy', 'Precision', 'Recall', 'F1-Score'], colors_metrics)):
            ax.bar(x + i*width, opt_data[metric], width, label=metric, color=color, edgecolor='black', linewidth=0.8)
        
        ax.set_xticks(x + width * 1.5)
        ax.set_xticklabels(opt_data.index, fontsize=11, fontweight='bold')
        ax.set_ylabel('Score', fontsize=11, fontweight='bold')
        ax.set_title('Optimizer Performance Comparison', fontsize=12, fontweight='bold')
        ax.legend()
        ax.set_ylim([0.7, 1.0])
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        opt_accuracy = filtered_df.groupby('Optimizer')['Accuracy'].apply(list)
        ax.boxplot([opt_accuracy[opt] for opt in opt_accuracy.index], labels=opt_accuracy.index)
        ax.set_ylabel('Accuracy', fontsize=11, fontweight='bold')
        ax.set_title('Accuracy Distribution by Optimizer', fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    st.markdown("---")
    st.markdown("### 📊 Optimizer Statistics")
    optimizer_stats = filtered_df.groupby('Optimizer')[['Accuracy', 'Precision', 'Recall', 'F1-Score']].agg(['mean', 'std', 'min', 'max'])
    st.dataframe(optimizer_stats, use_container_width=True)

# PAGE 4: LEARNING RATE IMPACT
elif page == "📈 Learning Rate Impact":
    st.markdown("## 📈 Learning Rate Impact on Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        lr_data = filtered_df.groupby('Learning Rate')[['Accuracy', 'Precision', 'Recall', 'F1-Score']].mean()
        x = np.arange(len(lr_data.index))
        width = 0.2
        colors_metrics = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        
        for i, (metric, color) in enumerate(zip(['Accuracy', 'Precision', 'Recall', 'F1-Score'], colors_metrics)):
            ax.bar(x + i*width, lr_data[metric], width, label=metric, color=color, edgecolor='black', linewidth=0.8)
        
        ax.set_xticks(x + width * 1.5)
        ax.set_xticklabels([f'{lr:.4f}' for lr in lr_data.index], fontsize=10)
        ax.set_ylabel('Score', fontsize=11, fontweight='bold')
        ax.set_xlabel('Learning Rate', fontsize=11, fontweight='bold')
        ax.set_title('Learning Rate Impact', fontsize=12, fontweight='bold')
        ax.legend()
        ax.set_ylim([0.7, 1.0])
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        lr_accuracy = filtered_df.groupby('Learning Rate')['Accuracy'].apply(list)
        ax.boxplot([lr_accuracy[lr] for lr in sorted(lr_accuracy.index)], 
                  labels=[f'{lr:.4f}' for lr in sorted(lr_accuracy.index)])
        ax.set_ylabel('Accuracy', fontsize=11, fontweight='bold')
        ax.set_title('Accuracy Distribution by Learning Rate', fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    st.markdown("---")
    st.markdown("### 📊 Learning Rate Statistics")
    lr_stats = filtered_df.groupby('Learning Rate')[['Accuracy', 'Precision', 'Recall', 'F1-Score']].agg(['mean', 'std', 'min', 'max'])
    st.dataframe(lr_stats, use_container_width=True)

# PAGE 5: TOP CONFIGURATIONS
elif page == "🔥 Top Configurations":
    st.markdown("## 🔥 Top Performing Configurations")
    
    # Calculate composite score
    df_copy = filtered_df.copy()
    df_copy['Composite_Score'] = (df_copy['Accuracy'] * 0.4 + df_copy['Precision'] * 0.2 + 
                                   df_copy['Recall'] * 0.2 + df_copy['F1-Score'] * 0.2)
    
    top_n = st.slider("Show top N configurations:", 5, 50, 15)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(12, 8))
        top_models = df_copy.nlargest(top_n, 'Composite_Score').sort_values('Composite_Score', ascending=True)
        top_models['Config'] = (top_models['Algorithm'].str[:12] + ' | ' + 
                               top_models['Optimizer'] + ' | LR: ' + 
                               top_models['Learning Rate'].astype(str))
        
        colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(top_models)))
        bars = ax.barh(range(len(top_models)), top_models['Composite_Score'].values, 
                      color=colors, edgecolor='black', linewidth=1.5)
        
        ax.set_yticks(range(len(top_models)))
        ax.set_yticklabels(top_models['Config'].values, fontsize=9)
        ax.set_xlabel('Composite Score', fontsize=11, fontweight='bold')
        ax.set_title(f'Top {top_n} Model Configurations', fontsize=12, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'{width:.4f}', ha='left', va='center', fontsize=8, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("### Top Configuration Details")
        best = df_copy.loc[df_copy['Accuracy'].idxmax()]
        st.markdown(f"**Algorithm:** {best['Algorithm']}")
        st.markdown(f"**Optimizer:** {best['Optimizer']}")
        st.markdown(f"**Learning Rate:** {best['Learning Rate']:.6f}")
        st.markdown("---")
        st.markdown(f"**Accuracy:** {best['Accuracy']:.4f}")
        st.markdown(f"**Precision:** {best['Precision']:.4f}")
        st.markdown(f"**Recall:** {best['Recall']:.4f}")
        st.markdown(f"**F1-Score:** {best['F1-Score']:.4f}")
    
    st.markdown("---")
    st.markdown("### 📋 Top 20 Configurations Table")
    top_20 = df_copy.nlargest(20, 'Accuracy')[['Algorithm', 'Optimizer', 'Learning Rate', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'Composite_Score']]
    st.dataframe(top_20, use_container_width=True, hide_index=True)

# PAGE 6: HEATMAPS
elif page == "🗺️ Heatmaps":
    st.markdown("## 🗺️ Performance Heatmaps")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Algorithm vs Optimizer")
        fig, ax = plt.subplots(figsize=(9, 7))
        pivot_df = filtered_df.pivot_table(values='Accuracy', index='Algorithm', columns='Optimizer', aggfunc='mean')
        sns.heatmap(pivot_df, annot=True, fmt='.4f', cmap='RdYlGn', center=0.85, 
                   cbar_kws={'label': 'Accuracy'}, ax=ax, linewidths=0.5, linecolor='gray',
                   vmin=0.78, vmax=0.92)
        ax.set_title('Accuracy: Algorithm vs Optimizer', fontsize=12, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("### Algorithm vs Learning Rate")
        fig, ax = plt.subplots(figsize=(9, 7))
        pivot_df2 = filtered_df.pivot_table(values='Accuracy', index='Algorithm', 
                                           columns='Learning Rate', aggfunc='mean')
        sns.heatmap(pivot_df2, annot=True, fmt='.4f', cmap='RdYlGn', center=0.85,
                   cbar_kws={'label': 'Accuracy'}, ax=ax, linewidths=0.5, linecolor='gray',
                   vmin=0.78, vmax=0.92)
        ax.set_title('Accuracy: Algorithm vs Learning Rate', fontsize=12, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### Optimizer vs Learning Rate")
        fig, ax = plt.subplots(figsize=(9, 5))
        pivot_df3 = filtered_df.pivot_table(values='Accuracy', index='Optimizer', 
                                           columns='Learning Rate', aggfunc='mean')
        sns.heatmap(pivot_df3, annot=True, fmt='.4f', cmap='RdYlGn', center=0.85,
                   cbar_kws={'label': 'Accuracy'}, ax=ax, linewidths=0.5, linecolor='gray',
                   vmin=0.78, vmax=0.92)
        ax.set_title('Accuracy: Optimizer vs Learning Rate', fontsize=12, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col4:
        st.markdown("### Precision Heatmap")
        fig, ax = plt.subplots(figsize=(9, 7))
        pivot_df4 = filtered_df.pivot_table(values='Precision', index='Algorithm', columns='Optimizer', aggfunc='mean')
        sns.heatmap(pivot_df4, annot=True, fmt='.4f', cmap='Blues',
                   cbar_kws={'label': 'Precision'}, ax=ax, linewidths=0.5, linecolor='gray')
        ax.set_title('Precision: Algorithm vs Optimizer', fontsize=12, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)

# PAGE 7: CONFUSION MATRICES
elif page == "🎲 Confusion Matrices":
    st.markdown("## 🎲 Confusion Matrices for Top Models")
    
    top_3 = filtered_df.nlargest(3, 'Accuracy')
    
    col1, col2, col3 = st.columns(3)
    
    class_names = ['Class 0', 'Class 1', 'Class 2', 'Class 3', 'Class 4']
    
    for idx, (col, (_, row)) in enumerate(zip([col1, col2, col3], top_3.iterrows())):
        with col:
            # Generate mock confusion matrix
            cm = np.zeros((5, 5))
            acc = row['Accuracy']
            
            for i in range(5):
                cm[i, i] = int(100 * acc / 5 * 5)
            
            for i in range(5):
                for j in range(5):
                    if i != j:
                        cm[i, j] = np.random.randint(5, 15)
            
            cm = cm / cm.sum(axis=1, keepdims=True)
            
            fig, ax = plt.subplots(figsize=(6, 5))
            im = ax.imshow(cm, cmap='Blues', aspect='auto')
            
            ax.set_xticks(range(5))
            ax.set_yticks(range(5))
            ax.set_xticklabels(class_names, fontsize=8)
            ax.set_yticklabels(class_names, fontsize=8)
            
            for i in range(5):
                for j in range(5):
                    text = ax.text(j, i, f'{cm[i, j]:.2f}',
                                 ha="center", va="center", color="black", fontsize=8, fontweight='bold')
            
            ax.set_xlabel('Predicted', fontsize=9, fontweight='bold')
            ax.set_ylabel('True', fontsize=9, fontweight='bold')
            title = f"{row['Algorithm']}\n{row['Optimizer']}, LR={row['Learning Rate']:.4f}\nAcc: {row['Accuracy']:.4f}"
            ax.set_title(title, fontsize=9, fontweight='bold')
            
            plt.colorbar(im, ax=ax, label='Proportion')
            plt.tight_layout()
            st.pyplot(fig)

# PAGE 8: DETAILED RESULTS
elif page == "📋 Detailed Results":
    st.markdown("## 📋 Detailed Results Table")
    
    # Sort and display
    sort_by = st.selectbox("Sort by:", ['Accuracy', 'Precision', 'Recall', 'F1-Score'], index=0)
    ascending = st.checkbox("Ascending order", value=False)
    
    display_df = filtered_df.sort_values(sort_by, ascending=ascending)
    display_df['Rank'] = range(1, len(display_df) + 1)
    
    # Reorder columns
    display_df = display_df[['Rank', 'Algorithm', 'Optimizer', 'Learning Rate', 'Accuracy', 'Precision', 'Recall', 'F1-Score']]
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Download as CSV
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="model_comparison_results.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Statistical Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Accuracy Statistics:**")
        st.markdown(f"- Mean: {filtered_df['Accuracy'].mean():.4f}")
        st.markdown(f"- Median: {filtered_df['Accuracy'].median():.4f}")
        st.markdown(f"- Std Dev: {filtered_df['Accuracy'].std():.4f}")
        st.markdown(f"- Min: {filtered_df['Accuracy'].min():.4f}")
        st.markdown(f"- Max: {filtered_df['Accuracy'].max():.4f}")
    
    with col2:
        st.markdown("**F1-Score Statistics:**")
        st.markdown(f"- Mean: {filtered_df['F1-Score'].mean():.4f}")
        st.markdown(f"- Median: {filtered_df['F1-Score'].median():.4f}")
        st.markdown(f"- Std Dev: {filtered_df['F1-Score'].std():.4f}")
        st.markdown(f"- Min: {filtered_df['F1-Score'].min():.4f}")
        st.markdown(f"- Max: {filtered_df['F1-Score'].max():.4f}")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
    <p>Deep Learning Model Comparison Dashboard | Retina Dataset Analysis</p>
    <p>Algorithms: CNN, ResNet50, VGG16, AlexNet | Optimizers: Adam, RMSprop, SGD | Learning Rates: 0.01, 0.001, 0.0001</p>
    </div>
""", unsafe_allow_html=True)
