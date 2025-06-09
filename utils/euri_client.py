"""
Euriai API client using the correct endpoint
"""

import requests
import os
from dotenv import load_dotenv
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class EuriClient:
    """Euriai API client with proper endpoint"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4.1-nano"):
        self.api_key = api_key or os.getenv("EURI_API_KEY")
        self.model = model
        self.base_url = "https://api.euron.one/api/v1/euri/alpha/chat/completions"
        
        if not self.api_key:
            raise Exception("EURI_API_KEY not found in environment variables or parameters.")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Test connection
        self._test_connection()
    
    def _test_connection(self):
        """Test the API connection with a simple request"""
        try:
            test_messages = [{"role": "user", "content": "Hello"}]
            response = self.chat_completion(test_messages, max_tokens=5)
            logger.info("✅ Euriai API connection successful")
            logger.info(f"   Test response: {response[:50]}...")
        except Exception as e:
            logger.warning(f"⚠️ Euriai API test failed: {str(e)}")
    
    def chat_completion(self, messages, model=None, temperature=0.7, max_tokens=1000):
        """
        Send a chat completion request to Euriai API
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use (defaults to instance model)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            
        Returns:
            String response from the API
        """
        if not self.api_key:
            raise Exception("EURI_API_KEY not found in environment variables.")

        payload = {
            "model": model or self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=60)
            response.raise_for_status()

            response_data = response.json()
            if "choices" in response_data and len(response_data["choices"]) > 0:
                return response_data["choices"][0]["message"]["content"]
            else:
                raise ValueError("Invalid response format from API")

        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Error parsing API response: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def get_available_models(self):
        """Get list of available models"""
        return [
            "gpt-4.1-nano",
            "gpt-4-turbo", 
            "gemini-2.0-flash-001",
            "llama-4-maverick",
            "claude-3-sonnet"
        ]

# Convenience function for backward compatibility
def euri_chat_completion(messages, model="gpt-4.1-nano", temperature=0.7, max_tokens=1000):
    """
    Convenience function for chat completion
    """
    client = EuriClient(model=model)
    return client.chat_completion(messages, model, temperature, max_tokens)

# Test function
def test_euri_client():
    """Test the Euriai client"""
    try:
        client = EuriClient()
        
        test_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello and tell me you're working correctly."}
        ]
        
        response = client.chat_completion(test_messages, max_tokens=50)
        print(f"✅ Euriai client test successful!")
        print(f"Response: {response}")
        return True
        
    except Exception as e:
        print(f"❌ Euriai client test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_euri_client()
