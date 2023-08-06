# NLPIE: A Lightweight Entity Linker

A lightweight entity linking tool using distilled clinical language models from Huggingface and spaCy/ScispaCy intended to connect clinical notes to UMLS codes. Additional mapping is available for ICD-10 and SNOMED CT entries. 

## Repository Structure

```
.
├── README.md
├── entity_linker.py
├── entity_linker_hf.py
├── mappings-from-UMLS
│ ├── cui_to_icd10_EXACT.json
│ ├── cui_to_icd10_RO.json
│ ├── cui_to_snomed_EXACT.json
│ └── cui_to_snomed_RO.json
├── preprocessor.py
├── query_filter.py
└── requirements.txt
```

## Installation

Install the required packages by running:

 
```bash
pip install -r requirements.txt
```

## Usage
### Preprocessor

Use the `InputPreprocessor` class in `preprocessor.py` to preprocess an input CSV file:


```python
from preprocessor import InputPreprocessor

input_path = 'input.csv'
output_path = 'preprocessed.csv'

preprocessor = InputPreprocessor(input_path)
preprocessed_data = preprocessor.preprocess_input_file(output_path)
```

## Query Filter

Use the `QueryFilter` class in `query_filter.py` to filter a preprocessed CSV file based on a text query:

```python
from query_filter import QueryFilter

query = "pneumonia"
input_csv_path = "preprocessed.csv"

query_filter = QueryFilter()
query_umls_codes = query_filter.process_query(query)
filtered_data, negated_rows = query_filter.filter_rows(query_umls_codes, input_csv_path)
query_filter.save_filtered_data_to_csv(filtered_data, negated_rows, query, input_csv_path)
```

