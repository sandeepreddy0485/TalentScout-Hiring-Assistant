# 🤖 TalentScout – AI-Powered Hiring Assistant

**TalentScout Hiring Assistant** is an AI/ML-inspired recruitment screening chatbot built with **Python and Streamlit**.

The application automates the initial candidate screening process by collecting candidate information through an interactive conversational interface, identifying the candidate's technology stack, and generating relevant technical interview questions.

TalentScout maintains conversation context, validates user inputs, handles unclear responses, and stores completed candidate profiles in a structured JSON format.

---

## 📌 Project Overview

Recruiters often spend significant time collecting basic candidate information and conducting initial technical screenings before moving candidates to further interview rounds.

**TalentScout Hiring Assistant** is designed to simplify this process through an interactive recruitment chatbot.

The assistant guides candidates through a structured conversation and collects information such as:

- Full Name
- Email Address
- Phone Number
- Years of Experience
- Desired Position
- Current Location
- Technical Skills / Tech Stack

Once the candidate provides their technology stack, TalentScout identifies the technologies and generates **3–5 relevant technical screening questions for each recognized technology**.

After completing the screening process, the candidate's information is stored locally in JSON format for future review.

---

## 🎯 Objectives

The main objectives of TalentScout are:

- Automate initial candidate information collection
- Provide an interactive chatbot-based recruitment experience
- Validate candidate information
- Identify technologies from candidate-provided tech stacks
- Generate technology-specific interview questions
- Maintain conversational context throughout the screening
- Handle invalid or unclear user inputs
- Support exit commands during the conversation
- Store candidate information in structured JSON format
- Build a modular and maintainable Python application
- Provide a foundation for future Generative AI integration

---

## ✨ Key Features

### 💬 Interactive Recruitment Chatbot

TalentScout provides a conversational interface that guides candidates through the initial screening process step by step.

Instead of displaying a long traditional application form, the chatbot collects candidate information through an interactive conversation.

```text
TalentScout
     │
     ▼
Candidate Introduction
     │
     ▼
Personal Information
     │
     ▼
Professional Experience
     │
     ▼
Desired Position
     │
     ▼
Tech Stack
     │
     ▼
Technical Questions
     │
     ▼
Candidate Profile Storage
```

---

### 👤 Candidate Information Collection

The chatbot collects important candidate details, including:

- Full name
- Email
- Phone number
- Years of experience
- Desired position
- Location
- Technology stack

Information is collected sequentially to create a structured screening experience.

---

### 🛠️ Tech Stack Detection

Candidates can provide their technical skills in a simple format.

For example:

```text
Python, Django, React, SQL
```

TalentScout processes and normalizes the provided technologies before generating relevant technical questions.

---

### ❓ Technical Question Generation

After identifying the candidate's technology stack, the assistant generates a set of technical screening questions.

The system can provide approximately **3–5 questions per recognized technology**, depending on the available question templates.

Example:

```text
Candidate Tech Stack
        │
        ▼
Python, Django, React, SQL
        │
        ▼
Technology Detection
        │
        ├── Python
        ├── Django
        ├── React
        └── SQL
        │
        ▼
Technical Question Generation
```

This allows the initial technical screening to be personalized according to the candidate's skills.

---

### ✅ Input Validation

TalentScout validates structured candidate information to improve data quality.

Validation logic includes:

- Email validation
- Phone number validation
- Experience validation

If invalid information is provided, the chatbot asks the candidate to provide the information again.

---

### 🧠 Conversation State Management

Streamlit applications rerun when users interact with the interface, making conversational state management an important challenge.

TalentScout uses:

```python
st.session_state
```

to maintain:

- Current conversation step
- Candidate information
- Chat messages
- Screening status
- Session completion state

This enables a continuous chatbot-like experience.

---

### 🔄 Conversation Context

The application maintains context throughout the screening process.

