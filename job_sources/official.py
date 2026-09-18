import html
import re
from html.parser import HTMLParser
from urllib.parse import urlencode, urljoin
import requests

class _Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []
        self._href = None
        self._text = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('href'):
            self._href = attrs['href']
            self._text = []
    def handle_data(self, data):
        if self._href and data.strip():
            self._text.append(data.strip())
    def handle_endtag(self, tag):
        if tag == 'a' and self._href:
            text = ' '.join(self._text)
            self.items.append((text, self._href))
            self._href = None
            self._text = []

def _plain(text):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', text or ''))).strip()

def _job(title, company, location, url, description=''):
    return {
        'company': company,
        'title': title.strip(),
        'location': location or 'India',
        'experience': '',
        'skills': '',
        'description': description[:1200],
        'source_url': url,
        'apply_url': url,
        'provider': 'official',
        'source_id': url,
        'official_source': True,
    }

def _request(url, timeout=5):
    return requests.get(url, timeout=timeout, headers={'User-Agent': 'SmartCompanyCareerMatch/7.0'}, allow_redirects=True)

def _tcs(source, timeout):
    url = source['url']
    r = _request(url, timeout)
    r.raise_for_status()
    text = _plain(r.text)
    jobs = []
    programs = [
        'TCS BPS Hiring', 'TCS Atlas Hiring', 'TCS MBA Hiring',
        'TCS BSc Ignite Hiring', 'TCS Sigma Hiring', 'TCS ILP', 'TCS Xplore'
    ]
    for p in programs:
        if p.lower() in text.lower():
            jobs.append(_job(p, 'TCS', 'India', url, 'Official TCS entry-level/fresher program listed on the TCS careers page.'))
    return jobs

def _generic(source, timeout):
    url = source['url']
    r = _request(url, timeout)
    r.raise_for_status()
    parser = _Parser()
    parser.feed(r.text)
    company = source['company']
    patterns = source.get('link_patterns', [])
    jobs = []
    seen = set()
    for text, href in parser.items:
        clean = _plain(text)
        full = urljoin(url, href)
        if not clean or len(clean) < 5 or len(clean) > 140:
            continue
        if patterns and not any(p.lower() in full.lower() for p in patterns):
            continue
        if full in seen:
            continue
        # Avoid navigation links and generic career labels.
        bad = {'search jobs', 'careers', 'jobs', 'find a job', 'view jobs', 'browse all jobs', 'learn more', 'apply'}
        if clean.lower() in bad:
            continue
        if not any(k in clean.lower() for k in [
            'engineer', 'developer', 'analyst', 'consultant', 'associate', 'intern',
            'graduate', 'trainee', 'specialist', 'architect', 'manager', 'scientist',
            'administrator', 'support', 'technology', 'software', 'data', 'business'
        ]):
            continue
        seen.add(full)
        jobs.append(_job(clean, company, source.get('default_location', 'India'), full))
        if len(jobs) >= source.get('max_jobs', 40):
            break
    return jobs

def get_official_jobs(source):
    provider_type = source.get('official_type', 'generic')
    timeout = source.get('timeout', 5)
    if provider_type == 'tcs':
        return _tcs(source, timeout)
    return _generic(source, timeout)
