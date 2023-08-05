from typing import Any, Union
from atri_core import AtriComponent



class BarChartCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.cartesianGrid: Union[Any, None] = state["cartesianGrid"] if state != None and "cartesianGrid" in state else None
		self.data: Union[Any, None] = state["data"] if state != None and "data" in state else None
		self.options: Union[Any, None] = state["options"] if state != None and "options" in state else None
		self.toolTip: Union[Any, None] = state["toolTip"] if state != None and "toolTip" in state else None
		self.legend: Union[Any, None] = state["legend"] if state != None and "legend" in state else None
		self.xAxis: Union[Any, None] = state["xAxis"] if state != None and "xAxis" in state else None
		self.yAxis: Union[Any, None] = state["yAxis"] if state != None and "yAxis" in state else None
		self.stacked: Union[Any, None] = state["stacked"] if state != None and "stacked" in state else None
		self.chartHeight: Union[Any, None] = state["chartHeight"] if state != None and "chartHeight" in state else None
		self.chartWidth: Union[Any, None] = state["chartWidth"] if state != None and "chartWidth" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def cartesianGrid(self):
		self._getter_access_tracker["cartesianGrid"] = {}
		return self._cartesianGrid
	@cartesianGrid.setter
	def cartesianGrid(self, state):
		self._setter_access_tracker["cartesianGrid"] = {}
		self._cartesianGrid = state
	@property
	def data(self):
		self._getter_access_tracker["data"] = {}
		return self._data
	@data.setter
	def data(self, state):
		self._setter_access_tracker["data"] = {}
		self._data = state
	@property
	def options(self):
		self._getter_access_tracker["options"] = {}
		return self._options
	@options.setter
	def options(self, state):
		self._setter_access_tracker["options"] = {}
		self._options = state
	@property
	def toolTip(self):
		self._getter_access_tracker["toolTip"] = {}
		return self._toolTip
	@toolTip.setter
	def toolTip(self, state):
		self._setter_access_tracker["toolTip"] = {}
		self._toolTip = state
	@property
	def legend(self):
		self._getter_access_tracker["legend"] = {}
		return self._legend
	@legend.setter
	def legend(self, state):
		self._setter_access_tracker["legend"] = {}
		self._legend = state
	@property
	def xAxis(self):
		self._getter_access_tracker["xAxis"] = {}
		return self._xAxis
	@xAxis.setter
	def xAxis(self, state):
		self._setter_access_tracker["xAxis"] = {}
		self._xAxis = state
	@property
	def yAxis(self):
		self._getter_access_tracker["yAxis"] = {}
		return self._yAxis
	@yAxis.setter
	def yAxis(self, state):
		self._setter_access_tracker["yAxis"] = {}
		self._yAxis = state
	@property
	def stacked(self):
		self._getter_access_tracker["stacked"] = {}
		return self._stacked
	@stacked.setter
	def stacked(self, state):
		self._setter_access_tracker["stacked"] = {}
		self._stacked = state
	@property
	def chartHeight(self):
		self._getter_access_tracker["chartHeight"] = {}
		return self._chartHeight
	@chartHeight.setter
	def chartHeight(self, state):
		self._setter_access_tracker["chartHeight"] = {}
		self._chartHeight = state
	@property
	def chartWidth(self):
		self._getter_access_tracker["chartWidth"] = {}
		return self._chartWidth
	@chartWidth.setter
	def chartWidth(self, state):
		self._setter_access_tracker["chartWidth"] = {}
		self._chartWidth = state

	def _to_json_fields(self):
		all_fields = {
			"cartesianGrid": self._cartesianGrid,
			"data": self._data,
			"options": self._options,
			"toolTip": self._toolTip,
			"legend": self._legend,
			"xAxis": self._xAxis,
			"yAxis": self._yAxis,
			"stacked": self._stacked,
			"chartHeight": self._chartHeight,
			"chartWidth": self._chartWidth
			}
		return {k: v for k, v in all_fields.items() if v is not None}


class BarChart(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "BarChart"
		self.nodePkg = "@atrilabs/react-component-manifests"
		
		self.custom = state["custom"] if state != None and "custom" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def custom(self):
		self._getter_access_tracker["custom"] = {}
		return self._custom
	@custom.setter
	def custom(self, state):
		self._setter_access_tracker["custom"] = {}
		self._custom = BarChartCustomClass(state)

	def _to_json_fields(self):
		all_fields = {
			"styles": self._styles,
			"custom": self._custom,
			}
		return {k: v for k, v in all_fields.items() if v is not None}