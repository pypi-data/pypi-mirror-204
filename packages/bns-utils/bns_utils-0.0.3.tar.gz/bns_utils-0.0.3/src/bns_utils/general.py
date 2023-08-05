import matplotlib.pyplot as plt 
from cycler import cycler
import matplotlib
from tqdm import tqdm
import ipywidgets as widgets
from ipywidgets import interact
import glob
import pandas as pd
import os
from scipy.signal import butter, filtfilt

#BNS utility functions

#setting the figure paramters 
plt.rcParams['figure.figsize'] = [10, 6]
plt.rcParams['figure.dpi'] = 100 # 200 e.g. is really fine, but slower
plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'Trebuchet MS'

#setting the color parameters
matplotlib.rcParams['axes.prop_cycle'] = cycler('color', ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])


def concat_csv_IP21_data(path):

    '''
    Documentation:

    Parameters:
    path: the path to the folder where the csv files are located

    Information:
    This function is used to concatenate all csv's in the same path into one pandas dataframe.
    It used to concatenate data that is pulled using a powershell script.
    Each csv needs to consist of two columns: TS and Value.
    The TS column needs to be in the format of: 2020-01-01 00:00:00
    The Value column needs to be in the format of: 0.0

    Returns:
    The function will return a pandas dataframe.
    The dataframe will have the index as the TS column and the columns will be the names of the csv files.
    The values will be the values of the Value column.
    The dataframe will be saved as a csv file in the same path as the csv files with the name IP21_data_Concat.csv

    Example:

    import BNS_utils as BNS
    DF = BNS.concat_csv_IP21_data(path)

    '''
    extension = 'csv'
    all_files = [i for i in glob.glob('*.{}'.format(extension))]
    DF = pd.DataFrame()
    os.chdir(path)
    for file in tqdm(all_files):
        #read and concatenate the data
        col_name = file[:-4]
        df = pd.read_csv(file)
        df['TS'] = pd.to_datetime(df['TS'])
        df.rename(columns = {'Value':col_name},inplace=True)
        df.set_index('TS',inplace=True)
        DF = pd.concat([DF,df],axis=1)
        #now I will remove the concatenated file
        os.remove(file)
    DF.to_csv('IP21_data_Concat.csv')
    return DF

# This function is going to be a filter for high frequency noise using the butterworth filter
# the sampling frequncy is specified in seconds and the cutoff frequency is specified in Hz


def butterworth_filter(data, sampling_frequency, cutoff_frequency, order):

    '''
    Documentation:

    Parameters:
    data: the data that needs to be filtered
    sampling_frequency: the sampling frequency of the data
    cutoff_frequency: the cutoff frequency of the filter
    order: the order of the filter

    Information:
    This function is used to filter high frequency noise from the data.
    The filter is a butterworth filter.

    Returns:
    The function will return a pandas dataframe.
    The dataframe will have the same index as the input data.
    The dataframe will have the same columns as the input data.
    The dataframe will have the filtered data.

    Example:

    import BNS_utils as BNS
    DF = BNS.butterworth_filter(data, sampling_frequency, cutoff_frequency, order)

    '''
    nyq = 0.5 * sampling_frequency
    normal_cutoff = cutoff_frequency / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

# This function will plot x and y data using pandas dataframes
# the x data will be the index of the dataframe
# the y data will be the columns of the dataframe
# the x data must be in datetime format 
# the y data must be in float format
# the function will allow specification of a widget which specifies the columns to plot
# the function will allow specification of a widget which specifies the start and end date of the plot

def plot_x_y_data(data, widget = False, start_date = None, end_date = None):

    '''
    Documentation:

    Parameters:
    data: the data that needs to be plotted
    widget: the widget that needs to be used to select the columns to plot
    start_date: the start date of the plot
    end_date: the end date of the plot

    Information:
    This function is used to plot x and y data using pandas dataframes.
    The x data will be the index of the dataframe.
    The y data will be the columns of the dataframe.
    The x data must be in datetime format.
    The y data must be in float format.
    The function will allow specification of a widget which specifies the columns to plot.
    The function will allow specification of a widget which specifies the start and end date of the plot.

    Returns:
    The function will return a plot.

    Example:

    import BNS_utils as BNS
    BNS.plot_x_y_data(data, widget = False, start_date = None, end_date = None)

    '''

    matplotlib.rcParams['figure.figsize'] = [16, 6]
    matplotlib.rcParams['figure.dpi'] = 100 # 200 e.g. is really fine, but slower
    matplotlib.rcParams['font.size'] = 14
    matplotlib.rcParams['font.family'] = 'Trebuchet MS'
    matplotlib.rcParams['axes.prop_cycle'] = cycler('color', ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
    #if the widget is not specified then I will create a widget for the user to select the columns to plot
    if widget == False:
        widget = widgets.SelectMultiple(
            options=data.columns,
            value=[data.columns[0]],
            #rows=10,
            description='Columns',
            disabled=False
        )
    #if the start and end date are not specified then I will create a widget for the user to select the start and end date
    if start_date == None:
        start_date = widgets.DatePicker(
            description='Start Date',
            disabled=False
        )
    if end_date == None:
        end_date = widgets.DatePicker(
            description='End Date',
            disabled=False
        )
    #now I will create the plot
    def plot_data(widget, start_date, end_date):
        #print(start_date,end_date,type(widget[0]))
        data[widget[0]][start_date:end_date].plot()
        plt.legend(widget)
        plt.show()

    #now I will create the interactive plot
    interact(plot_data, widget = widget, start_date = start_date, end_date = end_date)
