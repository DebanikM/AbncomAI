import streamlit as st
import os
import logging
from dotenv import load_dotenv
from utils.gemini_utils import generate_message, score_message_with_gemini
from utils.text_analysis import analyze_text
from utils.templates import format_message
from datetime import datetime
import streamlit.components.v1 as components

# Page configuration MUST come first
st.set_page_config(
    page_title="AbComm AI Assistant", 
    page_icon="🚨",
    layout="wide"
)

# Inject custom CSS for fonts
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Configure logging
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "app.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded.")

# App title and description
st.markdown("<div style='text-align: center; margin-top: -60px;'><H1 style='background-image: linear-gradient(to right, #00FFFF, #8A2BE2, #FF00FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>AbComm AI Assistant</H1></div>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>Built for responders. Tuned for customers.</div>", unsafe_allow_html=True)

# Inject CSS for main content spacing
st.markdown("""
<style>
    #main-content {
        margin-top: 30px; /* Adjust this value as needed */
    }
    /* Add horizontal gap between columns */
    #main-content > div > div:first-child {
        margin-right: 60px; /* Adjusted for a larger gap */
    }
</style>
""", unsafe_allow_html=True)

# Main layout with two columns
st.markdown("<div id='main-content'>", unsafe_allow_html=True) # Start of main content container
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Incident Details")
    
    # Severity level
    severity = st.selectbox(
        "Severity Level :red[*]",
        options=["Please select", "P0 - Critical", "P1 - High", "P2 - Medium", "P3 - Low"],
        index=0, # Set index to 0 to select the blank option initially
        help="Select the severity level of the incident"
    )
    
    # Impacted services
    st.markdown("Impacted Services :red[*]") # Use markdown for the label here
    
    # Create two columns for the checkboxes
    service_col1, service_col2 = st.columns(2)

    services = {}
    
    # Distribute checkboxes across the two columns
    with service_col1:
        services["Email Analysis"] = st.checkbox("Email Analysis")
        services["Account Protection"] = st.checkbox("Account Protection")
        services["Dashboard"] = st.checkbox("Dashboard")

    with service_col2:
        services["Threat Detection"] = st.checkbox("Threat Detection")
        services["API"] = st.checkbox("API")
        services["Reporting"] = st.checkbox("Reporting")
    
    # Check if at least one service is selected
    are_services_selected = any(services.values())
    
    # Customer impact
    customer_impact = st.text_area(
        "Customer Impact Description :red[*]",
        help="Describe how customers are affected by this incident"
    )
    
    # Root cause
    root_cause = st.text_area(
        "Root Cause (if known)",
        help="Explain the root cause if already identified"
    )
    
    # Mitigation steps
    mitigation = st.text_area(
        "Mitigation Steps in Progress :red[*]",
        help="Describe what steps are being taken to resolve the issue"
    )
    
    # ETA
    eta = st.text_input(
        "Estimated Time to Resolution :red[*]",
        help="Provide an estimate of when the issue will be resolved (e.g., '2 hours', 'by 5pm PT')"
    )
    
    # Message type
    message_type = st.selectbox(
        "Message Type :red[*]",
        options=["Please select", "Initial notification", "Status update", "Resolution notice"],
        index=0, # Set index to 0 to select the blank option initially
        help="Select the type of incident message"
    )
    
    # Tone preference
    tone = st.select_slider(
        "Communication Tone",
        options=["General audience", "Semi-technical", "Technical"],
        value="Semi-technical"
    )

    # Determine if the form is complete
    is_severity_selected = severity.strip() and severity != "Please select"
    is_services_selected = any(services.values())
    is_message_type_selected = message_type.strip() and message_type != "Please select"
    is_customer_impact_filled = customer_impact.strip()
    is_mitigation_filled = mitigation.strip()
    is_eta_filled = eta.strip()

    is_form_complete = all([
        is_severity_selected,
        is_services_selected,
        is_message_type_selected,
        is_customer_impact_filled,
        is_mitigation_filled,
        is_eta_filled
    ])

    # Submit button
    submit_button = st.button(label="Generate Message", disabled=not is_form_complete)

# Logic for generating the message
if submit_button:
    logger.info("Form submitted. Collecting incident data.")
    # Collect the form data
    impacted_services = [service for service, checked in services.items() if checked]
    
    # Prepare data for the AI
    incident_data = {
        "severity": severity,
        "impacted_services": impacted_services,
        "customer_impact": customer_impact,
        "root_cause": root_cause,
        "mitigation": mitigation,
        "eta": eta,
        "message_type": message_type,
        "tone": tone
    }
    
    logger.info(f"Incident data collected: {incident_data}")
    
    with st.spinner("Generating incident message..."):
        logger.info("Generating message using Gemini...")
        # Generate message using Gemini
        generated_message = generate_message(incident_data)
        logger.info("Message generated successfully.")
        
        # Analyze the text quality
        analysis_results = analyze_text(generated_message, tone=incident_data["tone"])
        
        # Score the message using LLM
        llm_scores = score_message_with_gemini(generated_message, incident_data["tone"])

        # Combine analysis results and LLM scores
        analysis_results.update(llm_scores)
        
        # Format message according to template
        formatted_message = format_message(generated_message, incident_data)

        # Store generated messages and analysis results in session state
        st.session_state['generated_message'] = generated_message
        st.session_state['formatted_message'] = formatted_message
        st.session_state['analysis_results'] = analysis_results
        st.session_state['incident_data'] = incident_data # Store incident data for formatted message/html

