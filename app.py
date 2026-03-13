#UI LOGICS ARE WRITTEN BY AI 

import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Ensure the 'src' directory is in the path for modular imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.extractor import DataExtractor
from src.processor import DDRProcessor
from src.generator import DDRGenerator

# Initialize environment variables
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="AI-Generalist DDR System",
    page_icon="🏗️",
    layout="wide"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { 
        width: 100%; 
        border-radius: 5px; 
        height: 3em; 
        background-color: #ff4b4b; 
        color: white; 
        font-weight: bold;
    }
    .stStatus { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🏗️ Automated Diagnostic Reporting System")
    st.info("Upload technical PDFs to generate a logically merged, client-friendly Detailed Diagnostic Report (DDR).")

    # --- Sidebar: Model & API Configuration ---
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # UI Selection List
        model_choice = st.selectbox(
            "AI Reasoning Engine",
            [
                "Mistral", 
                "Claude", 
                "Gemini", 
                "OpenAI", 
                "Groq", 
                "DeepSeek", 
                "OpenRouter", # Standalone Free Option
                "Cerebras"
            ],
            help="Select the AI provider. Each has different strengths in speed and reasoning."
        )

        st.divider()
        
        # Mapping UI names to Environment Variables
        # This MUST match the model_choice list above exactly
        key_env_map = {
            "Mistral": "MISTRAL_API_KEY",
            "Claude": "ANTHROPIC_API_KEY",
            "Gemini": "GEMINI_API_KEY",
            "OpenAI": "OPENAI_API_KEY",
            "Groq": "GROQ_API_KEY",
            "DeepSeek": "DEEPSEEK_API_KEY",
            "OpenRouter": "OPENROUTER_API_KEY", # New separate key
            "Cerebras": "CEREBRAS_API_KEY"
        }

        # Dynamic API Key Input
        env_var_name = key_env_map[model_choice]
        user_key = st.text_input(
            f"{model_choice} API Key", 
            type="password", 
            value=os.getenv(env_var_name, ""),
            help=f"Enter your {model_choice} API key. If already in .env, it will be pre-filled."
        )
        
        if user_key:
            os.environ[env_var_name] = user_key

        st.divider()
        st.caption("🚀 Fault-Tolerant AI Architecture v2.0")
        st.caption("Developed for AI-Generalist Assessment")

    # --- Main UI: File Uploads ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Site Inspection")
        inspection_file = st.file_uploader("Upload Inspection Report (PDF)", type=['pdf'], key="insp_upload")
        
    with col2:
        st.subheader("🔥 Thermal Data")
        thermal_file = st.file_uploader("Upload Thermal Images Document (PDF)", type=['pdf'], key="therm_upload")

    # --- Processing Logic ---
    if st.button("🚀 Generate Detailed Diagnostic Report"):
        if not inspection_file or not thermal_file:
            st.error("Please upload both the Inspection and Thermal PDFs to proceed.")
            return
        
        if not os.environ.get(env_var_name):
            st.error(f"Missing API Key for {model_choice}. Please provide it in the sidebar.")
            return

        try:
            # Step 1: Temporary File Storage
            with open("temp_insp.pdf", "wb") as f:
                f.write(inspection_file.getbuffer())
            with open("temp_therm.pdf", "wb") as f:
                f.write(thermal_file.getbuffer())

            # Step 2: Extraction and AI Reasoning
            status = st.status(f"⚡ Pipeline: {model_choice} is processing...", expanded=True)
            
            with status:
                st.write("📥 **[1/3] Multimodal Extraction**")
                extractor = DataExtractor("temp_insp.pdf", "temp_therm.pdf")
                data = extractor.run()
                st.toast("Extraction Complete!")

                st.write(f"🧠 **[2/3] Reasoning with {model_choice}**")
                processor = DDRProcessor()
                report_content = processor.analyze_data(
                    data['inspection']['text'], 
                    data['thermal']['text'],
                    model_choice=model_choice
                )
                
                if "❌" in report_content:
                    st.error(report_content)
                    return
                
                st.toast("AI Merging Complete!")

                st.write("📄 **[3/3] Generating Professional Document**")
                output_path = "output/Final_DDR_Report.docx"
                generator = DDRGenerator(output_path)
                all_images = data['inspection']['images'] + data['thermal']['images']
                generator.create_report(report_content, image_mappings=all_images)
                
            status.update(label=f"✅ DDR Generated successfully via {model_choice}!", state="complete")

            # --- Results Display ---
            st.success("Your report is ready for download.")
            
            tab1, tab2 = st.tabs(["📄 Report Preview", "💾 Download & Export"])
            
            with tab1:
                st.markdown("### Preview of Findings")
                st.markdown(report_content)
                
            with tab2:
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Professional DDR (.docx)",
                        data=file,
                        file_name="Detailed_Diagnostic_Report.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                st.balloons()

        except Exception as e:
            st.error(f"System Error: {str(e)}")

    st.divider()
    st.caption("Note: This system follows strict logic to mark missing data as 'Not Available'.")

if __name__ == "__main__":
    if not os.path.exists("output"):
        os.makedirs("output", exist_ok=True)
    main()