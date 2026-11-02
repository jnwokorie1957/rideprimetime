from pathlib import Path
import unittest

PUBLIC = Path(__file__).resolve().parents[1] / 'public'
SLUGS = ('bringing-a-companion-on-a-medical-ride-in-houston', 'planning-recurring-medical-rides-houston')

class PlanningArticleTests(unittest.TestCase):
    def test_discovery_metadata_and_no_internal_notes(self):
        for slug in SLUGS:
            path = '/articles/' + slug + '/'
            page = (PUBLIC / path.strip('/') / 'index.html').read_text()
            self.assertIn('https://www.rideprimetime.net' + path, page)
            self.assertIn(path, (PUBLIC / 'articles/index.html').read_text())
            self.assertIn(path, (PUBLIC / 'sitemap.xml').read_text())
            self.assertEqual(page.count('Published by Robert, CTO of Primetime Medical Transportation'), 1)
            for hidden in ('DRAFT', 'INTERNAL READINESS', 'internal_release_notes', '```', 'proposed_slug'):
                self.assertNotIn(hidden, page)
            self.assertIn('datetime="2026-11-02"', page)
            self.assertIn('/assets/articles.css', page)

    def test_companion_keeps_confirmation_and_privacy_boundaries(self):
        page = (PUBLIC / 'articles' / SLUGS[0] / 'index.html').read_text()
        for phrase in ('Sending an inquiry does not itself confirm a booking.', 'respect the person', 'Do not promise a relative a seat', 'hypothetical'):
            self.assertIn(phrase, page)

    def test_recurring_note_is_accessible_list_not_code(self):
        page = (PUBLIC / 'articles' / SLUGS[1] / 'index.html').read_text()
        self.assertIn('<li>REPEAT TRIP NOTE</li>', page)
        self.assertIn('<li>DATE:', page)
        self.assertIn('a request or quote alone is not a confirmed reservation', page)
        self.assertIn('hypothetical one-date request', page)

if __name__ == '__main__':
    unittest.main()
