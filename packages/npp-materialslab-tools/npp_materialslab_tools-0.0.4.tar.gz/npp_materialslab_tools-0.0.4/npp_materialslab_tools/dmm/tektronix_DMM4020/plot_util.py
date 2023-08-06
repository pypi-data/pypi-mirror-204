# this is a script for Tektronix DMM4020 Multimeter writen for a linux PC
#
# This is NOT COMPLETE YET. 
# 

#!/usr/bin/python
'''
    A simple script to draw a live graph 
    from the data output of a Tektronix DMM4020 Multimeter.

    Copyright (C) 2023  N. Papadakis
    Modified by  2013  JP Meijers
    
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
from collections import deque
from threading import Event
from time import sleep

# import sys, serial
import numpy as np
from matplotlib import pyplot as plt
from npp_materialslab_tools.dmm.tektronix_DMM4020._misc import (AnalogData,
                                                               AnalogPlot)

logging.basicConfig(level=logging.INFO)


def data_listener(strPort, analogData, ser):
    """DAta listener for Tektronix DMM 4020 

    Args:
        strPort (_type_): _description_
        analogData (_type_): _description_
        ser (_type_): _description_
    """    
  
    while True:
        try:
            ser.write("val?\n".encode())
            line = ser.read_all().decode()
            print(line)
            
            line_tuple = line.split()
            if(len(line_tuple)==2):
                value = float(line.split()[0])
                unit = line.split()[1]

                analogData.add(value, unit)
                
        except ValueError:
            pass
        except IndexError:
            pass


def data_listener_dummy( strPort:str, analogData, ser, 
        event:Event, update_interval:float=0.1, 
        fname:str=None):
    """Dummy data listener

    Args:
        strPort (_type_): _description_
        analogData (_type_): _description_
        ser (_type_): _description_
    TODO: save data to a file
    """    
    i = 0
    # initialising file for recording 
    file_object = None
    if fname is not None:
        fname_path = pathlib.Path(fname)
        fname_path.parent.mkdir(parents=True, exist_ok=True)
        file_object = open(fname_path,"w")
        file_object.write("no_meas\tvalue \tunits\n")
            
    # see https://superfastpython.com/stop-a-thread-in-python/ 
    # on mechanisms to stop events. 
    while not event.is_set():
        try:
            sleep(update_interval)
            
            # update values
            i = i+ 1
            value = np.sin(2*np.pi*(i % 100)/100)
            unit = "VDC"

            analogData.add(value, unit)
            # logging.info(f"{i}: {value} {unit}")
            if file_object:
                file_object.write(f"{i}\t{value}\t{unit}\n")

        except ValueError:
            pass
        except IndexError:
            pass
    # this is after the event is set 
    logging.info("Exiting thread")
    if  file_object:
        file_object.close()
        logging.info("File object closed")

# # main() function
# def main():
#     # expects 1 arg - serial port string
#     # if(len(sys.argv) != 2):
#     #     print ('Example usage: python showdata.py "/dev/tty.usbmodem411"')
#     #     exit(1)

#     #strPort = '/dev/tty.usbserial-A7006Yqh'
#     # strPort = sys.argv[1];
#     strPort = "COM4"

#     # plot parameters
#     analogData = AnalogData(x_tick_count)
#     analogPlot = AnalogPlot(analogData)

#     print ('plotting data...')

#     # open serial port
#     ser = serial.Serial(strPort, 19200)
#     line = ser.read_all().decode()

#     print(line)

#     thread = threading.Thread(target=data_listener,args=(strPort,analogData,ser))
#     thread.daemon = True
#     thread.start()

#     while True:
#         try:
#             analogPlot.update(analogData)
#             sleep(update_interval)


#         except KeyboardInterrupt:
#             print( 'exiting')
#             break
#     # close serial
#     ser.flush()
#     ser.close()


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

    # start data
    thread = threading.Thread(target=data_listener_dummy,
                              args=(strPort,analogData,ser, stopEvent,update_interval, fname))
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