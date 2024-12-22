from graphviz import Source
from pleenok.model.attack_tree import Node, Gate, GateType


def generate_dot(root: Node) -> str:
	gates_definitions = []
	basic_events_definitions = []
	relationships = []
	sequence_relationships = []
	subgraphs = []
	visited = set()

	def traverse(node: Node, parent_id: str = None):
		nonlocal gates_definitions, basic_events_definitions, relationships, sequence_relationships, subgraph
		node_id = node.get_id()
		if node_id in visited:
			return  # Skip already visited nodes
		visited.add(node_id)

		if isinstance(node, Gate):
			gates_definitions.append(f"\tn{node_id} [label=\"{node.gate_type.value}\"];")
			if node.label is not None:
				# gates_definitions
				basic_events_definitions.append(f"\tn{node_id}_label [label=\"{node.label}\"];")
				relationships.append(f"\tn{node_id} -> n{node_id}_label;")
			subgraph = []
			for child in node.children:
				child_id = child.get_id()
				if isinstance(child, Gate) and child.label is not None:
					relationships.append(f"\tn{child_id}_label -> n{node_id};")
				else:
					relationships.append(f"\tn{child_id} -> n{node_id};")
				traverse(child, node_id)
			if node.gate_type == GateType.SEQUENCE_AND:
				for i in range(len(node.children) - 1):
					c1 = node.children[i]
					c2 = node.children[i + 1]
					c1_id = "n" + c1.get_id()
					c2_id = "n" + c2.get_id()
					if isinstance(c1, Gate) and c1.label is not None:
						c1_id = c1_id + "_label"
					if isinstance(c2, Gate) and c2.label is not None:
						c2_id = c2_id + "_label"
					sequence_relationships.append(f"{c1_id} -> {c2_id}")
					subgraphs.append([f"{c1_id} {c2_id} "])
		else:
			if node.label is None:
				basic_events_definitions.append(f"\tn{node_id} [label=<<i>No action</i>>,shape=\"plain\",color=\"#ffffff\",fillcolor=\"#ffffff\"];")
			else:
				basic_events_definitions.append(f"\tn{node_id} [label=\"{node.label}\"];")

	traverse(root)

	dot = """
digraph AttackTree {
	ranksep = 0.5
	outputorder = "edgesfirst"
	rankdir = "BT"
	ordering = in
	
	node [
		color = "#000000"
		fillcolor = "#666666"
		fontcolor ="#FFFFFF"
		shape = "box"
		style = "filled, rounded"
		fontname = "Consolas,monospace"
		fontsize = 10
	]
"""
	dot += "\n".join(gates_definitions) + "\n"
	dot += """
	node [
		color = "#DD0000"
		fillcolor = "#F0F0F0"
		fontcolor ="#000000"
		shape = "oval"
		style = "filled"
		fontname = "Calibri,Arial,sans-serif"
		fontsize = 14
	]
"""
	dot += "\n".join(basic_events_definitions) + "\n"
	dot += """
	edge[
		dir = "none"
	]
"""
	dot += "\n".join(relationships) + "\n"
	dot += """
	edge[
		style = "dashed"
		color = "#666666"
		arrowhead = "vee"
		arrowsize = 0.5
		dir = "forward"
	]
	"""
	dot += "\n\t".join(sequence_relationships) + "\n"
	for subgraph in subgraphs:
		dot += f"\n	{{rank=same; {' '.join(subgraph)} }}"
	dot += "\n}"
	return Source(dot)
