import requests

def get_ashby_jobs(job_board_name, timeout=4):
    url = f"https://api.ashbyhq.com/posting-api/job-board/{job_board_name}"
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    jobs = []
    for job in data.get("jobs", []):
        if not job.get("isListed", True):
            continue
        jobs.append({
            "company": job_board_name,
            "title": job.get("title", ""),
            "location": job.get("location", ""),
            "experience": "",
            "skills": "",
            "description": job.get("descriptionPlain", ""),
            "source_url": job.get("jobUrl", ""),
            "apply_url": job.get("applyUrl", "")
        })
    return jobs
