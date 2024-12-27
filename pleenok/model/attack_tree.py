from typing import List, Union
from enum import Enum
import uuid


class GateType(Enum):
	AND = "AND"
	SEQUENCE_AND = "S-AND"
	OR = "OR"
	XOR = "XOR"


class Node:
	def __init__(self, label: str):
		self._id = uuid.uuid4()
		self.label = label

	def get_label(self) -> str:
		return self.label

	def get_id(self):
		return self._id.hex

	def __str__(self) -> str:
		if self.label is None:
			return "gate_" + self.get_id()
		else:
			return self.label


class Gate(Node):
	def __init__(self, gate_type: GateType, label: str = None):
		super().__init__(label)
		self.gate_type = gate_type
		self.children = []

	def add_child(self, child: Union['Gate', 'Node']):
		self.children.append(child)
		return self

	def add_gate(self, gate_type: GateType, label: str = None):
		g = Gate(gate_type, label)
		self.add_child(g)
		return g

	def add_attack(self, attack: str):
		be = Node(attack)
		self.add_child(be)
		return be

	def add_and_gate(self, label: str = None):
		return self.add_gate(GateType.AND, label)

	def add_sequence_and_gate(self, label: str = None):
		return self.add_gate(GateType.SEQUENCE_AND, label)

	def add_or_gate(self, label: str = None):
		return self.add_gate(GateType.OR, label)

	def __str__(self) -> str:
		return "gate_" + self.get_id()
