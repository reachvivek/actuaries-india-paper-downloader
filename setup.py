#!/usr/bin/env python3
"""
Setup script for Actuaries India PDF Downloader
This script automatically installs required dependencies and runs the application.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages from requirements.txt"""
    print("🔧 Setting up Actuaries India PDF Downloader...")
    print("📦 Installing required packages...")
    
    try:
        # Check if requirements.txt exists
        if not os.path.exists('requirements.txt'):
            print("❌ requirements.txt not found!")
            return False
            
        # Install packages
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True, check=True)
        
        print("✅ All packages installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        print("💡 Try running manually: pip install -r requirements.txt")
        return False

def run_application():
    """Run the main application"""
    print("\n🚀 Starting Actuaries India PDF Downloader...")
    try:
        import app
        app.main()
    except ImportError as e:
        print(f"❌ Error importing application: {e}")
        print("💡 Make sure app.py exists in the same directory")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main setup function"""
    print("=" * 60)
    print("🎓 ACTUARIES INDIA - PDF DOWNLOADER SETUP")
    print("=" * 60)
    print()
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"💡 Your version: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    # Install requirements
    if install_requirements():
        run_application()
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()