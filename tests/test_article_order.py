import re
import unittest
from datetime import date
from pathlib import Path
from articles import published_articles, render_articles


class ArticleOrderTests(unittest.TestCase):
    def test_dates_filtering_stable_ties_and_input_preservation(self):
        def article(slug, published_on, **extra):
            return dict(slug=slug, title=slug, summary='Summary', status='published',
                        published_on=published_on, sections=[('Heading', ['Body'])], sources=[], **extra)
        old = article('old', '2025-12-31', modified_on='2026-11-05')
        first = article('same-day-first', '2026-11-02')
        newest = article('newest', '2026-11-04')
        second = article('same-day-second', '2026-11-02')
        draft = dict(article('draft', '2026-11-05'), status='draft')
        unmarked = article('unmarked', '2026-11-05'); del unmarked['status']
        future = article('future', '9999-12-31')
        entries = [old, first, draft, newest, unmarked, second, future]
        original = [dict(entry) for entry in entries]
        expected = ['newest', 'same-day-first', 'same-day-second', 'old']
        self.assertEqual([a['slug'] for a in published_articles(entries, date(2026, 11, 5))], expected)
        pages = {}
        render_articles(entries, lambda t, s, p, b: b, lambda p, b: pages.update({p: b}))
        self.assertEqual(re.findall(r'<h2><a href="/articles/([^/]+)/"', pages['/articles/']), expected)
        self.assertEqual(entries, original)
        for slug in ('draft', 'unmarked', 'future'):
            self.assertNotIn('/articles/' + slug + '/', pages)

    def test_generated_index_dates_descend(self):
        index = (Path(__file__).resolve().parents[1] / 'public/articles/index.html').read_text(encoding='utf-8')
        dates = re.findall(r'<time datetime="([^"]+)">', index)
        self.assertEqual(len(dates), 5)
        self.assertEqual(dates, sorted(dates, reverse=True))
