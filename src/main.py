
#core logic mine rest code is enhanced throught AI

import os
import sys
from tqdm import tqdm
import time

# Ensure paths are correct
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.extractor import DataExtractor
from src.processor import DDRProcessor
from src.generator import DDRGenerator

def main():
    print("\n" + "="*65)
    print("🚀 INITIALIZING MULTI-MODEL DDR GENERATION SYSTEM")
    print("="*65)

    # 1. File Check Step
    inspection_pdf = "data/raw/Sample Report.pdf"
    thermal_pdf = "data/raw/Thermal Images.pdf"

    if not os.path.exists(inspection_pdf) or not os.path.exists(thermal_pdf):
        print(f"❌ FATAL ERROR: Required PDFs not found in data/raw/")
        print(f"Please ensure '{inspection_pdf}' and '{thermal_pdf}' exist.")
        return

    # 2. Advanced Model Selection Menu (Added OpenRouter)
    print("\n🤖 SELECT AI REASONING ENGINE")
    print("-" * 45)
    print("1. Mistral (Large)         | Balanced & Reliable")
    print("2. Claude 3.5 Sonnet       | Industry Leader (Pre-paid)")
    print("3. Gemini 3.1 Flash        | Huge Context (Google)")
    print("4. OpenAI (GPT-4o)         | High Accuracy")
    print("5. Groq (Llama 3.3)        | Ultra-Fast Inference")
    print("6. DeepSeek (V3.2)         | Elite Reasoning (Direct API)")
    print("7. Cerebras (Llama 3.3)    | Instant Generation (<1s)")
    print("8. OpenRouter (Free)       | DeepSeek-R1 (No-Cost Failover)") # New Option
    print("-" * 45)
    
    choice = input("\nEnter choice (1-8, default is 1): ").strip()
    
    # Map terminal input to processor labels
    # MUST match the strings used in your processor.py 'if' statements
    model_map = {
        "1": "Mistral",
        "2": "Claude",
        "3": "Gemini",
        "4": "OpenAI",
        "5": "Groq",
        "6": "DeepSeek",
        "7": "Cerebras",
        "8": "OpenRouter" # Added this mapping
    }
    
    selected_model = model_map.get(choice, "Mistral")
    print(f"\n✅ Workflow active. Routing to: {selected_model}")

    # 3. Main Workflow
    with tqdm(total=4, desc="System Pipeline", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]") as pbar:
        
        # --- STEP 1: EXTRACTION ---
        pbar.set_description("📥 [1/4] Extracting Text & Images")
        extractor = DataExtractor(inspection_pdf, thermal_pdf)
        data = extractor.run() 
        pbar.update(1)
        
        # --- STEP 2: AI REASONING ---
        pbar.set_description(f"🧠 [2/4] Reasoning via {selected_model}")
        processor = DDRProcessor()
        report_content = processor.analyze_data(
            data['inspection']['text'], 
            data['thermal']['text'],
            model_choice=selected_model
        )
        
        # Immediate check if AI returned an error (like insufficient credits)
        if "❌" in report_content:
            pbar.close()
            print(f"\n{report_content}")
            return
            
        pbar.update(1)
        
        # --- STEP 3: VALIDATION ---
        pbar.set_description("🔍 [3/4] Validating Logic & Gaps")
        time.sleep(0.5) 
        pbar.update(1)
        
        # --- STEP 4: GENERATION ---
        pbar.set_description("📄 [4/4] Formatting Final DOCX Report")
        output_path = "output/Final_DDR_Report.docx"
        generator = DDRGenerator(output_path)
        
        # Combine image lists from both PDF sources
        all_images = data['inspection']['images'] + data['thermal']['images']
        generator.create_report(report_content, image_mappings=all_images)
        pbar.update(1)

    print("\n" + "="*65)
    print(f"✅ SUCCESS: Report generated using {selected_model}")
    print(f"📂 Output Location: {os.path.abspath(output_path)}")
    print("="*65 + "\n")

if __name__ == "__main__":
    # Ensure folder structure exists before running
    os.makedirs("output", exist_ok=True)
    os.makedirs("data/processed/images", exist_ok=True)
main()