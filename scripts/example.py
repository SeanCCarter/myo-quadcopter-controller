import os
import sys
import threading
import time
sys.path.append('../our_stuff')
from PPM_generator.ppmGenerator


# Center is set when you first double tap to unlock.
# It is kept unlocked forever
def onUnlock():
	myo.rotSetCenter()
	myo.unlock("hold")
	# comm = ppmGenerator()
	# comm.set_channel_values([1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5])
	# comm.start()

# in case you end up pointing to weird directions,
# just point to where you want the center to be and double tap again
def onPoseEdge(pose, edge):
	if (pose == 'doubleTap') and (edge == "on"):
		myo.rotSetCenter()
		myo.vibrate(3)

def onBoxChange(box, edge):
	if myo.getVBox() == -1: 
		print("Up arrow down")
	else: 
		myo.keyboard("up_arrow","up","")
	
	if myo.getVBox() == 1: 
		print("Down arrow down")
	else: 
		myo.keyboard("down_arrow","up","")
	
	if myo.getHBox() == 1: 
		print("Right arrow down")
	else: 
		myo.keyboard("right_arrow","up","")
	
	if myo.getHBox() == -1: 
		print("Left arrow down")
	else: 
		myo.keyboard("left_arrow","up","")

	# this debug message will help you understand the logic:
	if edge == "on": 
		print("VBox=",myo.getVBox()," HBox=",myo.getHBox())

# def onPeriodic():
# 	sys.stderr.write("\x1b[2J\x1b[H")
# 	print(myo.getRoll())
# 	print(myo.getPitch())
# 	print(myo.getYaw())

