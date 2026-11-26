import unittest
from pathlib import Path
from articles import ARTICLES, published_articles
ROOT=Path(__file__).resolve().parents[1]
SLUG='comparing-private-pay-medical-ride-quotes-houston'
class QuoteComparisonTests(unittest.TestCase):
 def test_published_metadata_and_discovery(self):
  entry=next(article for article in published_articles(ARTICLES) if article['slug']==SLUG)
  self.assertEqual(entry['slug'], SLUG)
  page=(ROOT/'public/articles'/SLUG/'index.html').read_text()
  self.assertEqual(page.count('<h1>'),1)
  self.assertIn('rel="canonical" href="https://www.rideprimetime.net/articles/'+SLUG+'/',page)
  self.assertNotIn('Prepared with AI drafting assistance.',page)
  self.assertIn('Published by Robert, CTO of Primetime Medical Transportation',page)
  self.assertIn('/articles/'+SLUG+'/',(ROOT/'public/articles/index.html').read_text())
  self.assertIn('/articles/'+SLUG+'/',(ROOT/'public/sitemap.xml').read_text())
 def test_exact_reviewed_reader_content(self):
  import hashlib
  content=(ROOT/'content'/f'{SLUG}.md').read_bytes()
  self.assertEqual(hashlib.sha256(content).hexdigest(),'a8237f669120c28601b46552941aa57f02b5ae9655aca0f3bf93bd7c5950dc7d')
