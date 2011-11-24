#!/usr/bin/env python

import os
import sys
from twisted.internet import reactor
from twisted.internet import task
from twisted.internet import defer
import pypm

class NotConnectedError(Exception):
    """
    Raised when trying to start midi input when not connected.
    """
    pass

class MidiIn(object):

    def __init__(self, device):
        """
        Let's at least provide the known MIDI devices
        """
        self.num_of_devices = 0
        self.device_id = device
        self.midi_devices = []
        self.midi_in = None
        self.is_connected = False
        self.callbacks = []

        # Initilize MIDI
        self.get_midi_input_devices()
        print("Device ID: ".format(self.device_id))
        self.select_midi_device()
        #self._looping_call = task.LoopingCall(self.poll)
        self._looping_call = task.LoopingCall(self.poll)

    def get_midi_input_devices(self):
        """
        Returns a list of valid input devices
        """
        self.num_of_devices = pypm.CountDevices()
        # clear the list before populating it again
        self.midi_devices = []
        for i in range(self.num_of_devices):
            subsys, name, inp, outp, opened = pypm.GetDeviceInfo(i)
            self.midi_devices.append([i, name, inp, opened])
            print("Index:{} Name:{} Input:{} Opened?: {}".format(i, name, inp, opened))
        return self.midi_devices

    def select_midi_device(self):
        """
        Selects the MIDI device for reading
        """
        if self.midi_devices[self.device_id][2] == 1:
            # the device is not already open?
            if self.midi_devices[self.device_id][3] == 0:
                if self.midi_in is not None:
                    # close the MIDI device before trying to open it again
                    self.midi_in.Close()
                    del self.midi_in
                self.midi_in = pypm.Input(self.device_id)
                print("MIDI device selected: " + 
                        str(pypm.GetDeviceInfo(self.device_id)[1]))
                self.is_connected = True
        else:
            print("**** Invalid device! ********")
            self.is_connected = False

    def start(self):
        """
        Start polling
        Returns deferred
        """
        print("Starting MIDI loop")
        if self.is_connected:
            interval = 0.05
            return self._looping_call.start(interval)
        else:
            raise NotConnectedError("Not connected to any MIDI device!")
    
    def poll(self):
        """
        Here's how we poll
        """
        if self.midi_in.Poll():
            midi_events = self.midi_in.Read(1024)
            for midi_event in midi_events:
                print("GOT MIDI EVENT: {}".format(midi_event))
                self._call_callbacks(midi_event)

    def register_callback(self, callback):
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def _call_callbacks(self, event):
        """
        Called when a MIDI event occurs
        """
        for cb in self.callbacks:
            cb(event)

    def __del__(self):
        self.midi_in.Close()
        del self.midi_in
        pypm.Terminate()

if __name__ == "__main__":
    def _cb(event):
        if event[0][0] == 176:
            print("MIDI control: {}".format(event))

    try:
        device_id = int(sys.argv[-1])
    except:
        device_id = None
    midi_manager = MidiIn(device_id)
    midi_manager.register_callback(_cb)
    midi_manager.start()
    try:
        reactor.run()
    except KeyboardInterrupt:
        print "quit"
        reactor.stop()
