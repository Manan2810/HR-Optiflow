import re
import sys
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import PyPDF2
import docx

# Download stopwords if you haven't already
# nltk.download('stopwords')
resume_keywords = [
    "experience",
    "skills",
    "education",
    "summary",
    "objective",
    "accomplishments",
    "certifications",
    "qualifications",
    "references",
    "achievements",
    "awards",
    "projects",
    "responsibilities",
    "job",
    "position",
    "company",
    "industry",
    "contact",
    "address",
    "phone",
    "email",
    "linkedin",
    "github",
    "portfolio",
    # Add more keywords as needed
]

# You can also include industry-specific terms based on your analysis needs.
industry_keywords = [
    "programming",
    "marketing",
    "finance",
    "engineering",
    "sales",
    "healthcare",
    # Add relevant industry-specific terms
]

# Combine the resume and industry keywords
all_keywords = resume_keywords + industry_keywords




# Define your dataset of words to compare


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def extract_words_from_text1(text):
    # Tokenize the text into words
    words = word_tokenize(text.lower())
    # Remove common English stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    # Use regular expression to remove punctuation
    words = [word for word in words if re.match(r'^\w+$', word)]
    return words

def calculate_percentage_of_matches(extracted_words, dataset):
    match_count = sum(1 for word in extracted_words if word in dataset)
    percentage = (match_count / len(all_keywords)) * 100
    return percentage

# def main():
#     pdf_path = '/Users/mananmehra/Desktop/HR Optiflow/uploads/Internship Letter - Manan Mehra-Klassify.pdf'
#     extracted_text = extract_text_from_pdf(pdf_path)

#     # Extract words using NLTK, remove stopwords and punctuation
#     extracted_words = extract_words_from_text(extracted_text)
#     print(extracted_words)
#     # Calculate the percentage of matches
#     percentage = calculate_percentage_of_matches(extracted_words, all_keywords)

#     print(f"Percentage of words matching the dataset: {percentage:.2f}%")
    
#     if percentage > 25:
#         print("Resume selected!")
#     else:
#         print("Resume not selected.")

# if __name__ == "__main__":
#     main()