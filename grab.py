import pyscreenshot


def screenshot_to_file(name_file):

    pyscreenshot.grab(childprocess=False).save(name_file)

def ins_from_clip(name_file):
    pass
    # clipboard.paste().save(name_file)
    # pyscreenshot.grabclipboard().save(name_file)

