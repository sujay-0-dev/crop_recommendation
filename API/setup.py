"""
Setup script for the Crop Recommendation API
"""
import os
import sys
import subprocess
import pandas as pd
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    directories = ["data", "models", "logs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}/")

def check_data_file():
    """Check if data file exists"""
    data_file = Path("data/Crop_recommendation.csv")
    if not data_file.exists():
        print("⚠️  Warning: Crop_recommendation.csv not found in data/ directory")
        print("   Please place your dataset in data/Crop_recommendation.csv")
        print("   You can download it from: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset")
        return False
    else:
        # Validate data structure
        try:
            df = pd.read_csv(data_file)
            required_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label']
            missing_columns = set(required_columns) - set(df.columns)
            
            if missing_columns:
                print(f"❌ Missing columns in dataset: {missing_columns}")
                return False
            
            print(f"✓ Dataset found with {len(df)} rows and {len(df.columns)} columns")
            print(f"✓ Dataset contains {df['label'].nunique()} unique crops")
            return True
        except Exception as e:
            print(f"❌ Error reading dataset: {e}")
            return False

def train_initial_model():
    """Train the initial model"""
    print("🚀 Training initial model...")
    try:
        from model_training import train_and_save_model
        results = train_and_save_model("data/Crop_recommendation.csv")
        print("✓ Model trained successfully")
        print(f"  - Test Accuracy: {results['metrics']['test_accuracy']:.4f}")
        print(f"  - Training Samples: {results['metrics']['train_samples']}")
        print(f"  - Test Samples: {results['metrics']['test_samples']}")
        return True
    except Exception as e:
        print(f"❌ Model training failed: {e}")
        return False

def create_env_file():
    """Create environment file template"""
    env_content = """# Environment variables for Crop Recommendation API
PYTHONPATH=/app
LOG_LEVEL=info
MODEL_PATH=models/crop_recommendation_model.joblib
API_HOST=0.0.0.0
API_PORT=8000
"""
    
    with open(".env.example", "w") as f:
        f.write(env_content)
    print("✓ Created .env.example file")

def run_tests():
    """Run basic API tests"""
    print("🧪 Running basic tests...")
    try:
        import subprocess
        import time
        
        # Start the API in the background
        print("  Starting API server...")
        api_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--host", "127.0.0.1", "--port", "8001"  # Use different port for testing
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for server to start
        time.sleep(5)
        
        # Run tests
        test_result = subprocess.run([
            sys.executable, "test_api.py", "--url", "http://127.0.0.1:8001"
        ], capture_output=True, text=True)
        
        # Stop the API server
        api_process.terminate()
        api_process.wait()
        
        if test_result.returncode == 0:
            print("✓ Basic tests passed")
        else:
            print("⚠️  Some tests may have failed")
            
    except Exception as e:
        print(f"⚠️  Could not run automated tests: {e}")
        print("   You can manually test the API after starting it")

def main():
    """Main setup function"""
    print("=" * 60)
    print("🌾 CROP RECOMMENDATION API SETUP")
    print("=" * 60)
    
    # Step 1: Check Python version
    print("\n1. Checking Python version...")
    check_python_version()
    
    # Step 2: Install requirements
    print("\n2. Installing requirements...")
    install_requirements()
    
    # Step 3: Create directories
    print("\n3. Creating directories...")
    create_directories()
    
    # Step 4: Create environment file
    print("\n4. Creating configuration files...")
    create_env_file()
    
    # Step 5: Check data file
    print("\n5. Checking dataset...")
    data_available = check_data_file()
    
    # Step 6: Train model if data is available
    if data_available:
        print("\n6. Training initial model...")
        model_trained = train_initial_model()
        
        # Step 7: Run tests if model is trained
        if model_trained:
            print("\n7. Running tests...")
            run_tests()
    else:
        print("\n⚠️  Skipping model training - dataset not available")
        model_trained = False
    
    # Final instructions
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETED")
    print("=" * 60)
    
    if model_trained:
        print("✅ Your Crop Recommendation API is ready!")
        print("\nTo start the API server:")
        print("   python main.py")
        print("   # or")
        print("   uvicorn main:app --reload")
        print("\nAPI will be available at:")
        print("   • http://localhost:8000")
        print("   • Documentation: http://localhost:8000/docs")
        print("\nTo test the API:")
        print("   python test_api.py")
        
        print("\nTo deploy with Docker:")
        print("   docker-compose up --build")
        
    else:
        print("⚠️  Setup completed with warnings")
        print("\nNext steps:")
        print("1. Place your dataset in data/Crop_recommendation.csv")
        print("2. Run: python model_training.py")
        print("3. Run: python main.py")
    
    print("\n📖 For detailed instructions, see README.md")

if __name__ == "__main__":
    main()