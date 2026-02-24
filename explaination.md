# Project Explanation

This document explains what this project does in simple terms, and details the exact purpose of every file in the codebase.

## Overview
Imagine you need to Google 163 specific details about a company (like their CEO, Revenue, Competitors, ESG Ratings, etc.) and write it all down perfectly into a massive Excel spreadsheet. Doing this for 50 companies manually would take weeks.

This project **automates that entire process**. 
It takes a list of company names, searches the web for context, and asks an AI (a Large Language Model like LLaMA) to extract exactly those 163 data points nicely into a table. It then saves this data and combines it all into one big Excel file.

---

## What each file does

### The Root Folder
- **`main.py`**
  This is the "Boss" script. It handles the main loop. It loads the input data, loops through every company, triggers the AI scraping process, and when all companies are done, it takes the results and writes them to the final Excel file (`final_output.xlsx`).
- **`.env`**
  This stores your secret API keys (passwords for the AI services).
- **`.gitignore`**
  Tells Git (version control) which files to ignore, ensuring your secret `.env` and massive data outputs aren't accidentally uploaded to GitHub.
- **`README.md`**
  A quick-start guide for developers on how to install and run the project.

### The `src/` Folder (The Logic)
This folder contains the actual machinery—the python scripts doing the heavy lifting.

- **`agents.py`**
  The "Project Manager" for the AI. This script takes a company name, asks the AI for the 163 data points, receives the table, and checks it for errors. It also handles saving the result to a dedicated JSON file for that company.
  
- **`prompts.py`**
  The "Instructor". This script generates the exact words sent to the AI. It takes our strict formatting rules and search results from DuckDuckGo and dynamically creates the prompt (e.g., "Here is the context for Blinkit. Now output a table with exactly these 163 fields...").

- **`llm_provider.py`**
  The "Translator". A helper utility that allows the project to seamlessly switch between different AIs (like Groq's LLaMA 3, Google's Gemini, or OpenAI) so you aren't locked into one service.

- **`table_parser.py`**
  The "Data Extraction Tool". AI models sometimes return extra conversational text (e.g., "Sure, here is your table:"). This script is a custom regex parser that ignores the chatty text, perfectly extracts the Markdown Table from the AI's response, and converts it into a structured Python dictionary.

- **`schema.py`**
  The "Blueprint loader". It defines what a parameter should look like (ID, Category, Name) in the code and handles loading the massive 163-row ruleset into memory so the rest of the application can enforce it.

- **`parse_schema.py`**
  A utility script we ran once. It took the messy `prompt_text.txt` instructions and automatically converted the 163 parameters into a perfectly structured JSON array (`schema.json`).

### The `data/` Folder (The Information)
This folder separates the raw information from the code logic.

- **`data/input/companies.json`**
  The starting line. A simple list of the companies you want the code to research.
  
- **`data/input/prompt_text.txt`**
  The massive wall of text containing the original rules and the list of the 163 parameters we needed to extract.
  
- **`data/input/schema.json`**
  The structured, computer-readable version of the 163 parameters.

- **`data/output/`**
  Where the final results live.
  - **`final_output.xlsx`**: The ultimate end-goal. A giant spreadsheet of all companies and their 163 data columns.
  - **`parsed/`**: Contains the individual JSON files for every company after they are successfully processed by the AI.
  - **`logs/`**: Contains `raw_{company}.txt` files showing exactly what the AI spit out before parsing, useful for debugging if something breaks.
