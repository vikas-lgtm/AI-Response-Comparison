import requests
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai   # Gemini SDK
from difflib import SequenceMatcher   # for similarity comparison

def getLLM_Result_OpenRouter(prompt, model):
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
    }
    
    # Request payload
    payload = {
        "model": model,
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


def getLLM_Result_Gemini(prompt):
    load_dotenv()
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not gemini_key:
        raise ValueError("Please set GEMINI_API_KEY in your .env file")

    # configure Gemini client
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error with Gemini request: {str(e)}"

def text_similarity(a, b):
    """Return a similarity ratio between two texts"""
    return round(SequenceMatcher(None, a, b).ratio() * 100, 2)

def main():
    # Example prompt - you can modify this
    prompt = "Give me 10  Interview quetions and answers  on Java ,microservice, GCP cloud, Spring boot with 5+ years of experince"
    
    # Call the function to get the result
    deepseek_result = getLLM_Result_OpenRouter(prompt, "deepseek/deepseek-r1-0528:free")

    # Gemini response (via Google AI Studio API)
    gemini_result = getLLM_Result_Gemini(prompt)

    # Compare similarity
    similarity_score = text_similarity(deepseek_result, gemini_result)
    
    # Create markdown content
    markdown_content = f"""# AI Model Response

## Prompt
{prompt}

## DeepSeek Response
{deepseek_result}

## Gemini Response
{gemini_result}


## 🔍 Comparison
**Similarity Score:** {similarity_score}%

(A higher % means responses are more alike)
---
*Generated using OpenRouter + Gemini API*
"""
    
    # Save to markdown file
    output_file = "ai_response.md"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Comparison saved to {output_file}")
    except Exception as e:
        print(f"Error saving to file: {str(e)}")

if __name__ == "__main__":
    main()
