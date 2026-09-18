import re

COMPANY_ALIASES = {
    "TCS": ["tcs", "tata consultancy services", "tata consultancy"],
    "Cognizant": ["cognizant", "cts"],
    "Capgemini": ["capgemini", "cap gemini"],
    "Accenture": ["accenture", "accenture india"],
    "Deloitte": ["deloitte", "deloitte india"],
    "Apple": ["apple", "apple india"],
    "Microsoft": ["microsoft", "microsoft india", "msft"],
}

SKILLS = [
    "python", "java", "javascript", "typescript", "c", "c++", "c#",
    "go", "golang", "node.js", "node", "react", "reactjs", "django",
    "flask", "fastapi", "spring", "spring boot", "hibernate", "sql",
    "mysql", "postgresql", "mongodb", "docker", "kubernetes", "aws",
    "azure", "gcp", "git", "github", "rest", "rest api", "html", "css",
    "pandas", "numpy", "machine learning", "tensorflow", "pytorch",
    "power bi", "excel", "llms", "rag", "prompt engineering"
]

ROLE_ALIASES = {
    "software engineer": ["software engineer", "software developer", "sde", "developer"],
    "backend": ["backend", "back end", "backend developer", "backend engineer"],
    "frontend": ["frontend", "front end", "frontend developer", "frontend engineer"],
    "full stack": ["full stack", "fullstack", "full-stack"],
    "data analyst": ["data analyst", "analytics analyst"],
    "data scientist": ["data scientist", "data science"],
    "qa": ["qa", "quality assurance", "test engineer", "software tester"],
    "devops": ["devops", "dev ops", "site reliability", "sre"],
    "intern": ["intern", "internship", "internships"],
}

def parse_query(query):
    q = query.lower()
    found_skills = []
    for skill in SKILLS:
        if len(skill) <= 2:
            if re.search(r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])", q):
                found_skills.append(skill)
        elif skill in q:
            found_skills.append(skill)
    experience = ""
    if any(x in q for x in ["fresher", "freshers", "entry level", "entry-level", "graduate", "graduates", "new grad", "new graduate", "0-1", "0 to 1 year", "0-1 year"]):
        experience = "Fresher"
    location = ""
    known_locations = [
        "hyderabad", "bengaluru", "bangalore", "mumbai", "delhi",
        "pune", "chennai", "nandyal", "noida", "gurugram", "india"
    ]
    for loc in known_locations:
        if loc in q:
            location = loc
            break
    company = ""
    for canonical, aliases in COMPANY_ALIASES.items():
        if any(re.search(r"\b" + re.escape(alias) + r"\b", q) for alias in aliases):
            company = canonical
            break

    role = ""
    for canonical, aliases in ROLE_ALIASES.items():
        if any(re.search(r"\b" + re.escape(alias) + r"\b", q) for alias in aliases):
            role = canonical
            break

    # Natural-language experience variants.
    if not experience and any(x in q for x in ["entry", "early career", "graduate role", "graduate position"]):
        experience = "Fresher"

    return {"skills": found_skills, "experience": experience, "location": location, "company": company, "role": role}
