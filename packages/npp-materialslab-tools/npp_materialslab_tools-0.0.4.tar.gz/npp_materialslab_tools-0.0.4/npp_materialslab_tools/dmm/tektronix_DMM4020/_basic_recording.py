#%%
try:
    import serial
except ImportError:
    print("Probably pyserial is not installed.")
    print(" use conda or pip to install pyserial")
    print(" > conda install -c conda-forge pyserial")

import time
from typing import TextIO
import numpy as np
# %% [markdown]
# the Tektronix DMM4020 when it returns a value it sets


# %%
def record_from_DMM4020(
        fname:str|TextIO, n:int, 
        fs:float=1, 
        port:str="COM1", baudrate:int= 19200,
        verbose:bool=1):
    """Starts a recording session for a Tektronix DMM4020

    Args:
        fname (str|typing.TextIO) : Filenama or fileobject.
        n (int): number of data points (The duration in [seconds] is n/fs. )
        fs (float, optional): Sampling frequency in Hz. Defaults to 1.
        port (str, optional): . Defaults to "COM1".
        baudrate (int, optional): Baud rate. Defaults to 19200.
        verbose (bool, optioal): More verbose output. Defaults to True.
    """    
    # TODO see if it is poosible to envelope 
    # TODO SCPI Commands for fast rate
    # https://forum.tek.com/viewtopic.php?t=138561
    if isinstance(fname , str):
        file_object = open(fname, 'w')
    elif isinstance(fname , TextIO):
        file_object = fname
    dt = 1/fs
    print("Instructions: Press Ctrl+C to stop prematurely the loop!\n")
    # Append 'hello' at the end of file
    with serial.Serial(port=port,  baudrate=baudrate) as ser:
        try:
            for j in range(n):
                ser.write("val?\n".encode())
                data = ser.read_all().decode()
                dataline=data.split('\r')[0]
                data = parseline(dataline=dataline)
                if data.get('value') is not None:
                    str_toWrite = f"{j}\t {data.get('value')}\t {data.get('units')}\n"
                    file_object.write(str_toWrite)
                    if(verbose):
                        print(str_toWrite[:-1])
                time.sleep(dt)
        except KeyboardInterrupt:
            print ("Exiting Gratefully - because Ctrl-C was pressed")
            pass
    # Close the file
    file_object.close()



def parseline(dataline:str)->dict:
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


#%%
if __name__ == "__main__":
    fname = "sample101.txt"
    n=10000
    port= "COM4"
    baudrate= 19200
    record_from_DMM4020(fname=fname, n=n, fs=1,port=port , baudrate=baudrate)


# %%
