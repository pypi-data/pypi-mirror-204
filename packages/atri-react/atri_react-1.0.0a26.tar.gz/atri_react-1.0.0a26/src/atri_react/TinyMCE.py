from typing import Any, Union
from atri_core import AtriComponent



class TinyMCECustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.initialValue: Union[Any, None] = state["initialValue"] if state != None and "initialValue" in state else None
		self.value: Union[Any, None] = state["value"] if state != None and "value" in state else None
		self.disabled: Union[Any, None] = state["disabled"] if state != None and "disabled" in state else None
		self.inline: Union[Any, None] = state["inline"] if state != None and "inline" in state else None
		self.id: Union[Any, None] = state["id"] if state != None and "id" in state else None
		self.contentEditable: Union[Any, None] = state["contentEditable"] if state != None and "contentEditable" in state else None
		self.initOnMount: Union[Any, None] = state["initOnMount"] if state != None and "initOnMount" in state else None
		self.tinymceScriptSrc: Union[Any, None] = state["tinymceScriptSrc"] if state != None and "tinymceScriptSrc" in state else None
		self.plugins: Union[Any, None] = state["plugins"] if state != None and "plugins" in state else None
		self.toolbar: Union[Any, None] = state["toolbar"] if state != None and "toolbar" in state else None
		self.menubar: Union[Any, None] = state["menubar"] if state != None and "menubar" in state else None
		self.statusbar: Union[Any, None] = state["statusbar"] if state != None and "statusbar" in state else None
		self.branding: Union[Any, None] = state["branding"] if state != None and "branding" in state else None
		self.resize: Union[Any, None] = state["resize"] if state != None and "resize" in state else None
		self.paste_data_images: Union[Any, None] = state["paste_data_images"] if state != None and "paste_data_images" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def initialValue(self):
		self._getter_access_tracker["initialValue"] = {}
		return self._initialValue
	@initialValue.setter
	def initialValue(self, state):
		self._setter_access_tracker["initialValue"] = {}
		self._initialValue = state
	@property
	def value(self):
		self._getter_access_tracker["value"] = {}
		return self._value
	@value.setter
	def value(self, state):
		self._setter_access_tracker["value"] = {}
		self._value = state
	@property
	def disabled(self):
		self._getter_access_tracker["disabled"] = {}
		return self._disabled
	@disabled.setter
	def disabled(self, state):
		self._setter_access_tracker["disabled"] = {}
		self._disabled = state
	@property
	def inline(self):
		self._getter_access_tracker["inline"] = {}
		return self._inline
	@inline.setter
	def inline(self, state):
		self._setter_access_tracker["inline"] = {}
		self._inline = state
	@property
	def id(self):
		self._getter_access_tracker["id"] = {}
		return self._id
	@id.setter
	def id(self, state):
		self._setter_access_tracker["id"] = {}
		self._id = state
	@property
	def contentEditable(self):
		self._getter_access_tracker["contentEditable"] = {}
		return self._contentEditable
	@contentEditable.setter
	def contentEditable(self, state):
		self._setter_access_tracker["contentEditable"] = {}
		self._contentEditable = state
	@property
	def initOnMount(self):
		self._getter_access_tracker["initOnMount"] = {}
		return self._initOnMount
	@initOnMount.setter
	def initOnMount(self, state):
		self._setter_access_tracker["initOnMount"] = {}
		self._initOnMount = state
	@property
	def tinymceScriptSrc(self):
		self._getter_access_tracker["tinymceScriptSrc"] = {}
		return self._tinymceScriptSrc
	@tinymceScriptSrc.setter
	def tinymceScriptSrc(self, state):
		self._setter_access_tracker["tinymceScriptSrc"] = {}
		self._tinymceScriptSrc = state
	@property
	def plugins(self):
		self._getter_access_tracker["plugins"] = {}
		return self._plugins
	@plugins.setter
	def plugins(self, state):
		self._setter_access_tracker["plugins"] = {}
		self._plugins = state
	@property
	def toolbar(self):
		self._getter_access_tracker["toolbar"] = {}
		return self._toolbar
	@toolbar.setter
	def toolbar(self, state):
		self._setter_access_tracker["toolbar"] = {}
		self._toolbar = state
	@property
	def menubar(self):
		self._getter_access_tracker["menubar"] = {}
		return self._menubar
	@menubar.setter
	def menubar(self, state):
		self._setter_access_tracker["menubar"] = {}
		self._menubar = state
	@property
	def statusbar(self):
		self._getter_access_tracker["statusbar"] = {}
		return self._statusbar
	@statusbar.setter
	def statusbar(self, state):
		self._setter_access_tracker["statusbar"] = {}
		self._statusbar = state
	@property
	def branding(self):
		self._getter_access_tracker["branding"] = {}
		return self._branding
	@branding.setter
	def branding(self, state):
		self._setter_access_tracker["branding"] = {}
		self._branding = state
	@property
	def resize(self):
		self._getter_access_tracker["resize"] = {}
		return self._resize
	@resize.setter
	def resize(self, state):
		self._setter_access_tracker["resize"] = {}
		self._resize = state
	@property
	def paste_data_images(self):
		self._getter_access_tracker["paste_data_images"] = {}
		return self._paste_data_images
	@paste_data_images.setter
	def paste_data_images(self, state):
		self._setter_access_tracker["paste_data_images"] = {}
		self._paste_data_images = state

	def _to_json_fields(self):
		all_fields = {
			"initialValue": self._initialValue,
			"value": self._value,
			"disabled": self._disabled,
			"inline": self._inline,
			"id": self._id,
			"contentEditable": self._contentEditable,
			"initOnMount": self._initOnMount,
			"tinymceScriptSrc": self._tinymceScriptSrc,
			"plugins": self._plugins,
			"toolbar": self._toolbar,
			"menubar": self._menubar,
			"statusbar": self._statusbar,
			"branding": self._branding,
			"resize": self._resize,
			"paste_data_images": self._paste_data_images
			}
		return {k: v for k, v in all_fields.items() if v is not None}


class TinyMCE(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "TinyMCE"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onClick = False
		self.onEditorChange = False
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
		self._custom = TinyMCECustomClass(state)

	def _to_json_fields(self):
		all_fields = {
			"styles": self._styles,
			"custom": self._custom,
			}
		return {k: v for k, v in all_fields.items() if v is not None}