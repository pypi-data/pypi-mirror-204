
import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class DICOffsetSelectorClass:
    def __init__(self, df_ut, df_dic):
        self.df_ut = df_ut.copy()
        self.df_dico = df_dic.copy()
        self.offset_value = 0

        self.root = tk.Tk()
        self.root.title("Data Series Offset")

        # self.fig = Figure(figsize=(5, 4), dpi=100)
        # self.ax = self.fig.add_subplot(111)
        self.fig, self.axs = plt.subplots(ncols=1,nrows=2,sharex=True,figsize=(5, 4), dpi=100)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.slider = tk.Scale(self.root, from_=-10, to=10, resolution=0.1, orient=tk.HORIZONTAL,
                               command=self.on_slider_changed)
        self.slider.pack(side=tk.BOTTOM, fill=tk.X)

        # self.plot_data(0)
        self.plot_synced_graph(0)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


    def plot_synced_graph(self, offset):
        """plots the dic and tensile data to see if they correlate well
        
        Two plots are made:
        - one plot with the normalised force and the normalised strain
        - plot:
            - the force diff normalised wrt abs(max(force diff)
            - the strain diff normalised wrt abs(max(strain diff))

        TODO: I could use cross-correlation but this would require similar timestep. 
            
        Args:
            offset (float): Time offset in s (used only for the plot)
            dic_df (pd.DataFrame): dataframe obtained from dic
            ut_df (pd.DataFrame): dataframe obtained from imada
        """    
        # # this was commented out because the offset occurs outside 
        # dfCopy  = dic_df.copy()
        # dic_df.loc[:,"time_synced"] = dfCopy.loc[:,"time(s)"]-time_offset
        # axs = [axs]
        ts_ut = self.df_ut.time_s.copy()
        Fs_ut = self.df_ut.force_N.copy()
        ts_dic = self.df_dico.loc[:,"time(s)"].copy()-offset
        exx_dic = self.df_dico.e_xx.copy()
        # fig, axs = plt.subplots(ncols=1,nrows=2,sharex=True)
        self.axs[0].clear()
        self.axs[1].clear()
        # plot 1
        self.axs[0].plot(ts_ut, Fs_ut/Fs_ut.max(), '.', label ="Normalised Force")
        self.axs[0].plot(ts_dic.iloc[:-1], exx_dic.iloc[:-1]/exx_dic.iloc[:-1].max(), '.',label ="Normalised strain ")
        self.axs[0].set_title(f"Normalised Forces (from Imada) and Strains (from dic)\n Used to determine time offset: {offset} (s)")

        # plot 2 with normalised diffs (the  )
        self.axs[1].plot(ts_ut.iloc[:-1],np.abs(np.diff(Fs_ut))/np.abs(np.diff(Fs_ut)).max(), label ="force diff")
        self.axs[1].plot(ts_dic.iloc[:-1], np.abs(np.diff(exx_dic))/np.abs(np.diff(exx_dic)).max(),label ="Normalised strain ")
        self.axs[1].set_xlabel("Time (s)")
        self.canvas.draw()

    def plot_data(self, offset):
        # self.ax.clear()
        # self.ax.scatter(self.df_ut["time_s"], self.df_ut["force_N"], label="df_ut (time_s, force_N)")
        # self.ax.scatter(self.df_dico["time(s)"]+ offset, self.df_dico["e_xx"] , label="df_dico (time(s), e_xx + offset)")
        # self.ax.set_xlabel("Time")
        # self.ax.set_ylabel("Value")
        # self.ax.legend(loc='upper right')
        self.axs[0].clear()
        self.axs[1].clear()
        self.df_dico.loc[:,"time_synced"] = self.df_dico.loc[:,"time(s)"].copy()-offset
        self.axs[0].plot(self.df_ut.time_s,self.df_ut.force_N, '.', label ="Normalised Force")
        self.axs[1].plot(self.df_dico["time_synced"][:-1], self.df_dico.e_xx[:-1], '.',label ="Normalised strain ")
        self.axs[1].set_xlabel("Time (s)")
        self.axs[1].set_ylabel("$e_{xx}$ ()")
        self.axs[0].set_ylabel("Force (N)")
        self.canvas.draw()

    def on_slider_changed(self, val):
        offset = float(val)
        # self.plot_data(offset)
        self.plot_synced_graph(offset=offset)

    def on_closing(self):
        self.offset_value = self.slider.get()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

