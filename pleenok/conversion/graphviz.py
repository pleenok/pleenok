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
			gates_definitions.append(f"	n{node_id} [label=\"{node.gate_type.value}\"];")
			subgraph = []
			for child in node.children:
				child_id = child.get_id()
				relationships.append(f"  n{child_id} -> n{node_id};")
				traverse(child, node_id)
			if node.gate_type == GateType.SEQUENCE_AND:
				sequence_relationships.extend(
					[f"n{node.children[i].get_id()} -> n{node.children[i + 1].get_id()}" for i in
					 range(len(node.children) - 1)])
				subgraphs.append([f"n{child.get_id()}" for child in node.children])
		else:
			if node.label == None:
				basic_events_definitions.append(f"	n{node_id} [label=<<i>No action</i>>,shape=\"plain\",color=\"#ffffff\",fillcolor=\"#ffffff\"];")
			else:
				basic_events_definitions.append(f"	n{node_id} [label=\"{node.label}\"];")

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
	dot += "\n".join(sequence_relationships) + "\n"
	for subgraph in subgraphs:
		dot += f"	{{rank=same; {' '.join(subgraph)};}}\n"
	dot += "\n}"
	return Source(dot)
