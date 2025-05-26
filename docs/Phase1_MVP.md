# AbComm AI – Phase 1: MVP Documentation

## Overview
The Minimum Viable Product (MVP) phase of AbComm AI will deliver core functionality to automate incident message drafting using Flash-4, with deployment scheduled within 1 week.

## Features

### 1. Incident Input Form
- **Fields:**
  - Severity level (P0-P3)
  - Impacted services (checklist)
  - Customer impact description
  - Root cause (if known)
  - Mitigation steps in progress
  - Estimated time to resolution
  - Message type (initial/update/resolution)
  - Tone preference (technical/general)
- **Implementation:** Streamlit form components with appropriate validation

### 2. AI Message Generation
- **Functionality:** Integration with Gemini Flash-4 API to generate customer-facing updates
- **Prompt Engineering:** Structured prompts that incorporate best practices for incident communication
- **Output:** Concise, clear messaging that balances transparency with appropriate detail

### 3. Clarity and Tone Scoring
- **Implementation:** Textstat library integration for:
  - Readability metrics (Flesch Reading Ease)
  - Clarity scoring
  - Technical jargon detection
- **Display:** Visual indicators showing message quality scores

### 4. Status Page Preview
- **Design:** Visual mockup resembling Abnormal's existing status page
- **Functionality:** Real-time update of preview as message is generated/edited
- **Purpose:** Provide realistic context for how message will appear to customers

### 5. Download/Export Functionality
- **Formats:** Plain text, HTML, and Markdown
- **Implementation:** Download buttons for each format
- **Purpose:** Enable easy transfer to actual status page or other communication channels

## Technical Specifications

### Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python
- **AI Integration:** Gemini Flash-4 API
- **Deployment:** Streamlit Cloud

### Project Structure
```
abcomm-ai-tool/
├── .env                  # Environment variables including API keys
├── app.py                # Main application file
├── utils/
│   ├── Gemini_utils.py   # Gemini API integration functions
│   ├── text_analysis.py  # Text quality analysis functions
│   └── templates.py      # Message templates and formatting
└── requirements.txt      # Dependencies
```

### Key Dependencies
- streamlit==1.24.0
- Gemini==0.27.8
- python-dotenv==1.0.0
- textstat==0.7.3

## Development Tasks

1. **Setup & Environment Configuration** (Day 1)
   - Project initialization
   - Environment setup
   - API key management

2. **Input Form Development** (Day 1-2)
   - Design and implement input form
   - Add field validation
   - Create responsive layout

3. **Gemini Integration** (Day 2-3)
   - Implement API connection
   - Design effective prompts
   - Test message generation quality

4. **Clarity Scoring** (Day 3-4)
   - Integrate Textstat
   - Implement scoring algorithms
   - Create visual indicators

5. **UI Polishing & Preview** (Day 4-5)
   - Develop status page preview
   - Implement download functionality
   - Refine overall user interface

6. **Testing & Deployment** (Day 5-7)
   - User acceptance testing
   - Bug fixes
   - Deployment to Streamlit Cloud

## Success Criteria
- Functional end-to-end workflow from input to downloadable message
- Message generation time under 30 seconds
- Readability scores consistently above industry benchmarks
- Positive initial feedback from stakeholders

## Next Steps
Upon successful deployment and validation of the MVP, planning will begin for Phase 2 enhancements including interactive AI collaboration and more advanced templating features. 