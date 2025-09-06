"""
Test script for the Crop Recommendation API
"""
import requests
import json
import time
from typing import Dict, Any


class CropAPITester:
    """Test the Crop Recommendation API endpoints"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        
    def test_health(self) -> bool:
        """Test health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health")
            print(f"Health Check: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Status: {data.get('status')}")
                print(f"Model Loaded: {data.get('model_loaded')}")
                return data.get('model_loaded', False)
            return False
        except Exception as e:
            print(f"Health check failed: {e}")
            return False
    
    def test_root(self):
        """Test root endpoint"""
        try:
            response = requests.get(f"{self.base_url}/")
            print(f"Root endpoint: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {response.json()}")
        except Exception as e:
            print(f"Root endpoint test failed: {e}")
    
    def test_model_info(self):
        """Test model info endpoint"""
        try:
            response = requests.get(f"{self.base_url}/model/info")
            print(f"Model Info: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Model: {data.get('model_name')}")
                print(f"Accuracy: {data.get('accuracy')}")
                print(f"Crops: {len(data.get('supported_crops', []))}")
        except Exception as e:
            print(f"Model info test failed: {e}")
    
    def test_single_prediction(self):
        """Test single prediction endpoint"""
        # Test case from your notebook - rice example
        test_data = {
            "N": 90,
            "P": 42,
            "K": 43,
            "temperature": 20.879744,
            "humidity": 82.002744,
            "ph": 6.502985,
            "rainfall": 202.935536
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/predict",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            print(f"Single Prediction: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Predicted Crop: {data.get('predicted_crop')}")
                print(f"Confidence: {data.get('confidence'):.4f}")
                
                # Show top 3 probabilities
                probs = data.get('all_probabilities', {})
                sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:3]
                print("Top 3 predictions:")
                for crop, prob in sorted_probs:
                    print(f"  {crop}: {prob:.4f}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Single prediction test failed: {e}")
    
    def test_batch_prediction(self):
        """Test batch prediction endpoint"""
        # Multiple test cases
        test_batch = {
            "predictions": [
                {
                    "N": 90, "P": 42, "K": 43,
                    "temperature": 20.87, "humidity": 82.0,
                    "ph": 6.5, "rainfall": 202.9
                },
                {
                    "N": 85, "P": 58, "K": 41,
                    "temperature": 21.77, "humidity": 80.32,
                    "ph": 7.04, "rainfall": 226.66
                },
                {
                    "N": 60, "P": 55, "K": 44,
                    "temperature": 23.0, "humidity": 82.32,
                    "ph": 7.84, "rainfall": 263.96
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/predict/batch",
                json=test_batch,
                headers={"Content-Type": "application/json"}
            )
            print(f"Batch Prediction: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Total Predictions: {data.get('total_predictions')}")
                
                for i, pred in enumerate(data.get('predictions', [])):
                    print(f"Sample {i+1}: {pred.get('predicted_crop')} "
                          f"(confidence: {pred.get('confidence'):.4f})")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Batch prediction test failed: {e}")
    
    def test_feature_importance(self):
        """Test feature importance endpoint"""
        try:
            response = requests.get(f"{self.base_url}/model/feature-importance")
            print(f"Feature Importance: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                importance = data.get('feature_importance', {})
                print("Top 5 important features:")
                for i, (feature, score) in enumerate(list(importance.items())[:5]):
                    print(f"  {i+1}. {feature}: {score:.4f}")
        except Exception as e:
            print(f"Feature importance test failed: {e}")
    
    def test_invalid_input(self):
        """Test with invalid input data"""
        invalid_data = {
            "N": -10,  # Invalid negative value
            "P": 42,
            "K": 43,
            "temperature": 100,  # Invalid high temperature
            "humidity": 82.0,
            "ph": 6.5,
            "rainfall": 202.9
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/predict",
                json=invalid_data,
                headers={"Content-Type": "application/json"}
            )
            print(f"Invalid Input Test: {response.status_code}")
            if response.status_code != 200:
                print("✓ Correctly rejected invalid input")
            else:
                print("⚠ Invalid input was accepted")
        except Exception as e:
            print(f"Invalid input test failed: {e}")
    
    def performance_test(self, num_requests: int = 10):
        """Simple performance test"""
        test_data = {
            "N": 90, "P": 42, "K": 43,
            "temperature": 20.87, "humidity": 82.0,
            "ph": 6.5, "rainfall": 202.9
        }
        
        print(f"Performance test with {num_requests} requests...")
        times = []
        successful = 0
        
        for i in range(num_requests):
            try:
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/predict",
                    json=test_data,
                    headers={"Content-Type": "application/json"}
                )
                end_time = time.time()
                
                if response.status_code == 200:
                    successful += 1
                    times.append(end_time - start_time)
            except Exception as e:
                print(f"Request {i+1} failed: {e}")
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            print(f"Successful requests: {successful}/{num_requests}")
            print(f"Average response time: {avg_time:.4f}s")
            print(f"Min response time: {min_time:.4f}s")
            print(f"Max response time: {max_time:.4f}s")
    
    def run_all_tests(self):
        """Run all API tests"""
        print("=" * 50)
        print("CROP RECOMMENDATION API TESTS")
        print("=" * 50)
        
        # Basic connectivity
        print("\n1. Testing Basic Endpoints...")
        self.test_root()
        print()
        
        # Health check
        print("2. Testing Health Check...")
        model_loaded = self.test_health()
        print()
        
        if not model_loaded:
            print("❌ Model not loaded. Cannot proceed with prediction tests.")
            return
        
        # Model info
        print("3. Testing Model Info...")
        self.test_model_info()
        print()
        
        # Single prediction
        print("4. Testing Single Prediction...")
        self.test_single_prediction()
        print()
        
        # Batch prediction
        print("5. Testing Batch Prediction...")
        self.test_batch_prediction()
        print()
        
        # Feature importance
        print("6. Testing Feature Importance...")
        self.test_feature_importance()
        print()
        
        # Invalid input
        print("7. Testing Input Validation...")
        self.test_invalid_input()
        print()
        
        # Performance test
        print("8. Performance Test...")
        self.performance_test()
        print()
        
        print("=" * 50)
        print("TESTS COMPLETED")
        print("=" * 50)


def main():
    """Main function to run tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Crop Recommendation API")
    parser.add_argument(
        "--url", 
        default="http://localhost:8000",
        help="Base URL of the API (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--performance-requests",
        type=int,
        default=10,
        help="Number of requests for performance test (default: 10)"
    )
    
    args = parser.parse_args()
    
    # Create tester instance
    tester = CropAPITester(args.url)
    
    # Run all tests
    tester.run_all_tests()


if __name__ == "__main__":
    main()