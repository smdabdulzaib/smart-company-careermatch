# Public job-board identifiers collected from public ATS endpoints.
# They are intentionally configuration data: if a company changes ATS/provider,
# edit this list without changing the fetcher code.

JOB_SOURCES = [
    # Greenhouse
    {"provider": "greenhouse", "company": "Airbnb", "slug": "airbnb"},
    {"provider": "greenhouse", "company": "Anthropic", "slug": "anthropic"},
    {"provider": "greenhouse", "company": "Cloudflare", "slug": "cloudflare"},
    {"provider": "greenhouse", "company": "Coinbase", "slug": "coinbase"},
    {"provider": "greenhouse", "company": "Datadog", "slug": "datadog"},
    {"provider": "greenhouse", "company": "Discord", "slug": "discord"},
    {"provider": "greenhouse", "company": "Dropbox", "slug": "dropbox"},
    {"provider": "greenhouse", "company": "Figma", "slug": "figma"},
    {"provider": "greenhouse", "company": "GitLab", "slug": "gitlab"},
    {"provider": "greenhouse", "company": "Instacart", "slug": "instacart"},
    {"provider": "greenhouse", "company": "Lyft", "slug": "lyft"},
    {"provider": "greenhouse", "company": "Postman", "slug": "postman"},
    {"provider": "greenhouse", "company": "Reddit", "slug": "reddit"},
    {"provider": "greenhouse", "company": "Stripe", "slug": "stripe"},
    {"provider": "greenhouse", "company": "Vercel", "slug": "vercel"},
    {"provider": "greenhouse", "company": "Databricks", "slug": "databricks"},
    {"provider": "greenhouse", "company": "MongoDB", "slug": "mongodb"},
    {"provider": "greenhouse", "company": "Okta", "slug": "okta"},
    {"provider": "greenhouse", "company": "Pinterest", "slug": "pinterest"},
    {"provider": "greenhouse", "company": "Roblox", "slug": "roblox"},
    {"provider": "greenhouse", "company": "Samsara", "slug": "samsara"},
    {"provider": "greenhouse", "company": "Twilio", "slug": "twilio"},
    {"provider": "greenhouse", "company": "Udemy", "slug": "udemy"},
    {"provider": "greenhouse", "company": "Webflow", "slug": "webflow"},
    {"provider": "greenhouse", "company": "Zscaler", "slug": "zscaler"},

    # Ashby
    {"provider": "ashby", "company": "Linear", "slug": "linear"},
    {"provider": "ashby", "company": "Notion", "slug": "notion"},
    {"provider": "ashby", "company": "OpenAI", "slug": "openai"},
    {"provider": "ashby", "company": "Ramp", "slug": "ramp"},
    {"provider": "ashby", "company": "Replit", "slug": "replit"},
    {"provider": "ashby", "company": "RevenueCat", "slug": "revenuecat"},
    {"provider": "ashby", "company": "PostHog", "slug": "posthog"},
    {"provider": "ashby", "company": "Supabase", "slug": "supabase"},
    {"provider": "ashby", "company": "Neon", "slug": "neon"},
    {"provider": "ashby", "company": "Railway", "slug": "railway"},
    {"provider": "ashby", "company": "Retool", "slug": "retool"},
    {"provider": "ashby", "company": "Snyk", "slug": "snyk"},
    {"provider": "ashby", "company": "WorkOS", "slug": "workos"},

    # Lever
    {"provider": "lever", "company": "Spotify", "slug": "spotify"},
    {"provider": "lever", "company": "Plaid", "slug": "plaid"},
    {"provider": "lever", "company": "Outreach", "slug": "outreach"},
    {"provider": "lever", "company": "Toptal", "slug": "toptal"},
]

# Official career portals for companies that do not use the ATS feeds above.
# These are queried only for company-specific searches.
OFFICIAL_COMPANY_SOURCES = [
    {"provider": "official", "company": "TCS", "slug": "tcs", "url": "https://www.tcs.com/careers/india/entry-level", "official_type": "tcs", "fresher": True, "default_location": "India", "timeout": 5},
    {"provider": "official", "company": "Cognizant", "slug": "cognizant", "url": "https://careers.cognizant.com/india-en/jobs/", "official_type": "generic", "fresher": True, "default_location": "India", "link_patterns": ["/jobs/"], "timeout": 5},
    {"provider": "official", "company": "Capgemini", "slug": "capgemini", "url": "https://jobs.capgemini.com/in-en/search/", "official_type": "generic", "fresher": True, "default_location": "India", "link_patterns": ["/job/", "/jobs/"], "timeout": 5},
    {"provider": "official", "company": "Accenture", "slug": "accenture", "url": "https://www.accenture.com/in-en/careers/jobsearch", "official_type": "generic", "fresher": True, "default_location": "India", "link_patterns": ["/careers/jobdetails"], "timeout": 5},
    {"provider": "official", "company": "Deloitte", "slug": "deloitte", "url": "https://southasiacareers.deloitte.com/go/Deloitte-India/718244/", "official_type": "generic", "fresher": True, "default_location": "India", "link_patterns": ["/go/"], "timeout": 5},
    {"provider": "official", "company": "Apple", "slug": "apple", "url": "https://jobs.apple.com/en-in/search?location=india-INDC", "official_type": "generic", "fresher": True, "default_location": "India", "link_patterns": ["/en-in/details/"], "timeout": 5},
    {"provider": "official", "company": "Microsoft", "slug": "microsoft", "url": "https://careers.microsoft.com/v2/global/en/locations/india.html", "official_type": "generic", "fresher": True, "default_location": "India", "link_patterns": ["/v2/global/en/"], "timeout": 5},
]

JOB_SOURCES.extend(OFFICIAL_COMPANY_SOURCES)
