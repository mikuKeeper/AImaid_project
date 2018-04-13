from . import voice, display

yuyin = voice.yuyin.BaiduYuyin()
dsp = display.lookview.Display(position='right_bottom')
dsp.runPlay()

def talk(msg):
    print('女仆NANAMI: '+msg)
    try:
        yuyin.postText(msg)
        dsp.nextAction('talk')
        yuyin.playMp3()
    except Exception as e:
        print(e)
    dsp.nextAction('normal')

