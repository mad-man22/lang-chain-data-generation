from dataclasses import dataclass
from typing import Optional

@dataclass
class ParameterSpec:
    sr_no: int
    category: Optional[str]
    description: Optional[str]
    column_name: str
    parameter: Optional[str]
    content_type: Optional[str]
    min_elements: Optional[str]
    max_elements: Optional[str]
    ac: Optional[str]

def load_specs(schema_file="data/input/schema.json") -> list[ParameterSpec]:
    import json
    with open(schema_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    specs = []
    for row in data:
        # Assuming our json holds ID, Category, Description, Parameter, Type, MinMax, A/C
        specs.append(ParameterSpec(
            sr_no=int(row.get("ID", 0)),
            category=row.get("Category", ""),
            description=row.get("Description", ""),
            column_name=row.get("Parameter", ""), # The column name in output
            parameter=row.get("Parameter", ""), # Also parameter for logic
            content_type=row.get("Type", ""),
            min_elements=row.get("MinMax", "").split("|")[0].strip() if "|" in row.get("MinMax", "") else None,
            max_elements=row.get("MinMax", "").split("|")[1].strip() if "|" in row.get("MinMax", "") else None,
            ac=row.get("A/C", "")
        ))
    return specs
