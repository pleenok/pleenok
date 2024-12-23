from unittest import TestCase

from pleenok.conversion.process_tree import attack_tree_to_process_tree_string, process_tree_to_attack_tree
from pleenok.model.attack_tree import GateType, Gate
from pm4py.objects.process_tree.utils.generic import parse as parse_process_tree

from tests.utils import generate_at


class ProcessTreeTests(TestCase):

	def test_conversion_to_process_tree(self):
		at = generate_at()
		pt = attack_tree_to_process_tree_string(at)
		self.assertEqual(pt, "->('Exploit software',+(O(+('Spoof MAC address','Find LAN port'),+('Break WPA keys','Find WLAN')),'Get credentials'),'Run malicious script')")

	def test_to_process_tree_and_back(self):
		string = "->('Exploit software',+(O(+('Spoof MAC address','Find LAN port'),+('Break WPA keys','Find WLAN')),'Get credentials'),'Run malicious script')"
		pt = parse_process_tree(string)
		at2 = process_tree_to_attack_tree(pt)
		pt2 = attack_tree_to_process_tree_string(at2)
		self.assertEqual(string, pt2)