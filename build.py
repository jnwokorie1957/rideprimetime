"""Build the original static site. Uses only local, reviewed content in this file."""
from pathlib import Path
from html import escape
import json
from locations import LOCATIONS

ROOT=Path(__file__).resolve().parent
PUBLIC=ROOT/'public'
PREFIX='non-emergency-medical-transportation-'
PHONE='713-423-4430'
EMAIL='Info@RidePrimetime.net'
ORIGIN='https://www.rideprimetime.net'

# Editorial scope follows the owner's migration instructions. No legacy code or database input.
PAGES=[
('what-we-stand-for','A little more care for the journey.','ABOUT RIDE PRIMETIME','Ride Primetime offers private-pay wheelchair non-emergency transportation, with one wheelchair van and a focus on southwest Houston, southeast Houston and Bellaire.', [('A focused service','A single-van operation means every trip needs a conversation about timing, location and availability. Contact us before making plans around a pickup.'),('Your ride, clearly arranged','Discuss your pickup and destination, wheelchair requirements, any accompanying person and the return trip. Ask for a quote before confirming.')]),
('services','Transportation around your day.','OUR SERVICES','Private-pay wheelchair transportation for non-emergency trips. Tell us where you need to go and we will discuss whether the trip fits our service.', [('Medical appointments','Ask about transportation to scheduled, non-emergency appointments. Confirm timing and the return-trip plan.'),('Everyday destinations','Ask about family visits, social outings and other local destinations. Service depends on availability and trip suitability.'),('Plan before you book','We operate one wheelchair van. Equipment fit, assistance needs, locations and scheduling must be discussed before a reservation is confirmed.')]),
('book-today','Let’s plan your ride.','REQUEST AVAILABILITY','Call or email to discuss availability and a private-pay quote. A message is an inquiry; it is not a confirmed reservation.', [('Start with a call','Have your general pickup area, destination area and preferred date ready. Discuss wheelchair requirements directly with our team.'),('Confirm the details','Ask about the fare, pickup window, return journey, cancellation terms and any accompanying passenger before agreeing to the trip.'),('Keep sensitive details off email','Please do not email medical records, insurance numbers or detailed health information. Call to discuss the appropriate next step.')]),
('lets-connect','A real conversation comes first.','CONTACT US','Speak with Ride Primetime about private-pay wheelchair transportation in southwest Houston, southeast Houston and Bellaire.', [('Call Ride Primetime','Use the phone link below to open your device’s calling app. Availability and prices are confirmed directly.'),('Send an inquiry','The email link opens your email app. Please keep the message to a general inquiry and avoid health records or other sensitive information.')]),
('service-areas-covered','Close to the places that matter.','SERVICE AREA','Our focus is southwest Houston, southeast Houston and Bellaire. Contact us to confirm your pickup and destination are within our service area.', [('Southwest Houston','Ask about a trip within southwest Houston or between nearby destinations.'),('Southeast Houston','Discuss the location, appointment timing and return journey with us.'),('Bellaire','Call to check availability for wheelchair transportation to or from Bellaire.')]),
('faqs','A few things to know before you ride.','YOUR QUESTIONS',["Clear arrangements make planning easier. Call if your needs are not covered here."][0], [('Is this an emergency service?','No. For a medical emergency, call 911. Ride Primetime provides non-emergency transportation.'),('How do I pay?','This site offers private-pay transportation. Ask for a quote and payment arrangements directly. Do not assume insurance or Medicaid coverage.'),('Is a reservation confirmed when I email?','No. A reservation is confirmed only after the trip details, price and availability have been agreed directly.'),('Can I book a recurring trip?','Ask about your dates. We operate one wheelchair van, so recurring trips depend on scheduling and availability.'),('What if I need special assistance?','Discuss equipment fit, transfer needs, any accompanying person and assistance needs before booking. Do not assume medical supervision or specialized transport is included.')]),
('set-an-appointment','Talk through the timing.','APPOINTMENT TRANSPORT','Call to discuss transportation for a scheduled, non-emergency appointment. Allow time to confirm the pickup and return arrangements.', [('Before the appointment','Discuss the appointment time, travel area and mobility requirements.'),('After the appointment','Confirm a return-trip plan. If a facility requires an escort or responsible adult, arrange that separately and follow the facility’s instructions.')]),
('testimonials','Your experience matters.','FEEDBACK','We welcome feedback about your experience with Ride Primetime. Contact us directly to share it.', [('Share your feedback','Call or email a general comment. Please avoid sending health details or information about another passenger.'),('Help us improve','Tell us what worked well and what could make planning your next trip easier.')]),
('view-map-and-directions','Confirm your pickup area.','LOCATIONS','We focus on southwest Houston, southeast Houston and Bellaire. Call to confirm a specific trip; this website does not list a walk-in office.', [('Plan door to destination','Discuss your pickup and destination directly. Please avoid sending precise personal locations until you have confirmed how to share them.'),('Check the full journey','Include both the outward and return journey when asking about availability.')]),
('service-areas-covered/houston','Wheelchair transportation in Houston.','HOUSTON','Private-pay wheelchair transportation focused on southwest and southeast Houston, subject to availability.', [('Southwest and southeast Houston','Call with your general pickup and destination areas so we can check the route.'),('One van, planned trips','Confirm the trip before relying on a pickup time. We do not promise on-demand or emergency service.')]),
('service-areas-covered/pearland','Ask about a trip near Pearland.','AREA INQUIRIES','Our core focus is southwest Houston, southeast Houston and Bellaire. For a Pearland trip, call to check whether your route can be accommodated.', [('Confirm coverage first','Pearland trips are considered individually. Please confirm coverage and availability directly.'),('Share the general route','Discuss the date and general pickup and destination areas by phone.')]),
('service-areas-covered/sugar-land','Ask about a trip near Sugar Land.','AREA INQUIRIES','Our core focus is southwest Houston, southeast Houston and Bellaire. Call before planning a Sugar Land trip.', [('Availability is confirmed directly','Trips to or from Sugar Land need an individual availability check. Please call before making plans.'),('Plan the full journey','Discuss your dates, wheelchair requirements and return-trip needs.')]),
('what-we-stand-for/why-choose-us','A focused, personal approach.','WHY RIDE PRIMETIME','One wheelchair van. A clear service area. Direct conversations about the trip you need.', [('Clear expectations','Confirm the fare, route and timing before booking.'),('A practical conversation','Discuss your mobility needs and any accompanying passenger so trip suitability can be checked.')]),
('what-we-stand-for/get-to-know-the-owner','Get to know Ride Primetime.','OUR APPROACH','We keep the conversation personal and the service focused on private-pay wheelchair transportation.', [('Talk with us','Contact Ride Primetime to learn more about the service and how we plan trips.'),('Know what to expect','Ask about how we plan trips, the areas we cover and what to confirm before you travel.')]),
('lets-connect/unlock-20-percent-off-your-first-ride','Ask for a current quote.','PRICING INQUIRIES','Contact Ride Primetime for current private-pay pricing. Any discount or special offer must be confirmed directly before booking.', [('Confirm the fare','Ask for the price of your specific journey before booking.'),('No automatic discount','Any available offer must be confirmed directly. Please ask about current pricing when you call.')])
]
for slug,title,desc in [
('wheelchair-transportation','Wheelchair transportation','Private-pay wheelchair transportation for planned, non-emergency trips.'),
('ambulatory-transportation-nemt','Discuss your mobility needs','Our confirmed service is wheelchair transportation. Call to discuss whether your needs fit the service.'),
('dialysis-and-reoccuring-transportation','Planning recurring appointment trips','Ask about availability for recurring, non-emergency trips. Each schedule needs confirmation.'),
('hospital-transport-for-outpatient-services','Transportation for outpatient visits','Discuss non-emergency wheelchair transportation for a planned outpatient visit.'),
('outpatient-transportation','Plan your outpatient journey','Confirm transportation arrangements for a non-emergency outpatient appointment.'),
('social-events-transportation','Stay connected to your plans','Ask about private-pay wheelchair transportation for a family visit or social outing.')]:
    PAGES.append(('services/'+slug,title+'.','TRIP OPTIONS',desc,[('Check availability','We operate one wheelchair van, focused on southwest Houston, southeast Houston and Bellaire. Call before making a reservation.'),('Agree on the details','Discuss wheelchair fit, assistance needs, any accompanying passenger and the return journey. Facility escort or responsible-adult requirements must be arranged separately.')]))

