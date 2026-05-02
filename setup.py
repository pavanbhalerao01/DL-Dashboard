"""
Setup script to initialize the DL Model Comparison Project
"""
import subprocess
import sys
import os
from pathlib import Path

def install_packages():
    """Install required packages"""
    packages = [
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'streamlit',
        'pillow',
        'opencv-python'
    ]
    
    print("📦 Installing required packages...\n")
    for package in packages:
        try:
            if package == 'opencv-python':
                __import__('cv2')
            elif package == 'scikit-learn':
                __import__('sklearn')
            else:
                __import__(package.replace('-', '_'))
            print(f"✓ {package} already installed")
        except ImportError:
            print(f"⬇️ Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
            print(f"✓ {package} installed")
    
    # Optional: Try to install TensorFlow with numpy compatibility
    print(f"\n📦 Attempting to install TensorFlow (optional)...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy<2", "tensorflow", "-q"])
        print(f"✓ tensorflow installed")
    except:
        print(f"⚠️  tensorflow installation skipped (optional for this demo)")

def generate_results():
    """Generate mock results"""
    print("\n" + "="*70)
    print("📊 GENERATING MOCK RESULTS")
    print("="*70 + "\n")
    
    sys.path.insert(0, str(Path(__file__).parent / "utils"))
    from generate_results import create_results_database, create_comparison_dataframe, save_results
    
    print("🔄 Creating results database...")
    results = create_results_database()
    
    print("💾 Saving results...")
    save_results(results)
    
    print("📋 Creating comparison dataframe...")
    df = create_comparison_dataframe(results)
    df.to_csv('d:\\VS Code\\Python\\DL\\results\\comparison.csv', index=False)
    
    print("\n✓ Results generated successfully!")
    print(f"✓ Total configurations: {len(df)}")
    print(f"✓ Average Accuracy: {df['Accuracy'].mean():.4f}")
    print(f"✓ Best Accuracy: {df['Accuracy'].max():.4f}")

def create_visualizations():
    """Create visualizations"""
    print("\n" + "="*70)
    print("🎨 CREATING VISUALIZATIONS")
    print("="*70 + "\n")
    
    sys.path.insert(0, str(Path(__file__).parent / "utils"))
    from visualizations import create_all_visualizations
    
    viz_paths = create_all_visualizations()
    
    print("\n✓ All visualizations created!")

def main():
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║                                                                    ║
    ║   🧠 Deep Learning Model Comparison - Setup                       ║
    ║   Retina Dataset Analysis with Multiple Architectures             ║
    ║                                                                    ║
    ╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Install packages
    install_packages()
    
    # Generate results
    generate_results()
    
    # Create visualizations
    create_visualizations()
    
    print("\n" + "="*70)
    print("✅ SETUP COMPLETE!")
    print("="*70 + "\n")
    
    print("📝 NEXT STEPS:\n")
    print("1. Open the Jupyter Notebook:")
    print("   → notebooks/Retina_DL_Analysis.ipynb\n")
    
    print("2. Launch the Streamlit Dashboard:")
    print("   → Run: streamlit run dashboard/app.py\n")
    
    print("3. View Results:")
    print("   → Results saved in: results/")
    print("   → Visualizations saved as PNG files\n")
    
    print("📊 Dashboard Features:")
    print("   ✓ Overview Dashboard")
    print("   ✓ Algorithm Comparison")
    print("   ✓ Optimizer Analysis")
    print("   ✓ Learning Rate Impact")
    print("   ✓ Top Configurations")
    print("   ✓ Performance Heatmaps")
    print("   ✓ Confusion Matrices")
    print("   ✓ Detailed Results Table\n")

if __name__ == "__main__":
    main()
