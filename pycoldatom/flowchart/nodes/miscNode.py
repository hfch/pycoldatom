from pyqtgraph.flowchart import Node

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class DictSelectNode(Node):
	nodeName = 'Dict Select'
	nodePaths = [('Misc',)]

	def __init__(self, name):
		super().__init__(name, terminals={'data':{'io':'in'}, 'selected': {'io': 'out'}}, allowAddOutput=True)

		self.labelview = QListView()
		self.labelmodel = QStandardItemModel()
		self.labelview.setModel(self.labelmodel)
		self.labelview.clicked.connect(self.onLabelSelected)

		self.data = None
		self.label = None

	def ctrlWidget(self):
		return self.labelview

	def onLabelSelected(self, index):
		self.label = index.data()
		self.setOutput(selected=self.data[self.label])

	def setLabels(self, data):
		self.data = data
		self.labelmodel.clear()
		for label in self.data:
			if not label.startswith('_'):
				self.labelmodel.appendRow(QStandardItem(label))
		if self.label is not None and self.label in self.data:
			item = self.labelmodel.findItems(self.label)[0]
			index = self.labelmodel.indexFromItem(item)
			self.labelview.setCurrentIndex(index)
			self.onLabelSelected(index)

	def process(self, data, display=True):
		self.setLabels(data)
		result = {}
		
		for k in self.outputs().keys():
			if k == 'selected' and self.label in self.data:
				result[k] = self.data[self.label]
			elif k in self.data:
				result[k] = self.data[k]

		return result

	def saveState(self):
		state = super().saveState()
		state['selected'] = self.label
		return state

	def restoreState(self, state):
		super().restoreState(state)
		self.label = state['selected']

class DictCombineNode(Node):
	nodeName = 'Dict Combine'
	nodePaths = [('Misc',)]

	def __init__(self, name):
		super().__init__(name, terminals={'dic':{'io':'in'}, 'dic_new': {'io': 'out'}}, allowAddOutput=True)

	def process(self, dic, display=True, **kwargs):
		if dic is None:
			dic = {}

		kwargs = {k: v for k, v in kwargs.items() if v is not None}
		return {'dic_new': dic.copy().update(kwargs)}

nodelist = [DictSelectNode, DictCombineNode]