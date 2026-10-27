import unittest
from pathlib import Path

PUBLIC=Path(__file__).resolve().parents[1]/'public'

class TripClarityTests(unittest.TestCase):
    def test_home_quote_path_and_confirmation_stages(self):
        text=(PUBLIC/'index.html').read_text(encoding='utf-8')
        for phrase in ('including those who use mobility aids','Request a ride quote',
                       'required arrival time and return needs','If the return time is uncertain',
                       'Receive booking confirmation','A request or quote alone is not a confirmed reservation.'):
            self.assertIn(phrase,text)
        self.assertIn('href="/non-emergency-medical-transportation-book-today/">Request a ride quote',text)
        self.assertNotIn('<form',text)
    def test_vehicle_route_and_plural_navigation_are_consistent(self):
        for p in PUBLIC.rglob('*.html'):
            text=p.read_text(encoding='utf-8')
            nav=text.split('<nav id="navigation"')[1].split('</nav>')[0]
            self.assertIn('href="/our-vehicle/">Explore our vehicles',nav)
        page=(PUBLIC/'our-vehicle/index.html').read_text(encoding='utf-8')
        self.assertIn('https://www.rideprimetime.net/our-vehicle/',page)
        self.assertNotIn('/our-vehicles/',page)
