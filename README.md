# Ride Primetime static website

## Houston-wide update — October 20, 2026

The owner approved publication of the tested Houston-wide messaging and appointment-focused content. Hosting deployment requires a verified authorized Ride target. The preceding rollback baseline is `da2d2ffe253b2271ecc162dff692a6f819ac3da1`.

Original HTML/CSS/JavaScript rebuild for Firebase Hosting. No WordPress runtime, dependency installation or database is needed to build.

Build: `python build.py`

Test: `python -m unittest discover -s tests -v`

Local review: `python -m http.server 8080 --directory public`

Deploy after project selection and release review: `npx -y firebase-tools@latest deploy --only hosting --project YOUR_APPROVED_PROJECT_ID`

Only `public/` is deployed. No project alias is supplied so deployment cannot accidentally target PTHHS. Do not run Firebase initialization or deploy from the backup directory.

The site uses phone and email links, not a booking form. Contact details were verified against the published-page backup: 713-423-4430 and Info@RidePrimetime.net. Live verification was unavailable (fetch returned 401). A call/email is not a confirmed reservation. No messages were sent during testing.

All 24 historical sitemap routes remain accounted for: 22 retain pages, and Pearland and Sugar Land keep their existing temporary redirects to the coverage hub. Those surrounding cities are not silently included by the new Houston-wide instruction. Existing Houston, southwest Houston, southeast Houston and Bellaire routes remain intact. Three new topic pages cover the Texas Medical Center, rehabilitation appointments and facility coordinators, bringing the local sitemap to 28 canonical routes. These are distinct planning resources, not neighborhood doorway pages. The author archive redirect remains unchanged.

`houston_content.py` contains original content and official destination references. Coverage is Houston-wide while route suitability, capacity, timing and prices require individual confirmation. The owner-reported single van remains disclosed. Ambulatory and day-surgery guidance does not imply that a driver meets a facility's responsible-adult discharge requirement. Kelsey Bay Area ASC is described as planned for 2027, not currently open. No affiliations, insurance promises, guaranteed pickups, medical supervision or 24-hour service are claimed.

Automated checks cover routes, canonicals, metadata, service/topic links, contact link formats, scope boundaries, focus contrast and mobile menu behavior. They do not substitute for browser visual/keyboard QA or actual call/email delivery. The supported browser inventory was empty during this local review. No tracking, forms, advertising campaigns, account changes or external communications were added.

Release gates: verify target Firebase project; browser visual/keyboard review; verify service copy; publish to the verified public Ride repository through an authorized route. No billing, DNS or IAM changes are included.

The original backup was not malware-cleared (Defender reported Product/Feature disabled). No legacy scripts, PHP, CSS, JavaScript, fonts, video, database data or configuration were copied. The only reused image is the owner business logo, validated as a PNG. Public route names, contact details and service headings informed the rebuild.
