#!/usr/bin/env python3
"""
CognAI Startup Script - For folder structure with backend/ and frontend/ directories
Starts both FastAPI backend and Streamlit frontend
"""

import subprocess
import time
import sys
import os
import webbrowser
from threading import Thread

def start_backend():
    """Start FastAPI backend"""
    print("🔧 Starting FastAPI backend...")
    try:
        # Change to backend directory
        if not os.path.exists("backend"):
            print("❌ Backend directory not found!")
            return
        
        os.chdir("backend")
        
        # Start FastAPI with uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

def start_frontend():
    """Start Streamlit frontend"""
    print("🎨 Starting Streamlit frontend...")
    time.sleep(3)  # Wait for backend to start
    try:
        # Change to frontend directory
        original_dir = os.getcwd()
        
        if not os.path.exists("frontend"):
            print("❌ Frontend directory not found!")
            return
            
        os.chdir("frontend")
        
        # Start Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app.py", 
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")

def main():
    print("🧠 Starting CognAI...")
    print("=" * 50)
    
    # Check project structure
    if not os.path.exists("backend"):
        print("❌ Backend directory not found!")
        print("Please ensure you have the following structure:")
        print("  backend/main.py")
        print("  frontend/app.py")
        return
    
    if not os.path.exists("frontend"):
        print("❌ Frontend directory not found!")
        print("Please ensure you have the following structure:")
        print("  backend/main.py")
        print("  frontend/app.py")
        return
    
    # Check if required files exist
    if not os.path.exists("backend/main.py"):
        print("❌ backend/main.py not found!")
        return
    
    if not os.path.exists("frontend/app.py"):
        print("❌ frontend/app.py not found!")
        return
    
    print("✅ Project structure verified!")
    print("\n🔧 Starting services...")
    print("Backend will run on: http://localhost:8000")
    print("Frontend will run on: http://localhost:8501")
    print("Auth page will be available at: http://localhost:8000")
    print("\nPress Ctrl+C to stop both services")
    print("=" * 50)
    
    try:
        # Start backend in a separate thread
        backend_thread = Thread(target=start_backend, daemon=True)
        backend_thread.start()
        
        # Wait a moment, then start frontend in main thread
        time.sleep(2)
        print("✅ Backend started, now starting frontend...")
        
        # Open browser after a delay
        def open_browser():
            time.sleep(5)
            print("🌐 Opening browser...")
            try:
                webbrowser.open("http://localhost:8501")
            except:
                print("Could not open browser automatically. Please visit: http://localhost:8501")
        
        browser_thread = Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Start frontend (this will block)
        start_frontend()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down CognAI...")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()