from concurrent.futures import ThreadPoolExecutor, as_completed
from job_sources.ashby import get_ashby_jobs
from job_sources.greenhouse import get_greenhouse_jobs
from job_sources.lever import get_lever_jobs
from job_sources.official import get_official_jobs

FETCHERS = {
    "greenhouse": lambda s: get_greenhouse_jobs(s["slug"], s["company"], timeout=s.get("timeout", 4), include_content=s.get("include_content", True)),
    "ashby": lambda s: get_ashby_jobs(s["slug"], timeout=s.get("timeout", 4)),
    "lever": lambda s: get_lever_jobs(s["slug"], timeout=s.get("timeout", 4)),
    "official": lambda s: get_official_jobs(s),
}

def fetch_source(source):
    provider = source["provider"].lower()
    if provider not in FETCHERS:
        raise ValueError(f"Unsupported ATS provider: {provider}")
    return FETCHERS[provider](source)

def fetch_all_sources(sources, max_workers=8):
    jobs, health = [], []
    with ThreadPoolExecutor(max_workers=min(max_workers, max(1, len(sources)))) as pool:
        futures = {pool.submit(fetch_source, s): s for s in sources}
        for future in as_completed(futures):
            source = futures[future]
            try:
                result = future.result()
                jobs.extend(result)
                health.append({"provider": source["provider"], "company": source["company"], "slug": source["slug"], "status": "ok", "jobs": len(result)})
            except Exception as exc:
                health.append({"provider": source["provider"], "company": source["company"], "slug": source["slug"], "status": "error", "jobs": 0, "error": str(exc)})
    return jobs, health
