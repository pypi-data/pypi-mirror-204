from pygame_ui.constants import *
import pygame_ui.elements
import pygame.locals as pyglocal
import pygame.mouse as pygmouse


class Graphical_UI:
	"""
	The main GUI handler

	Is automatically called on ``pygame_ui.init()``

	Calling this manually is deprecated.
	"""

	elements = {}
	interactive_elements = []

	def __init__(self, objects:dict):
		for item_type, data in objects.items():
			self.elements[data['name']] = getattr(pygame_ui.elements, item_type)(data)

	def get_frame(self, frame_path:str=''):
		"""
		Returns the frame of given path.
		"""
		
		frame = self
		for i in frame_path.split('->'):
			if i in frame.elements.keys():
				frame = frame.elements[i]
			else:
				raise KeyError('No frame with name \''+i+'\' was found. '+MORE_INFO+'frame paths')
		return frame

	def get_element(self, name:str, frame_path:str=''):
		"""
		Returns the element with specified name at given path.
		"""

		frame = self.get_frame(frame_path)
		if name in frame.elements.keys():
			return frame.elements[name]
		else:
			raise KeyError('No element with name \''+name+'\' was found. '+MORE_INFO+'frame paths')

	def add_element(self, name:str, element:pygame_ui.elements.UI_Element, frame_path:str=''):
		"""
		Adds the specified element with it's name to the GUI or given frame.
		"""
		
		frame = self.get_frame(frame_path)
		frame.elements[name] = element

	def remove_element(self, name:str, frame_path:str=''):
		"""
		Removes the element specified by name (and path) from it's parent.
		"""

		frame = self.get_frame(frame_path)
		if name in frame.elements.keys():
			frame.elements.pop(name)
		else:
			raise KeyError('No element with name \''+frame_path+'\' was found. '+MORE_INFO+'frame paths')

	def get_interactive_elements(self):
		interactives = []
		for name, element in self.elements.items():
			if element.is_visible:
				if isinstance(element, pygame_ui.frame):
					interactives.extend(element.get_interactive_elements())
				elif element.is_hoverable or element.is_clickable:
					interactives.append(element)
		self.interactive_elements = interactives

	def event_handler(self, event):
		"""
		This handles all interactive elements.

		Must be called in the following context:
		>>> for event in pygame.event.get():
			Interface.event_handler(event)
		"""

		self.get_interactive_elements()

		element = None
		lmb, rmb, mmb = pygmouse.get_pressed(3)
		mpos = pygmouse.get_pos()
		
		for i in self.interactive_elements:
			mouse_in_boundry = i.rectangle.collidepoint(mpos)

			if mouse_in_boundry:
				if event.type in [pyglocal.MOUSEBUTTONDOWN, pyglocal.MOUSEBUTTONUP] and i.is_clickable:
					element = i
				elif event.type in [pyglocal.MOUSEMOTION, pyglocal.MOUSEWHEEL] and i.is_hoverable:
					element = i
			elif event.type in [pyglocal.MOUSEBUTTONUP, pyglocal.MOUSEMOTION, pyglocal.MOUSEWHEEL] and i.click_held:
				element = i
			
			if event.type == pyglocal.MOUSEBUTTONUP and lmb == 0:
				i.click_end = True
				i.click_held = False

		if element != None:
			if event.type in [pyglocal.MOUSEMOTION, pyglocal.MOUSEWHEEL]:
				if isinstance(element, pygame_ui.slider) and element.click_held:
					i.set_value_from_pos(mpos)

			elif event.type == pyglocal.MOUSEBUTTONDOWN and lmb == 1:
				element.click_start = True
				element.click_held = True
				if isinstance(element, pygame_ui.switch):
					element.state = not element.state

		return 1
	
	def draw(self, pygame_window):
		"""
		Main draw function which will draw all visible things layered like painter-style.
		
		Must be called in the following context:
		>>> Interface.draw(pygame_window)
		>>> pygame.display.flip()
		"""

		for i in self.elements.values():
			if i.is_visible:
				if i.background_color != None:
					i.draw_bg(pygame_window)
				i.draw(pygame_window)
		
		# Reset all temporary attribute values
		for i in self.interactive_elements:
			if i.is_clickable:
				i.click_start = False
				i.click_end = False
			if i.is_hoverable:
				i.hover_start = False
				i.hover_end = False
				
		return 1


def init(path_to_json:str='Interface.json'):
	"""
	This loads in the ``Interface.json`` file and created a GUI with it
	"""

	import json
	import os
	
	try:
		file = open(os.path.abspath(path_to_json))
	except FileNotFoundError:
		print(ISSUE_REPORT)
	UI = json.load(file)
	file.close()

	interface = Graphical_UI(UI)

	# clearing up namespace
	del json, os, pygame_ui.elements

	return interface