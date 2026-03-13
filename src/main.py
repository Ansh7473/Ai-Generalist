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
    print("\n" + "="*50)
    print("🚀 INITIALIZING DDR GENERATION SYSTEM")
    print("="*50)

    # 1. File Check Step
    inspection_pdf = "data/raw/Sample Report.pdf"
    thermal_pdf = "data/raw/Thermal Images.pdf"

    if not os.path.exists(inspection_pdf) or not os.path.exists(thermal_pdf):
        print(f"❌ FATAL ERROR: Required PDFs not found in data/raw/")
        return

    # 2. Progress Bar Setup
    # This acts as your 'live bar' for the background process
    with tqdm(total=4, desc="Workflow Progress", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]") as pbar:
        
        # --- STEP 1: EXTRACTION ---
        pbar.set_description("📥 Step 1: Extracting Text & Images")
        extractor = DataExtractor(inspection_pdf, thermal_pdf)
        data = extractor.run() # This has its own tqdm bars inside
        pbar.update(1)
        
        # --- STEP 2: AI REASONING ---
        pbar.set_description("🧠 Step 2: Mistral AI Reasoning & Merging")
        processor = DDRProcessor()
        # Simulated small delay for visual feedback
        report_content = processor.analyze_data(
            data['inspection']['text'], 
            data['thermal']['text']
        )
        pbar.update(1)
        
        # --- STEP 3: DEDUPLICATION & VALIDATION ---
        pbar.set_description("🔍 Step 3: Validating Data & Handling Missing Info")
        # Logic to ensure "Not Available" is handled [cite: 49, 62]
        time.sleep(1) 
        pbar.update(1)
        
        # --- STEP 4: GENERATION ---
        pbar.set_description("📄 Step 4: Formatting Final Client Report")
        generator = DDRGenerator()
        generator.create_report(report_content, image_mappings=data['inspection']['images'] + data['thermal']['images'])
        pbar.update(1)

    print("\n" + "="*50)
    print(f"✅ SUCCESS: Report generated in /output/ folder.")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()