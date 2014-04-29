import serial
import wx
import time
import datetime
from arduinoSerial import *
import json
import numpy
import os

class arduinoMonitor(wx.Frame):

	thumb = 0
	index = 0
	middle = 0
	ring = 0
	pinky = 0
	xTime = datetime.datetime.utcnow()

	indexTouch = 0
	middleTouch = 0
	ringTouch = 0
	pinkyTouch = 0

	dataCounter = 0;
	arraytowrite = []

	gestureList = ['negative', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 
				   'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

	def __init__(self, parent):
		wx.Frame.__init__(self, parent, wx.ID_ANY, "mbed Monitor", size=(700, 280))
		# set minimum size
		self.SetMinSize(self.GetSize())
		self.SetMaxSize(self.GetSize())

		# build a panel
		self.mp = wx.Panel(self, wx.ID_ANY)

		# build a status bar 
		self.statusBar = self.CreateStatusBar()

		# create a timer
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.updateData, self.timer)

		# create gauges
		self.thumbLabel = wx.StaticText(self.mp, -1, "Thumb", size=(70, -1), style=wx.ALIGN_RIGHT)
		self.thumbGauge = wx.Gauge(self.mp, -1, 100, size=(450, -1))
		self.thumbVal = wx.StaticText(self.mp, -1, "0", size=(100,-1), style = wx.ALIGN_LEFT)

		self.indexLabel = wx.StaticText(self.mp, -1, "Index", size=(70, -1), style=wx.ALIGN_RIGHT)
		self.indexGauge = wx.Gauge(self.mp, -1, 100, size=(450, -1))
		self.indexVal = wx.StaticText(self.mp, -1, "0", size=(100,-1), style = wx.ALIGN_LEFT)
		self.indexTouchVal = wx.StaticText(self.mp, -1, "0", size=(30,-1), style = wx.ALIGN_LEFT)

		self.middleLabel = wx.StaticText(self.mp, -1, "Middle", size=(70, -1), style=wx.ALIGN_RIGHT)
		self.middleGauge = wx.Gauge(self.mp, -1, 100, size=(450, -1))
		self.middleVal = wx.StaticText(self.mp, -1, "0", size=(100,-1), style = wx.ALIGN_LEFT)
		self.middleTouchVal = wx.StaticText(self.mp, -1, "0", size=(30,-1), style = wx.ALIGN_LEFT)

		self.ringLabel = wx.StaticText(self.mp, -1, "Ring", size=(70, -1), style=wx.ALIGN_RIGHT)
		self.ringGauge = wx.Gauge(self.mp, -1, 100, size=(450, -1))
		self.ringVal = wx.StaticText(self.mp, -1, "0", size=(100,-1), style = wx.ALIGN_LEFT)
		self.ringTouchVal = wx.StaticText(self.mp, -1, "0", size=(30,-1), style = wx.ALIGN_LEFT)

		self.pinkyLabel = wx.StaticText(self.mp, -1, "Pinky", size=(70, -1), style=wx.ALIGN_RIGHT)
		self.pinkyGauge = wx.Gauge(self.mp, -1, 100, size=(450, -1))
		self.pinkyVal = wx.StaticText(self.mp, -1, "0", size=(100,-1), style = wx.ALIGN_LEFT)
		self.pinkyTouchVal = wx.StaticText(self.mp, -1, "0", size=(30,-1), style = wx.ALIGN_LEFT)

		self.calibrateButton = wx.Button(self.mp, id=wx.ID_ANY, label = "Done Calibrating", size=(150,-1))
		self.gestureChoice = wx.Choice(self.mp, -1, size=(150, -1), choices=self.gestureList)
		self.collectButton = wx.Button(self.mp, id=wx.ID_ANY, label = "Collect Data", size=(150,-1))
		self.writeButton = wx.Button(self.mp, id=wx.ID_ANY, label = "Write to File", size=(150,-1))
		self.calibrateButton.Bind(wx.EVT_BUTTON, self.onCalibrate)
		self.collectButton.Bind(wx.EVT_BUTTON, self.onCollect)
		self.writeButton.Bind(wx.EVT_BUTTON, self.onWrite)
		
		
		# Define Sizers
		self.defineSizers()

		# initialize thread
		self.arduinoSerial = SerialData()

		self.timer.Start(50)

		# set status bar text
		self.statusBar.SetStatusText("Calibrating...hit 'Done Calibrating' button when finished")
		
	def onCalibrate(self, event):
		# signal that we are done with calibration
		for i in range(20):
			self.arduinoSerial.ser.write('1')
			time.sleep(0.005)
		self.statusBar.SetStatusText("Ready to collect data...hit 'Collect Data' button")

	def onCollect(self, event):
		temp = [self.thumb, self.index, self.middle, self.ring, self.pinky, 
			self.indexTouch, self.middleTouch, self.ringTouch, self.pinkyTouch, 
			self.gestureChoice.GetCurrentSelection()]
		self.dataCounter += 1;
		self.statusBar.SetStatusText("Data collected...total data points: " + str(self.dataCounter))
		self.arraytowrite.append(temp)

	def onWrite(self, event):
		saveDialog = wx.FileDialog(None, "Save file as...", os.getcwd(), "", "Binary file (*.bin)|*.bin", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		# cancel
		if saveDialog.ShowModal() == wx.ID_CANCEL:
			# update status
			self.statusBar.SetStatusText("Did not save")
			return
		else:
			f = open(saveDialog.GetPath(), 'w')
			json.dump(self.arraytowrite, f)
			f.close();
			self.arraytowrite = []
			# update status
			self.statusBar.SetStatusText("Saved binary file to " + saveDialog.GetPath())
			self.dataCounter = 0
			return

	def updateData(self, event):
		dataLine = self.arduinoSerial.next()
		#print dataLine
		parsedData = dataLine.split("/")
		if len(parsedData) >= 10:
			self.assignData(parsedData)
		

	def assignData(self, parsedData):
		# skip first entry
		# collect data from parsedData and keep track of time it was collected
		self.xTime = datetime.datetime.utcnow()
		self.thumb = int(parsedData[1])
		self.index = int(parsedData[2])
		self.middle = int(parsedData[3])
		self.ring = int(parsedData[4])
		self.pinky = int(parsedData[5])
		self.indexTouch = int(parsedData[6])
		self.middleTouch = int(parsedData[7])
		self.ringTouch = int(parsedData[8])
		self.pinkyTouch = int(parsedData[9])

		self.thumbGauge.SetValue(self.thumb)
		self.indexGauge.SetValue(self.index)
		self.middleGauge.SetValue(self.middle)
		self.ringGauge.SetValue(self.ring)
		self.pinkyGauge.SetValue(self.pinky)

		self.thumbVal.SetLabel(str(self.thumb))
		self.indexVal.SetLabel(str(self.index))
		self.middleVal.SetLabel(str(self.middle))
		self.ringVal.SetLabel(str(self.ring))
		self.pinkyVal.SetLabel(str(self.pinky))

		self.indexTouchVal.SetLabel(str(self.indexTouch))
		self.middleTouchVal.SetLabel(str(self.middleTouch))
		self.ringTouchVal.SetLabel(str(self.ringTouch))
		self.pinkyTouchVal.SetLabel(str(self.pinkyTouch))



	def defineSizers(self):
		self.thumbSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.thumbSizer.Add(self.thumbLabel, 0, wx.ALL, 5)
		self.thumbSizer.Add(self.thumbGauge, 0, wx.ALL, 5)
		self.thumbSizer.Add(self.thumbVal, 0, wx.ALL, 5)

		self.indexSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.indexSizer.Add(self.indexLabel, 0, wx.ALL, 5)
		self.indexSizer.Add(self.indexGauge, 0, wx.ALL, 5)
		self.indexSizer.Add(self.indexVal, 0, wx.ALL, 5)
		self.indexSizer.Add(self.indexTouchVal, 0, wx.ALL, 5)

		self.middleSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.middleSizer.Add(self.middleLabel, 0, wx.ALL, 5)
		self.middleSizer.Add(self.middleGauge, 0, wx.ALL, 5)
		self.middleSizer.Add(self.middleVal, 0, wx.ALL, 5)
		self.middleSizer.Add(self.middleTouchVal, 0, wx.ALL, 5)

		self.ringSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.ringSizer.Add(self.ringLabel, 0, wx.ALL, 5)
		self.ringSizer.Add(self.ringGauge, 0, wx.ALL, 5)
		self.ringSizer.Add(self.ringVal, 0, wx.ALL, 5)
		self.ringSizer.Add(self.ringTouchVal, 0, wx.ALL, 5)

		self.pinkySizer = wx.BoxSizer(wx.HORIZONTAL)
		self.pinkySizer.Add(self.pinkyLabel, 0, wx.ALL, 5)
		self.pinkySizer.Add(self.pinkyGauge, 0, wx.ALL, 5)
		self.pinkySizer.Add(self.pinkyVal, 0, wx.ALL, 5)
		self.pinkySizer.Add(self.pinkyTouchVal, 0, wx.ALL, 5)

		self.commandSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.commandSizer.Add(self.calibrateButton, 0, wx.ALL, 5)
		self.commandSizer.Add(self.gestureChoice, 0, wx.ALL, 5)
		self.commandSizer.Add(self.collectButton, 0, wx.ALL, 5)
		self.commandSizer.Add(self.writeButton, 0, wx.ALL, 5)

		self.topSizer = wx.BoxSizer(wx.VERTICAL)
		self.topSizer.Add(self.thumbSizer, 0, wx.ALL, 5)
		self.topSizer.Add(self.indexSizer, 0, wx.ALL, 5)
		self.topSizer.Add(self.middleSizer, 0, wx.ALL, 5)
		self.topSizer.Add(self.ringSizer, 0, wx.ALL, 5)
		self.topSizer.Add(self.pinkySizer, 0, wx.ALL, 5)
		self.topSizer.Add(self.commandSizer, 0, wx.ALL, 5)

		self.mp.SetAutoLayout(True)
		self.mp.SetSizer(self.topSizer)
		self.mp.Layout()
		self.Layout()


# below is needed for all GUIs
if __name__== '__main__':
	app = wx.App(False) # application object (inner workings) 
	frame = arduinoMonitor(parent = None) # frame object (what user sees)
	frame.Show() # show frame
	app.MainLoop() # run main loop	
