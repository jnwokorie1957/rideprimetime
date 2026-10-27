import unittest
from pathlib import Path
from html.parser import HTMLParser

PUBLIC=Path(__file__).resolve().parents[1]/'public'
class Images(HTMLParser):
    def __init__(self):super().__init__();self.images=[]
    def handle_starttag(self,t,a):
        if t=='img':self.images.append(dict(a))

class VehicleTests(unittest.TestCase):
    def test_home_keeps_illustration_and_links_to_dedicated_gallery(self):
        s=(PUBLIC/'index.html').read_text(encoding='utf-8');p=Images();p.feed(s)
        self.assertEqual([i['src'] for i in p.images][1:],['/assets/journey.svg'])
        self.assertIn('href="/our-vehicle/">Explore our vehicles',s.split('</main>')[0])

    def test_six_distinct_uncropped_lazy_gallery_photos(self):
        s=(PUBLIC/'our-vehicle/index.html').read_text(encoding='utf-8');p=Images();p.feed(s)
        images=[i for i in p.images if '/ride-primetime-' in i['src'] and i['src'].endswith('.jpg')]
        self.assertEqual(len(images),6);self.assertEqual(len({i['src'] for i in images}),6)
        for i in images:
            self.assertEqual(i['loading'],'lazy');self.assertEqual(i['decoding'],'async')
            self.assertEqual((i['width'],i['height']),('1024','683'))
            self.assertTrue(i['alt']);self.assertLess((PUBLIC/i['src'].lstrip('/')).stat().st_size,250000)
        self.assertIn('<h1>Explore our vehicles</h1>',s)
        self.assertIn('do not establish fit for every wheelchair',s)

    def test_shared_navigation_and_showcase(self):
        for path in PUBLIC.rglob('*.html'):
            s=path.read_text(encoding='utf-8');nav=s.split('<nav id="navigation"')[1].split('</nav>')[0]
            self.assertEqual(nav.count('href="/our-vehicle/"'),1,str(path))
        s=(PUBLIC/'our-vehicle/index.html').read_text(encoding='utf-8')
        for text in ('planned Houston transportation','confirmed individually','responsible adult','private-pay quote'):
            self.assertIn(text,s if text!='confirmed individually' else (PUBLIC/'index.html').read_text(encoding='utf-8'))
    def test_no_inquiry_prototype_in_release(self):
        self.assertEqual(list(PUBLIC.rglob('*inquiry*')),[])
        for path in PUBLIC.rglob('*.html'):
            self.assertNotIn('<form',path.read_text(encoding='utf-8'))

    def test_no_fleet_count_claims(self):
        for path in PUBLIC.rglob('*.html'):
            s=path.read_text(encoding='utf-8').lower()
            for claim in ('one van','one wheelchair','one-van','single-van','single vehicle','our only','our fleet'):
                self.assertNotIn(claim,s,str(path))

if __name__=='__main__':unittest.main()
