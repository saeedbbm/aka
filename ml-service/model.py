# ml-service/model.py

def predict(note: str) -> str:
    """
    Predict ICD-10 code based on keywords found in the clinical note.
    """
    lookup = {
        "chest pain": "I20.0",             
        "shortness of breath": "J96.0",     
        "diabetes": "E11",                 
        "hypertension": "I10",             
        "myocardial infarction": "I21",      
        "stroke": "I63",                   
    }
    
    note_lower = note.lower()
    for keyword, code in lookup.items():
        if keyword in note_lower:
            return code
    
    return "UNKNOWN"
