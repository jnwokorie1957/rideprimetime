from html.parser import HTMLParser
from pathlib import Path
import unittest
from articles import render_articles

ROOT = Path(__file__).resolve().parents[1]
class Tags(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.anchors=[]; self.headings=[]; self.navs=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.append(attrs['id'])
        if tag=='a':self.anchors.append(attrs.get('href',''))
        if tag=='h2':self.headings.append(attrs)
        if tag=='nav':self.navs.append(attrs)

class ArticleLayoutTests(unittest.TestCase):
    def test_all_section_links_have_unique_targets(self):
        for path in (ROOT/'public/articles').glob('*/index.html'):
            page=path.read_text(); tags=Tags();tags.feed(page)
            self.assertEqual(len(tags.ids),len(set(tags.ids)))
            links=[x[1:] for x in tags.anchors if x.startswith('#section-')]
            self.assertGreater(len(links),0)
            self.assertTrue(all(x in tags.ids for x in links))
            self.assertEqual(len(links),len([h for h in tags.headings if h.get('id','').startswith('section-')]))
            self.assertEqual(sum(n.get('aria-label')=='In this article' for n in tags.navs),1)
    def test_byline_and_article_stylesheet(self):
        for path in (ROOT/'public/articles').glob('*/index.html'):
            page=path.read_text()
            self.assertEqual(page.count('Published by Robert, CTO of Primetime Medical Transportation'),1)
            self.assertNotIn('Robert, AI CTO',page)
            self.assertIn('/assets/articles.css?v=20261102',page)
            self.assertIn('Back to all articles',page)
    def test_duplicate_headings_get_distinct_safe_targets(self):
        entry=dict(slug='sample',status='published',title='Example',summary='Summary',published_on='2026-01-01',sections=[('Same <heading>',['First']),('Same <heading>',['Second'])],sources=[])
        pages={};render_articles([entry],lambda t,s,p,b:b,lambda p,b:pages.update({p:b}))
        page=pages['/articles/sample/']; self.assertIn('id="section-1"',page);self.assertIn('id="section-2"',page)
        self.assertIn('Same &lt;heading&gt;',page);self.assertNotIn('<heading>',page)
    def test_index_cards_have_metadata_and_five_articles(self):
        page=(ROOT/'public/articles/index.html').read_text()
        self.assertEqual(page.count('class="article-card-meta"'),5)
        self.assertEqual(page.count('class="article-card-arrow" aria-hidden="true"'),5)
    def test_article_styles_are_not_added_to_service_pages(self):
        for path in (ROOT/'public').rglob('*.html'):
            if 'articles' not in path.relative_to(ROOT/'public').parts:
                self.assertNotIn('/assets/articles.css',path.read_text())
    def test_toc_overrides_shared_navigation_layout_and_handles_mobile(self):
        css=(ROOT/'public/assets/articles.css').read_text()
        self.assertIn('.article-toc{display:block;',css)
        self.assertIn('@media screen{.js nav.article-toc:not(.open){display:block}}',css)
        self.assertIn('@media(max-width:700px)',css)
        self.assertIn('grid-template-columns:1fr',css)
        self.assertIn('overflow-wrap:anywhere',css)
        self.assertNotIn('position:fixed',css)

if __name__=='__main__':unittest.main()
