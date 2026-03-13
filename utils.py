import os
import json
import re
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

EXITS = ["exit", "quit", "bye", "end"]

# Fallback question bank (used if API fails or for unknown tech)
TECH_QUESTION_BANK = {
    "python": [
        "Explain list comprehension and give an example.",
        "How do you manage virtual environments in Python?",
        "What is the difference between `deepcopy` and `shallow copy`?",
        "Explain Python decorators and a use case.",
        "How do you handle exceptions in Python?",
    ],
    "django": [
        "What are Django models and how do they map to database tables?",
        "Explain the request-response cycle in Django.",
        "How does Django authentication and authorization work?",
        "How do you define URL routes in Django?",
        "What are Django signals?",
    ],
    "flask": [
        "What is the Flask application context?",
        "How do you define routes in Flask?",
        "Explain the difference between Flask and Django.",
        "How do you manage extensions in Flask?",
        "How do you set up Flask unit testing?",
    ],
    "react": [
        "Describe the component lifecycle in React.",
        "What is JSX and why is it useful?",
        "How do you manage state in functional components?",
        "Explain props and state differences.",
        "How would you optimize React rendering performance?",
    ],
    "sql": [
        "What are primary keys and foreign keys?",
        "How do you write a JOIN query between two tables?",
        "What is normalization and why is it important?",
        "Explain the difference between DELETE and TRUNCATE.",
        "How do you index a table and why?",
    ],
    "node": [
        "Explain the Node.js event loop.",
        "How do you manage dependencies with npm/yarn?",
        "What is middleware in Express?",
        "How do you handle async operations in Node.js?",
        "What is the difference between CommonJS and ES Modules?",
    ],
    "express": [
        "How do you create routes in Express?",
        "How can you secure an Express app?",
        "Explain middleware execution order in Express.",
        "How do you handle errors in Express?",
        "How do you use template engines with Express?",
    ],
    "aws": [
        "Explain how to deploy a web app using AWS Elastic Beanstalk.",
        "What is the difference between EC2 and Lambda?",
        "How does AWS IAM work?",
        "What is S3 and what are its common use cases?",
        "How do you monitor AWS resources?",
    ],
}

FALLBACK_QUESTIONS = [
    "Tell me what you know about this technology.",
    "Describe a project where you used this technology.",
    "What are common pitfalls with this technology?",
]


def is_exit_command(user_text: str) -> bool:
    return user_text.strip().lower() in EXITS


def validate_input(field_key: str, text: str) -> bool:
    if not text or not text.strip():
        return False

    text = text.strip()
    if field_key == "email":
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        return bool(re.match(pattern, text))
    if field_key == "phone":
        digits = re.sub(r"[^0-9]", "", text)
        return 7 <= len(digits) <= 15
    if field_key == "experience":
        try:
            val = float(text)
            return 0 <= val <= 50
        except ValueError:
            return False
    return True


def collect_candidate_value(field_key: str, text: str):
    if field_key == "experience":
        return float(text)
    if field_key == "tech_stack":
        return text
    return text.strip()


def parse_tech_stack(raw_text: str) -> List[str]:
    techs = re.split(r"[,;|]", raw_text)
    parsed = []
    for tech in techs:
        normalized = tech.strip().lower()
        if not normalized:
            continue

        # Handle special characters
        normalized = normalized.replace(" .", "").replace("#", "sharp")
        normalized = normalized.replace("++", "pp")

        # Common synonyms
        if normalized in ["py", "python3", "python2"]:
            normalized = "python"
        if normalized in ["js", "javascript"]:
            normalized = "node"
        if normalized == "reactjs":
            normalized = "react"
        if normalized == "c#":
            normalized = "csharp"
        if normalized == "c++":
            normalized = "cpp"

        parsed.append(normalized)

    # Remove duplicates while preserving order
    unique = []
    for item in parsed:
        if item not in unique:
            unique.append(item)
    return unique


def generate_questions_for_tech_stack(tech_stack: List[str]) -> Dict[str, List[str]]:
    """
    Generate technical questions using OpenAI GPT (if available).
    Falls back to static question bank if API fails or key missing.
    """
    results = {}
    for tech in tech_stack:
        # Try OpenAI first if API key exists
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                # Import OpenAI only when needed to avoid initialization errors
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                
                prompt = f"""
You are a technical interviewer. Generate 4 concise, relevant technical questions to assess a candidate's proficiency in {tech}. 
The questions should range from basic to advanced and be specific to {tech}. 
Return only the questions as a numbered list, each on a new line starting with a number.
"""
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=300
                )
                questions_text = response.choices[0].message.content.strip()
                lines = questions_text.split('\n')
                questions = []
                for line in lines:
                    line = line.strip()
                    if line and (line[0].isdigit() or line.startswith("-") or line.startswith("•")):
                        clean = re.sub(r'^[\d\-\•\.\s]+', '', line).strip()
                        if clean:
                            questions.append(clean)
                if questions:
                    results[tech] = questions[:5]
                    continue  # success, skip fallback
            except Exception as e:
                print(f"OpenAI API error for {tech}: {e}")  # log to console

        # Fallback: use static bank
        known = TECH_QUESTION_BANK.get(tech.lower())
        if known:
            results[tech] = known[:5]
        else:
            # Generic fallback
            results[tech] = [f"{q} ({tech})" for q in FALLBACK_QUESTIONS]
    return results


def save_candidate(file_path: str, candidate: dict):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        if not os.path.isfile(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = []

    data.append(candidate)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return True


def analyze_sentiment(text: str) -> str:
    """
    Simple rule-based sentiment analysis.
    Returns one of: "Positive tone detected 👏", "Negative tone detected 😕", "Neutral tone."
    """
    positive = ["good", "great", "excellent", "confident", "strong", "positive", "love", "solid", "awesome", "happy"]
    negative = ["bad", "weak", "difficult", "struggle", "issue", "slow", "problem", "hard", "terrible", "sad"]

    lower = text.lower()
    score = 0
    for word in positive:
        if word in lower:
            score += 1
    for word in negative:
        if word in lower:
            score -= 1

    if score > 0:
        return "Positive tone detected 👏"
    if score < 0:
        return "Negative tone detected 😕"
    return "Neutral tone."