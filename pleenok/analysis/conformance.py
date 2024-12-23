from pleenok.model.attack_tree import Node
from pleenok.conversion.process_tree import attack_tree_to_process_tree_string
from pm4py.objects.process_tree.utils.generic import parse as parse_process_tree
import pandas as pd
import pm4py


def attack_successful(attack_tree: Node, attack_log: pd.DataFrame):
	process_tree = parse_process_tree(attack_tree_to_process_tree_string(attack_tree))
	pn, im, fm = pm4py.convert_to_petri_net(process_tree)
	return pm4py.conformance_diagnostics_alignments(attack_log, pn, im, fm)
