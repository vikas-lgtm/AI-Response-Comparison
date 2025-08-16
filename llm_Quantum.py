import requests
import json
import os
from dotenv import load_dotenv

def getLLM_Result(prompt, model):
    """
    Function to get LLM result using OpenRouter API
    
    Args:
        prompt (str): The input prompt to send to the AI model
        
    Returns:
        str: The response from the AI model
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # OpenRouter API endpoint
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Get API key from .env file
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError("Please set OPENROUTER_API_KEY in your .env file")
    
    # Headers for the API request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # "HTTP-Referer": "https://your-app.com",  # Replace with your app URL
        # "X-Title": "Your App Name"  # Replace with your app name
    }
    
    # Request payload
    payload = {
        "model": model,  # You can change this to any model
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        # Make the API request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the response
        result = response.json()
        
        # Extract the content from the response
        if result.get("choices") and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            return "No response received from the model"
            
    except requests.exceptions.RequestException as e:
        return f"Error making API request: {str(e)}"
    except json.JSONDecodeError as e:
        return f"Error parsing response: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def main():
    """
    Main function that calls getLLM_Result with a prompt and saves result to markdown file
    """
    # Example prompt - you can modify this
    prompt = "Explain quantum computing to a 10-year-old"
    
    # Call the function to get the result
    # result = getLLM_Result(prompt, "google/gemma-3n-e2b-it:free")
    result = getLLM_Result(prompt, "deepseek/deepseek-r1-0528:free")
    
    # Create markdown content
    markdown_content = f"""# AI Model Response

## Prompt
{prompt}

## Response
{result}

---
*Generated using OpenRouter API*
"""
    
    # Save to markdown file
    output_file = "ai_response.md"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Response saved to {output_file}")
    except Exception as e:
        print(f"Error saving to file: {str(e)}")

if __name__ == "__main__":
    main()
