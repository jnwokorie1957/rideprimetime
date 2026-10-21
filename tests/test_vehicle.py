import unittest
from pathlib import Path
from html.parser import HTMLParser

PUBLIC=Path(__file__).resolve().parents[1]/'public'
class Images(HTMLParser):
    def __init__(self):super().__init__();self.images=[]
    def handle_starttag(self,t,a):
        if t=='img':self.images.append(dict(a))

class VehicleTests(unittest.TestCase):
    def test_home_image_order_and_loading(self):
        s=(PUBLIC/'index.html').read_text(encoding='utf-8');p=Images();p.feed(s)
        self.assertEqual([i['src'] for i in p.images][1:],['/assets/journey.svg','/assets/ride-primetime-van.jpg','/assets/ride-primetime-ramp.jpg'])
        for image in p.images[2:]:
            self.assertEqual(image['loading'],'lazy');self.assertEqual(image['width'],'1024');self.assertEqual(image['height'],'683')
        self.assertIn('href="/our-vehicle/"',s.split('</main>')[0])
    def test_shared_navigation_and_showcase(self):
        for path in PUBLIC.rglob('*.html'):
            s=path.read_text(encoding='utf-8');nav=s.split('<nav id="navigation"')[1].split('</nav>')[0]
            self.assertEqual(nav.count('href="/our-vehicle/"'),1,str(path))
        s=(PUBLIC/'our-vehicle/index.html').read_text(encoding='utf-8')
        for text in ('one van','confirmed individually','responsible adult','private-pay quote'):
            self.assertIn(text,s if text!='confirmed individually' else (PUBLIC/'index.html').read_text(encoding='utf-8'))
    def test_no_inquiry_prototype_in_release(self):
        self.assertEqual(list(PUBLIC.rglob('*inquiry*')),[])
        for path in PUBLIC.rglob('*.html'):
            self.assertNotIn('<form',path.read_text(encoding='utf-8'))

if __name__=='__main__':unittest.main()
