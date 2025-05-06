import time

def auto_adjust(walle):
    walle.headAngle(0.5)
    walle.manual("UD_R",0)
    time.sleep(1)
    walle.manual("UD_L",0)
    time.sleep(1)
    walle.sadness(0)
    time.sleep(1)
    walle.blink()
    time.sleep(0.7)
    walle.sadness(0.7)
    time.sleep(1)
    walle.sadness(0)

def happy(walle):
    walle.sadness(0)
    walle.eyebrow(1)
    walle.blink()

EMOTES = {
    "Auto_adjust": auto_adjust,
    "Happy": happy
}