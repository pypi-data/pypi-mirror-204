from typing import Any, Union
from atri_core import AtriComponent



class DrawerCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.open: Union[Any, None] = state["open"] if state != None and "open" in state else None
		self.title: Union[Any, None] = state["title"] if state != None and "title" in state else None
		self.placement: Union[Any, None] = state["placement"] if state != None and "placement" in state else None
		self.size: Union[Any, None] = state["size"] if state != None and "size" in state else None
		self.closable: Union[Any, None] = state["closable"] if state != None and "closable" in state else None
		self.destroyOnClose: Union[Any, None] = state["destroyOnClose"] if state != None and "destroyOnClose" in state else None
		self.forceRender: Union[Any, None] = state["forceRender"] if state != None and "forceRender" in state else None
		self.autoFocus: Union[Any, None] = state["autoFocus"] if state != None and "autoFocus" in state else None
		self.keyboard: Union[Any, None] = state["keyboard"] if state != None and "keyboard" in state else None
		self.mask: Union[Any, None] = state["mask"] if state != None and "mask" in state else None
		self.maskClosable: Union[Any, None] = state["maskClosable"] if state != None and "maskClosable" in state else None
		self.zIndex: Union[Any, None] = state["zIndex"] if state != None and "zIndex" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def open(self):
		self._getter_access_tracker["open"] = {}
		return self._open
	@open.setter
	def open(self, state):
		self._setter_access_tracker["open"] = {}
		self._open = state
	@property
	def title(self):
		self._getter_access_tracker["title"] = {}
		return self._title
	@title.setter
	def title(self, state):
		self._setter_access_tracker["title"] = {}
		self._title = state
	@property
	def placement(self):
		self._getter_access_tracker["placement"] = {}
		return self._placement
	@placement.setter
	def placement(self, state):
		self._setter_access_tracker["placement"] = {}
		self._placement = state
	@property
	def size(self):
		self._getter_access_tracker["size"] = {}
		return self._size
	@size.setter
	def size(self, state):
		self._setter_access_tracker["size"] = {}
		self._size = state
	@property
	def closable(self):
		self._getter_access_tracker["closable"] = {}
		return self._closable
	@closable.setter
	def closable(self, state):
		self._setter_access_tracker["closable"] = {}
		self._closable = state
	@property
	def destroyOnClose(self):
		self._getter_access_tracker["destroyOnClose"] = {}
		return self._destroyOnClose
	@destroyOnClose.setter
	def destroyOnClose(self, state):
		self._setter_access_tracker["destroyOnClose"] = {}
		self._destroyOnClose = state
	@property
	def forceRender(self):
		self._getter_access_tracker["forceRender"] = {}
		return self._forceRender
	@forceRender.setter
	def forceRender(self, state):
		self._setter_access_tracker["forceRender"] = {}
		self._forceRender = state
	@property
	def autoFocus(self):
		self._getter_access_tracker["autoFocus"] = {}
		return self._autoFocus
	@autoFocus.setter
	def autoFocus(self, state):
		self._setter_access_tracker["autoFocus"] = {}
		self._autoFocus = state
	@property
	def keyboard(self):
		self._getter_access_tracker["keyboard"] = {}
		return self._keyboard
	@keyboard.setter
	def keyboard(self, state):
		self._setter_access_tracker["keyboard"] = {}
		self._keyboard = state
	@property
	def mask(self):
		self._getter_access_tracker["mask"] = {}
		return self._mask
	@mask.setter
	def mask(self, state):
		self._setter_access_tracker["mask"] = {}
		self._mask = state
	@property
	def maskClosable(self):
		self._getter_access_tracker["maskClosable"] = {}
		return self._maskClosable
	@maskClosable.setter
	def maskClosable(self, state):
		self._setter_access_tracker["maskClosable"] = {}
		self._maskClosable = state
	@property
	def zIndex(self):
		self._getter_access_tracker["zIndex"] = {}
		return self._zIndex
	@zIndex.setter
	def zIndex(self, state):
		self._setter_access_tracker["zIndex"] = {}
		self._zIndex = state

	def _to_json_fields(self):
		all_fields = {
			"open": self._open,
			"title": self._title,
			"placement": self._placement,
			"size": self._size,
			"closable": self._closable,
			"destroyOnClose": self._destroyOnClose,
			"forceRender": self._forceRender,
			"autoFocus": self._autoFocus,
			"keyboard": self._keyboard,
			"mask": self._mask,
			"maskClosable": self._maskClosable,
			"zIndex": self._zIndex
			}
		return {k: v for k, v in all_fields.items() if v is not None}


class Drawer(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Drawer"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onClick = False
		self.onClose = False
		self.afterOpenChange = False
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
		self._custom = DrawerCustomClass(state)

	def _to_json_fields(self):
		all_fields = {
			"styles": self._styles,
			"custom": self._custom,
			}
		return {k: v for k, v in all_fields.items() if v is not None}