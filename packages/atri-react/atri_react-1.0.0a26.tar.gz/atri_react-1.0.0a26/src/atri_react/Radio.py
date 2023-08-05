from typing import Any, Union
from atri_core import AtriComponent



class RadioCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.defaultValue: Union[Any, None] = state["defaultValue"] if state != None and "defaultValue" in state else None
		self.disabled: Union[Any, None] = state["disabled"] if state != None and "disabled" in state else None
		self.name: Union[Any, None] = state["name"] if state != None and "name" in state else None
		self.value: Union[Any, None] = state["value"] if state != None and "value" in state else None
		self.optionType: Union[Any, None] = state["optionType"] if state != None and "optionType" in state else None
		self.buttonStyle: Union[Any, None] = state["buttonStyle"] if state != None and "buttonStyle" in state else None
		self.size: Union[Any, None] = state["size"] if state != None and "size" in state else None
		self.options: Union[Any, None] = state["options"] if state != None and "options" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def defaultValue(self):
		self._getter_access_tracker["defaultValue"] = {}
		return self._defaultValue
	@defaultValue.setter
	def defaultValue(self, state):
		self._setter_access_tracker["defaultValue"] = {}
		self._defaultValue = state
	@property
	def disabled(self):
		self._getter_access_tracker["disabled"] = {}
		return self._disabled
	@disabled.setter
	def disabled(self, state):
		self._setter_access_tracker["disabled"] = {}
		self._disabled = state
	@property
	def name(self):
		self._getter_access_tracker["name"] = {}
		return self._name
	@name.setter
	def name(self, state):
		self._setter_access_tracker["name"] = {}
		self._name = state
	@property
	def value(self):
		self._getter_access_tracker["value"] = {}
		return self._value
	@value.setter
	def value(self, state):
		self._setter_access_tracker["value"] = {}
		self._value = state
	@property
	def optionType(self):
		self._getter_access_tracker["optionType"] = {}
		return self._optionType
	@optionType.setter
	def optionType(self, state):
		self._setter_access_tracker["optionType"] = {}
		self._optionType = state
	@property
	def buttonStyle(self):
		self._getter_access_tracker["buttonStyle"] = {}
		return self._buttonStyle
	@buttonStyle.setter
	def buttonStyle(self, state):
		self._setter_access_tracker["buttonStyle"] = {}
		self._buttonStyle = state
	@property
	def size(self):
		self._getter_access_tracker["size"] = {}
		return self._size
	@size.setter
	def size(self, state):
		self._setter_access_tracker["size"] = {}
		self._size = state
	@property
	def options(self):
		self._getter_access_tracker["options"] = {}
		return self._options
	@options.setter
	def options(self, state):
		self._setter_access_tracker["options"] = {}
		self._options = state

	def _to_json_fields(self):
		all_fields = {
			"defaultValue": self._defaultValue,
			"disabled": self._disabled,
			"name": self._name,
			"value": self._value,
			"optionType": self._optionType,
			"buttonStyle": self._buttonStyle,
			"size": self._size,
			"options": self._options
			}
		return {k: v for k, v in all_fields.items() if v is not None}


class Radio(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Radio"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onChange = False
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
		self._custom = RadioCustomClass(state)

	def _to_json_fields(self):
		all_fields = {
			"styles": self._styles,
			"custom": self._custom,
			}
		return {k: v for k, v in all_fields.items() if v is not None}