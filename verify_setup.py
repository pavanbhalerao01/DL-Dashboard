"""
Test script to verify installation and setup
"""
import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK\n")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} - Need 3.8 or higher\n")
        return False

def check_packages():
    """Check if required packages are installed"""
    print("📦 Checking required packages...")
    
    packages = {
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn',
        'sklearn': 'Scikit-Learn',
        'tensorflow': 'TensorFlow',
        'cv2': 'OpenCV',
        'streamlit': 'Streamlit',
        'PIL': 'Pillow',
        'jupyter': 'Jupyter',
    }
    
    missing = []
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT FOUND")
            missing.append(name)
    
    print()
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt\n")
        return False
    else:
        print("✓ All packages installed\n")
        return True

def check_directory_structure():
    """Check if directory structure is correct"""
    print("📁 Checking directory structure...")
    
    required_dirs = [
        'notebooks',
        'utils',
        'results',
        'dashboard',
        'data',
    ]
    
    base_path = Path(__file__).parent
    all_exist = True
    
    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ - MISSING")
            all_exist = False
    
    print()
    if not all_exist:
        print("❌ Some directories are missing\n")
        return False
    else:
        print("✓ Directory structure OK\n")
        return True

def check_files():
    """Check if key files exist"""
    print("📄 Checking key files...")
    
    required_files = {
        'notebooks/Retina_DL_Analysis.ipynb': 'Colab Notebook',
        'dashboard/app.py': 'Streamlit App',
        'utils/generate_results.py': 'Result Generator',
        'utils/visualizations.py': 'Visualization Module',
        'setup.py': 'Setup Script',
        'requirements.txt': 'Dependencies',
        'config.json': 'Configuration',
    }
    
    base_path = Path(__file__).parent
    all_exist = True
    
    for file_path, description in required_files.items():
        full_path = base_path / file_path
        if full_path.exists():
            print(f"  ✓ {description}")
        else:
            print(f"  ✗ {description} - MISSING ({file_path})")
            all_exist = False
    
    print()
    if not all_exist:
        print("❌ Some files are missing\n")
        return False
    else:
        print("✓ All key files present\n")
        return True

def check_results():
    """Check if results have been generated"""
    print("📊 Checking generated results...")
    
    results_dir = Path(__file__).parent / 'results'
    
    expected_files = [
        'all_results.json',
        'comparison.csv',
        'summary_stats.json',
    ]
    
    all_exist = True
    for file_name in expected_files:
        file_path = results_dir / file_name
        if file_path.exists():
            file_size = file_path.stat().st_size
            print(f"  ✓ {file_name} ({file_size:,} bytes)")
        else:
            print(f"  ✗ {file_name} - NOT GENERATED")
            all_exist = False
    
    print()
    if not all_exist:
        print("⚠️  Results not yet generated")
        print("Run: python setup.py\n")
        return False
    else:
        print("✓ Results generated\n")
        return True

def main():
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║                                                                    ║
    ║   🧠 Installation Verification Test                               ║
    ║   Deep Learning Model Comparison Platform                         ║
    ║                                                                    ║
    ╚════════════════════════════════════════════════════════════════════╝
    """)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_packages),
        ("Directory Structure", check_directory_structure),
        ("Key Files", check_files),
        ("Generated Results", check_results),
    ]
    
    results = []
    for name, check_func in checks:
        result = check_func()
        results.append((name, result))
    
    print("=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70 + "\n")
    
    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 70)
    
    if all_passed:
        print("✅ ALL CHECKS PASSED!")
        print("\nYou're ready to go! Run one of these commands:\n")
        print("  📓 jupyter notebook notebooks/Retina_DL_Analysis.ipynb")
        print("  📊 streamlit run dashboard/app.py")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print("\nFix the issues above and run this test again.")
    
    print("\n" + "=" * 70 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
