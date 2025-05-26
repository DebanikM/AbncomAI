# AbComm AI - System Flow Documentation

## Document Information
- **Project Name:** AbComm AI - Incident Messaging Assistant
- **Current Phase:** Phase 1 - MVP
- **Last Updated:** May 26, 2025
- **Updated By:** Development Team
- **Version:** 1.0

## System Architecture Overview

AbComm AI is a Streamlit-based web application that utilizes Google's Gemini Flash-4 API to generate customer-facing incident messages. The application follows a modular architecture with separate components for the user interface, AI integration, text analysis, and message formatting.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│  Streamlit UI   │───►│  Gemini Flash-4 │───►│ Text Analysis   │
│  (Input Form)   │    │  API Integration│    │ & Formatting    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                                              │
        │                                              │
        ▼                                              ▼
┌─────────────────┐                          ┌─────────────────┐
│                 │                          │                 │
│ User Feedback   │◄─────────────────────────│ Message Display │
│ & Editing       │                          │ & Export        │
│                 │                          │                 │
└─────────────────┘                          └─────────────────┘
```

## Component Breakdown

### 1. Streamlit User Interface
- **Purpose:** Provide a user-friendly interface for inputting incident details and viewing generated messages
- **Technologies:** Streamlit, Python
- **Interfaces:**
  - **Input:** User form submissions (incident details)
  - **Output:** Display of generated messages and quality metrics
- **Dependencies:** None (this is the entry point)
- **Constraints:** Limited customization options compared to a full-fledged web framework

### 2. Gemini API Integration
- **Purpose:** Connect to Google's Gemini Flash-4 API to generate incident messages
- **Technologies:** Python, google-generativeai library
- **Interfaces:**
  - **Input:** Structured incident data from the UI
  - **Output:** Generated message text
- **Dependencies:** Valid API key, internet connection
- **Constraints:** Subject to API rate limits and potential latency

### 3. Text Analysis Engine
- **Purpose:** Analyze generated messages for readability, clarity, and technical level
- **Technologies:** Python, textstat library
- **Interfaces:**
  - **Input:** Generated message text
  - **Output:** Quality metrics and scores
- **Dependencies:** None
- **Constraints:** Analysis is based on heuristics and may not perfectly match human perception

### 4. Message Formatter
- **Purpose:** Apply appropriate formatting and styling to messages
- **Technologies:** Python, HTML/CSS (for styling)
- **Interfaces:**
  - **Input:** Raw message text and incident metadata
  - **Output:** Formatted message with styling
- **Dependencies:** None
- **Constraints:** Limited to HTML/CSS styling that works within Streamlit

## Data Flow Diagrams

### Primary User Journey: Generating an Incident Message

```
┌─────────┐     ┌─────────────┐     ┌────────────┐     ┌───────────┐     ┌────────────┐
│         │     │             │     │            │     │           │     │            │
│  User   │────►│ Input Form  │────►│ Generate   │────►│ Analyze   │────►│ Display &  │
│         │     │ Submission  │     │ Message    │     │ Quality   │     │ Export     │
│         │     │             │     │            │     │           │     │            │
└─────────┘     └─────────────┘     └────────────┘     └───────────┘     └────────────┘
```

**Process Description:**
1. User fills out the incident details form with information about severity, impacted services, customer impact, etc.
2. User submits the form to generate a message
3. System sends structured data to Gemini API with an appropriate prompt
4. Gemini returns a generated message based on the incident details
5. System analyzes the message for readability, clarity, and technical level
6. System formats the message with appropriate styling
7. System displays the message, quality metrics, and status page preview to the user
8. User can download the message in various formats (TXT, MD, HTML)

## API Documentation

### Gemini Flash-4 API Integration
- **API:** Google's Gemini Flash-4 API
- **Method:** POST
- **Description:** Generates natural language content based on a prompt
- **Request Parameters:**
  - `prompt` (string): The structured prompt containing incident details and instructions
  - `model` (string): "models/flash-4"
  - `api_key` (string): Authentication key for the API
- **Response Format:**
  ```json
  {
    "text": "Generated message content",
    "usage": {
      "prompt_tokens": 123,
      "completion_tokens": 456,
      "total_tokens": 579
    }
  }
  ```
- **Error Responses:**
  - **Status Code 400:** Invalid request format
  - **Status Code 401:** Invalid API key
  - **Status Code 429:** Rate limit exceeded
  - **Status Code 500:** Internal server error

## AI Integration Flow

### Gemini Flash-4 Integration
- **Purpose:** Generate professional, clear incident messages based on user input
- **Prompt Engineering:**
  - **Input Context:** Structured data about the incident (severity, impacted services, customer impact, etc.)
  - **Prompt Template:**
    ```
    You are a highly skilled communications specialist at Abnormal Security, responsible for drafting incident status updates.
    Create a {message_type} for customers with the following details:
    
    - Severity: {severity}
    - Impacted Services: {impacted_services}
    - Customer Impact: {customer_impact}
    - Root Cause: {root_cause}
    - Mitigation Steps: {mitigation}
    - Estimated Resolution Time: {eta}
    
    Please craft a message that is:
    1. Clear, concise, and honest
    2. Written at a {tone} level
    3. Appropriate for a {message_type}
    4. Follows best practices for incident communication
    5. Avoids unnecessary technical jargon
    6. Instills confidence while being transparent
    ```
  - **Output Processing:** Raw text is analyzed for quality metrics and then formatted for display
- **Error Handling:**
  - **Timeout Handling:** Retry up to 3 times with exponential backoff
  - **Content Filtering:** Check for empty or malformed responses
  - **Fallback Mechanisms:** Display generic template if AI generation fails

## Error Handling Flows

### API Connection Failure
- **Trigger Condition:** Unable to connect to Gemini API or receive a valid response
- **System Response:** Display error message to user
- **User Impact:** Cannot generate new message
- **Recovery Process:** Prompt user to try again or use a template
- **Error Logging:** Log API error details for troubleshooting

### Invalid Input Data
- **Trigger Condition:** Missing required fields or invalid input values
- **System Response:** Form validation error messages
- **User Impact:** Cannot submit form until errors are corrected
- **Recovery Process:** Highlight problematic fields and provide guidance
- **Error Logging:** Log validation errors if they indicate a UI problem

## Data Models

### Incident Data Model
```
{
  "severity": string,           // Severity level (P0-P3)
  "impacted_services": string[],// List of affected services
  "customer_impact": string,    // Description of customer impact
  "root_cause": string,         // Description of root cause (optional)
  "mitigation": string,         // Mitigation steps in progress
  "eta": string,                // Estimated time to resolution
  "message_type": string,       // Initial/update/resolution
  "tone": string                // Technical level of the message
}
```

### Analysis Results Model
```
{
  "readability": float,         // Readability score (0-100)
  "clarity": float,             // Clarity score (0-100)
  "technical_level": float,     // Technical level score (0-100)
  "sentence_count": int,        // Number of sentences
  "word_count": int,            // Number of words
  "grade_level": float          // Reading grade level
}
```

## Security Flow

- **API Key Management:**
  - API keys stored in .env file (not in version control)
  - Keys loaded at runtime using python-dotenv
  
- **Data Protection:**
  - No user data or generated messages stored persistently
  - All processing happens in-memory during the session

## Change History

| Version | Date | Updated By | Changes |
|---------|------|------------|---------|
| 1.0 | May 26, 2025 | Development Team | Initial documentation for MVP phase |

## References
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Phase1_MVP.md](Phase1_MVP.md) - Project requirements document 