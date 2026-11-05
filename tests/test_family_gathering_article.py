from pathlib import Path
from html.parser import HTMLParser
import re
import unittest
from articles import ARTICLES, published_articles

ROOT = Path(__file__).resolve().parents[1]
SLUG = 'planning-wheelchair-ride-houston-family-gathering'
PATH = '/articles/' + SLUG + '/'


class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts = []
    def handle_data(self, data):
        self.parts.append(data)


class FamilyGatheringArticleTests(unittest.TestCase):
    def setUp(self):
        self.page = (ROOT / 'public' / PATH.strip('/') / 'index.html').read_text(encoding='utf-8')
        parser = Text(); parser.feed(self.page)
        self.text = ' '.join(parser.parts)

    def test_attribution_metadata_and_newest_discovery(self):
        self.assertIn('rel="canonical" href="https://www.rideprimetime.net' + PATH + '"', self.page)
        self.assertEqual(self.page.count('<h1>'), 1)
        self.assertEqual(self.text.count('Published by Robert, CTO of Primetime Medical Transportation'), 1)
        self.assertEqual(self.text.count('Prepared with AI drafting assistance.'), 1)
        self.assertIn('Research checked 2026-11-05', self.text)
        self.assertIn('datetime="2026-11-05"', self.page)
        self.assertEqual(published_articles(ARTICLES)[0]['slug'], SLUG)
        index = (ROOT / 'public/articles/index.html').read_text(encoding='utf-8')
        self.assertEqual(re.findall(r'<h2><a href="([^"]+)"', index)[0], PATH)
        self.assertIn(PATH, (ROOT / 'public/sitemap.xml').read_text(encoding='utf-8'))

    def test_selectable_checklist_sources_and_scope(self):
        self.assertEqual(self.page.count('<h2 id="section-'), 8)
        self.assertIn('<strong>Host checks:</strong>', self.page)
        self.assertNotIn('<img', self.page.split('<article ', 1)[1].split('</article>', 1)[0])
        for url in ('https://unitedspinal.org/top-10-disability-etiquette/',
                    'https://www.ada.gov/resources/title-iii-primer/',
                    'https://www.rideprimetime.net/non-emergency-medical-transportation-services/social-events-transportation/'):
            self.assertIn('href="' + url + '"', self.page)
        for value in ('must not be blocked by furniture or other items',
                      'not a building-access assessment or a determination of legal compliance',
                      'Do not assume the driver will stay', 'lifting or transfer assistance',
                      'hypothetical example', 'Each trip needs individual confirmation',
                      'An inquiry is not a confirmed reservation.'):
            self.assertIn(value, self.text)
        for marker in ('reader_copy', 'libfile_', 'Publication authority', 'INTERNAL EDITORIAL'):
            self.assertNotIn(marker, self.page)

    def test_current_analytics_and_no_new_booking_form(self):
        self.assertIn('/assets/analytics.js?v=e07b81562862', self.page)
        self.assertNotIn('<form', self.page)
        self.assertIn('For a medical emergency, call 911.', self.text)
