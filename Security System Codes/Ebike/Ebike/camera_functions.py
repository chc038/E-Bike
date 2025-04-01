from PIL import Image


def getFilename0():
    return "Camera_Files/lock_cam.jpg"
def getImage0():
    return Image.open(getFilename0())


