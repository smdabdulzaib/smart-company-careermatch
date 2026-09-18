import re

def _job_skills(job):
    text = " ".join([
        job.get("title", ""), job.get("description", ""), job.get("skills", "")
    ]).lower()
    candidates = [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "Golang",
        "Node.js", "React", "Django", "Flask", "FastAPI", "Spring Boot",
        "Hibernate", "SQL", "MySQL", "PostgreSQL", "MongoDB", "Docker",
        "Kubernetes", "AWS", "Azure", "Git", "REST API", "HTML", "CSS",
        "Pandas", "NumPy", "Machine Learning", "TensorFlow", "PyTorch",
        "Power BI", "Excel", "LLMs", "RAG", "Prompt Engineering"
    ]
    return [s for s in candidates if re.search(r"(?<!\w)" + re.escape(s.lower()) + r"(?!\w)", text)]

def match_resume_to_job(resume_skills, job):
    required = _job_skills(job)
    resume = {s.lower() for s in resume_skills}
    required_set = {s.lower() for s in required}
    matching = [s for s in required if s.lower() in resume]
    missing = [s for s in required if s.lower() not in resume]
    score = round(len(matching) / len(required) * 100) if required else 0
    return {"score": score, "matching": matching, "missing": missing, "required": required}
