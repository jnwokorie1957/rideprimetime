from pathlib import Path
import unittest

from articles import ARTICLES

ROOT = Path(__file__).resolve().parents[1]
SLUG = 'finding-right-entrance-houston-medical-campus-ride'
PATH = '/articles/' + SLUG + '/'


class EntranceArticleTests(unittest.TestCase):
    def setUp(self):
        self.page = (ROOT / 'public' / PATH.strip('/') / 'index.html').read_text(encoding='utf-8')

    def test_metadata_and_discovery(self):
        self.assertIn('rel="canonical" href="https://www.rideprimetime.net' + PATH + '"', self.page)
        self.assertEqual(self.page.count('<h1>'), 1)
        self.assertEqual(self.page.count('Published by Robert, CTO of Primetime Medical Transportation'), 1)
        self.assertIn('Published <time datetime="2026-11-04">2026-11-04</time>', self.page)
        self.assertIn('Research checked 2026-11-04', self.page)
        for index in ('articles/index.html', 'sitemap.xml'):
            self.assertIn(PATH, (ROOT / 'public' / index).read_text(encoding='utf-8'))
        self.assertIn('href="/articles/"', (ROOT / 'public/sitemap/index.html').read_text(encoding='utf-8'))

    def test_reader_only_and_accessible_structure(self):
        source = (ROOT / 'content' / (SLUG + '.md')).read_text(encoding='utf-8')
        for value in ('INTERNAL EDITORIAL HANDOFF', 'Library', 'libfile_', 'Status: Completed',
                      'Publication handoff:', 'Keyword seed:', 'Editorial note:', '<!--', 'os.setxattr'):
            self.assertNotIn(value, source)
            self.assertNotIn(value, self.page)
        self.assertEqual(self.page.count('<h2 id="section-'), 8)
        self.assertIn('aria-label="In this article"', self.page)
        self.assertIn('<ul><li>', self.page)
        self.assertIn('/assets/articles.css', self.page)
        self.assertIn('<strong>Vehicle meeting point:</strong>', self.page)

    def test_confirmation_and_hospital_boundaries(self):
        for value in ('An inquiry is not a confirmed reservation.', 'hypothetical example',
                      'not an endorsement or preferred-provider designation',
                      'not a booking form or an official facility procedure',
                      'Do not assume an outbound-and-return reservation includes an additional stop'):
            self.assertIn(value, self.page)
        for url in ('https://www.houstonmethodist.org/locations/texas-medical-center/for-patients/parking/',
                    'https://www.mdanderson.org/patients-family/becoming-our-patient/getting-to-md-anderson.html',
                    'https://www.rideprimetime.net/articles/houston-ride-quote-checklist/'):
            self.assertIn('href="' + url + '"', self.page)

    def test_prior_dates_unchanged(self):
        dates = {item['slug']: item['published_on'] for item in ARTICLES}
        self.assertEqual(dates['smarter-medical-transportation-iteration'], '2026-10-27')
        self.assertEqual(dates['houston-ride-quote-checklist'], '2026-10-28')
        self.assertEqual(dates['bringing-a-companion-on-a-medical-ride-in-houston'], '2026-11-02')
        self.assertEqual(dates['planning-recurring-medical-rides-houston'], '2026-11-02')
        self.assertEqual(dates[SLUG], '2026-11-04')


if __name__ == '__main__':
    unittest.main()
