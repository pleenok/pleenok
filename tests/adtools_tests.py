from unittest import TestCase

from pleenok.conversion.adtool import attack_tree_to_adtool_term
from tests.utils import generate_at


class ADToolsTests(TestCase):
	def test_conversion_to_adtools_term(self):
		at = generate_at()
		adtools_term = attack_tree_to_adtool_term(at)
		original_string = "SAND(Exploit software,AND(OR(AND(Spoof MAC address,Find LAN port),AND(Break WPA keys,Find WLAN)),Get credentials),Run malicious script)"
		self.assertEqual(original_string, adtools_term)