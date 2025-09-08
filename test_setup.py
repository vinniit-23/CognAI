#!/usr/bin/env python3
"""
CognAI Setup Verification Script - For backend/ and frontend/ folder structure
Tests if everything is configured correctly
"""

import os
import sys
import requests
import subprocess
from dotenv import load_dotenv

def check_project_structure():
    """Check if project structure is correct"""
    print("📁 Checking project structure...")
    
    required_structure = {
        "backend": "Backend directory",
        "frontend": "Frontend directory", 
        "backend/main.py": "FastAPI backend file",
        "frontend/app.py": "Streamlit frontend file"
    }
    
    all_good = True
    
    for path, description in required_structure.items():
        if os.path.exists(path):
            print(f"✅ {description}: Found")
        else:
            print(f"❌ {description}: Not found at {path}")
            all_good = False
    
    return all_good

def check_environment_variables():
    """Check if required environment variables are set"""
    print("\n🔧 Checking environment variables...")
    
    # Try loading from backend directory first
    env_paths = ["backend/.env", "frontend/.env", ".env"]
    env_loaded = False
    
    for env_path in env_paths:
        if os.path.exists(env_path):
            load_dotenv(env_path)
            print(f"✅ Environment file found: {env_path}")
            env_loaded = True
            break
    
    if not env_loaded:
        print("⚠️  No .env file found. Checking system environment variables...")
    
    required_vars = {
        "API_URL": "Backend API URL",
        "DESCOPE_PROJECT_ID": "Descope Project ID", 
        "DESCOPE_MANAGEMENT_KEY": "Descope Management Key",
        "GEMINI_API_KEY": "Gemini API Key"
    }
    
    all_good = True
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Show partial value for security
            if len(value) > 10:
                display_value = value[:6] + "..." + value[-4:]
            else:
                display_value = value
            print(f"✅ {description}: {display_value}")
        else:
            print(f"❌ {description}: Not set")
            all_good = False
    
    return all_good, env_loaded

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn", 
        "streamlit",
        "requests",
        "python-dotenv",
        "google-generativeai"
    ]
    
    all_good = True
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}: Installed")
        except ImportError:
            print(f"❌ {package}: Not installed")
            all_good = False
    
    return all_good

def test_backend_import():
    """Test if backend can be imported"""
    print("\n🔧 Testing backend...")
    
    try:
        if not os.path.exists("backend/main.py"):
            print("❌ Backend main.py not found")
            return False
        
        # Add backend directory to Python path
        sys.path.insert(0, "backend")
        
        # Try importing the main module
        import main
        print("✅ Backend imports successfully")
        
        # Check if FastAPI app exists
        if hasattr(main, 'app'):
            print("✅ FastAPI app found")
            return True
        else:
            print("❌ FastAPI app not found in main.py")
            return False
            
    except Exception as e:
        print(f"❌ Backend import error: {e}")
        return False
    finally:
        # Remove backend from path
        if "backend" in sys.path:
            sys.path.remove("backend")

def test_frontend_syntax():
    """Test if frontend file has correct syntax"""
    print("\n🎨 Testing frontend...")
    
    try:
        if not os.path.exists("frontend/app.py"):
            print("❌ Frontend app.py not found")
            return False
        
        # Read and check frontend file
        with open("frontend/app.py", 'r') as f:
            content = f.read()
            
        if "import streamlit" in content:
            print("✅ Frontend imports Streamlit correctly")
        else:
            print("❌ Frontend doesn't import Streamlit")
            return False
            
        if "st.title" in content or "st.markdown" in content:
            print("✅ Frontend uses Streamlit components")
            return True
        else:
            print("⚠️  Frontend might not have Streamlit UI components")
            return True  # Not critical
            
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def main():
    print("🧠 CognAI Setup Verification")
    print("=" * 50)
    
    # Check project structure
    structure_ok = check_project_structure()
    
    # Test dependencies
    deps_ok = check_dependencies()
    
    # Test environment variables
    env_ok, env_found = check_environment_variables()
    
    # Test backend
    backend_ok = test_backend_import()
    
    # Test frontend  
    frontend_ok = test_frontend_syntax()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SETUP SUMMARY")
    print("=" * 50)
    
    if structure_ok:
        print("✅ Project structure: OK")
    else:
        print("❌ Project structure: Issues found")
        print("   Expected structure:")
        print("   CognAI/")
        print("   ├── backend/main.py")
        print("   ├── frontend/app.py")
        print("   └── .env (in backend/ or root)")
    
    if deps_ok:
        print("✅ Dependencies: OK")
    else:
        print("❌ Dependencies: Missing packages")
        print("   Run: pip install fastapi uvicorn streamlit requests python-dotenv google-generativeai")
    
    if env_ok:
        print("✅ Environment: OK")
    else:
        print("❌ Environment: Missing variables")
        if not env_found:
            print("   Create .env file in backend/ directory with:")
            print("   API_URL=http://localhost:8000")
            print("   DESCOPE_PROJECT_ID=your_project_id")
            print("   DESCOPE_MANAGEMENT_KEY=your_management_key")
            print("   GEMINI_API_KEY=your_gemini_api_key")
    
    if backend_ok:
        print("✅ Backend: Ready")
    else:
        print("❌ Backend: Issues found")
    
    if frontend_ok:
        print("✅ Frontend: Ready")#!/usr/bin/env python3
