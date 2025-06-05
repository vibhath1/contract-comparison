#date_comparison.py

import spacy
from dateutil.parser import parse

# Load the spaCy English model outside the function for performance
nlp = spacy.load("en_core_web_sm")

def extract_dates(text):
    doc = nlp(text)
    dates = []
    for ent in doc.ents:
        if ent.label_ == "DATE":
            try:
                parsed_date = parse(ent.text, fuzzy=True, default=None, dayfirst=False, yearfirst=False)
                if parsed_date:
                    dates.append(parsed_date.date())
            except Exception as e:
                print(f"Error parsing date '{ent.text}': {e}")
    return dates

def compare_dates(dates_doc1, dates_doc2):
    results = {
        "added_dates": [],
        "removed_dates": [],
        "common_dates": [],
        "formatted_common_dates": []
    }
    
    set_doc1 = set(dates_doc1)
    set_doc2 = set(dates_doc2)
    
    results['added_dates'] = sorted(list(set_doc2 - set_doc1))
    results['removed_dates'] = sorted(list(set_doc1 - set_doc2))
    results['common_dates'] = list(set_doc1 & set_doc2)
    results['formatted_common_dates'] = [date.strftime("%Y-%m-%d") for date in results['common_dates']]
    
    return results

def compare_date_references(text1, text2):
    dates_doc1 = extract_dates(text1)
    dates_doc2 = extract_dates(text2)
    return compare_dates(dates_doc1, dates_doc2)