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

try:
    import sys

    import serial
except ImportError:
    print("Probably pyserial is not installed.")
    print(" use conda or pip to install pyserial")
    print(" > conda install -c conda-forge pyserial")


import numpy as np
from matplotlib import pyplot as plt
from npp_materialslab_tools.dmm.tektronix_DMM4020._misc import (AnalogData,
                                                                AnalogPlot)
from npp_materialslab_tools.dmm.tektronix_DMM4020.monitorMeasurementClassDummy import \
    DMMDataCollectorAbstract

logging.basicConfig(level=logging.ERROR)


class DMMDataCollector(DMMDataCollectorAbstract):
    """DMM data Collector. Class for requesting and processing data from the DMM

    It is designed to run as a separate thread.   

    """    

    def request_data(self):
        """Method that requests data from the DMM 
        (overrides the abstract method)
        
        """        
        # logging.info("Call from DMMDataCollector")
        self.ser.write("val?\n".encode())

    def collect_and_parse_response(self):
        """Method that collects the data from the buffer and parses them. 
        (overrides the abstract method)

        Returns a dictionary.
       
        """   
        # update values
        datalines = self.ser.read_all().decode()
        # logging.info("Call from DMMDataCollectorDummy.collect_and_parse_response")
        dataline=datalines.split('\r')[0]
        logging.debug(dataline)
        
        data = self.parseline(dataline=dataline) 
        return data
    
    

class DMMDataCollector_static():
    # TODO: test
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
    
        # initialising file for recording 
        self.file_object = None
        if self._fname is not None:
            fname_path = pathlib.Path(self._fname)
            fname_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_object = open(fname_path,"w")
            self.file_object.write("no_meas\tvalue \tunits\n")

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
        i = 0
        while not self.__event.is_set():
                try:
                    #  sent message 
                    self.ser.write("val?\n".encode())
                    # wait until next refresh
                    sleep(self.update_interval)

                    datalines = self.ser.read_all().decode()
                    logging.info(datalines)
                    dataline=datalines.split('\r')[0]
                    print(dataline)
                    data = self.parseline(dataline=dataline)
                    if data.get('value') is not None:
                        i = i+ 1
                        value = data.get('value')
                        unit = data.get('units')

                        str_toWrite = f"{i}\t{value}\t{unit}\n"
                                      
                        logging.info(str_toWrite[:-1])

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


                


#==========================================================================================
# # main() function
def record_and_plot(
        strPort:str,
        fname:str, 
        x_tick_count = 1000, 
        plt_config_kwargs={}, 
        update_interval:float= 0.1
    ):
    """function for writing from DMM

    Args:
        strPort (str): _description_
        fname (str): _description_
        x_tick_count (int, optional): _description_. Defaults to 1000.
        plt_config_kwargs (dict, optional): _description_. Defaults to {}.
        update_interval (float, optional): _description_. Defaults to 0.1.
    """    
    # expects 1 arg - serial port string
    # if(len(sys.argv) != 2):
    #     print ('Example usage: python showdata.py "/dev/tty.usbmodem411"')
    #     exit(1)

    #strPort = '/dev/tty.usbserial-A7006Yqh'
    # strPort = sys.argv[1];
    
    stopEvent = Event()
    # plot parameters
    analogData = AnalogData(x_tick_count)
    analogPlot = AnalogPlot(analogData, plt_config_kwargs=plt_config_kwargs)

    print ('plotting data...')
    print ('Press Ctrl+C to stop!')

    # open serial port
    ser = serial.Serial(strPort, 19200)

    # dmm_mon = DMMDataCollector_static(
    dmm_mon = DMMDataCollector(
                analogData=analogData, 
                ser=ser, 
                event=stopEvent,
                update_interval=update_interval,
                fname=fname)


    line = ser.read_all().decode()
    print(line)

    thread = threading.Thread(target=dmm_mon.run,args=())
    thread.daemon = True
    thread.start()

    while True:
        try:
            analogPlot.update(analogData)
            sleep(update_interval)
            
        except KeyboardInterrupt:
            print( 'exiting')
            break
    # close serial
    ser.flush()
    ser.close()



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
    fname = "output/recording.txt"
    record_and_plot(fname=fname, x_tick_count=x_tick_count, 
         plt_config_kwargs=plt_config,
         update_interval = update_interval
       )