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

    def test_return_guidance_keeps_publication_and_marks_update(self):
        page=(Path(__file__).resolve().parents[1]/'public/articles/houston-ride-quote-checklist/index.html').read_text(encoding='utf-8')
        self.assertIn('itemprop="datePublished" content="2026-10-28"',page)
        self.assertIn('itemprop="dateModified" content="2026-10-29"',page)
        self.assertIn('Updated <time datetime="2026-10-29">2026-10-29</time>',page)
        section=page.split('<h2>Give the return journey its own questions</h2>')[1].split('<h2>Keep a short planning note</h2>')[0]
        for text in ('hypothetical call opening','href="https://www.rideprimetime.net/">planning steps</a>',
                     'and through which channel?','appointment takes longer than expected?',
                     'Keep an estimated finish time separate from an agreed pickup time',
                     'should not be taken as confirmation of a return arrangement',
                     'do not imply that a vehicle waits'):
            self.assertIn(text,section)
