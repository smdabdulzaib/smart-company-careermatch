"""Company-aware interview question generation with lightweight local RAG.

The retriever ranks company/role question-bank documents using token overlap, then
combines them with technical, resume, and job-specific questions. No API key is
required; an optional LLM layer can be added later.
"""
import re

BASE = {
    "Python": ["What are Python's key features?", "Explain mutable vs immutable objects.", "How do you handle exceptions in Python?", "What are decorators and generators?", "How would you optimize slow Python code?"],
    "SQL": ["Explain INNER JOIN vs LEFT JOIN.", "What is normalization?", "WHERE vs HAVING?", "What are indexes?", "Explain window functions.", "What are ACID properties?"],
    "DSA": ["What is Big-O notation?", "Explain arrays and linked lists.", "When would you use a stack or queue?", "What is binary search?", "Explain BFS vs DFS.", "What is dynamic programming?"],
    "OOP": ["What are the four pillars of OOP?", "Explain encapsulation, inheritance, polymorphism, and abstraction.", "Composition vs inheritance?", "Class vs object?"],
    "REST API": ["What is a REST API?", "Explain GET, POST, PUT, PATCH and DELETE.", "What is idempotency?", "Authentication vs authorization?", "How would you secure a REST API?"],
    "HR": ["Tell me about yourself.", "Why do you want this role?", "Why should we hire you?", "Describe a challenging project.", "How do you work in a team?", "How do you handle deadlines?"]
}

COMPANY_BANK = {
    "TCS": [
        "Explain how you would approach a client requirement that is unclear.",
        "How would you ensure quality while delivering software for a large enterprise client?",
        "Describe a time you learned a new technology quickly.",
        "How would you troubleshoot a production issue reported by a client?",
        "What do you understand about IT services, consulting, and digital transformation?",
        "How would you communicate a technical issue to a non-technical client?",
        "What steps would you follow in an enterprise SDLC project?",
        "How would you handle being assigned to a technology different from your preference?",
    ],
    "Cognizant": [
        "How would you automate a repetitive business process using Python?",
        "How do you approach application maintenance and incident resolution?",
        "Explain how you would work with business analysts and client stakeholders.",
        "How would you test an application before a client release?",
        "How do cloud and data technologies support digital business transformation?",
        "Describe a project where you improved efficiency or reduced manual work.",
        "How would you investigate a defect that cannot be reproduced locally?",
        "How do you manage learning requirements across multiple client projects?",
    ],
    "Capgemini": [
        "How would you design a maintainable solution for an enterprise customer?",
        "Explain your approach to Agile ceremonies and sprint commitments.",
        "How would you handle conflicting requirements from two stakeholders?",
        "What testing levels would you use before deploying a client application?",
        "How would you migrate a legacy application component safely?",
        "Describe how you would collaborate in a distributed delivery team.",
        "How would you monitor and troubleshoot an application after deployment?",
        "What does responsible use of automation and AI mean in enterprise projects?",
    ],
    "Accenture": [
        "How would you translate a business problem into a technical solution?",
        "How would you explain the value of a technology solution to a client?",
        "Describe how you would work in a consulting project with changing requirements.",
        "How would you use data or automation to improve a business process?",
        "How would you handle multiple priorities across client deliverables?",
        "What is your approach to continuous learning in a consulting environment?",
        "How would you validate that a solution creates measurable business value?",
        "How would you manage risks before a client-facing release?",
    ],
    "Deloitte": [
        "How would you design a secure application for a business client?",
        "How would you explain a technical recommendation to an executive stakeholder?",
        "What controls would you consider when handling sensitive business data?",
        "How would you validate data quality in an analytics or reporting project?",
        "How would you approach requirements, documentation, testing, and auditability?",
        "Describe a time you identified a process improvement opportunity.",
        "How would you manage scope changes in a consulting engagement?",
        "How do technology, risk, and compliance interact in enterprise systems?",
    ],
    "Apple": [
        "How would you debug a performance issue in a user-facing application?",
        "How would you design a reliable feature with a strong user experience?",
        "How do you think about memory, concurrency, and resource management?",
        "How would you test software across different devices or operating conditions?",
        "Describe a project where attention to detail materially improved the result.",
        "How would you investigate a crash that occurs only for some users?",
        "How would you balance simplicity, performance, privacy, and maintainability?",
        "How would you collaborate with designers, hardware teams, and software engineers?",
    ],
    "Microsoft": [
        "Explain how you would design a scalable service for millions of users.",
        "How would you diagnose latency in a distributed application?",
        "What trade-offs would you consider when designing an API?",
        "How would you test code for correctness, reliability, and maintainability?",
        "Explain a data structure or algorithm you used to solve a difficult problem.",
        "How would you handle failure in a cloud-based service?",
        "How would you improve the accessibility and usability of a software feature?",
        "Describe how you receive and apply code-review feedback.",
    ],
}

ALIASES = {"Tata Consultancy Services": "TCS"}

def _tokens(text):
    return set(re.findall(r"[a-z0-9+#.]+", (text or "").lower()))

def _company(job):
    name = job.get("company", "")
    for key in COMPANY_BANK:
        if key.lower() in name.lower() or name.lower() in key.lower():
            return key
    return ALIASES.get(name, "")

def _job_text(job):
    return " ".join([job.get("title", ""), job.get("description", ""), job.get("skills", "")])

def retrieve_company_questions(job, k=8):
    """Lightweight local RAG: retrieve the most relevant company documents/questions."""
    company = _company(job)
    if not company:
        return []
    query = _tokens(_job_text(job))
    questions = COMPANY_BANK[company]
    scored = []
    for q in questions:
        overlap = len(query & _tokens(q))
        scored.append((overlap, q))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [q for _, q in scored[:k]]

def generate_100_questions(job, resume_skills=None):
    text = _job_text(job)
    selected = []
    company = _company(job)
    if company:
        selected.extend([(f"{company} — Retrieved", q) for q in retrieve_company_questions(job)])
    for category, questions in BASE.items():
        if category.lower() in text.lower() or category in ["HR"]:
            selected.extend([(category, q) for q in questions])
    for skill in (resume_skills or []):
        selected.extend([("Resume", f"How have you used {skill} in your projects or training?"), ("Resume", f"What practical problem can you solve using {skill}?")])
    title = job.get("title", "this role")
    if company:
        selected.extend([(f"{company} — Role", f"For a {title} position at {company}, how would you demonstrate strong problem-solving and ownership?")])
    selected.extend([("Job-specific", f"For the {title} role, how would you approach a new task: clarify requirements, design, implement, test, and explain trade-offs?")])
    out, seen = [], set()
    for category, q in selected:
        if q not in seen:
            seen.add(q); out.append(f"[{category}] {q}")
    i = 1
    while len(out) < 100:
        q = f"[Job-specific] For the {title} role, interview problem {i}: explain your assumptions, solution, testing strategy, and trade-offs."
        if q not in seen:
            seen.add(q); out.append(q)
        i += 1
    return out[:100]
