# Process Automation

This project is a multi-agent system designed to automate the collection, validation, and aggregation of 163 specific corporate data points for various companies, outputting the results directly into a structured Excel file.

## Getting Started

### 1. Requirements

- Python 3.9+
- The API keys for the LLM providers (e.g., Groq, Gemini)

### 2. Setup

1. **Install Dependencies:**
   Install the required Python packages (we highly recommend doing this inside a virtual environment).
   ```bash
   pip install langchain langgraph langchain-groq pandas openpyxl python-dotenv duckduckgo-search
   ```

2. **Environment Variables:**
   A `.env` file should be present in the root of the directory containing your API keys:
   ```env
   GROQ_API_KEY=your_key_here
   ```

3. **Input Data:**
   Add the list of companies you wish to process in `data/input/companies.json`.

### 3. Execution

You can run the full pipeline with a single command:
```bash
python main.py
```

Check the `data/output/` directory for the `final_output.xlsx` containing your collected data! For an in-depth code explanation, please read `explaination.md`.
