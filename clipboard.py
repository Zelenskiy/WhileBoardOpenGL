from PIL import ImageGrab
im = ImageGrab.grabclipboard()
im.save('image.png','PNG')