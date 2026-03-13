import fitz  # PyMuPDF
import os

class DataExtractor:
    def __init__(self, inspection_path, thermal_path, output_img_dir="data/processed/images"):
        self.inspection_path = inspection_path
        self.thermal_path = thermal_path
        self.output_img_dir = output_img_dir
        os.makedirs(output_img_dir, exist_ok=True)

    def extract_data(self, pdf_path, prefix):
        """Extracts text and saves images from a PDF."""
        doc = fitz.open(pdf_path)
        full_text = ""
        image_data = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            full_text += f"\n--- Page {page_num + 1} ---\n" + page.get_text()

            # Image extraction [cite: 55]
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                img_name = f"{prefix}_p{page_num+1}_i{img_index}.png"
                img_path = os.path.join(self.output_img_dir, img_name)
                
                with open(img_path, "wb") as f:
                    f.write(image_bytes)
                
                image_data.append({"path": img_path, "page": page_num + 1})

        return full_text, image_data

    def run(self):
        print("Extracting Inspection Data...")
        insp_text, insp_imgs = self.extract_data(self.inspection_path, "insp")
        
        print("Extracting Thermal Data...")
        therm_text, therm_imgs = self.extract_data(self.thermal_path, "thermal")

        return {
            "inspection": {"text": insp_text, "images": insp_imgs},
            "thermal": {"text": therm_text, "images": therm_imgs}
        }