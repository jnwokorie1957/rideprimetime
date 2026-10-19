# Ride Primetime static website

Original HTML/CSS/JavaScript rebuild for Firebase Hosting. No WordPress runtime, dependency installation or database is needed to build.

Build: `python build.py`

Test: `python -m unittest discover -s tests -v`

Local review: `python -m http.server 8080 --directory public`

Deploy after project selection and release review: `npx -y firebase-tools@latest deploy --only hosting --project YOUR_APPROVED_PROJECT_ID`

Only `public/` is deployed. No project alias is supplied so deployment cannot accidentally target PTHHS. Do not run Firebase initialization or deploy from the backup directory.

The site uses phone and email links, not a booking form. Contact details were verified against the published-page backup: 713-423-4430 and Info@RidePrimetime.net. Live verification was unavailable (fetch returned 401). A call/email is not a confirmed reservation. No messages were sent during testing.

All 24 historical sitemap routes remain accounted for: 22 retain pages, and two unconfirmed city routes temporarily redirect to the coverage hub. Three new confirmed-area pages bring the current sitemap to 25 routes. The location hub links Houston, southwest Houston, southeast Houston and Bellaire pages. Pearland and Sugar Land remain local drafts pending owner coverage confirmation. Other historical city mentions are listed in the private local draft inventory. The author archive redirects to About. No testimonials, credentials or guarantees were fabricated.

Release gates: verify target Firebase project; browser visual/keyboard review; verify service copy; publish to the verified public Ride repository through an authorized route. No billing, DNS or IAM changes are included.

The original backup was not malware-cleared (Defender reported Product/Feature disabled). No legacy scripts, PHP, CSS, JavaScript, fonts, video, database data or configuration were copied. The only reused image is the owner business logo, validated as a PNG. Public route names, contact details and service headings informed the rebuild.
