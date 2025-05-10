import os
import json
import requests
from ats_scoring_logic import rule_based_score
from dotenv import load_dotenv

load_dotenv()

def get_ats_analysis(resume_text, job_description):
    # Get rule-based score
    rule_data = rule_based_score(resume_text, job_description)

    # Get LLM-based analysis
    prompt = f"""
    Analyze the following resume and job description.

    JOB DESCRIPTION:
    {job_description}

    RESUME:
    {resume_text}

    1. Give a subjective ATS-style score from 0 to 100.
    2. Suggest exactly 3 improvements to increase the score.

    Respond only in JSON format like:
    {{
      "llm_score": 78,
      "suggestions": ["Add more data analysis tools", "Mention project outcomes", "Include SQL certification"]
    }}
    """

    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://rezoome.cursor.run",
        "X-Title": "Rezoome ATS Checker"
    }

    payload = {
        "model": "openchat/openchat-3.5-0106",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }

    try:
        # Using the correct OpenRouter API endpoint
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30  # Adding timeout
        )
        
        # Debug logging
        print("API Response Status:", response.status_code)
        print("API Response Headers:", response.headers)
        print("API Response:", response.text)
        
        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            print("Response content:", response.text)
            raise requests.exceptions.HTTPError(f"API request failed with status {response.status_code}")
        
        response_json = response.json()
        
        if 'choices' not in response_json:
            print("Error: 'choices' not found in response. Full response:", response_json)
            raise KeyError("API response missing 'choices' field")
            
        if not response_json['choices']:
            print("Error: Empty choices array in response")
            raise KeyError("API response has empty choices array")
            
        content = response_json['choices'][0]['message']['content']
        print("Content from API:", content)
        
        llm_json = json.loads(content)
        
        # Validate the response format
        if 'llm_score' not in llm_json or 'suggestions' not in llm_json:
            raise ValueError("API response missing required fields: llm_score or suggestions")
            
        if not isinstance(llm_json['llm_score'], (int, float)) or not isinstance(llm_json['suggestions'], list):
            raise ValueError("Invalid response format: llm_score should be a number and suggestions should be a list")

        # Calculate final score as average of rule-based and LLM scores
        final_score = round((rule_data['rule_score'] + llm_json['llm_score']) / 2)

        return {
            "score": final_score,
            "top_keywords": rule_data['jd_keywords'],
            "missing_keywords": rule_data['missing_keywords'],
            "suggestions": llm_json['suggestions'],
            "details": {
                "rule_based": rule_data['rule_score'],
                "llm_based": llm_json['llm_score']
            }
        }
        
    except requests.exceptions.RequestException as e:
        print("Error making API request:", str(e))
        # Fallback to rule-based scoring only if API fails
        return {
            "score": rule_data['rule_score'],
            "top_keywords": rule_data['jd_keywords'],
            "missing_keywords": rule_data['missing_keywords'],
            "suggestions": ["Unable to get AI suggestions due to API error. Please try again later."],
            "details": {
                "rule_based": rule_data['rule_score'],
                "llm_based": None
            }
        }
    except json.JSONDecodeError as e:
        print("Error decoding JSON from API response:", str(e))
        raise
    except KeyError as e:
        print("Error accessing API response fields:", str(e))
        raise
    except Exception as e:
        print("Unexpected error:", str(e))
        raise 