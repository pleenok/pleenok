import pm4py

from pleenok.analysis.conformance import attack_successful
from pleenok.model.attack_tree import Gate, GateType
from pleenok.conversion.graphviz import generate_dot
from pleenok.conversion.adtool import attack_tree_to_adtool_term
from pleenok.conversion.process_tree import attack_tree_to_process_tree_string, process_tree_to_attack_tree
from pleenok.conversion.risqflan import generate_risqflan
from pleenok.utils.log_utils import str_to_log

o1 = Gate(GateType.SEQUENCE_AND)
o1.add_attack("Exploit software")
o2 = o1.add_gate(GateType.AND, "Entered")
o1.add_attack("Run malicious script")
o3 = o2.add_gate(GateType.OR)
o2.add_attack("Get credentials")
o4 = o3.add_gate(GateType.AND)
o4.add_attack("Spoof MAC address")
o4.add_attack("Find LAN port")
o5 = o3.add_gate(GateType.AND)
o5.add_attack("Break WPA keys")
o5.add_attack("Find WLAN")

# Generate DOT
# print(generate_dot(o1))

# Generate ADTool term
print(attack_tree_to_adtool_term(o1))

# Convert to process tree string
# print(attack_tree_to_process_tree_string(o1))

# Convert from process tree to attack tree
# from pm4py.objects.process_tree.utils.generic import parse as parse_process_tree
# process_tree = parse_process_tree("->('Exploit software',+(O(+('Spoof MAC address','Find LAN port'),+('Break WPA keys','Find WLAN')),'Get credentials'),'Run malicious script')")
# print(generate_dot(process_tree_to_attack_tree(process_tree)))

# Convert to RisQFLan
# print(generate_risqflan(o1))


# Process mining operations
log = str_to_log(["KABEFG", "KEBAFG", "KECDFG", "KDCEFG"])
process_tree = pm4py.discover_process_tree_inductive(log)
at = process_tree_to_attack_tree(process_tree)
print(str(generate_dot(at)))

attack_log = str_to_log(["KECAFG"])
alignment = attack_successful(o1, attack_log)
print(alignment[0])