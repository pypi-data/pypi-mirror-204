"""
Pygame UI
=========

A python library for quickly building user interfaces for pygame.

Make sure you read the ``Getting started`` section of the documentation in the library folder.
"""

from pygame_ui.base import *
from pygame_ui.elements import *

# release, year, month, session
__version__ = '0.0.0.3'

#print('Pygame UI ' + __version__)

def test():
	try:
		import pygame_ui.base
		import pygame_ui.constants
		import pygame_ui.elements
		print('Successfully installed! enjoy :)\nversion: '+__version__)
		del pygame_ui.base, pygame_ui.constants, pygame_ui.elements
	except:
		print(ISSUE_REPORT)

# Base64
# VGhpcyBjb2RlIHdhcyB3cml0dGVuIGJ5IFJlZG5heEdhbWluZyBvbiBnaXRodWI=