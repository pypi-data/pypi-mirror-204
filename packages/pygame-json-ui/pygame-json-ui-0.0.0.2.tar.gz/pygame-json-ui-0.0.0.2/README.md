
# Pygame UI README

[Pygame UI](https://github.com/RednaxGaming/pygame_ui) is a package for building user interfaces in [pygame](https://www.pygame.org/).

It is currently a work in progress, but if you wanna test it out, feel free to do so :)

## Table Of Content

- [Quick Start](#quick-start)
   - [Installation](#installation)
   - [Setup](#setup)
      - [Python](#python-file)
      - [JSON](#json-file)
- [Element List](#element-list)
- [Attribute List](#attribute-list)
   - [General](#general)
   - [Frame](#frame)
   - [Label](#label)
   - [Button](#button)
- [Frames](#frames)
   - [Frame Path](#frame-path)
- [Examples](#examples)
- [FAQ](#faq)

## Quick Start

### Installation

First of all, you'll need to manually add the pygame_ui folder to your site-packages, because the module is not yet available on pip.

When this is done you can test your installation, by executing the following:
```python
>>> import pygame_ui
>>> pygame_ui.test()
Successfully installed! enjoy :)
Version: x.x.x.x
```

### Setup

You will have two files in the same folder:
- whatever.py
- Interface.json <-- Specifically with that name and capitalization!

Here a simple example for making a label:

#### Python File

Notice that the `event_handler` is actually not required unless you want interactive elements to function as expected.

```python
import pygame
import pygame_ui

# Creating a window
pygame.init()
screen = pygame.display.set_mode((1280, 720), vsync=1)
pygame.display.set_caption("GUI")
clock = pygame.time.Clock()


# Initializing interface
Interface = pygame_ui.init()


while True:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         quit()
      # Call event handler
      Interface.event_handler(event)

   screen.fill((0,0,0))

   # Draw interface
   Interface.draw(screen)

   pygame.display.flip()
   clock.tick(60)
```

#### JSON File
MUST be named `Interface.json` and in the same folder as python file!

```json
{
   "label": {
      "name": "test_label",
      "position": [200,100],
      "size": [120,80],
      "background_color": [200,0,0],
      "text": "IT WORKS!",
      "font_size": 20,
      "auto_size": true
   }
}
```

## Element List

All of the following items will be refered to as `elements`:
- Frame
- Label
- Button
- Switch (not implemented yet)
- Slider (...)
- Dropdown (...)

## Attribute List

### General
These attributes can be given to any element type
- `name: str` MUST be given to every element.
- `position: [x,y]` Sets position from top-left of screen to top-left of element boundry box.
- `size: [x,y]` Sets the size of the element boundry box.
- `background_color: (r,g,b)` The boundry box will be filled with this color. Don't set this for transparency.
- `is_visible: bool` (default = true).
- `is_hoverable: bool` (default = false).
- `is_clickable: bool` (default = false).

### Frame
- `contents: {}` See [frames](#frames) for more info.

### Label

- `text: str` Exactly what you think it is.
- `text_color: (r,g,b)` (default = (255,255,255))
- `text_aa: bool` anti-aliasing (default = true)
- `font_name: str` (default = 'Arial')
- `font_size: int` (default = 10)
- `font_bold: bool` (default = false)
- `font_italic: bool` (default = false)
- `auto_size: bool` This will overwrite size of the boundry box to fit the text within (default = false).

### Button

- `contents: {}` The button is basically just a frame with the following default attributes added to it. Making a button manually from a frame is possible, but deprecated.
- `is_clickable: bool` (default = true)
- `is_hoverable: bool` (default = true)
- `click_start: bool` (default = false)
- `click_end: bool` (default = false)
- `held: bool` (default = false)
- `hover_start: bool` (default = false)
- `hover_end: bool` (default = false)
- `hovered: bool` (default = false)

## Frames

Frames can contain `elements` Just like how a folder can contain files and other folders.
Frames can also hold other frames, and yes, those can contain frames aswell (see [Frame-ception](#frame-ception)). When a frame is invisible, it's `elements` will also be invisable. Deleting a frame will also delete it's `elements`.

### Frame Path

A frame path is a string representation of the route to a certain frame.

Say we have the following json file
```json
{
   "frame": {
      "name": "Arthur"
      "contents": {
         "frame": {
            "name": "Bertha"
            "contents": {
               "frame": {
                  "name": "Pippinpaddleopsicopolis"
               }
            }
         },
         "frame": {
            "name": "Cedric"
         }
      }
   }
}
```

and i wanted to access `Pippinpaddleopsicopolis`

The syntax for the frame path is very simple:
```
Arthur->Bertha->Pippinpaddleopsicopolis
```

## Examples

All examples use [this](#python-file) python file as base.

### A button

```json
{
   "button": {
      "name": "harry the button",
      "position": [250,120],
      "size": [200,200],
      "background_color": [100,0,0],
      "contents": {
         "label": {
            "name": "jonathan the label",
            "position": [260,150],
            "font_size": 30,
            "auto_size": true
         }
      }
   }
}
```
With this called after `pygame_ui.init()`:
```python
harry = Interface.get_element('harry the button', 'frame1->frame2')
jonathan = Interface.get_element('jonathan the label', 'frame1->frame2->harry the button')
```
And this between `event_handler()` and `draw()`:
```python
jonathan.text = "start: "+str(harry.click_start)+", end: "+str(harry.click_end)+", held: "+str(harry.held)
```


### Adding An Element Post Initialization

```python
play_label = pygame_ui.label(position=[100,100], size=[100,100], text="play now", text_size=20)
Interface.add_element('play', play_label)
```

### Adding An Element To A Frame

```python
play_label = pygame_ui.label(position=[100,100], size=[100,100], text="play now", text_size=20)
Interface.add_element('play', play_label, 'Arthur->Bertha->Pippinpaddleopsicopolis')
```

### Removing An Element From A Frame

```python
Interface.remove_element('Pippinpaddleopsicopolis', 'Arthur->Bertha')
```

### Get Element Object
```python
play_label = Interface.get_element('play', 'Arthur->Bertha->Pippinpaddleopsicopolis')
play_label.text = 'THE THIRD'
```

### Frame-ception

Just... don't ask me why.

#### Python
```python
import pygame
import pygame_ui

pygame.init()
screen = pygame.display.set_mode((1280, 720), vsync=1)
pygame.display.set_caption("Frame-ception")
clock = pygame.time.Clock()

Interface = pygame_ui.init()

path = 'frame0'
for i in range(100):
   frame = 'frame'+str(i+1)
   Interface.add_element(frame, pygame_ui.frame(), path)
   path += '->'+frame

while True:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         quit()

   screen.fill((0,0,0))

   Interface.draw(screen)

   pygame.display.flip()
   clock.tick(60)
```

#### JSON
```json
{
   "frame": {
      "name": "frame0",
      "contents": {}
   }
}
```

## FAQ

Nothing yet lol.