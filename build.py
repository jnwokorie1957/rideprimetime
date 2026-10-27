"""Build the original static site. Uses only local, reviewed content in this file."""
from pathlib import Path
from html import escape
import json
from locations import LOCATIONS
from vehicle import vehicle_section, vehicle_page
from articles import ARTICLES, render_articles, published_articles, reconcile_article_output
from houston_content import apply_content, TITLES, TOPICS, SOURCES

ROOT=Path(__file__).resolve().parent
PUBLIC=ROOT/'public'
PREFIX='non-emergency-medical-transportation-'
PHONE='713-423-4430'
EMAIL='Info@RidePrimetime.net'
ORIGIN='https://www.rideprimetime.net'

# Editorial scope follows the owner's migration instructions. No legacy code or database input.
PAGES=[
('what-we-stand-for','A little more care for the journey.','ABOUT RIDE PRIMETIME','Ride Primetime offers private-pay wheelchair and ambulatory transportation across Houston, with individually confirmed routes.', [('A focused service','Every trip starts with a conversation about timing, location and availability. Contact us before making plans around a pickup.'),('Your ride, clearly arranged','Discuss your pickup and destination, wheelchair requirements, any accompanying person and the return trip. Ask for a quote before confirming.')]),
('services','Transportation around your day.','OUR SERVICES','Private-pay wheelchair and ambulatory transportation across Houston for planned appointments and everyday trips. Explore Medical Center, day-surgery, dialysis and rehabilitation ride planning, then call to confirm your route.', [('Medical appointments','Ask about transportation to scheduled, non-emergency appointments. Confirm timing and the return-trip plan.'),('Everyday destinations','Ask about family visits, social outings and other local destinations. Service depends on availability and trip suitability.'),('Plan before you book','Equipment fit, assistance needs, locations and scheduling must be discussed before a reservation is confirmed.')]),
('book-today','Let’s plan your ride.','REQUEST AVAILABILITY','Call or email to discuss availability and a private-pay quote. A message is an inquiry; it is not a confirmed reservation.', [('Start with a call','Have your Houston pickup area, destination building, preferred date and required check-in time ready. Tell us whether you need wheelchair or ambulatory transportation, any mobility aid and any accompanying passenger. For recurring dialysis or rehabilitation, list the requested dates.'),('Confirm the details','Confirm the route, pickup window, fare and cancellation terms directly. Discuss who will call when you are ready for the return and how timing changes are handled. For outpatient surgery, arrange any facility-required responsible adult separately; a driver does not automatically meet that requirement.'),('Keep sensitive details off email','Please do not email medical records, insurance numbers or detailed health information. Call to discuss the appropriate next step.')]),
('lets-connect','A real conversation comes first.','CONTACT US','Speak with Ride Primetime about private-pay wheelchair and ambulatory transportation across Houston.', [('Call Ride Primetime','Use the phone link below to open your device’s calling app. Availability and prices are confirmed directly.'),('Send an inquiry','The email link opens your email app. Please keep the message to a general inquiry and avoid health records or other sensitive information.')]),
('service-areas-covered','Close to the places that matter.','SERVICE AREA','Our coverage extends across Houston. Contact us to confirm your pickup and destination are within our service area.', [('Southwest Houston','Ask about a trip within southwest Houston or between nearby destinations.'),('Southeast Houston','Discuss the location, appointment timing and return journey with us.'),('Bellaire','Call to check availability for wheelchair transportation to or from Bellaire.')]),
('faqs','A few things to know before you ride.','YOUR QUESTIONS',["Clear arrangements make planning easier. Call if your needs are not covered here."][0], [('Is this an emergency service?','No. For a medical emergency, call 911. Ride Primetime provides non-emergency transportation.'),('How do I pay?','This site offers private-pay transportation. Ask for a quote and payment arrangements directly. Do not assume insurance or Medicaid coverage.'),('Is a reservation confirmed when I email?','No. A reservation is confirmed only after the trip details, price and availability have been agreed directly.'),('Can I book a recurring trip?','Ask about your dates. Recurring trips depend on scheduling and availability.'),('What if I need special assistance?','Discuss equipment fit, transfer needs, any accompanying person and assistance needs before booking. Do not assume medical supervision or specialized transport is included.')]),
('set-an-appointment','Talk through the timing.','APPOINTMENT TRANSPORT','Call to discuss transportation for a scheduled, non-emergency appointment. Allow time to confirm the pickup and return arrangements.', [('Before the appointment','Discuss the appointment time, travel area and mobility requirements.'),('After the appointment','Confirm a return-trip plan. If a facility requires an escort or responsible adult, arrange that separately and follow the facility’s instructions.')]),
('testimonials','Your experience matters.','FEEDBACK','We welcome feedback about your experience with Ride Primetime. Contact us directly to share it.', [('Share your feedback','Call or email a general comment. Please avoid sending health details or information about another passenger.'),('Help us improve','Tell us what worked well and what could make planning your next trip easier.')]),
('view-map-and-directions','Confirm your pickup area.','LOCATIONS','We serve Houston citywide. Call to confirm a specific trip; this website does not list a walk-in office.', [('Plan door to destination','Discuss your pickup and destination directly. Please avoid sending precise personal locations until you have confirmed how to share them.'),('Check the full journey','Include both the outward and return journey when asking about availability.')]),
('service-areas-covered/houston','Wheelchair transportation in Houston.','HOUSTON','Private-pay wheelchair transportation focused on southwest and southeast Houston, subject to availability.', [('Southwest and southeast Houston','Call with your general pickup and destination areas so we can check the route.'),('Individually planned trips','Confirm the trip before relying on a pickup time. We do not promise on-demand or emergency service.')]),
('service-areas-covered/pearland','Ask about a trip near Pearland.','AREA INQUIRIES','Our core focus is southwest Houston, southeast Houston and Bellaire. For a Pearland trip, call to check whether your route can be accommodated.', [('Confirm coverage first','Pearland trips are considered individually. Please confirm coverage and availability directly.'),('Share the general route','Discuss the date and general pickup and destination areas by phone.')]),
('service-areas-covered/sugar-land','Ask about a trip near Sugar Land.','AREA INQUIRIES','Our core focus is southwest Houston, southeast Houston and Bellaire. Call before planning a Sugar Land trip.', [('Availability is confirmed directly','Trips to or from Sugar Land need an individual availability check. Please call before making plans.'),('Plan the full journey','Discuss your dates, wheelchair requirements and return-trip needs.')]),
('what-we-stand-for/why-choose-us','A focused, personal approach.','WHY RIDE PRIMETIME','Houston-wide coverage. Direct conversations about the trip you need.', [('Clear expectations','Confirm the fare, route and timing before booking.'),('A practical conversation','Discuss your mobility needs and any accompanying passenger so trip suitability can be checked.')]),
('what-we-stand-for/get-to-know-the-owner','Get to know Ride Primetime.','OUR APPROACH','We plan private-pay wheelchair and ambulatory transportation across Houston through direct conversations about each trip.', [('Talk with us','Contact Ride Primetime to learn more about the service and how we plan trips.'),('Know what to expect','Ask about how we plan trips, the areas we cover and what to confirm before you travel.')]),
('lets-connect/unlock-20-percent-off-your-first-ride','Ask for a current quote.','PRICING INQUIRIES','Contact Ride Primetime for current private-pay pricing. Any discount or special offer must be confirmed directly before booking.', [('Confirm the fare','Ask for the price of your specific journey before booking.'),('No automatic discount','Any available offer must be confirmed directly. Please ask about current pricing when you call.')])
]
for slug,title,desc in [
('wheelchair-transportation','Wheelchair transportation','Private-pay wheelchair transportation for planned, non-emergency trips.'),
('ambulatory-transportation-nemt','Discuss your mobility needs','Our confirmed service is wheelchair transportation. Call to discuss whether your needs fit the service.'),
('dialysis-and-reoccuring-transportation','Planning recurring appointment trips','Ask about availability for recurring, non-emergency trips. Each schedule needs confirmation.'),
('hospital-transport-for-outpatient-services','Transportation for outpatient visits','Discuss non-emergency wheelchair transportation for a planned outpatient visit.'),
('outpatient-transportation','Plan your outpatient journey','Confirm transportation arrangements for a non-emergency outpatient appointment.'),
('social-events-transportation','Stay connected to your plans','Ask about private-pay wheelchair transportation for a family visit or social outing.')]:
    PAGES.append(('services/'+slug,title+'.','TRIP OPTIONS',desc,[('Check availability','We serve Houston with planned wheelchair-accessible transportation. Every route and date is confirmed individually. Call before making a reservation.'),('Agree on the details','Discuss wheelchair fit, assistance needs, any accompanying passenger and the return journey. Facility escort or responsible-adult requirements must be arranged separately.')]))

