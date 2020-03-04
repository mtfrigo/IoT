#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import RPi.GPIO as GPIO
import time

class LEDBAR(object):

	pd = 26 #DATA IN
	pc = 27 #CLK IN

	CmdMode = 0x0000  # Work on 8-bit mode
	ON = 0x00ff       # 8-bit 1 data
	OFF = 0x0000     # 8-bit 0 data

	def __init__(self, pd=12, pc=13):
		# Intialize the library (must be called once before other functions).

		self.setPD(pd)
		self.setPC(pc)

	def setPD(self, pd):
		self.pd = pd

	def setPC(self, pc):
		self.pc = pc

	def isBitSet(self, x, n):
		return (x & n**2) != 0

	def sendData(self, d):
		clk = True
		GPIO.output(self.pc, 0)
		time.sleep(0.0005)

		for i in range(1,17):
			GPIO.output(self.pc, clk)
			GPIO.output(self.pd, self.isBitSet(d,i))
			clk = not clk
			time.sleep(0.00001)

		GPIO.output(self.pc,0)
		time.sleep(0.0005)
	
	def latchData(self):

		l = False

		GPIO.output(self.pd, 0)

		time.sleep(0.0005)

		for i in range(1,9):
			GPIO.output(self.pd,l)
			l = not l

		time.sleep(0.0005)	

	def setup(self):

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pd, GPIO.OUT)
		GPIO.setup(self.pc, GPIO.OUT)
		GPIO.output(self.pd, 0)
		GPIO.output(self.pc, 0)

		#sendData(CmdMode)
		for i in range(1,13):
			self.sendData(self.OFF)

		self.latchData()

	def sendLedArray(self, l):
		#sendData(CmdMode)
		for i in l:
			if i:
				self.sendData(self.ON)
			else:
				self.sendData(self.OFF)
		self.latchData()

	def pattern_countUp(self):
		self.sendLedArray([1,0,0,0,0,0,0,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([1,1,0,0,0,0,0,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([1,1,1,0,0,0,0,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([1,1,1,1,0,0,0,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([1,1,1,1,1,0,0,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([1,1,1,1,1,1,0,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([1,1,1,1,1,1,1,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([1,1,1,1,1,1,1,1,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([1,1,1,1,1,1,1,1,1,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([1,1,1,1,1,1,1,1,1,1,0,0])
		
		
	def pattern_Kitt(self):
		self.sendLedArray([1,0,0,0,0,0,0,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,1,0,0,0,0,0,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,0,1,0,0,0,0,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,0,0,1,0,0,0,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,0,0,0,1,0,0,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,0,0,0,0,1,0,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,0,0,0,0,0,1,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,0,0,0,0,0,0,1,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,0,0,0,0,0,0,0,1,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,0,0,0,0,0,0,0,0,1,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,0,0,0,0,0,0,0,1,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,0,0,0,0,0,0,1,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,0,0,0,0,0,1,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,0,0,0,0,1,0,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,0,0,0,1,0,0,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,0,0,1,0,0,0,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,0,1,0,0,0,0,0,0,0,0,0])
		time.sleep(0.1)
		self.sendLedArray([0,1,0,0,0,0,0,0,0,0,0,0])

	def sendInteger(self, i):
		if i == 0 or i < 0:
			self.sendLedArray([0,0,0,0,0,0,0,0,0,0,0,0])
		elif i == 1:
			self.sendLedArray([1,0,0,0,0,0,0,0,0,0,0,0])
		elif i == 2:
			self.sendLedArray([1,1,0,0,0,0,0,0,0,0,0,0])
		elif i == 3:
			self.sendLedArray([1,1,1,0,0,0,0,0,0,0,0,0])
		elif i == 4:
			self.sendLedArray([1,1,1,1,0,0,0,0,0,0,0,0])
		elif i == 5:
			self.sendLedArray([1,1,1,1,1,0,0,0,0,0,0,0])
		elif i == 6:
			self.sendLedArray([1,1,1,1,1,1,0,0,0,0,0,0])
		elif i == 7:
			self.sendLedArray([1,1,1,1,1,1,1,0,0,0,0,0])
		elif i == 8:
			self.sendLedArray([1,1,1,1,1,1,1,1,0,0,0,0])
		elif i == 9:
			self.sendLedArray([1,1,1,1,1,1,1,1,1,0,0,0])
		elif i == 10 or i > 10:
			self.sendLedArray([1,1,1,1,1,1,1,1,1,1,0,0])