#!usr/bin/python
''' DON'T TOUCH THESE FIRST LINES! '''
''' ============================== '''
from PyoConnect import *
myo = Myo(sys.argv[1] if len(sys.argv) >= 2 else None)
''' ============================== '''

import os
import sys
import threading
import time
# sys.path.append('../our_stuff')
from PPM_generator import ppmGenerator

comm = ppmGenerator()
comm.set_channel_values([1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5])
comm.start()

# Center is set when you first double tap to unlock.
# It is kept unlocked forever
def onUnlock():
	#global throttle_center = myo.getRoll()
	myo.rotSetCenter()
	myo.unlock("hold")


# in case you end up pointing to weird directions,
# just point to where you want the center to be and double tap again
def onPoseEdge(pose, edge):
	if (pose == 'doubleTap') and (edge == "on"):
		myo.rotSetCenter()
		comm.throttle_center = myo.getRoll()
		myo.vibrate(3)


def onBoxChange(box, edge):
	if myo.getVBox() == -1: 
		comm.set_channel_value(3,1)
	elif myo.getVBox() == 1: 
		comm.set_channel_value(3,2)
	else: 
		comm.set_channel_value(3,1.5)
	
	if myo.getHBox() == -1: 
		comm.set_channel_value(2,1)
	elif myo.getHBox() == 1: 
		comm.set_channel_value(2,2)
	else: 
		comm.set_channel_value(2,1.5)

	# this debug message will help you understand the logic:
	if edge == "on": 
		print("VBox=",myo.getVBox()," HBox=",myo.getHBox())

def onPeriodic():
	#sys.stderr.write("\x1b[2J\x1b[H")
	#print comm.lengths
	try:
		#print myo.getRoll()
		print comm.throttle_center
		throttle_pos = (comm.throttle_center + myo.getRoll())
	except:
		pass

myo.onUnlock = onUnlock
myo.onPoseEdge = onPoseEdge
myo.onBoxChange = onBoxChange
myo.onPeriodic = onPeriodic

myo.connect()
while True:
	myo.run()
	myo.tick()