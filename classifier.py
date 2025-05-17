def infer_subject(text: str) -> str:
    keywords = {
        "Physics": ["force", "acceleration", "newton", "velocity", "motion", "gravity"],
        "Biology": ["photosynthesis", "cell", "organism", "dna", "evolution", "plant"],
        "Math": ["algebra", "calculus", "equation", "integral", "derivative", "matrix"],
        "Chemistry": ["atom", "molecule", "reaction", "acid", "base", "compound"],
        "History": ["war", "revolution", "empire", "king", "battle", "treaty"]
    }
    text = text.lower()
    for subject, terms in keywords.items():
        if any(term in text for term in terms):
            return subject
    return "General"
