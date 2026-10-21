# Ride Primetime vehicle showcase release

Pending independent visual review and publication. The illustrated homepage hero precedes a section with the two approved vehicle photos. Explore Our Vehicle links from the shared desktop/mobile navigation to /our-vehicle/. Existing Houston content and routes remain intact.

This isolated release was reconstructed from verified photo tree fa903566be5dc5c5d7f77c90e861437ef3735db9. Remote main was checked as d5db466166e3bbf9f20409dbfb58031e3e4f59ea on October 21, 2026. The earlier photo commit creation remains uncertain; no duplicate of that commit was created. A future distinct showcase commit must use a freshly verified main parent.

The inquiry prototype remains in the original local workspace and Library preview, entirely outside this release. No inquiry.py, inquiry CSS/JS, online form, Maps integration or email backend is included. DNS remains on hold; deploy only to rideprimetime-b0793 after review. The regular domains still serve the older site.

Build: python build.py. Tests: python -m unittest discover -s tests -v; node tests/menu.test.cjs. Browser screenshots and real keyboard checks are separate release gates, not covered by these tests.

Rollback: retain published Hosting version 58c02f117f159a54 and photo tree above. No old resources are deleted.

---

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

All 24 historical sitemap routes remain accounted for: 22 retain pages, and Pearland and Sugar Land keep their existing temporary redirects to the coverage hub. Those surrounding cities are not silently included by the new Houston-wide instruction. Existing Houston, southwest Houston, southeast Houston and Bellaire routes remain intact. Three new topic pages cover the Texas Medical Center, rehabilitation appointments and facility coordinators, bringing the sitemap to 28 canonical routes. Two additional district guides for West Houston/Memorial and North/Northwest Houston bring the current total to 30. These are distinct planning resources, not neighborhood doorway pages. They reuse the existing page hero, numbered cards, location links, fonts, colors, spacing, navigation, buttons and responsive styles. The Medical Center guide retains its existing service URL instead of adding a duplicate location page. The author archive redirect remains unchanged.

`houston_content.py` contains original content and official destination references. Coverage is Houston-wide while route suitability, capacity, timing and prices require individual confirmation. The owner-reported single van remains disclosed. Ambulatory and day-surgery guidance does not imply that a driver meets a facility's responsible-adult discharge requirement. Kelsey Bay Area ASC is described as planned for 2027, not currently open. No affiliations, insurance promises, guaranteed pickups, medical supervision or 24-hour service are claimed.

Automated checks cover routes, canonicals, metadata, service/topic links, contact link formats, scope boundaries, focus contrast and mobile menu behavior. They do not substitute for browser visual/keyboard QA or actual call/email delivery. The supported browser inventory was empty during this local review. No tracking, forms, advertising campaigns, account changes or external communications were added.

Release gates: verify target Firebase project; browser visual/keyboard review; verify service copy; publish to the verified public Ride repository through an authorized route. No billing, DNS or IAM changes are included.

The original backup was not malware-cleared (Defender reported Product/Feature disabled). No legacy scripts, PHP, CSS, JavaScript, fonts, video, database data or configuration were copied. The only reused image is the owner business logo, validated as a PNG. Public route names, contact details and service headings informed the rebuild.
