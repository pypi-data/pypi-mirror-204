# TODO: Consider the following:
#    - Create an abstract DMMDataCollector class with the following methods
#       - init
#       - init_File    
#       - parseline
#       - requestdata (override)
#       - collect_and_parse_response (override)
#   - Child classes:
#       - DMMDataCollectorDummy
#       - DMMDataCollector4020
#
#
# This is NOT COMPLETE YET. 
# 


#!/usr/bin/python
'''
    A simple script to draw a live graph 
    from the data output of a Tektronix DMM4020 Multimeter.

    Copyright (C) 2023  N. Papadakis
    Modified:  2013  JP Meijers script
    
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
Sources: 
    http://stackoverflow.com/questions/18791722/can-you-plot-live-data-in-matplotlib
    https://gist.github.com/electronut/5641933
TODO: 
    h5py for logging on disk
'''

import logging
import pathlib
import threading
# from collections import deque
from threading import Event
from time import sleep

# import sys, serial
import numpy as np
from matplotlib import pyplot as plt
from npp_materialslab_tools.dmm.tektronix_DMM4020._misc import (AnalogData,
                                                               AnalogPlot)

logging.basicConfig(level=logging.INFO)



class DMMDataCollectorAbstract():
    # TODO: complete and test this class
    # TODO: see **abc** module AbstractClass and @abstractmethod
    # 
    # The idea is to make Dummy and DMM4020 to inherit from this class
    _meas_cntr=0 # measurement counter
    def __init__(self,
            analogData, ser, 
            event:Event, update_interval:float=0.1, 
            fname:str=None) -> None:
        self.ser = ser 
        self.analogData = analogData
        self.__event = event
        self.update_interval= update_interval
        self._fname = fname
        if fname:
            self.init_file()

    def init_file(self):
        """method for initialising file if required
        """        
        # initialising file for recording 
        self.file_object = None
        if self._fname is not None:
            fname_path = pathlib.Path(self._fname)
            fname_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_object = open(fname_path,"w")
            self.file_object.write("no_meas\tvalue \tunits\n")

    def request_data(self):
        """abstract method. Needs to be overriden in child classes
        e.g.:
        self.ser.write("val?\n".encode())
        """        
        # logging.debug("Call from DMMDataCollectorAbstract")
        # 
        pass

    def collect_and_parse_response(self):
        """abstract method. Needs to be overriden in child classes
        e.g.:
            datalines = self.ser.read_all().decode()
            logging.info(datalines)
            dataline=datalines.split('\r')[0]
            data = self.parseline(dataline=dataline)        
        """   
        # logging.debug("Call from DMMDataCollectorAbstract.collect_and_parse_response")
        value = None
        units = None
        return {"value": value, "units": units}
    
    def parseline(self, dataline:str)->dict:
        """parses one line of output from the TektronixDMM4020

        Args:
            dataline (str): one data line (after removing \r\n)

        Returns:
            dict: {"value", "units"}
        """    

        # data = ser.read_all().decode()
        # dataline = data.split('\r')[0]
        data_units = dataline.split(" ")
        try:
            value = np.float64(data_units[0])
            units=data_units[1].strip()
        except ValueError:
            value = None
            units = "Value Error"

        return {"value": value, "units": units}

    def run(self):
        self._meas_cntr = 0
        logging.info("starting thread")
        while not self.__event.is_set():
                try:
                    #  sent message 
                    self.request_data()
                    # wait until next refresh
                    sleep(self.update_interval)

                    data = self.collect_and_parse_response()

                    if data.get('value') is not None:
                        self._meas_cntr = self._meas_cntr+ 1
                        value = data.get('value')
                        unit = data.get('units')

                        str_toWrite = f"{self._meas_cntr}\t{value}\t{unit}\n"
                                      
                        logging.debug(str_toWrite[:-1])

                        self.analogData.add(value, unit)
                        if self.file_object:
                            self.file_object.write(str_toWrite)

                except ValueError:
                    pass
                except IndexError:
                    pass
        # this is after the event is set 
        logging.info("Exiting thread")
        if  self.file_object:
            self.file_object.close()
        logging.info("File object closed.")


class DMMDataCollectorDummy(DMMDataCollectorAbstract):
    """Dummy DMM data generator to simulate the collection process when DMM is not present 
     
    This is for development purposes only
    """    
    

    def request_data(self):
        """abstract method. Needs to be overriden in child classes
        e.g.:
        self.ser.write("val?\n".encode())
        """        
        logging.debug("Call from DMMDataCollector")
        # 
        pass

    def collect_and_parse_response(self):
        """abstract method. Needs to be overriden in child classes
        e.g.:
            datalines = self.ser.read_all().decode()
            logging.info(datalines)
            dataline=datalines.split('\r')[0]
            data = self.parseline(dataline=dataline)        
        """   
        # logging.debug("Call from DMMDataCollectorDummy.collect_and_parse_response")

        # update values
        
        value = np.sin(2*np.pi*(self._meas_cntr % 100)/100)
        units = "VDC"
        return {"value": value, "units": units}
    
    

def record_and_plot_dummy(fname:str, 
            x_tick_count = 1000, 
            plt_config_kwargs={}, 
            update_interval:float= 0.1
        ):
    # === 
    stopEvent = Event()
    strPort = None
    ser = None
    # plot parameters
    analogData = AnalogData(x_tick_count)
    analogPlot = AnalogPlot(analogData, plt_config_kwargs=plt_config_kwargs)
            # plt_height=plt_y, plt_width=plt_x, plt_dpi=dpi, 
            # plt_format=plt_format, ylims=ylims)

    print ('plotting data...')
    print ('Press Ctrl+C to stop!')

    dmm_mon = DMMDataCollectorDummy(
                analogData=analogData, 
                ser=ser, 
                event=stopEvent,
                update_interval=update_interval,
                fname=fname)
    # start data
    thread = threading.Thread(target=dmm_mon.run, args=())
    thread.daemon = True
    thread.start()

    while True:
        try:
            analogPlot.update(analogData)
            sleep(update_interval)

        except KeyboardInterrupt:
            # Check this question 
            # https://stackoverflow.com/questions/292095/polling-the-keyboard-detect-a-keypress-in-python
            stopEvent.set()
            print( 'Attempting to exit....')
            thread.join()
            print( 'Thread Closed gracefully')
            break
    # # close serial
    # ser.flush()
    # ser.close()

# call main
if __name__ == '__main__':
    #X axis
    #Remeber that the time per tick is the rate at which the multimeter samples
    x_tick_count = 1000
    #GUI refresh time in seconds
    update_interval = 0.5
    plt_config = {
        "x_tick_count": x_tick_count,
        "plt_x":800, "plt_y":600, 
        "dpi":72, 
        "plt_format":".", 
        "ylims" : None
    }
    fname = "recording.txt"
    record_and_plot_dummy(fname=fname, x_tick_count=x_tick_count, 
         plt_config_kwargs=plt_config,
         update_interval = update_interval
       )