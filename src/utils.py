import pdfplumber
import PyMuPDF
import re
from typing import Dict, List, Tuple

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from PDF file using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text with pdfplumber: {e}")
        try:
            # Fallback to PyMuPDF if pdfplumber fails
            doc = PyMuPDF.open(stream=pdf_file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
        except Exception as e:
            print(f"Error extracting text with PyMuPDF: {e}")
            return ""
    return text

def calculate_ats_score(resume_text: str, job_description: str) -> Tuple[float, Dict]:
    """Calculate ATS score based on resume and job description."""
    # Convert both texts to lowercase for case-insensitive matching
    resume_lower = resume_text.lower()
    job_desc_lower = job_description.lower()
    
    # Extract keywords from job description
    keywords = extract_keywords(job_desc_lower)
    
    # Calculate matches
    matches = {keyword: resume_lower.count(keyword) for keyword in keywords}
    total_matches = sum(matches.values())
    
    # Calculate score (0-100)
    max_possible_matches = len(keywords) * 3  # Assume each keyword should appear up to 3 times
    score = min(100, (total_matches / max_possible_matches) * 100) if max_possible_matches > 0 else 0
    
    return score, {
        "matches": matches,
        "total_matches": total_matches,
        "keywords": keywords
    }

def extract_keywords(text: str) -> List[str]:
    """Extract important keywords from text."""
    # Remove common words and punctuation
    words = re.findall(r'\b\w+\b', text.lower())
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    keywords = [word for word in words if word not in common_words and len(word) > 2]
    
    # Count word frequencies
    word_freq = {}
    for word in keywords:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Return top keywords (words that appear more than once)
    return [word for word, freq in word_freq.items() if freq > 1]

def get_keyword_gaps(resume_text: str, job_description: str) -> Dict:
    """Analyze resume against job description to find missing keywords."""
    # Extract keywords from job description
    job_keywords = extract_keywords(job_description.lower())
    resume_keywords = extract_keywords(resume_text.lower())
    
    # Find missing keywords
    missing_keywords = [kw for kw in job_keywords if kw not in resume_keywords]
    
    # Categorize keywords (simple categorization for now)
    must_have = missing_keywords[:len(missing_keywords)//2]
    nice_to_have = missing_keywords[len(missing_keywords)//2:]
    
    return {
        "must_have": must_have,
        "nice_to_have": nice_to_have,
        "total_missing": len(missing_keywords)
    } 