import streamlit as st
from job_sources.aggregator import search_jobs, get_source_health, company_status
from nlp_processor import parse_query
from resume_parser import extract_resume_text, extract_skills
from skill_matcher import match_resume_to_job
from preparation import build_preparation_plan
from interview import generate_100_questions

st.set_page_config(page_title="Smart Company CareerMatch", page_icon="💼", layout="wide")
st.title("💼 Smart Company CareerMatch")
st.caption("Smart Company Job Search & Career Preparation Assistant")

st.info("⚡ Fast Search is the default: it checks only relevant/focused public ATS sources. 🌐 Search all is optional and may take longer.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔎 Job Search", "📄 Resume Analysis", "🎯 Job Matching",
    "📚 Personalized Preparation", "🎤 Interview"
])

if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []

with tab1:
    st.subheader("Natural-language company/job search")
    query = st.text_input("Search", placeholder="Python fresher jobs in Hyderabad")
    c_search, c_all, c_refresh = st.columns(3)
    if c_search.button("⚡ Fast Search", type="primary"):
        if not query.strip():
            st.warning("Enter a job search first.")
        else:
            with st.spinner("Understanding your search and checking the relevant company/source..."):
                parsed = parse_query(query)
                st.session_state.parsed_query = parsed
                st.session_state.jobs = search_jobs(query)
                st.session_state.company_status = company_status(query, st.session_state.jobs)
    if c_all.button("🌐 Search All Live Sources"):
        if not query.strip():
            st.warning("Enter a job search first.")
        else:
            with st.spinner("Searching all configured public sources. This can take longer..."):
                st.session_state.parsed_query = parse_query(query)
                st.session_state.jobs = search_jobs(query, search_all=True, force_refresh=True)
                st.session_state.company_status = company_status(query, st.session_state.jobs)
    if c_refresh.button("🔄 Refresh Fast Results"):
        if not query.strip():
            st.warning("Enter a job search first.")
        else:
            with st.spinner("Refreshing the relevant source..."):
                st.session_state.parsed_query = parse_query(query)
                st.session_state.jobs = search_jobs(query, force_refresh=True)
                st.session_state.company_status = company_status(query, st.session_state.jobs)

    if "parsed_query" in st.session_state:
        p = st.session_state.parsed_query
        with st.expander("🧠 What CareerMatch understood"):
            st.write(f"**Company:** {p.get('company') or 'Any company'}")
            st.write(f"**Experience:** {p.get('experience') or 'Any level'}")
            st.write(f"**Location:** {p.get('location') or 'Any location'}")
            st.write(f"**Role:** {p.get('role') or 'Any role'}")
            st.write(f"**Skills:** {', '.join(p.get('skills', [])) or 'Any skills'}")

    if "company_status" in st.session_state and st.session_state.company_status:
        cs = st.session_state.company_status
        if cs["status"] == "available":
            st.success("🟢 " + cs["message"])
        elif cs["status"] == "not_found":
            st.warning("🟡 " + cs["message"])
        elif cs["status"] == "unavailable":
            st.error("🔴 " + cs["message"])
        else:
            st.info("🔵 " + cs["message"])
        st.link_button("Open official career portal", cs["profile"]["career_url"])
        if cs["profile"].get("fresher_url"):
            st.link_button("Open fresher / graduate page", cs["profile"]["fresher_url"])

    if st.session_state.jobs:
        st.success(f"Found {len(st.session_state.jobs)} matching jobs.")
        with st.expander("Source health"):
            for source in get_source_health():
                st.write(f"{source['company']} ({source['provider']}/{source['slug']}): {source['status']} — {source['jobs']} jobs")
        for job in st.session_state.jobs:
            with st.container(border=True):
                st.markdown(f"### {job['title']}")
                st.write(f"**Company:** {job['company']}")
                st.write(f"**Location:** {job['location'] or 'Not specified'}")
                if job.get("description"):
                    st.write(job["description"][:700] + ("..." if len(job["description"]) > 700 else ""))
                c1, c2 = st.columns(2)
                c1.link_button("View Job", job["source_url"] or "#")
                c2.link_button("Apply", job["apply_url"] or job["source_url"] or "#")

with tab2:
    st.subheader("Resume Analysis")
    uploaded = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])
    if uploaded:
        try:
            text = extract_resume_text(uploaded)
            skills = extract_skills(text)
            st.session_state.resume_text = text
            st.session_state.resume_skills = skills
            st.success("Resume analyzed.")
            st.write("**Detected Skills**")
            st.write(", ".join(skills) if skills else "No configured skills detected.")
        except Exception as e:
            st.error(str(e))

with tab3:
    st.subheader("Resume → Job Matching")
    if not st.session_state.resume_skills:
        st.info("Upload a resume in Resume Analysis first.")
    elif not st.session_state.jobs:
        st.info("Search jobs first.")
    else:
        for job in st.session_state.jobs:
            result = match_resume_to_job(st.session_state.resume_skills, job)
            st.markdown(f"### {job['company']} — {job['title']}")
            st.progress(result["score"] / 100)
            st.write(f"**Match:** {result['score']}%")
            st.write("**Matching skills:** " + (", ".join(result["matching"]) or "None"))
            st.write("**Missing skills:** " + (", ".join(result["missing"]) or "None"))

with tab4:
    st.subheader("Personalized Preparation")
    if not st.session_state.resume_skills or not st.session_state.jobs:
        st.info("Upload a resume and search for jobs first.")
    else:
        for job in st.session_state.jobs:
            result = match_resume_to_job(st.session_state.resume_skills, job)
            st.markdown(f"### {job['company']} — {job['title']}")
            plan = build_preparation_plan(result["missing"])
            for day, topic in plan:
                st.write(f"**Day {day} →** {topic}")

with tab5:
    st.subheader("100 Relevant Interview Questions")
    if not st.session_state.jobs:
        st.info("Search for a job first.")
    else:
        selected = st.selectbox(
            "Select a job", st.session_state.jobs,
            format_func=lambda j: f"{j['company']} — {j['title']}"
        )
        questions = generate_100_questions(selected, st.session_state.resume_skills)
        for i, q in enumerate(questions, 1):
            st.write(f"{i}. {q}")
