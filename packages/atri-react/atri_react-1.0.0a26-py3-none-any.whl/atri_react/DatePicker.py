from typing import Any, Union
from atri_core import AtriComponent



class DatePickerCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.picker: Union[Any, None] = state["picker"] if state != None and "picker" in state else None
		self.showTime: Union[Any, None] = state["showTime"] if state != None and "showTime" in state else None
		self.size: Union[Any, None] = state["size"] if state != None and "size" in state else None
		self.placement: Union[Any, None] = state["placement"] if state != None and "placement" in state else None
		self.format: Union[Any, None] = state["format"] if state != None and "format" in state else None
		self.placeholder: Union[Any, None] = state["placeholder"] if state != None and "placeholder" in state else None
		self.bordered: Union[Any, None] = state["bordered"] if state != None and "bordered" in state else None
		self.disabled: Union[Any, None] = state["disabled"] if state != None and "disabled" in state else None
		self.status: Union[Any, None] = state["status"] if state != None and "status" in state else None
		self.range: Union[Any, None] = state["range"] if state != None and "range" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def picker(self):
		self._getter_access_tracker["picker"] = {}
		return self._picker
	@picker.setter
	def picker(self, state):
		self._setter_access_tracker["picker"] = {}
		self._picker = state
	@property
	def showTime(self):
		self._getter_access_tracker["showTime"] = {}
		return self._showTime
	@showTime.setter
	def showTime(self, state):
		self._setter_access_tracker["showTime"] = {}
		self._showTime = state
	@property
	def size(self):
		self._getter_access_tracker["size"] = {}
		return self._size
	@size.setter
	def size(self, state):
		self._setter_access_tracker["size"] = {}
		self._size = state
	@property
	def placement(self):
		self._getter_access_tracker["placement"] = {}
		return self._placement
	@placement.setter
	def placement(self, state):
		self._setter_access_tracker["placement"] = {}
		self._placement = state
	@property
	def format(self):
		self._getter_access_tracker["format"] = {}
		return self._format
	@format.setter
	def format(self, state):
		self._setter_access_tracker["format"] = {}
		self._format = state
	@property
	def placeholder(self):
		self._getter_access_tracker["placeholder"] = {}
		return self._placeholder
	@placeholder.setter
	def placeholder(self, state):
		self._setter_access_tracker["placeholder"] = {}
		self._placeholder = state
	@property
	def bordered(self):
		self._getter_access_tracker["bordered"] = {}
		return self._bordered
	@bordered.setter
	def bordered(self, state):
		self._setter_access_tracker["bordered"] = {}
		self._bordered = state
	@property
	def disabled(self):
		self._getter_access_tracker["disabled"] = {}
		return self._disabled
	@disabled.setter
	def disabled(self, state):
		self._setter_access_tracker["disabled"] = {}
		self._disabled = state
	@property
	def status(self):
		self._getter_access_tracker["status"] = {}
		return self._status
	@status.setter
	def status(self, state):
		self._setter_access_tracker["status"] = {}
		self._status = state
	@property
	def range(self):
		self._getter_access_tracker["range"] = {}
		return self._range
	@range.setter
	def range(self, state):
		self._setter_access_tracker["range"] = {}
		self._range = state

	def _to_json_fields(self):
		all_fields = {
			"picker": self._picker,
			"showTime": self._showTime,
			"size": self._size,
			"placement": self._placement,
			"format": self._format,
			"placeholder": self._placeholder,
			"bordered": self._bordered,
			"disabled": self._disabled,
			"status": self._status,
			"range": self._range
			}
		return {k: v for k, v in all_fields.items() if v is not None}


class DatePicker(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "DatePicker"
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
		self._custom = DatePickerCustomClass(state)

	def _to_json_fields(self):
		all_fields = {
			"styles": self._styles,
			"custom": self._custom,
			}
		return {k: v for k, v in all_fields.items() if v is not None}