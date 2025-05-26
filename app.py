import streamlit as st
import os
import logging
from dotenv import load_dotenv
from utils.gemini_utils import generate_message
from utils.text_analysis import analyze_text
from utils.templates import format_message

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

# Page configuration
st.set_page_config(
    page_title="AbComm AI - Incident Messaging Assistant", 
    page_icon="🚨",
    layout="wide"
)

logger.info("Streamlit page configured.")

# App title and description
st.title("AbComm AI - Incident Messaging Assistant")
st.markdown("""
    Generate professional customer-facing incident messages with AI assistance.
    This tool helps create clear, appropriate communications for service incidents.
""")

# Main layout with two columns
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Incident Details")
    
    # Form for incident details
    with st.form(key="incident_form"):
        # Severity level
        severity = st.selectbox(
            "Severity Level",
            options=["P0 - Critical", "P1 - High", "P2 - Medium", "P3 - Low"],
            help="Select the severity level of the incident"
        )
        
        # Impacted services
        st.write("Impacted Services")
        services = {
            "Email Analysis": st.checkbox("Email Analysis"),
            "Threat Detection": st.checkbox("Threat Detection"),
            "Account Protection": st.checkbox("Account Protection"),
            "API": st.checkbox("API"),
            "Dashboard": st.checkbox("Dashboard"),
            "Reporting": st.checkbox("Reporting")
        }
        
        # Customer impact
        customer_impact = st.text_area(
            "Customer Impact Description",
            help="Describe how customers are affected by this incident"
        )
        
        # Root cause
        root_cause = st.text_area(
            "Root Cause (if known)",
            help="Explain the root cause if already identified"
        )
        
        # Mitigation steps
        mitigation = st.text_area(
            "Mitigation Steps in Progress",
            help="Describe what steps are being taken to resolve the issue"
        )
        
        # ETA
        eta = st.text_input(
            "Estimated Time to Resolution",
            help="Provide an estimate of when the issue will be resolved (e.g., '2 hours', 'by 5pm PT')"
        )
        
        # Message type
        message_type = st.radio(
            "Message Type",
            options=["Initial notification", "Status update", "Resolution notice"],
            horizontal=True
        )
        
        # Tone preference
        tone = st.select_slider(
            "Communication Tone",
            options=["General audience", "Semi-technical", "Technical"],
            value="Semi-technical"
        )
        
        # Submit button
        submit_button = st.form_submit_button(label="Generate Message")

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
        analysis_results = analyze_text(generated_message)
        
        # Format message according to template
        formatted_message = format_message(generated_message, incident_data)

# Display results in the second column
with col2:
    st.subheader("Generated Message")
    
    if submit_button:
        logger.info("Displaying generated message and metrics.")
        # Display the formatted message
        st.markdown("### Preview")
        st.markdown(formatted_message)
        
        # Display quality metrics
        st.markdown("### Quality Metrics")
        
        # Readability score
        readability = analysis_results.get("readability", 0)
        st.metric("Readability Score", f"{readability}/100")
        
        # Progress bars for metrics
        st.progress(readability/100, "Readability")
        st.progress(analysis_results.get("clarity", 0)/100, "Clarity")
        st.progress(analysis_results.get("technical_level", 0)/100, "Technical Level")
        
        # Status page preview
        st.markdown("### Status Page Preview")
        st.markdown("""
        <div style="border:1px solid #ddd; padding:15px; border-radius:5px; background-color:#f9f9f9;">
            <h3 style="color:#d93025;">Abnormal Security Status</h3>
            <div style="background-color:#fff; padding:10px; border-radius:5px; border:1px solid #eee;">
        """, unsafe_allow_html=True)
        st.markdown(formatted_message, unsafe_allow_html=True)
        st.markdown("""
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Download options
        st.markdown("### Export Options")
        
        col_txt, col_md, col_html = st.columns(3)
        
        with col_txt:
            st.download_button(
                label="Download TXT",
                data=generated_message,
                file_name="incident_message.txt",
                mime="text/plain"
            )
        
        with col_md:
            st.download_button(
                label="Download MD",
                data=formatted_message,
                file_name="incident_message.md",
                mime="text/markdown"
            )
        
        with col_html:
            html_version = f"<html><body>{formatted_message}</body></html>"
            st.download_button(
                label="Download HTML",
                data=html_version,
                file_name="incident_message.html",
                mime="text/html"
            )

logger.info("App finished rendering.") 