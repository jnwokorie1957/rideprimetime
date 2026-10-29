import unittest
from articles import render_articles, ARTICLES, inline
from pathlib import Path

class ArticleTests(unittest.TestCase):
    def sample(self):
        return dict(status='published',slug='test-topic',title='Test & topic',summary='Test summary',published_on='2026-10-27',
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
        for text in ('Published by Robert, AI CTO of Primetime Medical Transportation','datetime="2026-10-27"','Text &lt;not markup&gt;',
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
        for text in ('https://www.rideprimetime.net'+path,'Published by Robert, AI CTO of Primetime Medical Transportation',
                     'Research checked 2026-10-27','hypothetical planning example',
                     'possible future improvements','not a claim about a currently deployed',
                     'https://www.w3.org/WAI/tutorials/forms/notifications/',
                     'subject to trip suitability and availability','<ul><li>'):
            self.assertIn(text,page)
        self.assertNotIn('25 years',page)
        self.assertNotIn('not yet published',page)
        self.assertNotIn('Prepared with AI drafting assistance',page)
        self.assertNotIn('"@type": "Person"',page)
        self.assertIn(path,(root/'sitemap.xml').read_text())
        self.assertIn(path,(root/'articles/index.html').read_text())
        self.assertIn('href="/articles/"',(root/'index.html').read_text())
        self.assertIn('href="/articles/"',(root/'sitemap/index.html').read_text())

    def test_inline_markup_cannot_inject_html_or_attributes(self):
        self.assertEqual(inline('<script>'), '&lt;script&gt;')
        self.assertNotIn('<a ',inline('[bad](javascript:alert)'))
        self.assertIn('&quot;',inline('[safe](https://example.org/"test)'))

    def test_multiple_published_articles_and_drafts(self):
        first=self.sample();second=dict(self.sample(),slug='second-topic',title='Second article')
        draft=dict(self.sample(),slug='draft-topic',status='draft')
        unmarked=dict(self.sample(),slug='unmarked');unmarked.pop('status')
        future=dict(self.sample(),slug='future-topic',published_on='9999-12-31')
        paths,pages=self.render([first,draft,second,unmarked,future])
        self.assertEqual(paths,['/articles/','/articles/test-topic/','/articles/second-topic/'])
        self.assertEqual(set(pages),set(paths))
        for slug in ('test-topic','second-topic'):
            self.assertIn('href="/articles/'+slug+'/"',pages['/articles/'])
        for slug in ('draft-topic','unmarked','future-topic'):
            self.assertNotIn(slug,''.join(pages.values()))
        self.assertEqual(self.render([draft,unmarked,future]),([],{}))

    def test_shared_navigation_has_one_article_index_link(self):
        root=Path(__file__).resolve().parents[1]/'public'
        for p in root.rglob('*.html'):
            nav=p.read_text(encoding='utf-8').split('<nav id="navigation"')[1].split('</nav>')[0]
            self.assertEqual(nav.count('href="/articles/">Articles</a>'),1,str(p))

    def test_incremental_drafts_and_removed_entries_leave_no_generated_page(self):
        from contextlib import contextmanager
        from uuid import uuid4
        import shutil
        @contextmanager
        def ordinary_workspace_directory():
            parent=Path(__file__).resolve().parents[1]
            folder=parent/('_article_test_'+uuid4().hex)
            folder.mkdir()
            try:yield folder
            finally:
                assert folder.resolve().parent == parent.resolve()
                shutil.rmtree(folder)
        from articles import reconcile_article_output
        for replacement in ({'status':'draft'},{'published_on':'9999-12-31'},None):
            with ordinary_workspace_directory() as folder:
                public=Path(folder)
                def write(path,body):
                    page=public/path.strip('/')/'index.html'
                    page.parent.mkdir(parents=True,exist_ok=True);page.write_text(body)
                entry=self.sample()
                paths=render_articles([entry],lambda t,s,p,b:b,write)
                reconcile_article_output(public,paths)
                self.assertTrue((public/'articles/test-topic/index.html').exists())
                unrelated=public/'articles/notes.txt';unrelated.write_text('Keep this asset')
                sibling=public/'privacy-policy/index.html';sibling.parent.mkdir();sibling.write_text('Keep this page')
                next_entries=[] if replacement is None else [dict(entry,**replacement)]
                paths=render_articles(next_entries,lambda t,s,p,b:b,write)
                reconcile_article_output(public,paths)
                self.assertFalse((public/'articles/test-topic/index.html').exists())
                self.assertFalse((public/'articles/index.html').exists())
                self.assertEqual(unrelated.read_text(),'Keep this asset')
                self.assertEqual(sibling.read_text(),'Keep this page')

    def test_testing_plan_hierarchy_and_hypothetical_boundaries(self):
        from articles import block
        page=(Path(__file__).resolve().parents[1]/'public/articles/smarter-medical-transportation-iteration/index.html').read_text(encoding='utf-8')
        section=page.split('<h2>Before adding a feature, write down what should happen</h2>')[1].split('<h2>Treat wheelchair suitability')[0]
        self.assertEqual(section.count('<h3>'),6)
        self.assertNotIn('### ',section)
        for value in ('hypothetical future inquiry tool using invented test details','not descriptions of a live RidePrimetime',
                      'Receipt established, arrangements unconfirmed','Receipt cannot be established',
                      'not live RidePrimetime notices','https://www.w3.org/WAI/tutorials/forms/validation/',
                      'https://www.w3.org/WAI/test-evaluate/preliminary/'):
            self.assertIn(value,section)
        self.assertIn('Published <time datetime="2026-10-27">2026-10-27</time>',page)
        self.assertIn('Updated <time datetime="2026-10-29">2026-10-29</time>',page)
        self.assertEqual(block('### <script>'),'<h3>&lt;script&gt;</h3>')
        self.assertEqual(block('ordinary paragraph'),'<p>ordinary paragraph</p>')