OUTPATIENT_SECTIONS = {
    'services/hospital-transport-for-outpatient-services': [
        ('Confirm the hospital entrance', 'Ask the facility which entrance and department to use for the outpatient visit. Discuss the pickup point and wheelchair access with Ride Primetime before confirming the trip.'),
        ('Plan for check-in and release', 'Use the facility\'s requested arrival time when discussing the ride. Ask how to coordinate the return if the visit ends earlier or later than expected; a return pickup is subject to an agreed plan and availability.'),
        ('Arrange any required escort', 'Ask the hospital about responsible-adult or escort requirements, especially after a procedure. Arrange that person separately. Transportation does not replace facility discharge requirements or medical supervision.'),
    ],
    'services/outpatient-transportation': [
        ('Plan a clinic or therapy visit', 'For a scheduled non-emergency clinic, therapy or other outpatient appointment, discuss the destination area, appointment time and wheelchair requirements before booking.'),
        ('Discuss the full appointment schedule', 'Tell us whether the trip is a single visit or part of a series. Each date and return arrangement needs confirmation; recurring availability is not automatic.'),
        ('Check the return arrangements', 'Ask the clinic about the expected appointment length and any accompanying-person requirements. Confirm how the outward and return journeys will be arranged, and ask about the fare and cancellation terms.'),
    ],
}
PAGES=[(slug,title,kicker,desc,OUTPATIENT_SECTIONS.get(slug,items)) for slug,title,kicker,desc,items in PAGES]

