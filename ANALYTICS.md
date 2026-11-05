# Public website analytics — October 31, 2026

Owner-requested Google Analytics 4 uses property `561765914`, stream `16244067646` and measurement ID `G-T9M25PS348`. Every canonical public page loads deferred `/assets/analytics.js`. Google automatically measures public page views, sessions and engagement; enhanced scroll measurement and phone/email click intent are enabled. Advertising features, automatic forms/search/outbound links/video/downloads are disabled. Query strings, fragments, contact destinations, message contents and form values are not sent. Browser Do Not Track and Global Privacy Control visits are excluded. The privacy page describes this collection.

Both businesses' owner-only reports are available at `https://pthhs.net/primetime#analytics` using the existing administrator sign-in. The dashboard calls a separate authenticated backend using read-only Google Analytics access. Its source and deployment configuration live in the PTHHS repository. No reporting credentials or service-account keys are deployed to this public Ride site.

Google Search Console verified `https://www.rideprimetime.net/` through the permanent `public/google42b973e2d43e4ad9.html` file. Keep that file after future rebuilds. Google accepted the sitemap, discovered 34 pages and confirmed the homepage is indexed. New indexing remains Google's decision.

Released Firebase Hosting version: `e126206de3b7e982` on October 31, 2026. The production manifest was preserved. The existing live booking page received only the tag because Git main contains a separate pending booking-content change. Other canonical marketing pages matched production before editing. The source generator includes analytics for future builds, and public privacy copy was updated to match actual tracking. All 40 site tests and the menu checks pass; verification files are excluded from marketing-page semantic tests.
# Live daily totals — November 4, 2026

The shared owner dashboard now counts public page loads independently of GA4,
refreshing today's live card every5seconds and resetting at Chicago midnight.
The first partial day is labeled with its start time; GA4's processed-today
total remains separately labeled beneath it. Native Chrome visits changed
Ride's count from1to2 automatically after publication.

The page-view message is `{"v":1}` to the owner's
https://pthhs.net/api/public-page-view, omitting credentials and referrer.
Existing DNT/GPC and public-page guards apply. CSP permits this one owner
endpoint. No Google permission or service account change was needed.

## Live visitors — November 4, 2026

The primary visitor card now counts browser sessions active within 60 seconds
and updates every 5 seconds. Google's 30-minute users remain separately labeled.
Visible pages send 15-second heartbeats with temporary random session/document
tokens; these never add page views. A same-origin browser token avoids counting
multiple tabs twice and expires after 30 minutes of inactivity. The server
stores only hashes and temporary presence timestamps; activity expires after
60 seconds, with automatic TTL cleanup. No page address, contact/form contents,
or private operations activity is sent. The public notice and build.py describe
this behavior. Native Chrome testing showed 0 → 1 when visiting and 1 → 0 after
closing, without pressing dashboard Refresh. The backend implementation and
scoped retention policy are maintained in the PTHHS repository.
