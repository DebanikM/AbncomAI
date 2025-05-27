import os
import google.generativeai as genai
from typing import Dict, List, Any

# Initialize the Gemini API with the API key
def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    genai.configure(api_key=api_key)

# Generate message using Gemini 2.5 Flash Preview model
def generate_message(incident_data: Dict[str, Any]) -> str:
    # Initialize Gemini
    init_gemini()
    
    # Create a model instance
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-preview-05-20")
    model = genai.GenerativeModel(model_name)
    
    # Format the prompt for the AI
    prompt = create_prompt(incident_data)
    
    # Generate response
    response = model.generate_content(prompt)
    
    # Return the message
    return response.text

# Create a structured prompt for the Gemini model
def create_prompt(incident_data: Dict[str, Any]) -> str:
    # Extract data from the incident_data dictionary
    severity = incident_data.get("severity", "")
    impacted_services = ", ".join(incident_data.get("impacted_services", []))
    customer_impact = incident_data.get("customer_impact", "")
    root_cause = incident_data.get("root_cause", "")
    mitigation = incident_data.get("mitigation", "")
    eta = incident_data.get("eta", "")
    message_type = incident_data.get("message_type", "")
    tone = incident_data.get("tone", "")
    
    # Create a structured prompt for the AI
    prompt = f"""
    You are a highly skilled communications specialist at Abnormal Security, responsible for drafting incident status updates. 
    Create a {message_type.lower()} for customers with the following details:
    
    - Severity: {severity}
    - Impacted Services: {impacted_services if impacted_services else "None specified"}
    - Customer Impact: {customer_impact}
    - Root Cause: {root_cause if root_cause else "Not yet determined"}
    - Mitigation Steps: {mitigation}
    - Estimated Resolution Time: {eta if eta else "Currently unknown"}
    
    Please craft a message that is:
    1. Clear, concise, and honest
    2. Written at a {tone.lower()} level
    3. Appropriate for a {message_type.lower()}
    4. Follows best practices for incident communication
    5. Avoids unnecessary technical jargon
    6. Instills confidence while being transparent
    
    Your response should be ready to use with minimal editing. 
    Do not include any explanations, just the message itself.
    
    **Crucially, prioritize extreme clarity and ease of understanding.** Aim for a high readability score by using very simple language, short sentences (ideally under 15-20 words), and avoiding jargon or explaining any necessary technical terms clearly. The message should be easily understood by someone with a general audience background, even if the selected tone is semi-technical or technical.
    """
    
    return prompt 

def score_message_with_gemini(message: str, tone: str) -> Dict[str, Any]:
    """
    Score the generated message using Gemini based on readability, clarity, and technical level.
    
    Args:
        message: The message text to score.
        tone: The intended communication tone ("General audience", "Semi-technical", or "Technical").
        
    Returns:
        Dictionary containing LLM-based scores.
    """
    init_gemini()
    
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-preview-05-20")
    model = genai.GenerativeModel(model_name)
    
    # Craft a prompt for scoring
    scoring_prompt = f"""
    You are an expert in technical communication and content analysis. 
    Your task is to evaluate the following incident message based on three criteria: readability, clarity, and technical level.
    Provide a score for each criterion on a scale of 0 to 100, where 100 is the best score.
    Consider the intended audience tone, which is '{tone}'.
    
    - Readability: How easy is the message to understand for the intended audience? Use simple language, short sentences, and clear structure.
    - Clarity: How clear and unambiguous is the message? Is the information presented logically and easy to follow?
    - Technical Level: How appropriate is the level of technical detail for the intended audience '{tone}'? (0 = General, 50 = Semi-technical, 100 = Technical)
    
    Analyze the following message:
    
    ---
    {message}
    ---
    
    Provide the scores in a JSON object with the keys 'readability_llm', 'clarity_llm', and 'technical_level_llm'.
    Example: {{ "readability_llm": 85, "clarity_llm": 90, "technical_level_llm": 40 }}
    Do NOT include any other text or explanation, just the JSON object.
    """
    
    response = model.generate_content(scoring_prompt)
    
    try:
        # Attempt to parse the JSON response
        # The response might contain markdown code block, so we need to handle that
        json_string = response.text.strip()
        if json_string.startswith('```json') and json_string.endswith('```'):
            json_string = json_string[7:-3].strip()
        elif json_string.startswith('```') and json_string.endswith('```'):
             json_string = json_string[3:-3].strip()
             
        import json
        scores = json.loads(json_string)
        
        # Validate keys and data types
        if all(key in scores and isinstance(scores[key], (int, float)) for key in ['readability_llm', 'clarity_llm', 'technical_level_llm']):
            return scores
        else:
            print(f"Warning: LLM response JSON has incorrect format: {scores}")
            return {}
            
    except Exception as e:
        print(f"Error parsing LLM scoring response: {e}")
        print(f"Raw LLM response: {response.text}")
        return {} 