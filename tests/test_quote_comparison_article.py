import unittest
from pathlib import Path
from articles import ARTICLES, published_articles
ROOT=Path(__file__).resolve().parents[1]
SLUG='comparing-private-pay-medical-ride-quotes-houston'
class QuoteComparisonTests(unittest.TestCase):
 def test_published_metadata_and_discovery(self):
  entry=published_articles(ARTICLES)[0]
  self.assertEqual(entry['slug'], SLUG)
  page=(ROOT/'public/articles'/SLUG/'index.html').read_text()
  self.assertEqual(page.count('<h1>'),1)
  self.assertIn('rel="canonical" href="https://www.rideprimetime.net/articles/'+SLUG+'/',page)
  self.assertEqual(page.count('Prepared with AI drafting assistance.'),1)
  self.assertIn('Published by Robert, CTO of Primetime Medical Transportation',page)
  self.assertIn('/articles/'+SLUG+'/',(ROOT/'public/articles/index.html').read_text())
  self.assertIn('/articles/'+SLUG+'/',(ROOT/'public/sitemap.xml').read_text())
 def test_exact_reviewed_reader_content(self):
  import hashlib
  content=(ROOT/'content'/f'{SLUG}.md').read_bytes()
  self.assertEqual(hashlib.sha256(content).hexdigest(),'069c9eb0efc2095cf45ef0a024eaae746f2e7b45776a0a91a7fa60cdb97cae2f')
