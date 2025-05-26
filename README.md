# AbComm AI - Incident Messaging Assistant

AbComm AI is a tool designed to help Abnormal Security teams create clear, effective customer-facing messages during service incidents.

## Features

- Generate professional incident messages using Gemini Flash-4 AI
- Input form for all relevant incident details
- Real-time message quality scoring
- Status page preview
- Export options (TXT, MD, HTML)

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Gemini API key from [Google AI Studio](https://ai.google.dev/)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/abcomm-ai.git
   cd abcomm-ai
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root:
   ```
   cp env.example .env
   ```

6. Add your Gemini API key to the `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Fill in the incident details form with information about the service incident

4. Click "Generate Message" to create an AI-powered incident message

5. Review the message, check quality metrics, and make any necessary edits

6. Use the export options to download the message in your preferred format

## Project Structure

```
abcomm-ai/
├── app.py                  # Main Streamlit application
├── .env                    # Environment variables (API keys)
├── requirements.txt        # Python dependencies
├── utils/
│   ├── gemini_utils.py     # Gemini API integration
│   ├── text_analysis.py    # Text quality analysis
│   └── templates.py        # Message formatting templates
└── README.md               # This file
```

## Development

This project is in active development as part of a phased approach:

- **Phase 1 (Current):** MVP with core functionality
- **Phase 2:** Enhanced UI, template library, and AI collaboration
- **Phase 3:** Advanced features including multi-channel distribution

## License

[Specify your license information here] 