def route(slug):return '/'+PREFIX+slug+'/'
PENDING_SLUGS={'service-areas-covered/pearland','service-areas-covered/sugar-land'}
PAGES=[p for p in PAGES if p[0] not in PENDING_SLUGS and p[0]!='service-areas-covered/houston']
for key,loc in LOCATIONS.items():
    PAGES.append(('service-areas-covered/'+key,loc['title'],loc['name'].upper(),loc['intro'],loc['sections']))
for slug in PENDING_SLUGS:
    old=PUBLIC/(PREFIX+slug)/'index.html'
    if old.is_file():
        assert old.resolve().is_relative_to(PUBLIC.resolve())
        draft=ROOT/'drafts'/(slug.split('/')[-1]+'.html');draft.parent.mkdir(exist_ok=True)
        draft.write_bytes(old.read_bytes());old.unlink()

PAGE_TITLES = {
    'what-we-stand-for': 'About Our Houston Wheelchair and Ambulatory Transportation',
    'services': 'Houston Wheelchair and Ambulatory Transportation Services',
    'book-today': 'Request a Houston Ride and Private-Pay Quote',
    'lets-connect': 'Contact Ride Primetime in Houston',
    'service-areas-covered': 'Wheelchair Transportation Areas: Houston and Bellaire',
    'faqs': 'Wheelchair and Ambulatory Transportation FAQs',
    'set-an-appointment': 'Plan Non-Emergency Appointment Transportation',
    'testimonials': 'Share Your Ride Primetime Feedback',
    'view-map-and-directions': 'Confirm Your Houston or Bellaire Pickup Area',
    'what-we-stand-for/why-choose-us': 'Our Approach to Private-Pay Houston Transportation',
    'what-we-stand-for/get-to-know-the-owner': 'Get to Know Ride Primetime',
    'lets-connect/unlock-20-percent-off-your-first-ride': 'Ask About Current Private-Pay Ride Pricing',
    'services/wheelchair-transportation': 'Private-Pay Wheelchair Transportation in Houston',
    'services/ambulatory-transportation-nemt': 'Discuss Mobility Needs and Trip Suitability',
    'services/dialysis-and-reoccuring-transportation': 'Plan Dialysis and Recurring Appointment Rides',
    'services/hospital-transport-for-outpatient-services': 'Wheelchair Transportation for Hospital Outpatient Visits',
    'services/outpatient-transportation': 'Plan a Non-Emergency Outpatient Journey',
    'services/social-events-transportation': 'Wheelchair Transportation for Social and Family Visits',
}

