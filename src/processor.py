import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

class DDRProcessor:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.model = "mistral-large-latest"
        self.client = Mistral(api_key=self.api_key)

    def analyze_data(self, inspection_text, thermal_text):
        prompt = f"""
        You are an expert technical building inspector. Your task is to generate a Detailed Diagnostic Report (DDR).
        
        INPUT DATA:
        --- Inspection Report ---
        {inspection_text}
        
        --- Thermal Report ---
        {thermal_text}
        
        REQUIREMENTS:
        1. Combine information logically. Avoid duplicate points.
        2. If information is missing, write "Not Available".
        3. Do NOT invent facts.
        4. Use simple, client-friendly language. Avoid jargon.
        
        STRUCTURE:
        1. Property Issue Summary
        2. Area-wise Observations (List findings by area)
        3. Probable Root Cause
        4. Severity Assessment (Include reasoning: Low, Medium, High)
        5. Recommended Actions
        6. Additional Notes
        7. Missing or Unclear Information
        """
        
        # This uses the new Mistral SDK pattern
        response = self.client.chat.complete(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    