"""
CognAI Setup Verification Script
Tests if everything is configured correctly
"""

import os
import sys
import requests
import subprocess
from dotenv import load_dotenv

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: Found at {filepath}")
        return True
    else:
        print(f"❌ {description}: Not found at {filepath}")
        return False

def check_environment_variables():
    """Check if required environment variables are set"""
    load_dotenv()
    
    required_vars = {
        "API_URL": "Backend API URL",
        "DESCOPE_PROJECT_ID": "Descope Project ID", 
        "DESCOPE_MANAGEMENT_KEY": "Descope Management Key",
        "GEMINI_API_KEY": "Gemini API Key"
    }
    
    all_good = True
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Show partial value for security
            if len(value) > 10:
                display_value = value[:6] + "..." + value[-4:]
            else:
                display_value = value
            print(f"✅ {description}: {display_value}")
        else:
            print(f"❌ {description}: Not set")
            all_good = False
    
    return all_good

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        "fastapi",
        "uvicorn", 
        "streamlit",
        "requests",
        "python-dotenv",
        "google-generativeai"
    ]
    
    all_good = True
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}: Installed")
        except ImportError:
            print(f"❌ {package}: Not installed")
            all_good = False
    
    return all_good

def test_backend_start():
    """Test if backend can start"""
    print("\n🔧 Testing backend startup...")
    
    try:
        # Try to start backend process briefly
        backend_files = ["main.py", "backend/main.py"]
        backend_file = None
        
        for file in backend_files:
            if os.path.exists(file):
                backend_file = file
                break
        
        if not backend_file:
            print("❌ Backend main.py not found")
            return False
        
        print(f"✅ Backend file found: {backend_file}")
        
        # Test import
        sys.path.insert(0, os.path.dirname(backend_file) or ".")
        try:
            import main
            print("✅ Backend imports successfully")
            return True
        except Exception as e:
            print(f"❌ Backend import error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_frontend_start():
    """Test if frontend can start"""
    print("\n🎨 Testing frontend startup...")
    
    try:
        frontend_files = ["app.py", "frontend/app.py"]
        frontend_file = None
        
        for file in frontend_files:
            if os.path.exists(file):
                frontend_file = file
                break
        
        if not frontend_file:
            print("❌ Frontend app.py not found")
            return False
        
        print(f"✅ Frontend file found: {frontend_file}")
        
        # Basic syntax check
        with open(frontend_file, 'r') as f:
            content = f.read()
            if "import streamlit" in content:
                print("✅ Frontend imports Streamlit correctly")
                return True
            else:
                print("❌ Frontend doesn't import Streamlit")
                return False
                
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def main():
    print("🧠 CognAI Setup Verification")
    print("=" * 50)
    
    # Test files
    print("\n📁 Checking project files...")
    files_ok = True
    files_ok &= check_file_exists("main.py", "Backend (main.py)") or check_file_exists("backend/main.py", "Backend (backend/main.py)")
    files_ok &= check_file_exists("app.py", "Frontend (app.py)") or check_file_exists("frontend/app.py", "Frontend (frontend/app.py)")
    files_ok &= check_file_exists(".env", "Environment variables (.env)")
    
    # Test dependencies
    print("\n📦 Checking dependencies...")
    deps_ok = check_dependencies()
    
    # Test environment variables
    print("\n🔧 Checking environment variables...")
    env_ok = check_environment_variables()
    
    # Test backend
    backend_ok = test_backend_start()
    
    # Test frontend  
    frontend_ok = test_frontend_start()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SETUP SUMMARY")
    print("=" * 50)
    
    if files_ok:
        print("✅ Project files: OK")
    else:
        print("❌ Project files: Issues found")
    
    if deps_ok:
        print("✅ Dependencies: OK")
    else:
        print("❌ Dependencies: Missing packages")
        print("   Run: pip install -r requirements.txt")
    
    if env_ok:
        print("✅ Environment: OK")
    else:
        print("❌ Environment: Missing variables")
        print("   Copy .env.example to .env and fill in values")
    
    if backend_ok:
        print("✅ Backend: Ready")
    else:
        print("❌ Backend: Issues found")
    
    if frontend_ok:
        print("✅ Frontend: Ready")
    else:
        print("❌ Frontend: Issues found")
    
    if all([files_ok, deps_ok, env_ok, backend_ok, frontend_ok]):
        print("\n🎉 ALL CHECKS PASSED!")
        print("You can now run: python start_cognai.py")
    else:
        print("\n⚠️  Please fix the issues above before starting CognAI")
    
    print("\n📝 Next steps:")
    print("1. Fix any issues shown above")
    print("2. Run: python start_cognai.py")
    print("3. Open http://localhost:8501 in your browser")

if __name__ == "__main__":
    main()