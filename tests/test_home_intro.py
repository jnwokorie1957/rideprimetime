import unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]/'public'
class Metadata(HTMLParser):
    def __init__(self):super().__init__();self.descriptions=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='meta' and (a.get('name')=='description' or a.get('property')=='og:description'):self.descriptions.append(a['content'])
class HomeIntroTests(unittest.TestCase):
    def test_company_introduction_covers_both_services(self):
        s=(ROOT/'index.html').read_text(encoding='utf-8');p=Metadata();p.feed(s)
        wording='Private-pay wheelchair and ambulatory transportation'
        self.assertIn('<p class="lead">'+wording,s)
        self.assertEqual(len(p.descriptions),2)
        for description in p.descriptions:self.assertTrue(description.startswith(wording))
        self.assertIn('Houston Wheelchair and Ambulatory Transportation',s)
        self.assertIn('not a confirmed reservation',s)
        self.assertIn('Trips confirmed individually',s)
    def test_focused_service_and_discharge_language_retained(self):
        s=(ROOT/'non-emergency-medical-transportation-services/wheelchair-transportation/index.html').read_text(encoding='utf-8')
        self.assertIn('Private-Pay Wheelchair Transportation in Houston',s)
        self.assertIn('wheelchair dimensions',s)
        s=(ROOT/'non-emergency-medical-transportation-services/ambulatory-transportation-nemt/index.html').read_text(encoding='utf-8')
        self.assertIn('responsible',s);self.assertIn('not automatically',s)
if __name__=='__main__':unittest.main()