```text
Start Conversation
       │
       ▼
Collect Field
       │
       ▼
Validate Input
       │
    ┌──┴──┐
    │     │
 Valid  Invalid
    │     │
    ▼     ▼
 Next   Ask Again
 Field
    │
    ▼
Continue Conversation
```

---

### 🚪 Exit Command Detection

Candidates can exit the screening process using supported exit keywords.

The system detects these commands and ends the session gracefully instead of forcing the candidate to complete the entire process.

---

### 🤔 Handling Unclear Input

If the candidate provides an invalid or unclear response, TalentScout uses fallback messages to guide them back into the expected conversation flow.

This improves the reliability and usability of the chatbot.

---

### 💾 Candidate Profile Storage

After the screening process is completed, candidate information is stored in JSON format.

```text
data/candidates.json
```

A stored candidate profile can contain information such as:

```json
{
  "name": "Candidate Name",
  "email": "candidate@example.com",
  "phone": "XXXXXXXXXX",
  "experience": "2",
  "position": "Software Developer",
  "location": "Hyderabad",
  "tech_stack": [
    "Python",
    "Django",
    "React",
    "SQL"
  ]
}
```

This provides a simple persistent storage mechanism for candidate information.

---

## 🏗️ System Architecture

```text
                         Candidate
                             │
                             ▼
                    Streamlit Interface
                             │
                             ▼
                    Conversation Engine
                             │
               ┌─────────────┼─────────────┐
               │             │             │
               ▼             ▼             ▼
          Input          Session        Prompt
        Validation        State        Templates
               │             │             │
               └─────────────┼─────────────┘
                             │
                             ▼
                    Candidate Profile
                             │
                             ▼
                    Tech Stack Parser
                             │
                             ▼
                 Question Generation
                             │
                             ▼
                  Technical Screening
                             │
                             ▼
                   JSON Persistence
                             │
                             ▼
                  data/candidates.json
```

---

## 🔄 Conversation Flow

The application follows a structured screening workflow.

### Step 1 – Greeting

The chatbot welcomes the candidate and explains the screening process.

### Step 2 – Candidate Information

TalentScout collects candidate information one field at a time.

```text
Full Name
    │
    ▼
Email Address
    │
    ▼
Phone Number
    │
    ▼
Years of Experience
    │
    ▼
Desired Position
    │
    ▼
Location
    │
    ▼
Technology Stack
```

### Step 3 – Input Validation

Structured inputs such as email, phone, and experience are validated.

If an input is invalid:

```text
Invalid Input
      │
      ▼
Fallback Message
      │
      ▼
Request Input Again
```

### Step 4 – Tech Stack Processing

The candidate's technical skills are normalized and matched against supported technologies.

### Step 5 – Technical Questions

Relevant technical questions are generated for recognized technologies.

### Step 6 – Candidate Storage

The completed candidate profile is stored in:

```text
data/candidates.json
```

### Step 7 – Completion

The assistant displays a thank-you message and completes the screening session.

---

## 🛠️ Tech Stack

### Programming Language

- Python

### Web Application Framework

- Streamlit

### Data Storage

- JSON

### Application Concepts

- Conversational UI
- Input Validation
- Session State Management
- Rule-Based Question Generation
- Technology Normalization
- Modular Python Architecture

### Development Tools

- Git
- GitHub
- VS Code

---

## 📁 Project Structure

```text
TalentScout-Hiring-Assistant/
│
├── .gitignore
├── README.md
├── app.py
├── prompt_templates.py
├── requirements.txt
├── runtime.txt
└── utils.py
```

The application may generate a data directory during usage:

```text
data/
└── candidates.json
```

---

## 📄 File Description

| File | Description |
|---|---|
| `app.py` | Main Streamlit application and conversation flow |
| `prompt_templates.py` | Contains chatbot messages and prompt templates |
| `utils.py` | Contains validation, technology processing, question lookup, and JSON persistence utilities |
| `requirements.txt` | Python package dependencies |
| `runtime.txt` | Specifies the Python runtime version |
| `.gitignore` | Prevents unnecessary files and virtual environments from being committed |
| `README.md` | Project documentation |

