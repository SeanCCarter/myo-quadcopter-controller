import math
from alsaaudio import *
import threading, thread, Queue

class GenSignal:
    signal = ""
    duration = 0.0225 # seconds
    mmdiv = 4.4 #0.1ms
    mmdiv = 19.2
    samplerate = 44100 # Hz
    samplerate = 192000
    samples = int(duration*samplerate) #992.25
#   amplitude = 32760 #max volume
    amplitude = 20262

    channels = {1: 0.0, #throttle
        2: 100.0,
        3: 100.0,
        4: 100.0,
        5: 0.0,
        6: 0.0,
        7: 0.0,
        8: 100.0,
    }

    def generate(self):
        clist = []
        #start with a stop
        clist += [-self.amplitude]*int(self.mmdiv*4)
        for i in self.channels:
            #ppm base (0.7ms)
            clist += [self.amplitude]*int(self.mmdiv*7)
            #ppm signal (1.7ms max)
            servo = self.channels[i]*0.75/100
            signal = (self.mmdiv*10)*servo
            clist += [self.amplitude]*int( signal )
            clist += [-self.amplitude]*int(self.mmdiv*4)

        #complete the ppm signal with a starting null signal that fill in the 22.5ms frame (here f.ex 992 self.samples)
        signallist = []
        for i in range(0, self.samples-len(clist)):
            signallist += [0]

        #add our ppm channels
        signallist += clist

        s=pack('<'+self.samples*'l',*signallist)
        self.signal = s

class Signal(threading.Thread):
    """This class is the thread generating the audio ppm sound"""
    signal = ""
    card = PCM(type=PCM_PLAYBACK, mode=PCM_NONBLOCK, card='default')
    card.setchannels(2)
    card.setrate(192000)
    card.setformat(PCM_FORMAT_S16_LE)
    card.setperiodsize(192000)
    print "Sound card initialized"

    def __init__(self, q):
        self.queue_in = q
        threading.Thread.__init__(self)
    

    def run(self):
        item = None
        while True:
            try:
                item = self.queue_in.get_nowait()
                if type(item) is not int:
                    self.signal = item
                else:
                    break
            except Queue.Empty:
                pass
            self.card.write(self.signal)


if __name__ == '__main__':
    q = Queue.Queue(0)
    s = Signal(q)
    gen = GenSignal()
    q.put_nowait(gen.signal)
    while True:
        q.put_nowait(gen.signal)
