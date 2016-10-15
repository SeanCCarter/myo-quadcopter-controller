import math
import pyaudio

class ppmGenerator:

    def __init__(self):
        self.BITRATE = 44100 #number of frames per second/frameset.      
        self.MINVALUE = 0
        self.MAXVALUE = 225
        self.FRAME = [0,0,0,0,0,0,0,0]
        PyAudio = pyaudio.PyAudio
        p = PyAudio()
        self.stream = p.open(format = p.get_format_from_width(1), 
           channels = 1, 
           rate = self.BITRATE, 
           output = True)

    #writes the current frame to the stream
    def write(self):
        self.stream.write(self.framemaker(self.FRAME))

    #sets the channel values
    def set_channel_values(self,lengths):
        self.lengths = lengths

    #makes string that will set the level of the output for a certain length of time, in milliseconds
    def halfpulsemaker(self,length,level):
        r = ''
        l = (length  * self.BITRATE)/1000
        for i in range(int(l)):
            r += chr(level)
        return r

    #makes a pulse of a given length, in milliseconds
    def pulsemaker(self,length):
        return self.halfpulsemaker(0.25,self.MINVALUE) + self.halfpulsemaker(length - .25, self.MAXVALUE)

    #takes in an array of pulse lengths, makes a full frame out of them
    def framemaker(self,lengths):
        totallength = 0
        r = ''
        for i in range(0,7):
            totallength += lengths[i]
            r += self.pulsemaker(lengths[i])
        r += self.halfpulsemaker(22.5 - totallength,self.MAXVALUE)
        return r