import unittest,json,re,xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote

ROOT=Path(__file__).resolve().parents[1]; PUBLIC=ROOT/'public'
class Page(HTMLParser):
    def __init__(self):super().__init__();self.tags=[];self.ids=[];self.refs=[];self.text=[]
    def handle_starttag(self,t,a):
        d=dict(a);self.tags.append((t,d))
        if 'id' in d:self.ids.append(d['id'])
        for k in ('href','src'):
            if k in d:self.refs.append(d[k])
    def handle_data(self,s):self.text.append(s)

class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages={p:Page() for p in PUBLIC.rglob('*.html')}
        for p,parser in cls.pages.items():parser.feed(p.read_text(encoding='utf-8'))
    def test_page_count_and_sitemap(self):
        self.assertEqual(len(self.pages),31) # 30 canonical routes plus 404
        urls=[e.text for e in ET.parse(PUBLIC/'sitemap.xml').iter() if e.tag.endswith('loc')]
        self.assertEqual(len(urls),30);self.assertEqual(len(set(urls)),30)
        for u in urls:self.assertTrue((PUBLIC/urlsplit(u).path.strip('/')/'index.html').is_file(),u)
    def test_all_local_references_resolve(self):
        for p,parser in self.pages.items():
            for u in parser.refs:
                a=urlsplit(u)
                if a.scheme in ('tel','mailto'):continue
                if a.scheme or a.netloc:continue
                if not a.path:
                    self.assertIn(a.fragment,parser.ids);continue
                dest=PUBLIC/unquote(a.path).lstrip('/')
                if not dest.suffix:dest=dest/'index.html'
                self.assertTrue(dest.is_file(),f'{p}: {u}')
    def test_semantics_accessibility_and_metadata(self):
        titles=set()
        for p,parser in self.pages.items():
            self.assertEqual(sum(t=='h1' for t,d in parser.tags),1,p)
            self.assertEqual(len(parser.ids),len(set(parser.ids)),p)
            self.assertIn(('html',{'lang':'en'}),parser.tags)
            self.assertTrue(any(t=='a' and d.get('href')=='#main' for t,d in parser.tags))
            self.assertTrue(any(t=='meta' and d.get('name')=='description' and len(d.get('content',''))>20 for t,d in parser.tags))
            self.assertTrue(any(t=='link' and d.get('rel')=='canonical' for t,d in parser.tags))
            for t,d in parser.tags:
                if t=='img':self.assertTrue(d.get('alt'))
            s=p.read_text(encoding='utf-8'); title=re.search(r'<title>(.*?)</title>',s).group(1)
            self.assertNotIn(title,titles);titles.add(title)
    def test_contact_and_no_fake_forms(self):
        for p,parser in self.pages.items():
            self.assertIn('tel:+17134234430',parser.refs)
            self.assertIn('mailto:Info@RidePrimetime.net',parser.refs)
            self.assertFalse(any(t in ('form','iframe') for t,d in parser.tags),p)
            self.assertIn('not a confirmed reservation',' '.join(parser.text))
    def test_no_legacy_code_or_private_file_types(self):
        allowed={'.html','.css','.js','.svg','.xml','.txt','.png'}
        for p in PUBLIC.rglob('*'):
            if p.is_file():self.assertIn(p.suffix,allowed,p)
        combined='\n'.join(p.read_text(encoding='utf-8') for p in PUBLIC.rglob('*') if p.is_file() and p.suffix!='.png')
        for marker in ('<?php','DB_PASSWORD','AUTH_KEY','BEGIN PRIVATE KEY','wp-config','admin-ajax.php','forminator_nonce','eval(','document.write(','innerHTML','fetch('):self.assertNotIn(marker,combined)
        for claim in ('Medicaid accepted','guaranteed on-time','our fleet','bariatric transport','stretcher transport','booking confirmed','submission successful'):self.assertNotIn(claim,combined)
    def test_no_third_party_active_resources(self):
        for p,parser in self.pages.items():
            for t,d in parser.tags:
                if t in ('script','img','iframe','link') and d.get('rel')!='canonical':
                    for key in ('src','href'):
                        if key in d:self.assertFalse(urlsplit(d[key]).netloc,(p,d[key]))
                self.assertFalse(any(k.startswith('on') for k in d),p)
                self.assertNotIn('style',d)
    def test_firebase_isolated_config(self):
        config=json.loads((ROOT/'firebase.json').read_text())['hosting']
        self.assertEqual(config['public'],'public')
        self.assertNotIn('rewrites',config)
        self.assertFalse((ROOT/'.firebaserc').exists())
        headers={h['key']:h['value'] for r in config['headers'] for h in r['headers']}
        self.assertIn("form-action 'none'",headers['Content-Security-Policy'])
        self.assertEqual(headers['X-Content-Type-Options'],'nosniff')
    def test_brand_contrast(self):
        def lum(s):
            v=[int(s[n:n+2],16)/255 for n in (0,2,4)]
            v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v]
            return .2126*v[0]+.7152*v[1]+.0722*v[2]
        for color in ('0964ca','142b45','506277'):
            self.assertGreaterEqual((1.05)/(lum(color)+.05),4.5,color)
        # Ring against adjacent surface: light pages/footer, blue CTA and dark utility.
        for ring,surface in [('142b45','ffffff'),('142b45','eaf3fd'),('142b45','f7f9fc'),('ffffff','0964ca'),('ffffff','142b45')]:
            a,b=sorted((lum(ring),lum(surface)))
            self.assertGreaterEqual((b+.05)/(a+.05),3,(ring,surface))
        css=(PUBLIC/'assets/site.css').read_text(encoding='utf-8')
        self.assertIn('outline:3px solid var(--ink);outline-offset:5px',css)
        self.assertIn('.utility a:focus-visible,.contact-band a:focus-visible{outline-color:#fff}',css)
    def test_services_are_directly_discoverable(self):
        hub=PUBLIC/'non-emergency-medical-transportation-services/index.html'
        content=hub.read_text(encoding='utf-8')
        links=re.findall(r'<a class="service-link" href="([^"]+)">([^<]+)</a>',content)
        expected={p.parent.name for p in (PUBLIC/'non-emergency-medical-transportation-services').glob('*/index.html')}
        self.assertEqual(len(links),9)
        self.assertEqual({urlsplit(href).path.strip('/').split('/')[-1] for href,label in links},expected)
        for href,label in links:
            self.assertGreater(len(label),20)
            self.assertNotIn(label.lower(),('learn more','click here'))
        for slug,term in [('services','Wheelchair Transportation Services'),('book-today','Quote'),('lets-connect','Contact'),('faqs','FAQs')]:
            source=(PUBLIC/('non-emergency-medical-transportation-'+slug)/'index.html').read_text(encoding='utf-8')
            self.assertIn(term,re.search(r'<title>(.*?)</title>',source).group(1))
    def test_location_coverage_and_redirects(self):
        cfg=json.loads((ROOT/'firebase.json').read_text())['hosting']
        prefix='/non-emergency-medical-transportation-service-areas-covered/'
        for slug in ('houston','southwest-houston','southeast-houston','bellaire'):
            p=PUBLIC/(prefix+slug).strip('/')/'index.html'
            page=self.pages[p]
            self.assertEqual(sum(t=='article' for t,d in page.tags),6)
            for other in ('houston','southwest-houston','southeast-houston','bellaire'):self.assertIn(prefix+other+'/',page.refs)
        for slug in ('pearland','sugar-land'):
            self.assertFalse((PUBLIC/(prefix+slug).strip('/')/'index.html').exists())
            self.assertTrue(any(slug in r['source'] and r['type']==302 for r in cfg['redirects']))

    def test_houston_wide_scope_and_truthful_boundaries(self):
        combined=' '.join(' '.join(page.text) for page in self.pages.values())
        for old in ('focus on southwest Houston, southeast Houston and Bellaire', 'focused on southwest Houston', 'Our confirmed service is wheelchair transportation', 'Outside these areas?'):
            self.assertNotIn(old,combined)
        hub=' '.join(self.pages[PUBLIC/'non-emergency-medical-transportation-service-areas-covered/index.html'].text)
        self.assertIn('north, south, east, west and central Houston',hub)
        self.assertIn('one wheelchair-accessible van',hub)
        for slug in ('ambulatory-transportation-nemt','outpatient-transportation','texas-medical-center-transportation','facility-coordinators'):
            text=' '.join(self.pages[PUBLIC/'non-emergency-medical-transportation-services'/slug/'index.html'].text)
            self.assertRegex(text,r'responsible[ -]adult')
            self.assertIn('not automatically',text)
        outpatient=' '.join(self.pages[PUBLIC/'non-emergency-medical-transportation-services/outpatient-transportation/index.html'].text)
        self.assertIn('opening in 2027',outpatient)
        self.assertNotIn('24-hour service',combined)

    def test_new_topics_reachable_without_footer(self):
        home=(PUBLIC/'index.html').read_text(encoding='utf-8').split('<footer>')[0]
        for slug in ('texas-medical-center-transportation','rehabilitation-appointment-transportation','facility-coordinators'):
            self.assertIn('/non-emergency-medical-transportation-services/'+slug+'/',home)
        for p,parser in self.pages.items():
            canonical=[d['href'] for t,d in parser.tags if t=='link' and d.get('rel')=='canonical']
            expected='https://www.rideprimetime.net/'+(p.relative_to(PUBLIC).parent.as_posix().strip('.')+'/' if p.name=='index.html' else '404.html')
            self.assertEqual(canonical,[expected.replace('net//','net/')])

    def test_original_routes_preserved(self):
        original={'privacy-policy','sitemap','non-emergency-medical-transportation-lets-connect','non-emergency-medical-transportation-testimonials','non-emergency-medical-transportation-faqs','non-emergency-medical-transportation-services','non-emergency-medical-transportation-what-we-stand-for','non-emergency-medical-transportation-book-today','non-emergency-medical-transportation-set-an-appointment','non-emergency-medical-transportation-view-map-and-directions','non-emergency-medical-transportation-service-areas-covered'}
        original.update('non-emergency-medical-transportation-services/'+s for s in ('ambulatory-transportation-nemt','wheelchair-transportation','outpatient-transportation','hospital-transport-for-outpatient-services','dialysis-and-reoccuring-transportation','social-events-transportation'))
        original.update('non-emergency-medical-transportation-what-we-stand-for/'+s for s in ('get-to-know-the-owner','why-choose-us'))
        original.add('non-emergency-medical-transportation-lets-connect/unlock-20-percent-off-your-first-ride')
        original.add('non-emergency-medical-transportation-service-areas-covered/houston')
        for slug in original:self.assertTrue((PUBLIC/slug/'index.html').exists(),slug)
        self.assertTrue((PUBLIC/'index.html').exists())

    def test_district_guides_have_distinct_local_utility(self):
        prefix='non-emergency-medical-transportation-service-areas-covered'
        hub=self.pages[PUBLIC/prefix/'index.html']
        texts=[]
        for slug,fact in [('west-houston-memorial','Frostwood Drive'),('north-northwest-houston','Cypress Woods Medical Drive')]:
            page=self.pages[PUBLIC/prefix/slug/'index.html'];text=' '.join(page.text);texts.append(text)
            self.assertIn('/'+prefix+'/'+slug+'/',hub.refs)
            self.assertIn(fact,text)
            self.assertEqual(sum(t=='article' for t,d in page.tags),6)
            self.assertTrue(any(urlsplit(ref).netloc in ('memorialhermann.org','www.houstonmethodist.org') for ref in page.refs))
            self.assertRegex(text,r'(?i)one[- ](?:wheelchair-accessible )?van')
        self.assertNotIn('Frostwood Drive',texts[1])
        self.assertNotIn('Cypress Woods Medical Drive',texts[0])

if __name__=='__main__':unittest.main()
