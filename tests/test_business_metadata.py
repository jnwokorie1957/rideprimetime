import unittest,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'public'
class BusinessMetadataTests(unittest.TestCase):
    def test_general_service_titles_and_og_agree(self):
        for slug in ('services','what-we-stand-for','faqs'):
            text=(ROOT/('non-emergency-medical-transportation-'+slug)/'index.html').read_text(encoding='utf-8')
            title=re.search(r'<title>(.*?)</title>',text).group(1)
            self.assertIn('Wheelchair and Ambulatory',title)
            self.assertIn('property="og:title" content="'+title+'"',text)
        text=(ROOT/'non-emergency-medical-transportation-book-today/index.html').read_text(encoding='utf-8')
        self.assertIn('Request a Houston Ride and Private-Pay Quote',text)
        self.assertNotIn('Request a Wheelchair Ride',text)
    def test_focused_service_and_booking_safeguards(self):
        text=(ROOT/'non-emergency-medical-transportation-services/wheelchair-transportation/index.html').read_text(encoding='utf-8')
        self.assertIn('<title>Private-Pay Wheelchair Transportation in Houston',text)
        text=(ROOT/'non-emergency-medical-transportation-book-today/index.html').read_text(encoding='utf-8')
        self.assertNotIn('<form',text);self.assertIn('not a confirmed reservation',text)
if __name__=='__main__':unittest.main()
