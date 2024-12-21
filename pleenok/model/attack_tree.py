from typing import List, Union
from enum import Enum
import uuid


class GateType(Enum):
	AND = "AND"
	SEQUENCE_AND = "S-AND"
	OR = "OR"
	XOR = "XOR"


class Node:
	def __init__(self):
		self._id = uuid.uuid4()

	def get_id(self):
		return self._id.hex

	def __str__(self) -> str:
		return "node_" + self.get_id()


class Gate(Node):
	def __init__(self, gate_type: GateType):
		super().__init__()
		self.gate_type = gate_type
		self.children = []

	def add_child(self, child: Union['Gate', 'BasicEvent']):
		self.children.append(child)
		return self

	def add_gate(self, gate_type: GateType):
		g = Gate(gate_type)
		self.add_child(g)
		return g

	def add_attack(self, attack: str):
		be = BasicEvent(attack)
		self.add_child(be)
		return be

	def __str__(self) -> str:
		return "gate_" + self.get_id()


class BasicEvent(Node):
	def __init__(self, label: str):
		super().__init__()
		self.label = label

	def get_label(self) -> str:
		return self.label

	def __str__(self) -> str:
		return self.get_label()
