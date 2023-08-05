from typing import Any, Union
from atri_core import AtriComponent



class IframeCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.src: Union[Any, None] = state["src"] if state != None and "src" in state else None
		self.id: Union[Any, None] = state["id"] if state != None and "id" in state else None
		self.title: Union[Any, None] = state["title"] if state != None and "title" in state else None
		self.allow: Union[Any, None] = state["allow"] if state != None and "allow" in state else None
		self.referrerPolicy: Union[Any, None] = state["referrerPolicy"] if state != None and "referrerPolicy" in state else None
		self.sandbox: Union[Any, None] = state["sandbox"] if state != None and "sandbox" in state else None
		self.loading: Union[Any, None] = state["loading"] if state != None and "loading" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def src(self):
		self._getter_access_tracker["src"] = {}
		return self._src
	@src.setter
	def src(self, state):
		self._setter_access_tracker["src"] = {}
		self._src = state
	@property
	def id(self):
		self._getter_access_tracker["id"] = {}
		return self._id
	@id.setter
	def id(self, state):
		self._setter_access_tracker["id"] = {}
		self._id = state
	@property
	def title(self):
		self._getter_access_tracker["title"] = {}
		return self._title
	@title.setter
	def title(self, state):
		self._setter_access_tracker["title"] = {}
		self._title = state
	@property
	def allow(self):
		self._getter_access_tracker["allow"] = {}
		return self._allow
	@allow.setter
	def allow(self, state):
		self._setter_access_tracker["allow"] = {}
		self._allow = state
	@property
	def referrerPolicy(self):
		self._getter_access_tracker["referrerPolicy"] = {}
		return self._referrerPolicy
	@referrerPolicy.setter
	def referrerPolicy(self, state):
		self._setter_access_tracker["referrerPolicy"] = {}
		self._referrerPolicy = state
	@property
	def sandbox(self):
		self._getter_access_tracker["sandbox"] = {}
		return self._sandbox
	@sandbox.setter
	def sandbox(self, state):
		self._setter_access_tracker["sandbox"] = {}
		self._sandbox = state
	@property
	def loading(self):
		self._getter_access_tracker["loading"] = {}
		return self._loading
	@loading.setter
	def loading(self, state):
		self._setter_access_tracker["loading"] = {}
		self._loading = state

	def _to_json_fields(self):
		all_fields = {
			"src": self._src,
			"id": self._id,
			"title": self._title,
			"allow": self._allow,
			"referrerPolicy": self._referrerPolicy,
			"sandbox": self._sandbox,
			"loading": self._loading
			}
		return {k: v for k, v in all_fields.items() if v is not None}


class Iframe(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Iframe"
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
		self._custom = IframeCustomClass(state)

	def _to_json_fields(self):
		all_fields = {
			"styles": self._styles,
			"custom": self._custom,
			}
		return {k: v for k, v in all_fields.items() if v is not None}