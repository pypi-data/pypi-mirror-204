from typing import Any, Union
from atri_core import AtriComponent



class DivCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	

	def _to_json_fields(self):
		all_fields = {

			}
		return {k: v for k, v in all_fields.items() if v is not None}


class Div(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Div"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onClick = False
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
		self._custom = DivCustomClass(state)

	def _to_json_fields(self):
		all_fields = {
			"styles": self._styles,
			"custom": self._custom,
			}
		return {k: v for k, v in all_fields.items() if v is not None}