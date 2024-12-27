from pleenok.model.attack_tree import Gate, GateType, AttackTree


def generate_at():
	at = Gate(GateType.SEQUENCE_AND)
	at.add_attack("Exploit software")
	o2 = at.add_gate(GateType.AND, "Entered")
	at.add_attack("Run malicious script")
	o3 = o2.add_gate(GateType.OR)
	o2.add_attack("Get credentials")
	o4 = o3.add_gate(GateType.AND)
	o4.add_attack("Spoof MAC address")
	o4.add_attack("Find LAN port")
	o5 = o3.add_gate(GateType.AND)
	o5.add_attack("Break WPA keys")
	o5.add_attack("Find WLAN")
	return AttackTree(at, "test")