# Display results in the second column
with col2:
    st.subheader("Generated Message")
    
    # Check if message has been generated and stored in session state
    if 'generated_message' in st.session_state:
        logger.info("Displaying generated message and metrics from session state.")
        # Retrieve from session state
        generated_message_from_state = st.session_state['generated_message']
        formatted_message_from_state = st.session_state['formatted_message']
        analysis_results_from_state = st.session_state['analysis_results']
        incident_data_from_state = st.session_state['incident_data']

        # Display the formatted message
        st.markdown("### Preview")
        st.markdown(generated_message_from_state)
        
        # Display quality metrics from LLM
        st.markdown("### Quality Metrics")

        # Readability Score LLM
        readability_llm = analysis_results_from_state.get("readability_llm", 0)
        st.metric("Readability", f"{readability_llm}/100")
        st.progress(readability_llm/100)

        # Clarity Score LLM
        clarity_llm = analysis_results_from_state.get("clarity_llm", 0)
        st.metric("Clarity", f"{clarity_llm}/100")
        st.progress(clarity_llm/100)

        # Technical Level LLM with classification
        technical_llm = analysis_results_from_state.get("technical_level_llm", 0)
        level_llm = "General" if technical_llm < 30 else "Semi-Tech" if technical_llm < 70 else "Technical"
        st.metric("Technical Level", f"{technical_llm}/100 ({level_llm})")
        st.progress(technical_llm/100)

        # Status page preview
        st.markdown("### Status Page Preview")
        # Use triple single quotes for the HTML string to avoid markdown interpretation and concatenation issues
        html_preview = f'''
<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; background-color: #f8f9fa; font-family: 'Segoe UI', Arial, sans-serif; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
    <div style="display: flex; flex-direction: column; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #e0e0e0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="background-color: {'#d93025' if 'P0' in incident_data_from_state["severity"] else '#e65100' if 'P1' in incident_data_from_state["severity"] else '#f9a825' if 'P2' in incident_data_from_state["severity"] else '#4CAF50'}; color: white; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 14px;">
                    {incident_data_from_state["severity"].split(' - ')[0]}
                </span>
                <h3 style="margin: 0; color: #202124; font-size: 18px;">
                    Abnormal Security Status
                </h3>
            </div>
            <span style="color: #5f6368; font-size: 13px;">
                {datetime.now().strftime('%b %d, %Y %I:%M %p')} UTC
            </span>
        </div>
        <!-- Severity bar with marker -->
        <div style="width: 100%; margin-top: 15px; text-align: center;">
            <div style="width: 80%; height: 20px; background: linear-gradient(to right, #00ff00, #ffff00, #ff9900, #ff0000); border-radius: 5px; margin: 0 auto; position: relative;">
                <!-- Marker -->
                <div style="position: absolute; top: -10px; width: 2px; height: 30px; background-color: black; {'left: calc(5% - 1px);' if 'P3' in incident_data_from_state["severity"] else ''} {'left: calc(35% - 1px);' if 'P2' in incident_data_from_state["severity"] else ''} {'left: calc(65% - 1px);' if 'P1' in incident_data_from_state["severity"] else ''} {'left: calc(95% - 1px);' if 'P0' in incident_data_from_state["severity"] else ''}"></div>
            </div>
            <div style="display: flex; justify-content: space-between; width: 80%; margin: 5px auto 0 auto;">
                <span style="font-size: 12px;">P3 (Low)</span>
                <span style="font-size: 12px;">P2 (Medium)</span>
                <span style="font-size: 12px;">P1 (High)</span>
                <span style="font-size: 12px;">P0 (Critical)</span>
            </div>
        </div>
    </div>

    <div style="margin-bottom: 16px;">
        <p style="margin: 0 0 8px 0; font-weight: 600; color: #202124; {'border-left: 4px solid #4285f4; padding-left: 8px;' if incident_data_from_state["message_type"] == 'Initial notification' else ''} {'border-left: 4px solid #f9a825; padding-left: 8px;' if incident_data_from_state["message_type"] == 'Status update' else ''} {'border-left: 4px solid #00ff00; padding-left: 8px;' if incident_data_from_state["message_type"] == 'Resolution notice' else ''}">
            {incident_data_from_state["message_type"]}
        </p>
        <div style="margin: 0; color: #000000; line-height: 1.5; white-space: pre-line;">
            {generated_message_from_state.replace('**', '').replace('_', '').replace('```', '')}
        </div>
    </div>

    <div style="background-color: #f1f3f4; border-radius: 4px; padding: 12px; margin-bottom: 16px;">
        <p style="margin: 0 0 8px 0; font-weight: 600; color: #202124;">
            Impacted Services
        </p>
        <ul style="margin: 0; padding-left: 20px; color: #000000;">
            {"".join(f"<li>{service}</li>" for service in incident_data_from_state["impacted_services"])}
        </ul>
    </div>

    <div style="display: flex; align-items: center; gap: 8px; color: #5f6368; font-size: 14px;">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 8V12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 16H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Last updated: {datetime.now().strftime('%I:%M %p')} UTC</span>
    </div>
</div>
'''
        # Use components.html to display the raw HTML
        components.html(html_preview, height=500, scrolling=True)
        
        # Download options
        st.markdown("### Export Options")
        
        col_txt, col_md, col_html = st.columns(3)
        
        with col_txt:
            st.download_button(
                label="Download TXT",
                data=generated_message_from_state,
                file_name="incident_message.txt",
                mime="text/plain"
            )
        
        with col_md:
            st.download_button(
                label="Download MD",
                data=formatted_message_from_state,
                file_name="incident_message.md",
                mime="text/markdown"
            )
        
        with col_html:
            st.download_button(
                label="Download HTML",
                data=html_preview,
                file_name="incident_message.html",
                mime="text/html"
            )

logger.info("App finished rendering.")
st.markdown("</div>", unsafe_allow_html=True) # End of main content container 