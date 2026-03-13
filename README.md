# AI-Powered DDR Generation System (Mistral AI)

## 📌 Project Objective
[cite_start]This system automates the conversion of raw site inspection and thermal data into a structured, client-ready **Detailed Diagnostic Report (DDR)**[cite: 25, 34]. 

## 🛠️ Tech Stack
- [cite_start]**LLM:** Mistral AI (Reasoning, Deduplication, and Synthesis) [cite: 27, 37]
- **Orchestration:** LangChain
- [cite_start]**Extraction:** PyMuPDF / Unstructured (Text & Image extraction) [cite: 51, 55]
- **Language:** Python 3.10+

## 🚀 Key Features
- [cite_start]**Multimodal Data Merging:** Combines general site observations with thermal imaging data.
- [cite_start]**Conflict & Gap Handling:** Explicitly identifies missing information as "Not Available" and flags data conflicts[cite: 61, 62].
- [cite_start]**Severity Assessment:** Uses AI reasoning to assign severity levels with clear logic[cite: 46].
- [cite_start]**Image Integration:** Automatically places relevant inspection images into corresponding report sections[cite: 52, 56].

## ⚙️ Setup & Installation
1. Clone the repository: `git clone https://github.com/Ansh7473/Ai-Generalist`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure Environment: Create a `.env` file based on `.env.example` and add your `MISTRAL_API_KEY`.
4. Run the generator: `python src/main.py` 

