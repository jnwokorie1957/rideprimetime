import unittest
from pathlib import Path
from html.parser import HTMLParser

class ChecklistTests(unittest.TestCase):
    def test_published_checklist_and_discovery(self):
        root=Path(__file__).resolve().parents[1]/'public'
        route='/articles/houston-ride-quote-checklist/'
        page=(root/route.strip('/')/'index.html').read_text(encoding='utf-8')
        for value in ('Published by Robert, AI CTO of Primetime Medical Transportation','datetime="2026-10-28"',
            '713-423-4430','hypothetical preparation note','https://www.tmc.edu/operations/tmc-campus/updates-and-alerts/',
            'https://www.rideprimetime.net'+route,'https://schema.org/Organization','itemprop="name" content="Primetime Medical Transportation"'):
            self.assertIn(value,page)
        for value in ('Unpublished article draft','Editorial handoff','Prepared with AI drafting assistance','25 years','https://schema.org/Person'):
            self.assertNotIn(value,page)
        self.assertEqual(page.count('<h1>'),1)
        self.assertEqual(page.count('<h2>'),7) # six editorial sections and shared contact heading
        for file in ['articles/index.html','sitemap.xml']:
            self.assertIn(route,(root/file).read_text(encoding='utf-8'))
        self.assertIn('/articles/smarter-medical-transportation-iteration/',(root/'articles/index.html').read_text(encoding='utf-8'))
        self.assertIn('A quote or inquiry alone is not a confirmed reservation.',page)
