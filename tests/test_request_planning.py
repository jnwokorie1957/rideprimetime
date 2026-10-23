import unittest
from pathlib import Path
class RequestPlanningTests(unittest.TestCase):
    def test_call_checklist_covers_both_services_and_return_safeguards(self):
        root=Path(__file__).resolve().parents[1]
        s=(root/'public/non-emergency-medical-transportation-book-today/index.html').read_text(encoding='utf-8')
        for text in ('wheelchair or ambulatory transportation','required check-in time','recurring dialysis or rehabilitation','list the requested dates','responsible adult separately','does not automatically meet','not a confirmed reservation','Please do not email medical records'):
            self.assertIn(text,s)
        self.assertEqual(s.count('<article class="card">'),3)
        self.assertNotIn('<form',s)
        self.assertIn('tel:+17134234430',s)
        self.assertIn('mailto:Info@RidePrimetime.net',s)