---

## 🧩 Prompt Design

The `prompt_templates.py` module contains reusable conversation templates.

These include:

### `GREETING_TEXT`

Provides the welcome message and introduces the candidate to the screening process.

### `ABOUT_TEXT`

Provides information about the TalentScout Hiring Assistant.

### `CONFUSED_TEXT`

Handles invalid, unclear, or unexpected user input.

### `EXIT_TEXT`

Provides a graceful response when the candidate chooses to exit the screening process.

### `THANK_YOU_TEXT`

Displays the final message after the candidate completes the screening.

Separating these messages from the main application logic makes the project easier to maintain and extend.

---

## ⚙️ Utility Functions

The `utils.py` module contains reusable application logic.

It handles functionality such as:

- Email validation
- Phone number validation
- Experience validation
- Exit command detection
- Technology stack normalization
- Technical question lookup
- Candidate profile persistence
- JSON data storage

This modular structure keeps the main application code cleaner and more maintainable.

---

## 🧠 Session State Management

One of the main technical challenges when developing a chatbot using Streamlit is maintaining conversation state.

Streamlit reruns the application whenever the user interacts with the interface.

TalentScout solves this using:

```python
st.session_state
```

The session state acts as the application's conversation memory.

Conceptually:

```text
User Message
     │
     ▼
Streamlit Rerun
     │
     ▼
Read Session State
     │
     ▼
Determine Current Step
     │
     ▼
Process User Input
     │
     ▼
Update Session State
     │
     ▼
Render Updated Conversation
```

This enables the application to maintain a continuous conversation.

---

## ❓ Question Generation Logic

The current version uses technology detection and predefined question templates to generate technical screening questions.

```text
Candidate Input
"Python, Django, React, SQL"
            │
            ▼
      Normalize Input
            │
            ▼
    Identify Technologies
            │
     ┌──────┼──────┐
     ▼      ▼      ▼
  Python  Django  React ...
     │      │      │
     ▼      ▼      ▼
Question Templates
     │      │      │
     └──────┼──────┘
            │
            ▼
 Technical Question Set
```

This approach allows the application to generate relevant questions without requiring an external AI API.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have installed:

- Python 3.11+
- pip
- Git

---

## 📥 Clone the Repository

```bash
git clone https://github.com/sandeepreddy0485/TalentScout-Hiring-Assistant.git
```

Navigate to the project:

```bash
cd TalentScout-Hiring-Assistant
```

---

## 🐍 Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

The current version does not require an OpenAI API key to run.

However, the project can be extended with Generative AI functionality.

For future OpenAI integration, create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
```

> Never commit real API keys or secrets to GitHub.

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Streamlit will display the local application URL in the terminal.

Typically:

```text
http://localhost:8501
```

Open the URL in your browser to use TalentScout.

---

## 🧪 Example Conversation

```text
TalentScout:
Welcome to TalentScout Hiring Assistant!
I'll guide you through the initial screening process.

Candidate:
John Doe

TalentScout:
Please enter your email address.

Candidate:
john@example.com

TalentScout:
Please provide your phone number.

...

TalentScout:
Please enter your technology stack.

Candidate:
Python, Django, React, SQL

TalentScout:
Here are your technical screening questions.

Python:
• [Python technical question]
• [Python technical question]
• [Python technical question]

Django:
• [Django technical question]
• [Django technical question]
• [Django technical question]

React:
• [React technical question]

SQL:
• [SQL technical question]

