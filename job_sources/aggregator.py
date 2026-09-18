import streamlit as st
from job_sources.companies import JOB_SOURCES
from job_sources.company_profiles import COMPANY_PROFILES
from job_sources.fetcher import fetch_all_sources
from nlp_processor import parse_query

LAST_HEALTH = []

FAST_SOURCE_NAMES = {"Stripe", "GitLab", "Datadog", "Cloudflare", "OpenAI", "Spotify"}
FAST_SOURCES = []
for source in JOB_SOURCES:
    if source["company"] in FAST_SOURCE_NAMES:
        item = dict(source)
        item["timeout"] = 3
        item["include_content"] = False if item["provider"] == "greenhouse" else True
        FAST_SOURCES.append(item)

@st.cache_data(ttl=900, show_spinner=False)
def _fetch_cached_sources(source_key):
    sources = [dict(item) for item in source_key]
    return fetch_all_sources(sources, max_workers=len(sources))

def _source_key(sources):
    return tuple(tuple(sorted(s.items())) for s in sources)

def _sources_for_query(query):
    parsed = parse_query(query)
    if parsed.get("company"):
        # Company-specific searches are isolated to that company. This prevents
        # a TCS/Apple/etc. query from returning unrelated companies.
        return [s for s in JOB_SOURCES if s["company"].lower() == parsed["company"].lower()]
    return FAST_SOURCES

def get_all_jobs(force_refresh=False, sources=None):
    global LAST_HEALTH
    selected = sources or FAST_SOURCES
    if not selected:
        return []
    key = _source_key(selected)
    if force_refresh:
        _fetch_cached_sources.clear()
    jobs, health = _fetch_cached_sources(key)
    LAST_HEALTH = health
    return jobs

def _score(job, filters, raw_query):
    title = job.get("title", "")
    location = job.get("location", "")
    company = job.get("company", "")
    text = " ".join([company, title, location, job.get("description", ""), job.get("skills", "")]).lower()
    points = 0
    for skill in filters["skills"]:
        if skill.lower() in text:
            points += 4
    requested_location = (filters.get("location") or "").lower()
    q = raw_query.lower()
    if filters.get("company") and company.lower() == filters["company"].lower():
        points += 100
    if filters.get("role") and filters["role"].lower() in text:
        points += 12
    if requested_location and requested_location in text:
        points += 12
    if "hyderabad" in q or "india" in q:
        if any(x in location.lower() for x in ["hyderabad", "india", "remote"]):
            points += 8
    if filters.get("experience") and any(x in text for x in ["fresher", "entry level", "graduate", "junior", "0-1 year", "new grad"]):
        points += 5
    return points

def company_status(query, jobs):
    parsed = parse_query(query)
    company = parsed.get("company")
    if not company:
        return None
    profile = COMPANY_PROFILES.get(company)
    if not profile:
        return None

    company_jobs = [j for j in jobs if j.get("company", "").lower() == company.lower()]
    fresher_requested = parsed.get("experience") == "Fresher"

    if company_jobs:
        if fresher_requested:
            fresher_jobs = [j for j in company_jobs if any(x in (j.get("title", "") + " " + j.get("description", "")).lower() for x in [
                "fresher", "graduate", "entry level", "new grad", "junior", "0-1", "intern", "trainee", "early career"
            ])]
            if fresher_jobs:
                return {"status": "available", "message": f"{company} fresher/entry-level opportunities found.", "profile": profile}
            # If an official source returned live jobs but none are clearly fresher,
            # report that honestly instead of claiming the company is not hiring.
            return {"status": "not_found", "message": f"No fresher/entry-level matches were found in the live {company} results right now. Other current {company} jobs are shown below.", "profile": profile}
        return {"status": "available", "message": f"Live {company} opportunities found.", "profile": profile}

    company_sources = [s for s in JOB_SOURCES if s["company"].lower() == company.lower()]
    official = any(s["provider"] == "official" for s in company_sources)
    health = [h for h in LAST_HEALTH if h.get("company", "").lower() == company.lower()]
    if official and health and all(h.get("status") == "error" for h in health):
        return {"status": "unavailable", "message": f"The {company} official careers source could not be reached right now. This is not the same as the company not hiring.", "profile": profile}
    if official:
        return {"status": "not_found", "message": f"No matching {company} opportunities were extracted from the official live page right now. Open the official portal to verify the latest openings.", "profile": profile}
    return {"status": "unavailable", "message": f"Live {company} job data is currently unavailable.", "profile": profile}

def search_jobs(query, limit=100, force_refresh=False, search_all=False):
    filters = parse_query(query)
    selected_sources = JOB_SOURCES if search_all else _sources_for_query(query)
    jobs = get_all_jobs(force_refresh=force_refresh, sources=selected_sources)
    ranked = sorted(jobs, key=lambda j: _score(j, filters, query), reverse=True)
    scored = [(j, _score(j, filters, query)) for j in ranked]
    matches = [j for j, score in scored if score > 0]
    return (matches or ranked)[:limit]

def get_source_health():
    return LAST_HEALTH
