import math
import pyaudio

class ppmGenerator:

    def __init__(self):
        self.BITRATE = 44100 #number of frames per second/frameset.      
        self.MINVALUE = 0
        self.MAXVALUE = 255
        self.lengths = [0,0,0,0,0,0,0,0]
        self.framemaker()
        PyAudio = pyaudio.PyAudio
        p = PyAudio()
        self.stream = p.open(format = p.get_format_from_width(1), 
           channels = 1, 
           rate = self.BITRATE, 
           output = True)

    #writes the current frame to the stream
    def write(self):
        self.stream.write(self.frame)

    #sets the channel values
    def set_channel_values(self,lengths):
        self.lengths = lengths
        self.framemaker()

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
    def framemaker(self):
        totallength = 0
        r = ''
        for i in range(0,8):
            totallength += self.lengths[i]
            r += self.pulsemaker(self.lengths[i])
        totallength += 1
        r += self.pulsemaker(1)
        r += self.halfpulsemaker(19.2 - totallength,self.MAXVALUE)
        self.frame = r

    def write_multiframe(self, n):
        frames = self.frame*n
        self.stream.write(frames)


if __name__ == '__main__':
    print "hello world"
    g = ppmGenerator()
    g.set_channel_values([1,1.5,2,1.5,1.5,2,1.5,1])
    g.write_multiframe(1000)
    # for x in range(0,20000):
    #     g.write()
        #print "i wrote a stream"