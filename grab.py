def screenshot_to_file(name_file):
    import pyscreenshot
    pyscreenshot.grab(childprocess=False).save(name_file)
