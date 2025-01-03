import re

POSSIBLE_DISEASES = [
    "Psoriasis",
    "Varicose Veins",
    "peptic ulcer disease",
    "drug reaction",
    "gastroesophageal reflux disease",
    "allergy",
    "urinary tract infection",
    "Malaria",
    "Jaundice",
    "Cervical spondylosis",
    "Migraine",
    "Hypertension",
    "Bronchial Asthma",
    "Acne",
    "Arthritis",
    "Dimorphic Hemorrhoids",
    "Pneumonia",
    "Common Cold",
    "Fungal infection",
    "Dengue",
    "Impetigo",
    "Chicken pox",
    "Typhoid",
    "diabetes",
]


class InvalidDiagnosisException(Exception):
    def __init__(self, message, diagnosis=None):
        self.message = message
        self.diagnosis = diagnosis
        if diagnosis:
            self.message += f"\nDiagnosis: {self.diagnosis}"
        super().__init__(self.message)


# sometimes models will enclose the JSON in markdown! (e.g. ```json)
# this function removes those delimiters should they be there
def json_completion(completion):
    completion = re.sub(r"^```json\n", "", completion.strip())
    completion = re.sub(r"\n```$", "", completion)
    return completion
