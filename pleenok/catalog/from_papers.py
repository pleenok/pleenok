from pleenok.model.attack_tree import AttackTree, Gate, GateType


def falco21_fig4() -> AttackTree:
	# From https://doi.org/10.1109/SMC-IT51442.2021.00016
	at = Gate(GateType.SEQUENCE_AND, "Tamper data received from CubeSAT")
	at1 = at.add_and_gate("Admin access to database server")
	at1.add_attack("Login to server via SSH")
	at11 = at1.add_or_gate("Steal credentials to database")
	at11.add_attack("Search for misconfiguration")
	at11.add_attack("Get priviledged access to server")
	at1.add_attack("Login to phpMyAdmin interface")
	at.add_attack("Change data logged in flight database")
	return AttackTree(at)
