import json
import logging
import pathlib

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def create_variables_from_json(json_file_path):
    """this is an auxiliary function that automates the 
    reading of the config file. 

    Args:
        json_file_path (_type_): _description_

    Returns:
        _type_: _description_
    """    
    with open(json_file_path, 'r') as f:
        json_data = json.load(f)

    json_data["TENSILEDATA_DIR"] = pathlib.Path(json_data["TENSILEDATA_DIR"])
    
    if  json_data["UTDATA_FNAME"] == "":
        # look for file name
        if (csvpath := next(json_data["TENSILEDATA_DIR"].glob("*.csv"), None)) is None:
            raise(FileExistsError("No .csv file present!"))
        else:
            print(f"Found file: {csvpath}")
            json_data["UTDATA"] = pathlib.Path(csvpath)
    else:      
        json_data["UTDATA"] = json_data["TENSILEDATA_DIR"] / json_data["UTDATA_FNAME"]
    json_data["IMG_DIR"] = pathlib.Path(json_data["IMG_DIR"])
    return json_data

def check_folder_for_csv(folder_path:pathlib.Path):
    """this is an auxiliary function checks a folder for a single csv  file

    Args:
        folder_path (_type_): _description_

    Returns:
        _type_: _description_
    """    
    if (csvpath := next(folder_path.glob("*.csv"), None)) is None:
        raise(FileExistsError("No .csv file present!"))
    else:
        print(f"Found file: {csvpath}")
        UTDATA = pathlib.Path(csvpath)
    return UTDATA


def convert_labview_to_metainfo(in_fname:pathlib.Path,out_fname:pathlib.Path, img_ext:str="png"):
    """coverts the output file from labview to the "meta-data.txt" required by pydic

    Args:
        in_fname (pathlib.Path): input filename
        out_fname (pathlib.Path): output filename 
        img_ext (str): Image file extension 
    """    
    dfcols = ['ImgNo', "Timestamp", 'ElapsedTime']
    df = pd.read_csv(in_fname, delimiter="\t", header=None, names=dfcols)

    df['filename'] = df.ImgNo.apply(lambda x: f"Cam_{x:05d}.{img_ext}")

    df = df.loc[:, ['filename', "ElapsedTime"]]
    # The following mocks up the force 
    df['force'] = df['ElapsedTime'].round(decimals=0)

    df.columns= ['file', 'time(s)', 'force(N)']

    df.to_csv(out_fname, index=False, sep='\t')


def plot_synced_graph(time_offset, dic_df:pd.DataFrame, ut_df:pd.DataFrame):
    """plots the dic and tensile data to see if they correlate well
    
    Two plots are made:
    - one plot with the normalised force and the normalised strain
    - plot:
        - the force diff normalised wrt abs(max(force diff)
        - the strain diff normalised wrt abs(max(strain diff))

    TODO: I could use cross-correlation but this would require similar timestep. 
        
    Args:
        time_offset (float): Time offset in s (used only for the plot)
        dic_df (pd.DataFrame): dataframe obtained from dic
        ut_df (pd.DataFrame): dataframe obtained from imada
    """    
    # # this was commented out because the offset occurs outside 
    # dfCopy  = dic_df.copy()
    # dic_df.loc[:,"time_synced"] = dfCopy.loc[:,"time(s)"]-time_offset
    # axs = [axs]
    ts_ut = ut_df.time_s
    Fs_ut = ut_df.force_N
    ts_dic = dic_df["time_synced"]
    exx_dic = dic_df.e_xx
    fig, axs = plt.subplots(ncols=1,nrows=2,sharex=True)

    # plot 1
    axs[0].plot(ts_ut, Fs_ut/Fs_ut.max(), '.', label ="Normalised Force")
    axs[0].plot(ts_dic.iloc[:-1], exx_dic.iloc[:-1]/exx_dic.iloc[:-1].max(), '.',label ="Normalised strain ")
    axs[0].set_title(f"Normalised Forces (from Imada) and Strains (from dic)\n Used to determine time offset: {time_offset} (s)")

    # plot 2 with normalised diffs (the  )
    axs[1].plot(ts_ut.iloc[:-1],np.abs(np.diff(Fs_ut))/np.abs(np.diff(Fs_ut)).max(), label ="force diff")
    axs[1].plot(ts_dic.iloc[:-1], np.abs(np.diff(exx_dic))/np.abs(np.diff(exx_dic)).max(),label ="Normalised strain ")
    axs[1].set_xlabel("Time (s)")



# %% [markdown]
# # Resampling
# ## obsolete attempt with pandas.resample
# The following is an failed attempt to resampling the dataframe 
# on sub second time scale. 
# 
# Issues:
# - I could not obtain meaningful values when I resampled
#%%
# index_td = pd.to_timedelta(df_dic['time_synced'], unit ="s")
# # index_td = pd.to_datetime(df_dic['time_synced'], unit ="s")
# df_dict = df_dic.set_index(index_td )
# df_dict.resample('100ms',origin=0).interpolate('linear')


def resample_dic_df(df_dic:pd.DataFrame,  ts:np.ndarray)->pd.DataFrame:
    """resamples the DIC analysis dataframe, on another time vector.

    Args:
        df_dic (pd.DataFrame): DIC Dataframe 
        ts (np.ndarray): new time vector. eg: np.arange(0,14,step=0.5).

    Returns:
        pd.DataFrame: new DataFrame with results 
    """
    dss = []
    for columnname in df_dic.iloc[:,:4]:

        interp_data = np.interp(ts, df_dic['time_synced'],df_dic[columnname])
        ds_new = pd.Series(interp_data, index = ts, name=columnname)
        dss.append(ds_new)
    res_df = pd.concat(dss,axis=1)
    return res_df 

def resample_ut(df_ut:pd.DataFrame,  ts:np.ndarray)->pd.DataFrame:
    """resamples the IMADA M testing machine results, on another time vector.

    Args:
        df_ut (pd.DataFrame): imada ut machine Dataframe (columms: [force_N, disp_mm, time_s])
        ts (np.ndarray): new time vector. eg: np.arange(0,14,step=0.5).

    Returns:
        pd.DataFrame: new DataFrame with results 
    """
    assert all([df_ut.columns[k]== v  for  k, v in enumerate(['force_N', 'disp_mm', 'time_s'])]), "Columns in input Df should be ['force_N', 'disp_mm', 'time_s']"
    dss = []
    for columnname in df_ut.iloc[:,:2]:
        logging.debug(columnname)
        interp_data = np.interp(ts, df_ut['time_s'],df_ut[columnname])
        ds_new = pd.Series(interp_data, index = ts, name=columnname)
        dss.append(ds_new)
    res_df = pd.concat(dss,axis=1)
    return res_df

