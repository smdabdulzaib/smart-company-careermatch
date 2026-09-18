import html
from html.parser import HTMLParser
import requests

class _TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, data):
        if data.strip():
            self.parts.append(data.strip())

def html_to_text(value):
    if not value:
        return ""
    # Greenhouse descriptions may contain HTML entities; decode twice defensively.
    value = html.unescape(html.unescape(value))
    parser = _TextParser()
    parser.feed(value)
    return " ".join(parser.parts)

def get_greenhouse_jobs(board_token, company_name=None, timeout=4, include_content=True):
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"
    response = requests.get(url, params={"content": "true" if include_content else "false"}, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    jobs = []
    for job in data.get("jobs", []):
        location = (job.get("location") or {}).get("name", "")
        description = html_to_text(job.get("content", ""))
        jobs.append({
            "company": job.get("company_name") or company_name or board_token,
            "title": job.get("title", ""),
            "location": location,
            "experience": "",
            "skills": "",
            "description": description,
            "source_url": job.get("absolute_url", ""),
            "apply_url": job.get("absolute_url", ""),
            "provider": "greenhouse",
            "source_id": str(job.get("id", "")),
            "updated_at": job.get("updated_at", ""),
        })
    return jobs
