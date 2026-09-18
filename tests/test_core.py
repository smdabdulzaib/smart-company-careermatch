import unittest
from nlp_processor import parse_query
from skill_matcher import match_resume_to_job
from interview import generate_100_questions

class TestCore(unittest.TestCase):
    def test_nlp(self):
        result = parse_query("Python fresher jobs in Hyderabad")
        self.assertIn("python", result["skills"])
        self.assertEqual(result["experience"], "Fresher")
        self.assertEqual(result["location"], "hyderabad")

    def test_matching(self):
        job = {"title":"Python Developer", "description":"Python SQL REST API"}
        result = match_resume_to_job(["Python", "SQL"], job)
        self.assertGreater(result["score"], 0)
        self.assertIn("REST API", result["missing"])

    def test_100_questions(self):
        job = {"title":"Python Developer", "description":"Python SQL REST API"}
        qs = generate_100_questions(job, ["Python", "SQL"])
        self.assertEqual(len(qs), 100)
        self.assertEqual(len(set(qs)), 100)

if __name__ == "__main__":
    unittest.main()

# Natural-language company/entity regression checks.
def _extra_nlp_tests():
    cases = [
        ("TCS fresher jobs in Hyderabad", "TCS", "Fresher", "hyderabad"),
        ("Tata Consultancy Services software developer fresher in India", "TCS", "Fresher", "india"),
        ("Apple entry level software engineer jobs in India", "Apple", "Fresher", "india"),
        ("Microsoft backend jobs in Hyderabad", "Microsoft", "", "hyderabad"),
    ]
    for query, company, experience, location in cases:
        result = parse_query(query)
        assert result["company"] == company
        assert result["experience"] == experience
        assert result["location"] == location

_extra_nlp_tests()

class TestCompanyInterviewQuestions(unittest.TestCase):
    def test_company_specific_questions_differ(self):
        from interview import generate_100_questions
        tcs = generate_100_questions({"company": "TCS", "title": "Software Engineer", "description": "Python REST API"})
        apple = generate_100_questions({"company": "Apple", "title": "Software Engineer", "description": "Python REST API"})
        self.assertNotEqual(tcs[:8], apple[:8])
        self.assertTrue(any("TCS" in q for q in tcs))
        self.assertTrue(any("Apple" in q for q in apple))
