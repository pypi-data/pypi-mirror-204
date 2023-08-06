from collections import deque

import matplotlib.pyplot as plt
import numpy as np
import logging

# class that holds analog data for N samples
class AnalogData:
    """container for data from the Tektronix DMM4020 
    """    
    def __init__(self, maxLen:int):
        """Constructor 

        Args:
            maxLen (int): maximum queue length
        """     
        self.values = deque([0.0]*maxLen)
        self.unit = "Unit"
        self.maxLen = maxLen

        # internal variables for update
        self._min = 0
        self._max = 0
        self._flagUpdate = False
        self._flagNeedsInitialise = True

    def addToBuf(self, buf, val):
        """ ring buffer increases up to max length

        Args:
            buf (_type_): _description_
            val (_type_): _description_
        """        
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.pop()
            # TODO:when popping check the new range (smaller plot over time).
            buf.appendleft(val)

    

    def add(self, value:float, unit):
        """Add data and units, and updates min - internally

        Args:
            value (float): value 
            unit (_type_): units for measurement 
        """
        if self._flagNeedsInitialise:
            self.values = deque([value]*self.maxLen)
            self._flagNeedsInitialise = False
            self._flagUpdate = True
                    # internal variables for update
            # internal variables for update
            self._min = value
            self._max = value
            
        self.addToBuf(self.values, value)
        self.unit = unit
        if value >self._max :
            self._flagUpdate=True
            self._max= value
        if value <self._min :
            self._min= value
            self._flagUpdate=True
    
    @property
    def data_range(self):
        """returns a list with min max for consumption in ylims
        """        
        return [self._min, self._max]

    @property
    def is_update_required(self):
        """ notifies if update is required and resets the flag
        """    
        if self._flagUpdate:    
            self._flagUpdate= False
            return True
        return False

    
# plot class
class AnalogPlot:
    """Class for plotting data
    """    
    _delay_for_plot_refresh= 0.01
    def __init__(self, analogData:AnalogData, plt_config_kwargs:dict={}
                 ):
        """Constructor for object

        Args:
            analogData (AnalogData): _description_
        """       
        self._plt_config = plt_config_kwargs
        self.analogData = analogData
        plt.ion() 
        self.initialise_fig()
    
    def initialise_fig(self):
        plt_width = self._plt_config.get("plt_x",800)
        plt_height = self._plt_config.get("plt_y",600)
        plt_dpi = self._plt_config.get(" ",72) 
        plt_format = self._plt_config.get("plt_format",".")
        ylims = self._plt_config.get("ylims", None)
        #set plot size
        # self.fig = plt.figure(num=1,figsize=(plt_width/plt_dpi, plt_height/plt_dpi), dpi=plt_dpi)
        self.fig, self.ax = plt.subplots(nrows=1, ncols=1, 
                figsize=(plt_width/plt_dpi, plt_height/plt_dpi), dpi=plt_dpi,
                num=1)
        # set plot to animated
        plt.ion() 
        self.axline, = self.ax.plot(self.analogData.values, plt_format)
        if ylims is not None:
            plt.ylim(ylims)
        plt.ylabel(self.analogData.unit)
        plt.xlabel( "Time [# of measurements]")
    
    def update(self, analogData:AnalogData):
        """ update plot as new data are coming in

        Args:
            analogData (AnalogData): The container for the data from the Tektronix
        """        
        self.axline.set_ydata(analogData.values)
        if analogData.is_update_required:
            plt.ylim(analogData.data_range)
            plt.ylabel(analogData.unit) # there is no check for this one.
        plt.pause(self._delay_for_plot_refresh)
        plt.draw()