def service_cards():
    items=[p for p in PAGES if p[0].startswith('services/')]
    return '<div class="cards">'+''.join(
        f'<article class="card"><span class="card-number">{n:02}</span><h2><a class="service-link" href="{route(slug)}">{escape(PAGE_TITLES[slug])}</a></h2><p>{escape(desc)}</p></article>'
        for n,(slug,title,kicker,desc,sections) in enumerate(items,1))+'</div>'

PAGES=apply_content(PAGES)
PAGE_TITLES.update(TITLES)

def topic_links():
    return '<div class="location-links">'+''.join(f'<a href="{route(slug)}">{escape(label)}</a>' for slug,label in TOPICS)+'</div>'

def location_links():
    return '<nav class="location-links" aria-label="Related locations">'+''.join(f'<a href="{route("service-areas-covered/"+key)}">{escape(loc["name"])}</a>' for key,loc in LOCATIONS.items())+'</nav><p class="related-links"><a href="'+route('services/wheelchair-transportation')+'">Wheelchair service</a> · <a href="'+route('book-today')+'">Plan your trip</a> · <a href="'+route('faqs')+'">Booking questions</a></p>'
CONTACT=route('lets-connect'); BOOK=route('book-today')
def cta():return f'<div class="actions"><a class="button" href="tel:+17134234430">Call {PHONE} <span aria-hidden="true">↗</span></a><a class="button secondary" href="mailto:{EMAIL}">Email an inquiry</a></div><p class="fine">An inquiry is not a confirmed reservation. For a medical emergency, call 911.</p>'
def header():
    return f'''<a class="skip" href="#main">Skip to content</a><div class="utility"><div class="wrap">PRIVATE-PAY HOUSTON TRANSPORTATION <a href="tel:+17134234430">{PHONE}</a></div></div><header><div class="wrap nav"><a class="brand" href="/" aria-label="Ride Primetime home"><img class="business-logo" src="/assets/ride-primetime-logo.png" width="399" height="206" alt="Primetime Medical Transportation"><span class="brand-accessible">Ride Primetime</span></a><button class="menu-toggle" aria-expanded="false" aria-controls="navigation">Menu <span aria-hidden="true">☰</span></button><nav id="navigation" aria-label="Main navigation"><a href="{route('services')}">Services</a><a href="{route('service-areas-covered')}">Service area</a><a href="/our-vehicle/">Explore our vehicles</a>{article_link()}<a href="{route('what-we-stand-for')}">About</a><a href="{route('faqs')}">FAQs</a><a class="nav-contact" href="{CONTACT}">Contact us ↗</a></nav></div></header>'''