OUTPATIENT_SECTIONS = {
    'services/hospital-transport-for-outpatient-services': [
        ('Confirm the hospital entrance', 'Ask the facility which entrance and department to use for the outpatient visit. Discuss the pickup point and wheelchair access with Ride Primetime before confirming the trip.'),
        ('Plan for check-in and release', 'Use the facility\'s requested arrival time when discussing the ride. Ask how to coordinate the return if the visit ends earlier or later than expected; a return pickup is subject to an agreed plan and availability.'),
        ('Arrange any required escort', 'Ask the hospital about responsible-adult or escort requirements, especially after a procedure. Arrange that person separately. Transportation does not replace facility discharge requirements or medical supervision.'),
    ],
    'services/outpatient-transportation': [
        ('Plan a clinic or therapy visit', 'For a scheduled non-emergency clinic, therapy or other outpatient appointment, discuss the destination area, appointment time and wheelchair requirements before booking.'),
        ('Discuss the full appointment schedule', 'Tell us whether the trip is a single visit or part of a series. One wheelchair van serves planned trips, so each date and return arrangement needs confirmation; recurring availability is not automatic.'),
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
    'what-we-stand-for': 'About Our Houston Wheelchair Transportation Service',
    'services': 'Private-Pay Wheelchair Transportation Services in Houston',
    'book-today': 'Request a Wheelchair Ride and Private-Pay Quote',
    'lets-connect': 'Contact Ride Primetime in Houston',
    'service-areas-covered': 'Wheelchair Transportation Areas: Houston and Bellaire',
    'faqs': 'Wheelchair Transportation and Booking FAQs',
    'set-an-appointment': 'Plan Non-Emergency Appointment Transportation',
    'testimonials': 'Share Your Ride Primetime Feedback',
    'view-map-and-directions': 'Confirm Your Houston or Bellaire Pickup Area',
    'what-we-stand-for/why-choose-us': 'Our Approach to Private-Pay Wheelchair Transportation',
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

def location_links():
    return '<nav class="location-links" aria-label="Related locations">'+''.join(f'<a href="{route("service-areas-covered/"+key)}">{escape(loc["name"])}</a>' for key,loc in LOCATIONS.items())+'</nav><p class="related-links"><a href="'+route('services/wheelchair-transportation')+'">Wheelchair service</a> · <a href="'+route('book-today')+'">Plan your trip</a> · <a href="'+route('faqs')+'">Booking questions</a></p>'
CONTACT=route('lets-connect'); BOOK=route('book-today')
def cta():return f'<div class="actions"><a class="button" href="tel:+17134234430">Call {PHONE} <span aria-hidden="true">↗</span></a><a class="button secondary" href="mailto:{EMAIL}">Email an inquiry</a></div><p class="fine">An inquiry is not a confirmed reservation. For a medical emergency, call 911.</p>'
def header():
    return f'''<a class="skip" href="#main">Skip to content</a><div class="utility"><div class="wrap">PRIVATE-PAY WHEELCHAIR TRANSPORTATION <a href="tel:+17134234430">{PHONE}</a></div></div><header><div class="wrap nav"><a class="brand" href="/" aria-label="Ride Primetime home"><img class="business-logo" src="/assets/ride-primetime-logo.png" width="399" height="206" alt="Primetime Medical Transportation"><span class="brand-accessible">Ride Primetime</span></a><button class="menu-toggle" aria-expanded="false" aria-controls="navigation">Menu <span aria-hidden="true">☰</span></button><nav id="navigation" aria-label="Main navigation"><a href="{route('services')}">Services</a><a href="{route('service-areas-covered')}">Service area</a><a href="{route('what-we-stand-for')}">About</a><a href="{route('faqs')}">FAQs</a><a class="nav-contact" href="{CONTACT}">Contact us ↗</a></nav></div></header>'''
def footer():return f'''<section class="contact-band"><div class="wrap"><div><p class="eyebrow">YOUR NEXT STEP</p><h2>Let’s talk about your trip.</h2><p>Check availability, discuss your needs and get a private-pay quote.</p></div>{cta()}</div></section><footer><div class="wrap footer-grid"><div><a class="footer-brand" href="/">RIDE <b>PRIMETIME</b></a><p>Private-pay wheelchair transportation.<br>Southwest Houston · Southeast Houston · Bellaire</p></div><div><h3>Get in touch</h3><a href="tel:+17134234430">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a></div><div><h3>Explore</h3><a href="{BOOK}">Plan a ride</a><a href="/privacy-policy/">Privacy</a><a href="/sitemap/">All pages</a></div></div><div class="wrap footer-bottom">© 2026 Ride Primetime. <span>Non-emergency trips. Availability confirmed directly.</span></div></footer><script src="/assets/site.js" defer></script>'''
def document(title,description,path,body):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | Ride Primetime</title><meta name="description" content="{escape(description,quote=True)}"><link rel="canonical" href="{ORIGIN}{path}"><meta name="theme-color" content="#0964ca"><meta property="og:title" content="{escape(title,quote=True)} | Ride Primetime"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:type" content="website"><meta property="og:url" content="{ORIGIN}{path}"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css"></head><body>{header()}<main id="main">{body}</main>{footer()}</body></html>'''
def write(path,html):
    p=PUBLIC/path.strip('/')/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(html,encoding='utf-8')
def cards(items):return '<div class="cards">'+''.join(f'<article class="card"><span class="card-number">{n:02}</span><h2>{escape(t)}</h2><p>{escape(s)}</p></article>' for n,(t,s) in enumerate(items,1))+'</div>'
hero=f'''<section class="hero wrap"><div class="hero-copy"><p class="eyebrow"><span class="dot"></span> HOUSTON, TEXAS</p><h1>Wheelchair rides.<br>Houston roots.<br><em>Personal care.</em></h1><p class="lead">Private-pay wheelchair transportation for the places—and people—that matter to you.</p>{cta()}<div class="hero-foot"><span aria-hidden="true">◎</span> Southwest Houston · Southeast Houston · Bellaire</div></div><div class="hero-art"><div class="art-label"><span class="dot"></span> A LITTLE MORE CARE FOR THE JOURNEY</div><img src="/assets/journey.svg" width="620" height="620" alt="Original illustration of a wheelchair-accessible van along a Houston neighborhood route"><div class="art-bottom"><b>One van. A personal approach.</b><span>Trips planned directly with you.</span></div></div></section><section class="value-strip"><div class="wrap"><span>PRIVATE-PAY</span><span>WHEELCHAIR TRANSPORTATION</span><span>LOCAL, PLANNED TRIPS</span></div></section><section class="section wrap"><div class="section-intro"><p class="eyebrow">WHERE LIFE TAKES YOU</p><h2>Make room for<br>what matters.</h2><p>From recurring appointments to time with family, start with a conversation about a wheelchair-accessible journey. Our private-pay service is planned directly with you.</p></div>{cards([('Appointments & care','Discuss a planned, non-emergency appointment and arrange the outward and return journey.'),('Family & everyday plans','Ask about trips to see family, attend a social occasion or reach a local destination.'),('A journey that fits','Share your wheelchair and assistance needs so suitability can be checked before booking.')])}<a class="text-link" href="{route('services')}">Explore trip options <span aria-hidden="true">→</span></a></section><section class="area-section"><div class="wrap area-grid"><div><p class="eyebrow">ROOTED IN HOUSTON</p><h2>Local focus.<br>Thoughtful planning.</h2><p>We operate one wheelchair van with a focus on southwest Houston, southeast Houston and Bellaire. Every route and reservation is confirmed directly.</p><a class="text-link" href="{route('service-areas-covered')}">Check your service area →</a></div><div class="area-list"><div><span>01</span><h3>Southwest Houston</h3></div><div><span>02</span><h3>Southeast Houston</h3></div><div><span>03</span><h3>Bellaire</h3></div><p>Outside these areas? Call to discuss your route.</p></div></div></section><section class="section wrap"><p class="eyebrow">SIMPLE STEPS</p><h2>Let’s get the details right.</h2>{cards([('Tell us about your trip','Call with the general pickup and destination areas, date and timing.'),('Discuss your needs','Confirm wheelchair fit, assistance needs, any companion and your return plans.'),('Agree before you go','Confirm availability, fare and arrangements directly. An inquiry is not a booking.')])}</section>'''
write('/',document('Private-pay wheelchair transportation in Houston','Private-pay wheelchair transportation focused on southwest Houston, southeast Houston and Bellaire. Call Ride Primetime to discuss your trip.','/',hero))
paths=['/']
for slug,title,kicker,desc,items in PAGES:
    path=route(slug);paths.append(path)
    body=f'<section class="page-hero wrap"><a class="breadcrumb" href="/">Home /</a><p class="eyebrow">{escape(kicker)}</p><h1>{escape(title)}</h1><p class="lead">{escape(desc)}</p></section><section class="section wrap page-content">{cards(items)}</section>'
    if slug == "services":
        body+=f'<section class="section wrap page-content"><h2>Explore trip options</h2>{service_cards()}</section>'
    if slug.startswith('service-areas-covered'):
        loc=LOCATIONS.get(slug.rsplit('/',1)[-1],{})
        source=loc.get('source')
        note=f'<p class="fine">Local geography: <a href="{source[1]}">{escape(source[0])}</a>. Geographic context does not establish a business affiliation or guaranteed availability.</p>' if source else ''
        body+=f'<section class="wrap section prose"><h2>Explore local trip planning</h2>{location_links()}{note}</section>'
    write(path,document(PAGE_TITLES.get(slug,title),desc,path,body))
privacy='<section class="page-hero wrap"><p class="eyebrow">PRIVACY</p><h1>A simpler website.<br>Less information to share.</h1><p class="lead">This website does not include an online booking form, advertising trackers or analytics scripts.</p></section><section class="section wrap prose"><h2>When you visit</h2><p>Hosting providers may process technical information such as IP addresses and request logs to deliver and protect the site. This site does not set application cookies or store information in your browser.</p><h2>When you contact us</h2><p>Calling or emailing uses your phone or email provider. Your communication is received by Ride Primetime to respond to your inquiry. Please do not email medical records, insurance numbers or detailed health information.</p><h2>Questions and requests</h2><p>Contact Ride Primetime using the phone or email links below to ask about information you have shared. This website does not collect payment details or confirm bookings.</p></section>'
write('/privacy-policy/',document('Privacy','How this static website handles visits and contact inquiries.','/privacy-policy/',privacy));paths.append('/privacy-policy/')
links=''.join(f'<li><a href="{route(s)}">{escape(t)}</a></li>' for s,t,*_ in PAGES)
write('/sitemap/',document('All pages','Browse Ride Primetime service and contact information.','/sitemap/',f'<section class="page-hero wrap"><p class="eyebrow">EXPLORE</p><h1>Find your next step.</h1></section><section class="section wrap prose"><ul class="site-map"><li><a href="/">Home</a></li>{links}<li><a href="/privacy-policy/">Privacy policy</a></li></ul></section>'));paths.append('/sitemap/')
(PUBLIC/'404.html').write_text(document('Page not found','Find your way back to Ride Primetime.','/404.html','<section class="page-hero wrap"><p class="eyebrow">404</p><h1>Let’s get you back<br>on the right route.</h1><p>This page could not be found.</p><a class="button" href="/">Return home</a></section>'),encoding='utf-8')
(PUBLIC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN}{p}</loc></url>' for p in paths)+'</urlset>',encoding='utf-8')
(PUBLIC/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n',encoding='utf-8')
print(json.dumps({'pages':len(paths),'output':str(PUBLIC),'legacy_code_files_used':0,'reused_business_logo':1}))
