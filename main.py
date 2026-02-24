import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from src.agents import collect_company_data, write_individual_file, build_failed_provider_payload
from src.schema import load_specs

def main():
    specs = load_specs("data/input/schema.json")
    
    with open("data/input/companies.json", "r", encoding="utf-8") as f:
        companies = json.load(f)
        
    all_results = []
    for comp in companies:
        c_name = comp["company_name"]
        print(f"\\nProcessing {c_name}...")
        
        try:
            # We use Groq as the standard based on previous limits, but fallback correctly
            payload = collect_company_data(
                company_name=c_name, 
                specs=specs, 
                provider="groq", 
                model="llama-3.3-70b-versatile"
            )
            print(f"Collected {payload['row_count']} rows for {c_name}.")
        except Exception as e:
            print(f"Failed to collect for {c_name}: {e}")
            payload = build_failed_provider_payload(c_name, specs, "groq", str(e))
            
        write_individual_file("data/output/parsed", c_name, payload)
        
        # Transform payload into a flat structure for the Excel output
        # E.g. {"Company Name": "Blinkit", "Short Name": "...", ...}
        flat_dict = {"Company Name": c_name}
        for row in payload["rows"]:
            param = row.get("Parameter")
            val = row.get("Research Output / Data", "Not Found")
            if param:
                flat_dict[param] = val
        all_results.append(flat_dict)
        
    df = pd.DataFrame(all_results)
    
    # Order columns based on the original 163 params schema
    cols = [s.parameter for s in specs]
    
    present_cols = [c for c in cols if c in df.columns]
    extra_cols = [c for c in df.columns if c not in cols and c != "Company Name"]
    
    # Ensure Company Name is first if not already
    final_cols = ["Company Name"] + [c for c in present_cols if c != "Company Name"] + extra_cols
    df = df[final_cols]
    
    out_file = "data/output/final_output.xlsx"
    df.to_excel(out_file, index=False)
    print(f"\\nSuccessfully exported {len(all_results)} companies to {out_file}")

if __name__ == "__main__":
    main()
