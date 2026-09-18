import requests

def get_lever_jobs(company_slug, timeout=4):
    url = f"https://api.lever.co/v0/postings/{company_slug}?mode=json"
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    jobs = []
    for job in data:
        categories = job.get("categories", {})
        jobs.append({
            "company": company_slug,
            "title": job.get("text", ""),
            "location": categories.get("location", ""),
            "experience": "",
            "skills": "",
            "description": job.get("descriptionPlain", ""),
            "source_url": job.get("hostedUrl", ""),
            "apply_url": job.get("applyUrl", "")
        })
    return jobs
