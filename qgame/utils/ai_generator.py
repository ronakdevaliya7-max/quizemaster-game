import os
import json
import google.generativeai as genai

def generate_questions_with_gemini(board, standard, subject, num_questions=10):
    """
    Calls Google Gemini API to generate Quiz Questions in the required 3-language JSON format.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise Exception("GEMINI_API_KEY is not set in the environment variables. Please add it to your server configuration.")
        
    genai.configure(api_key=api_key)
    
    # Using gemini-1.5-flash-latest for better compatibility across regions
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = f"""
Act as a Senior Education Content Creator for {board} Board.
I am building a multilingual educational Quiz Game.

Please generate {num_questions} real, curriculum-based MCQ questions for:
Standard: {standard}
Subject: {subject}

For every question, you MUST provide the text in 3 languages: English, Gujarati, and Hindi.

Return ONLY a valid JSON array. Do not add any extra text, markdown formatting, or ```json tags outside the JSON.

Use this EXACT JSON structure for each question:
[
    {{
        "board": "{board}",
        "standard": "{standard}",
        "stream": "General",
        "subject": "{subject}",
        "chapter": "Appropriate Chapter Name Here",
        "topic": "Appropriate Topic Name Here",
        "difficulty": "Medium",
        "question": {{
            "en": "English question text",
            "gu": "Gujarati question text",
            "hi": "Hindi question text"
        }},
        "options": {{
            "en": ["Option A", "Option B", "Option C", "Option D"],
            "gu": ["Option A", "Option B", "Option C", "Option D"],
            "hi": ["Option A", "Option B", "Option C", "Option D"]
        }},
        "correct_option": "A",
        "explanation": {{
            "en": "English explanation",
            "gu": "Gujarati explanation",
            "hi": "Hindi explanation"
        }},
        "source": "{board} Textbook",
        "source_type": "Official",
        "verified": true
    }}
]

Generate exactly {num_questions} distinct, accurate questions.
"""
    
    try:
        response = model.generate_content(prompt)
        text_output = response.text
        
        # Clean up markdown if AI included it
        if text_output.startswith("```json"):
            text_output = text_output.replace("```json", "", 1)
        if text_output.startswith("```"):
            text_output = text_output.replace("```", "", 1)
        if text_output.endswith("```"):
            text_output = text_output[::-1].replace("```", "", 1)[::-1]
            
        data = json.loads(text_output.strip())
        return data
    except Exception as e:
        raise Exception(f"Failed to generate questions from AI: {str(e)}")
