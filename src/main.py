import os
import sys

# Ensure the root directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.extractor import DataExtractor
from src.processor import DDRProcessor
from src.generator import DDRGenerator

def main():
    # File paths based on your filenames
    inspection_pdf = "data/raw/Sample Report.pdf"
    thermal_pdf = "data/raw/Thermal Images.pdf"

    # Check if files exist to avoid FileNotFoundError
    if not os.path.exists(inspection_pdf) or not os.path.exists(thermal_pdf):
        print("❌ Error: One or both PDF files are missing in 'data/raw/'")
        return

    print(f"✅ Found: {inspection_pdf}")
    print(f"✅ Found: {thermal_pdf}")

    # 1. Extract Text & Images [cite: 31, 32, 51]
    # This fulfills the requirement to extract textual observations and images
    extractor = DataExtractor(inspection_pdf, thermal_pdf)
    data = extractor.run()
    
    # 2. Process with Mistral [cite: 34, 35, 36, 37]
    # Logic to combine information, avoid duplicates, and handle missing details
    processor = DDRProcessor()
    report_content = processor.analyze_data(
        data['inspection']['text'], 
        data['thermal']['text']
    )
    
    # 3. Generate Final Document [cite: 42, 52]
    # Structured into the 7 mandatory sections including Property Issue Summary and Recommendations
    generator = DDRGenerator()
    # Passing the extracted images to be placed in appropriate sections
    generator.create_report(report_content, image_mappings=data['inspection']['images'] + data['thermal']['images']) 
    
    print("--- DDR Workflow Complete! Check the /output folder for Final_DDR_Report.docx ---")

if __name__ == "__main__":
    main()