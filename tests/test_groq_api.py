"""
Test Groq API Connection
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_groq_api():
    """Test if Groq API key is valid and working"""
    
    api_key = os.getenv('GROQ_API_KEY')
    
    print("=" * 60)
    print("Testing Groq API Connection")
    print("=" * 60)
    
    # Check if API key exists
    if not api_key:
        print("ERROR: GROQ_API_KEY not found in .env file")
        return False
    
    print(f"OK: API Key found: {api_key[:20]}...{api_key[-10:]}")
    print()
    
    # Try to import and use Groq
    try:
        from groq import Groq
        print("OK: Groq library imported successfully")
    except ImportError as e:
        print(f"ERROR: Failed to import Groq library: {e}")
        print("Run: pip install groq")
        return False
    
    # Try to create client
    try:
        print("\nCreating Groq client...")
        client = Groq(api_key=api_key)
        print("OK: Groq client created successfully")
    except Exception as e:
        print(f"ERROR: Failed to create Groq client: {e}")
        print("\nPossible issues:")
        print("1. Invalid API key")
        print("2. Network connection problem")
        print("3. Groq library version mismatch")
        return False
    
    # Try a simple API call
    try:
        print("\nTesting API call with a simple query...")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": "Say 'Hello from Mohi ERP!' in exactly 5 words."
                }
            ],
            max_tokens=50,
            temperature=0.5
        )
        
        result = response.choices[0].message.content
        print("OK: API call successful")
        print("\nResponse from Groq AI:")
        print(f"   {result}")
        print()
        
    except Exception as e:
        print(f"ERROR: API call failed: {e}")
        print("\nPossible issues:")
        print("1. Invalid API key")
        print("2. API quota exceeded")
        print("3. Network/firewall blocking the request")
        print("4. Groq service temporarily unavailable")
        return False
    
    print("=" * 60)
    print("OK: All tests passed. Groq API is working correctly.")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = test_groq_api()
    exit(0 if success else 1)
