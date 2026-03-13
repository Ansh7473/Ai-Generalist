
#core logic mine rest code is enhanced throught AI
import os
from dotenv import load_dotenv

load_dotenv()

class DDRProcessor:
    def __init__(self):
        # All API keys mapped from your .env
        self.keys = {
            "Mistral": os.getenv("MISTRAL_API_KEY"),
            "Claude": os.getenv("ANTHROPIC_API_KEY"),
            "OpenAI": os.getenv("OPENAI_API_KEY"),
            "Gemini": os.getenv("GEMINI_API_KEY"),
            "Groq": os.getenv("GROQ_API_KEY"),
            "DeepSeek": os.getenv("DEEPSEEK_API_KEY"),
            "OpenRouter": os.getenv("OPENROUTER_API_KEY"),
            "Cerebras": os.getenv("CEREBRAS_API_KEY")
        }

    def analyze_data(self, inspection_text, thermal_text, model_choice="Mistral"):
        # The central 'Rulebook' for the report
        system_instruction = (
            "You are a professional building diagnostic expert. "
            "Merge Site Inspection data with Thermal Imaging data into a 7-section DDR: "
            "1. Property Issue Summary, 2. Area-wise Observations, 3. Root Cause Analysis, "
            "4. Severity Assessment, 5. Recommended Actions, 6. Limitations, 7. Disclaimer. "
            "Rules: Use simple language. Write 'Not Available' for missing data. Provide Severity reasoning."
        )
        user_content = f"INSPECTION DATA:\n{inspection_text}\n\nTHERMAL DATA:\n{thermal_text}"

        try:
            if "OpenRouter" in model_choice:
                from openai import OpenAI
                client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=self.keys["OpenRouter"])
                try:
                    response = client.chat.completions.create(
                        model="openrouter/free", 
                        messages=[{"role": "system", "content": system_instruction}, {"role": "user", "content": user_content}],
                        timeout=40
                    )
                    return response.choices[0].message.content
                except Exception:
                    response = client.chat.completions.create(
                        model="google/gemini-2.0-flash-001:free",
                        messages=[{"role": "system", "content": system_instruction}, {"role": "user", "content": user_content}]
                    )
                    return response.choices[0].message.content

            # --- DEEPSEEK (Direct V3.2 - Paid/Standard) ---
            elif "DeepSeek" in model_choice:
                from openai import OpenAI
                client = OpenAI(api_key=self.keys["DeepSeek"], base_url="https://api.deepseek.com")
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_content}
                    ]
                )
                return response.choices[0].message.content

            # --- CEREBRAS (Ultra-Fast Inference) ---
            elif "Cerebras" in model_choice:
                from cerebras.cloud.sdk import Cerebras
                client = Cerebras(api_key=self.keys["Cerebras"])
                try:
                    response = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": user_content}
                        ],
                        model="llama-3.3-70b",
                        max_completion_tokens=2048,
                        temperature=0.2
                    )
                except Exception:
                    response = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": user_content}
                        ],
                        model="llama3.1-8b",
                        max_completion_tokens=2048,
                        temperature=0.2
                    )
                return response.choices[0].message.content

            # --- GEMINI 2.0 FLASH ---
            elif "Gemini" in model_choice:
                from google import genai
                client = genai.Client(api_key=self.keys["Gemini"])
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=f"{system_instruction}\n\n{user_content}"
                )
                return response.text

            # --- GROQ (Llama 3.3 Versatile) ---
            elif "Groq" in model_choice:
                from groq import Groq
                client = Groq(api_key=self.keys["Groq"])
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_content}
                    ]
                )
                return response.choices[0].message.content

            # --- OPENAI GPT-4o ---
            elif "OpenAI" in model_choice:
                from openai import OpenAI
                client = OpenAI(api_key=self.keys["OpenAI"])
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_content}
                    ]
                )
                return response.choices[0].message.content

            # --- CLAUDE 3.5 SONNET ---
            elif "Claude" in model_choice:
                import anthropic
                client = anthropic.Anthropic(api_key=self.keys["Claude"])
                response = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=4000,
                    system=system_instruction,
                    messages=[{"role": "user", "content": user_content}]
                )
                return response.content[0].text

            
            # --- MISTRAL LARGE (Adaptive Logic) ---
            else:
                from mistralai.client import Mistral
                
                if not self.keys["Mistral"]:
                    return "❌ Mistral Error: API Key is missing in .env"

                client = Mistral(api_key=self.keys["Mistral"])
                response = client.chat.complete(
                    model="mistral-large-latest",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_content}
                    ]
                )
                return response.choices[0].message.content

        except Exception as e:
            return f"❌ {model_choice} Error: {str(e)}"