def article_link():return '<a href="/articles/">Articles</a>' if published_articles(ARTICLES) else ''

def footer():return f'''<section class="contact-band"><div class="wrap"><div><p class="eyebrow">YOUR NEXT STEP</p><h2>Let’s talk about your trip.</h2><p>Check availability, discuss your needs and get a private-pay quote.</p></div>{cta()}</div></section><footer><div class="wrap footer-grid"><div><a class="footer-brand" href="/">RIDE <b>PRIMETIME</b></a><p>Private-pay wheelchair and ambulatory transportation.<br>Houston-wide coverage · Trips confirmed individually</p></div><div><h3>Get in touch</h3><a href="tel:+17134234430">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a></div><div><h3>Explore</h3>{article_link()}<a href="{BOOK}">Plan a ride</a><a href="/privacy-policy/">Privacy</a><a href="/sitemap/">All pages</a></div></div><div class="wrap footer-bottom">© 2026 Ride Primetime. <span>Non-emergency trips. Availability confirmed directly.</span></div></footer><script src="/assets/site.js" defer></script>'''
def document(title,description,path,body):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | Ride Primetime</title><meta name="description" content="{escape(description,quote=True)}"><link rel="canonical" href="{ORIGIN}{path}"><meta name="theme-color" content="#0964ca"><meta property="og:title" content="{escape(title,quote=True)} | Ride Primetime"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:type" content="website"><meta property="og:url" content="{ORIGIN}{path}"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css"></head><body>{header()}<main id="main">{body}</main>{footer()}</body></html>'''
def write(path,html):
    p=PUBLIC/path.strip('/')/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(html,encoding='utf-8')
def cards(items):return '<div class="cards">'+''.join(f'<article class="card"><span class="card-number">{n:02}</span><h2>{escape(t)}</h2><p>{escape(s)}</p></article>' for n,(t,s) in enumerate(items,1))+'</div>'
hero=f'''<section class="hero wrap"><div class="hero-copy"><p class="eyebrow"><span class="dot"></span> HOUSTON, TEXAS</p><h1>Wheelchair &amp;<br>ambulatory rides.<br><em>Across Houston.</em></h1><div class="hero-service-choices" role="group" aria-label="Explore transportation services"><a class="hero-service-choice" href="{route('services/ambulatory-transportation-nemt')}"><strong>Ambulatory<br>Transportation</strong><span class="choice-action">View service &#8599;</span></a><a class="hero-service-choice" href="{route('services/wheelchair-transportation')}"><strong>Wheelchair<br>Transportation</strong><span class="choice-action">View service &#8599;</span></a></div><p class="lead">Private-pay wheelchair and ambulatory transportation for planned Texas Medical Center visits, outpatient surgery pickups and recurring dialysis appointments across Houston.</p><p>Ambulatory transportation is for riders who travel seated in a passenger seat, including those who use mobility aids. Wheelchair transportation is for riders traveling in their wheelchair. Discuss transfers, boarding and suitability with us.</p><p class="fine">Discuss boarding needs, wheelchair fit and any mobility aids before booking. For surgery pickups, confirm the facility's responsible-adult requirements separately. Every trip needs staff confirmation.</p><div class="actions"><a class="button" href="{route('book-today')}">Request a ride quote</a><a class="button secondary" href="tel:+17134234430">Call 713-423-4430</a></div><div class="hero-foot"><span aria-hidden="true">◎</span> Houston-wide coverage · Trips confirmed individually</div></div><div class="hero-art"><img src="/assets/journey.svg" width="620" height="620" fetchpriority="high" decoding="async" alt="Illustration of a wheelchair-accessible van along a Houston neighborhood route"><div class="art-label">HOUSTON, TEXAS</div><div class="art-bottom"><b>A personal approach to every trip.</b><span>Trips planned directly with you.</span></div></div></section><section class="value-strip"><div class="wrap"><span>PRIVATE-PAY</span><span>WHEELCHAIR &amp; AMBULATORY</span><span>LOCAL, PLANNED TRIPS</span></div></section>{vehicle_section()}<section class="section wrap"><div class="section-intro"><p class="eyebrow">WHERE LIFE TAKES YOU</p><h2>Make room for<br>what matters.</h2><p>From recurring appointments to time with family, start with a conversation about wheelchair or ambulatory transportation. Our private-pay service is planned directly with you.</p></div>{cards([('Appointments & care','Discuss a planned, non-emergency appointment and arrange the outward and return journey.'),('Family & everyday plans','Ask about trips to see family, attend a social occasion or reach a local destination.'),('A journey that fits','Share your wheelchair and assistance needs so suitability can be checked before booking.')])}<a class="text-link" href="{route('services')}">Explore trip options <span aria-hidden="true">→</span></a></section><section class="area-section"><div class="wrap area-grid"><div><p class="eyebrow">ROOTED IN HOUSTON</p><h2>Across Houston.<br>Planned with you.</h2><p>We serve north, south, east, west and central Houston with planned wheelchair and ambulatory transportation. Coverage is citywide; route suitability, timing and capacity are confirmed for each reservation.</p><a class="text-link" href="{route('service-areas-covered')}">Check your service area →</a></div><div class="area-list"><div><span>01</span><h3>Texas Medical Center visits</h3></div><div><span>02</span><h3>Outpatient and day surgery</h3></div><div><span>03</span><h3>Dialysis and rehabilitation</h3></div><p>Tell us your Houston pickup area, destination and arrival time.</p></div></div></section><section class="section wrap"><p class="eyebrow">SIMPLE STEPS</p><h2>Let’s get the details right.</h2>{cards([('Request a ride quote','Share your pickup and destination, date, required arrival time and return needs. Mention mobility aids, boarding needs and any companion.'),('Confirm the details','Discuss availability, trip suitability, assistance needs and the private-pay price. If the return time is uncertain, ask how to arrange it.'),('Receive booking confirmation','Agree on the trip arrangements with our staff before you travel. A request or quote alone is not a confirmed reservation.')])}</section>'''
hero+=f'<section class="section wrap"><p class="eyebrow">PLAN AROUND YOUR VISIT</p><h2>Find the right ride information.</h2>{topic_links()}</section>'
write('/',document('Houston Wheelchair and Ambulatory Transportation','Private-pay wheelchair and ambulatory transportation across Houston. Plan Texas Medical Center, outpatient, dialysis and rehabilitation transportation with Ride Primetime.','/',hero))
write('/our-vehicle/',document('Explore our vehicles in Houston','Explore Ride Primetime vehicle photos: exterior, passenger seating, interior and rear ramp. Confirm boarding needs and trip suitability before booking.','/our-vehicle/',vehicle_page()))
paths=['/','/our-vehicle/']
for slug,title,kicker,desc,items in PAGES:
    path=route(slug);paths.append(path)
    body=f'<section class="page-hero wrap"><a class="breadcrumb" href="/">Home /</a><p class="eyebrow">{escape(kicker)}</p><h1>{escape(title)}</h1><p class="lead">{escape(desc)}</p></section><section class="section wrap page-content">{cards(items)}</section>'
    if slug == "services/wheelchair-transportation":
        body += '<section class="section wrap page-content"><div class="area-grid"><div class="hero-art vehicle-photo"><img src="/assets/ride-primetime-ramp.jpg" width="1024" height="683" loading="lazy" decoding="async" alt="Rear of the Ride Primetime van with its access ramp extended and a wheelchair beside it"></div><div><p class="eyebrow">OUR WHEELCHAIR-ACCESSIBLE VAN</p><h2>Plan a ride that fits.</h2><p>Discuss your wheelchair dimensions, boarding needs and any accompanying passenger before booking. Equipment fit and the assistance needed for your trip are confirmed directly.</p></div></div></section>'
    if slug == "services":
        body+=f'<section class="section wrap page-content"><h2>Explore trip options</h2>{service_cards()}</section>'
    if slug.startswith('service-areas-covered'):
        loc=LOCATIONS.get(slug.rsplit('/',1)[-1],{})
        source=loc.get('source')
        note=f'<p class="fine">Local reference: <a href="{source[1]}">{escape(source[0])}</a>. Geographic context does not establish a business affiliation or guaranteed availability.</p>' if source else ''
        body+=f'<section class="wrap section prose"><h2>Explore local trip planning</h2>{location_links()}{note}</section>'
    if slug.startswith('services') or slug == 'service-areas-covered':
        body+=f'<section class="section wrap prose"><h2>Plan your next step</h2>{topic_links()}<p><a href="{BOOK}">Request availability and a private-pay quote</a></p></section>'
    if slug in SOURCES:
        refs=''.join(f'<li><a href="{url}">{escape(label)}</a></li>' for label,url in SOURCES[slug])
        body+=f'<section class="wrap prose section"><h2>Official destination information</h2><ul>{refs}</ul><p class="fine">Checked October 20, 2026. Confirm current instructions with the facility. These links do not imply affiliation or guaranteed transportation availability.</p></section>'
    write(path,document(PAGE_TITLES.get(slug,title),desc,path,body))
