import fitz  # PyMuPDF
import os
from tqdm import tqdm

class DataExtractor:
    def __init__(self, inspection_path, thermal_path, output_img_dir="data/processed/images"):
        self.inspection_path = inspection_path
        self.thermal_path = thermal_path
        self.output_img_dir = output_img_dir
        os.makedirs(output_img_dir, exist_ok=True)

    def extract_data(self, pdf_path, prefix):
        doc = fitz.open(pdf_path)
        full_text = ""
        image_data = []
        
        # Add Progress Bar for pages
        for page_num in tqdm(range(len(doc)), desc=f"Processing {prefix}"):
            page = doc[page_num]
            full_text += f"\n--- Page {page_num + 1} ---\n" + page.get_text()

            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                img_name = f"{prefix}_p{page_num+1}_i{img_index}.png"
                img_path = os.path.join(self.output_img_dir, img_name)
                
                with open(img_path, "wb") as f:
                    f.write(base_image["image"])
                
                image_data.append({"path": img_path, "page": page_num + 1})

        return full_text, image_data

    def run(self):
        # Using a main progress bar for the two files
        results = {}
        for pdf, prefix in [(self.inspection_path, "insp"), (self.thermal_path, "thermal")]:
            text, imgs = self.extract_data(pdf, prefix)
            results[prefix] = {"text": text, "images": imgs}
        
        return {
            "inspection": results["insp"],
            "thermal": results["thermal"]
        }