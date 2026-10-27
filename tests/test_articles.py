import unittest
from articles import render_articles, ARTICLES, inline
from pathlib import Path

class ArticleTests(unittest.TestCase):
    def sample(self):
        return dict(slug='test-topic',title='Test & topic',summary='Test summary',published_on='2026-10-27',
                    sections=[('Heading',['Text <not markup>'])],sources=[('Official source','https://example.org/reference')])

    def render(self, entries):
        pages={}
        paths=render_articles(entries,lambda title,summary,path,body: body,lambda path,body: pages.update({path:body}))
        return paths,pages

    def test_empty_registry_has_no_placeholder_or_index(self):
        self.assertEqual(self.render([]),([],{}))

    def test_routes_sources_attribution_and_escaped_content(self):
        paths,pages=self.render([self.sample()])
        self.assertEqual(paths,['/articles/','/articles/test-topic/'])
        body=pages[paths[1]]
        for text in ('Published by Primetime Medical Transportation / RidePrimetime','datetime="2026-10-27"','Text &lt;not markup&gt;',
                     'https://example.org/reference','href="/articles/"'):
            self.assertIn(text,body)
        self.assertNotIn('reviewed by',body.lower())
        self.assertIn('href="/articles/test-topic/"',pages['/articles/'])

    def test_invalid_inputs_fail_before_writing(self):
        for changes in ({'slug':'../escape'},{'published_on':'not-a-date'},
                        {'sources':[('bad','javascript:alert(1)')]},{'sections':[]}):
            entry=self.sample();entry.update(changes)
            with self.assertRaises(ValueError):self.render([entry])
        with self.assertRaises(ValueError):self.render([self.sample(),self.sample()])

    def test_reviewed_article_and_discovery(self):
        root=Path(__file__).resolve().parents[1]/'public'
        path='/articles/smarter-medical-transportation-iteration/'
        page=(root/path.strip('/')/'index.html').read_text(encoding='utf-8')
        for text in ('https://www.rideprimetime.net'+path,'Prepared with AI drafting assistance',
                     'Research checked 2026-10-27','hypothetical planning example',
                     'possible future improvements','not a claim about a currently deployed',
                     'https://www.w3.org/WAI/tutorials/forms/notifications/',
                     'subject to trip suitability and availability','<ul><li>'):
            self.assertIn(text,page)
        self.assertNotIn('25 years',page)
        self.assertNotIn('not yet published',page)
        self.assertIn(path,(root/'sitemap.xml').read_text())
        self.assertIn(path,(root/'articles/index.html').read_text())
        self.assertIn('href="/articles/"',(root/'index.html').read_text())
        self.assertIn('href="/articles/"',(root/'sitemap/index.html').read_text())

    def test_inline_markup_cannot_inject_html_or_attributes(self):
        self.assertEqual(inline('<script>'), '&lt;script&gt;')
        self.assertNotIn('<a ',inline('[bad](javascript:alert)'))
        self.assertIn('&quot;',inline('[safe](https://example.org/"test)'))