privacy='<section class="page-hero wrap"><p class="eyebrow">PRIVACY</p><h1>A simpler website.<br>Less information to share.</h1><p class="lead">This website does not include an online booking form, advertising trackers or analytics scripts.</p></section><section class="section wrap prose"><h2>When you visit</h2><p>Hosting providers may process technical information such as IP addresses and request logs to deliver and protect the site. This site does not set application cookies or store information in your browser.</p><h2>When you contact us</h2><p>Calling or emailing uses your phone or email provider. Your communication is received by Ride Primetime to respond to your inquiry. Please do not email medical records, insurance numbers or detailed health information.</p><h2>Questions and requests</h2><p>Contact Ride Primetime using the phone or email links below to ask about information you have shared. This website does not collect payment details or confirm bookings.</p></section>'
write('/privacy-policy/',document('Privacy','How this static website handles visits and contact inquiries.','/privacy-policy/',privacy));paths.append('/privacy-policy/')
article_paths=render_articles(ARTICLES,document,write)
reconcile_article_output(PUBLIC,article_paths)
paths.extend(article_paths)
article_sitemap_link='<li><a href="/articles/">Articles</a></li>' if published_articles(ARTICLES) else ''
links=''.join(f'<li><a href="{route(s)}">{escape(PAGE_TITLES.get(s,t))}</a></li>' for s,t,*_ in PAGES)
write('/sitemap/',document('All pages','Browse Ride Primetime service and contact information.','/sitemap/',f'<section class="page-hero wrap"><p class="eyebrow">EXPLORE</p><h1>Find your next step.</h1></section><section class="section wrap prose"><ul class="site-map"><li><a href="/">Home</a></li><li><a href="/our-vehicle/">Explore our vehicles</a></li>{links}{article_sitemap_link}<li><a href="/privacy-policy/">Privacy policy</a></li></ul></section>'));paths.append('/sitemap/')
(PUBLIC/'404.html').write_text(document('Page not found','Find your way back to Ride Primetime.','/404.html','<section class="page-hero wrap"><p class="eyebrow">404</p><h1>Let’s get you back<br>on the right route.</h1><p>This page could not be found.</p><a class="button" href="/">Return home</a></section>'),encoding='utf-8')
(PUBLIC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN}{p}</loc></url>' for p in paths)+'</urlset>',encoding='utf-8')
(PUBLIC/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n',encoding='utf-8')
print(json.dumps({'pages':len(paths),'output':str(PUBLIC),'legacy_code_files_used':0,'reused_business_logo':1}))
