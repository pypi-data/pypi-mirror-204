"""
blabla
"""

from importlib import import_module
import os
import sys

import pygame.font as pygfont
import pygame.rect as pygrect
import pygame.draw as pygdraw

from pygame_ui.constants import *


sys.path.append(os.getcwd())

pygfont.init()


class UI_Element:
	is_visible = True
	is_hoverable = False
	is_clickable = False
	position = [0,0]
	size = [0,0]
	auto_size = False
	background_color = None

	def __init__(self, initial_data, kwargs):
		for dictionary in initial_data:
			for key in dictionary:
				setattr(self, key, dictionary[key])
		for key in kwargs:
			setattr(self, key, kwargs[key])
		
		self.rectangle = pygrect.Rect(self.position, self.size)
	
	def change_position(self, new_position):
		"""
		You can figure this one out yourself. If you can't then... *sigh*
		"""
		self.position = new_position
		self.rectangle = pygrect.Rect(self.position, self.size)

	def change_size(self, new_size):
		"""
		You can figure this one out yourself. If you can't then... *sigh*
		"""
		self.size = new_size
		self.rectangle = pygrect.Rect(self.position, self.size)
	
	def draw_bg(self, pygame_window):
		if self.auto_size:
			if isinstance(self, label):
				auto_rect = pygrect.Rect(self.position, self.font.size(self.text))
			pygdraw.rect(pygame_window, self.background_color, auto_rect)
		else:
			pygdraw.rect(pygame_window, self.background_color, self.rectangle)


class frame(UI_Element):
	"""
	The UI element that works as a sort of bundle or group.

	Yes, frame-ception is a thing.
	"""
	
	contents = {}

	def __init__(self, *initial_data, **kwargs):
		self.elements = {}
		super().__init__(initial_data, kwargs)
		for item_type, data in self.contents.items():
			self.elements[data['name']] = globals()[item_type](data)
	
	def get_interactive_elements(self):
		interactives = []
		for name, element in self.elements.items():
			if element.is_visible:
				if isinstance(element, frame) and not isinstance(element, button):
					interactives.extend(element.get_interactive_elements())
				elif element.is_hoverable or element.is_clickable:
					interactives.append(element)
		return interactives
	
	def draw(self, pygame_window):
		for i in self.elements.values():
			if i.is_visible:
				if i.background_color != None:
					i.draw_bg(pygame_window)
				i.draw(pygame_window)


class button(frame):
	is_clickable = True
	is_hoverable = True
	click_start = False
	click_end = False
	held = False
	hover_start = False
	hover_end = False
	hovered = False


class label(UI_Element):
	"""
	The UI element for text.

	Anything with letters will use this class.
	"""
	
	text = "Empty Label"
	text_color = (255,255,255)
	text_aa = True
	font_name = 'Arial'
	font_size = 10
	font_bold = False
	font_italic = False

	def __init__(self, *initial_data, **kwargs):
		super().__init__(initial_data, kwargs)
		self.font = pygfont.SysFont(self.font_name, self.font_size, self.font_bold, self.font_italic)
	
	def change_font(self, **kwargs):
		"""
		Used to change attributes of the font.

		The keyword arguments must exist in the following list:
		>>> ['font_name', 'font_size', 'font_bold', 'font_bold']
		"""

		for key in kwargs:
			if key in FONT_ATTRIBUTES:
				setattr(self, key, kwargs[key])
			else:
				raise KeyError(key+' is not a font attribute. '+MUST_BE+FONT_ATTRIBUTES+'\n'+ISSUE_REPORT)
		self.font = pygfont.SysFont(self.font_name, self.font_size, self.font_bold, self.font_italic)

	def draw(self, pygame_window):
		text_render = self.font.render(self.text, self.text_aa, self.text_color, self.background_color)
		pygame_window.blit(text_render, self.position)


class switch(UI_Element):
	is_clickable = True

	def __init__(self, *initial_data, **kwargs):
		super().__init__(initial_data, kwargs)

	def draw(self, pygame_window):
		pass


class slider(UI_Element):
	is_clickable = True

	def __init__(self, *initial_data, **kwargs):
		super().__init__(initial_data, kwargs)

	def draw(self, pygame_window):
		pass


class dropdown(UI_Element):
	is_clickable = True

	def __init__(self, *initial_data, **kwargs):
		super().__init__(initial_data, kwargs)

	def draw(self, pygame_window):
		pass