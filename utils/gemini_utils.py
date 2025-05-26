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
    """
    
    return prompt 