TalentScout:
Thank you for completing the screening process.
```

---

## 🎯 Challenges & Solutions

### Challenge 1: Maintaining Conversation State

**Problem:** Streamlit reruns the application after every user interaction.

**Solution:** Used `st.session_state` to maintain the current step, conversation messages, candidate data, and session status.

---

### Challenge 2: Technology Detection

**Problem:** Candidates may enter technology names in different formats.

**Solution:** Implemented technology normalization and mapping logic to identify supported technologies consistently.

---

### Challenge 3: Invalid User Input

**Problem:** Candidates may provide incorrectly formatted emails, phone numbers, or experience values.

**Solution:** Implemented dedicated validation functions with fallback messages that request corrected input.

---

### Challenge 4: Persistent Candidate Data

**Problem:** Candidate information needs to remain available after the conversation ends.

**Solution:** Implemented JSON-based persistence to store completed candidate profiles.

---

## 🔮 Future Improvements

Potential future enhancements include:

- 🤖 OpenAI or Gemini API integration
- 🧠 LLM-generated technical questions
- 💬 Dynamic AI-powered conversations
- 📊 Recruiter dashboard
- 🗄️ PostgreSQL or MongoDB database
- 🔐 Recruiter authentication
- 👥 Candidate management
- 📄 Resume upload and parsing
- 🎯 AI-powered resume screening
- 📈 Candidate scoring and ranking
- 🗣️ Sentiment analysis
- 🌍 Multi-language support
- 💾 Persistent conversation history
- 📧 Email notifications
- 📅 Interview scheduling
- 🎥 Video interview integration
- 📊 Recruitment analytics
- ☁️ Cloud deployment
- 🐳 Docker containerization

---

## 🚀 Future AI Architecture

A future version of TalentScout could integrate Large Language Models to create a more intelligent recruitment assistant.

```text
                         Candidate
                             │
                             ▼
                      TalentScout UI
                             │
                             ▼
                     Conversation Engine
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
         Resume Parser                Candidate Profile
              │                             │
              └──────────────┬──────────────┘
                             │
                             ▼
                     Large Language Model
                             │
               ┌─────────────┼─────────────┐
               │             │             │
               ▼             ▼             ▼
           Question      Candidate      Skill Gap
          Generation     Evaluation      Analysis
               │             │             │
               └─────────────┼─────────────┘
                             │
                             ▼
                     Candidate Scoring
                             │
                             ▼
                     Recruiter Dashboard
```

---

## 💡 Potential Use Cases

TalentScout can serve as a foundation for:

### 🏢 Recruitment

Automating initial candidate information collection and technical screening.

### 🎓 Campus Placements

Conducting preliminary technical screening for students.

### 💼 Recruitment Agencies

Standardizing candidate intake and initial assessment.

### 🚀 Startups

Providing lightweight recruitment automation for small hiring teams.

### 🧑‍💻 Developer Hiring

Generating technology-specific questions based on candidate skills.

---

## ⚠️ Current Project Scope

The current version of TalentScout is an **AI/ML-inspired recruitment screening chatbot** built with Python and Streamlit.

Technical questions are generated using technology detection and predefined question templates. The current application does **not require an external LLM or OpenAI API** to function.

Advanced Generative AI capabilities described in the Future Improvements section are planned extensions and are not presented as existing functionality.

---

## ⚠️ Disclaimer

TalentScout is developed for educational and demonstration purposes.

Automated recruitment tools should not be used as the sole basis for employment decisions. Candidate evaluation should involve appropriate human review and should consider fairness, transparency, privacy, and potential bias.

---

## 👨‍💻 Developer

**Sandeep Reddy Yaramala**

B.Tech Computer Science & Engineering Student

Interested in:

- Software Engineering
- Artificial Intelligence
- Machine Learning
- Generative AI
- Full-Stack Development

### GitHub

@sandeepreddy0485

---

## 🤝 Contributing

Contributions and suggestions are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/your-feature-name
```

3. Make your changes.
4. Commit your changes:

```bash
git commit -m "Add new feature"
```

5. Push your branch:

```bash
git push origin feature/your-feature-name
```

6. Open a Pull Request.

---

## ⭐ Support

If you find TalentScout interesting or useful, consider giving the repository a ⭐.

---

## 📄 License

This project is intended for educational and personal development purposes.

---

### 🤖 TalentScout Hiring Assistant

**A conversational recruitment screening assistant built with Python and Streamlit.**
