PROJECT_DIR="Ai_Generalist"

# Create the main project structure
mkdir -p {data/raw,data/processed,src,output,docs/screenshots}

# Create placeholder files for the core logic
touch src/main.py             # Main entry point for the AI workflow
touch src/extractor.py        # Logic for PDF/Image extraction [cite: 51, 55]
touch src/processor.py        # Logic for reasoning and merging data [cite: 37, 69]
touch src/generator.py        # Logic for DDR report formatting [cite: 41, 53]
touch app.py
# Create documentation and submission files
touch README.md               # Setup instructions and project overview
touch requirements.txt        # Python dependencies
touch .gitignore              # Ensure API keys/temp files aren't tracked
touch submission_links.txt
