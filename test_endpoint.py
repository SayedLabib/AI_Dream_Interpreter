import requests
import json

# Test the complete interpretation endpoint
url = "http://localhost:8020/api/v1/dream-ai/complete-interpretation"
payload = {
    "dream_description": "I was flying over a beautiful landscape with golden fields and mountains in the distance. I felt free and peaceful."
}

try:
    print("Testing complete interpretation endpoint...")
    response = requests.post(url, json=payload, timeout=120)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("SUCCESS!")
        print(f"Processing time: {result.get('processing_time', 'N/A')} seconds")
        print(f"Analysis interpretation: {result.get('analysis', {}).get('interpretation', 'N/A')[:200]}...")
        print(f"Image URL: {result.get('generated_image', {}).get('image_url', 'N/A')}")
    else:
        print("ERROR!")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"Request failed: {e}")
