import os
from treelib import Tree, Node 
import numpy as np
import McsPy.McsCMOSMEA as McsCMOSMEA
from tqdm import tqdm
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

def frame_ref_to_onset(frame_ref, first_onset_index = 184, visualize_window = (250_000,350_000), stimulus_interval = 60, on_duration = 30, sampling_rate = 20000,overlay_split_num = 5):
    plt.rcParams['figure.figsize'] = [30, 5]
    def frame_ref_to_onset_plot(frame_ref = frame_ref, first_onset_index = first_onset_index, stimulus_interval = stimulus_interval, on_duration = on_duration, sampling_rate = sampling_rate, overlay_split_num = overlay_split_num, find_first_onset = True, visualize_window = visualize_window):
        '''
        Convert frame_ref to onset_index
        input:
            frame_ref: 2d array, first row is the light, second row is the frame
            first_onset_index: the index of the first onset, it needs to be manually adjusted
            stimulus_interval: the interval between two stimulus in a unit of frame number
            sampling_rate: the sampling rate of the frame_ref
        output:
            It plots the frame_ref and the onset_index with index number
        return: 
            onset_index: the index of all onsets in a unit of sampling number according to sampling_rate
            off_set_index: the index of all offsets in a unit of sampling number according to sampling_rate
            peaks: the index of all frames in a unit of sampling number according to sampling_rate
            first_onset_index: the index of the first onset
        '''
        prominence = 0.5 * max(frame_ref[1])
        distance = sampling_rate / (stimulus_interval + 10)
        peaks, _ = find_peaks(frame_ref[1], prominence=prominence,distance=distance)
        onset_index = peaks[first_onset_index:][::stimulus_interval] # the index of all onsets in a unit of sampling number according to sampling_rate
        offset_index = peaks[first_onset_index + on_duration:][::stimulus_interval]
        
        # lable the peaks with index number
        scale_factor = max(frame_ref[1])/max(frame_ref[0])
        overlay_factor = 0.03 * max(frame_ref[1]) # to avoid overlap of labels

        if find_first_onset:
            for i, peak in enumerate(peaks):
                if i > 2:
                    plt.text(peak, frame_ref[1][peak]+ i % overlay_split_num * overlay_factor, str(i), fontsize=6)
        
        plt.plot(frame_ref[1])
        plt.plot(frame_ref[0]*scale_factor)
        plt.plot(peaks, frame_ref[1][peaks], "x")
        
        if not find_first_onset:
            plt.plot(onset_index, frame_ref[0][onset_index]*scale_factor, "x")
            plt.plot(offset_index, frame_ref[0][offset_index]*scale_factor, "x")

            for i, onset in enumerate(onset_index):
                if i > 1:
                    plt.text(onset, frame_ref[0][onset]*scale_factor+ i % overlay_split_num * overlay_factor, str(i), fontsize=6)
        if visualize_window[1] != 0:
            plt.xlim(visualize_window)
        plt.show()
        return onset_index, offset_index, peaks, first_onset_index
    
    test_light_ref = frame_ref[:,0:visualize_window[1]]
    frame_ref_to_onset_plot(test_light_ref, first_onset_index=0) # find the first onset index by showing the plot indexed frames from 0
    frame_ref_to_onset_plot(test_light_ref, first_onset_index=first_onset_index, find_first_onset=False) # validate the position of the first onset index by showing the plot indexed frames from first_onset_index
    onset_index, offset_index, peaks, first_onset_index = frame_ref_to_onset_plot(frame_ref, first_onset_index=first_onset_index, find_first_onset=False, visualize_window= (0,0))
    plt.rcdefaults()
    return onset_index, offset_index, peaks, first_onset_index



def load_light_ref(filepath, sampling_rate=2000):
    ''' load light reference from .cmcr file
    filepath: path to the .cmcr or .cmtr file
    sampling_rate: sampling rate of the light reference
    '''
    raw_data = McsCMOSMEA.McsData(filepath)
    light_ref = raw_data.Acquisition.Analog_Data.ChannelData_1[:,::sampling_rate]
    return light_ref

def load_raw_data(filepath):
    ''' load raw data from .cmcr or .cmtr file
    filepath: path to the .cmcr or .cmtr file'''
    raw_data = McsCMOSMEA.McsData(filepath)
    return raw_data

def import_cmtr_firing_rate(filename, bin_size = 100): 
    """Import a .cmtr file and return a dictionary of units holding the timestamps and waveforms.
    :param filename: The path to the .cmtr file.
    :return: A dictionary of units holding the timestamps and waveforms.

    Note: 
    1. This function is used for GUI, where is named as import_cmtr_gui
    2. interval is set to 100ms, which is 10Hz
    3. Time scale of timestamps is in nanoseconds and bin_size is defined in milliseconds
    """
    all_units = {}
    processed = McsCMOSMEA.McsData(filename)

    def event_rate_in_interval(timestamps, length, interval):
        bins = np.arange(0, length, interval)
        hist, _ = np.histogram(timestamps, bins=bins)
        event_rate = hist / interval *1_000_000
        return event_rate

    for unit in tqdm(range(processed.Spike_Sorter.Units.shape[0])):
        data = eval("np.array(processed.Spike_Sorter.Unit_" + str(unit+1)+".get_peaks_timestamps())")
        data = event_rate_in_interval(data, length = processed.attributes["LB.RecordingDuration"], interval=bin_size * 1000) # 100ms interval, 10 hz
        col = eval("processed.Spike_Sorter.Unit_" + str(unit+1) + ".attributes['Column']")
        row = eval("processed.Spike_Sorter.Unit_" + str(unit+1) + ".attributes['Row']")
        waveform = eval("processed.Spike_Sorter.Unit_" + str(unit+1) + ".get_peaks_cutouts().T.mean(axis=1)")
        all_units[str(unit+1)] = {"unitID": unit+1, "data": data, "col": col, "row": row, \
            "waveform": waveform, "filename": filename, "globalID": -1}
    return all_units


def import_cmtr_raw(filename):
    """Import a .cmtr file and return a list of units holding the timestamps and waveforms.
    :param filename: The path to the .cmtr file.
    :return: A list of units holding the timestamps and waveforms.
    """
    all_units = {"units_data":[], "meta_data":[]}
    processed = McsCMOSMEA.McsData(filename)
    for unit in tqdm(range(processed.Spike_Sorter.Units.shape[0])):
        data = eval("np.array(processed.Spike_Sorter.Unit_" + str(unit+1)+".get_peaks_timestamps())")
        col = eval("processed.Spike_Sorter.Unit_" + str(unit+1) + ".attributes['Column']")
        row = eval("processed.Spike_Sorter.Unit_" + str(unit+1) + ".attributes['Row']")
        waveform = eval("processed.Spike_Sorter.Unit_" + str(unit+1) + ".get_peaks_cutouts().T.mean(axis=1)")
        all_units["units_data"].append({"unitID": unit+1, "data": data, "col": col, "row": row, \
            "waveform": waveform, "filename": filename, "globalID": -1})
    all_units["meta_data"].append({"analog":None})
    return all_units


def get_file_list(directory, file_extension=".pkl"):
    """
    Get the list of files with a specific extension in a directory and its subdirectories.
    :param directory: The directory to search for files.
    :param file_extension: The file extension to search for.
    :return: A list of file names with their absolute paths.
    """

    # Create an empty list to store the file names and their absolute paths
    file_list = []
    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Get the absolute path of the file
            abs_path = os.path.abspath(os.path.join(root, file))
            
            # Add the file name and its absolute path to the list
            if file.endswith(file_extension):
                file_list.append( abs_path)

    return file_list

def dict_to_tree(data, parent_id=None, tree=None):
    """
    Convert a dictionary to a tree.
    :param data: The dictionary to convert.
    :param parent_id: The parent node id.
    :param tree: The tree object.
    :return: The tree object.

    # Convert the nested dictionary to a tree structure diagram
    tree = dict_to_tree(nested_dict)

    # Display the tree structure diagram
    tree.show()
    """

    if tree is None:
        tree = Tree()
        root_id = "root"
        tree.create_node(tag="Root", identifier=root_id)
        return dict_to_tree(data, parent_id=root_id, tree=tree)

    for key, value in data.items():
        node_id = f"{parent_id}.{key}" if parent_id else key
        tag = f"{key} ({type(value).__name__}"
        
        if isinstance(value, (list, tuple, np.ndarray)):
            tag += f", length: {len(value)}"
        elif isinstance(value, dict):
            tag += f", length: {len(value)}"
        elif isinstance(value, str):
            tag += f", length: {len(value)}"
            tag += f", value: {value}"
        elif isinstance(value, (int, float)):
            tag += f", value: {value}"
        
        tag += ")"
        
        tree.create_node(tag=tag, identifier=node_id, parent=parent_id)
        
        if isinstance(value, dict):
            dict_to_tree(value, parent_id=node_id, tree=tree)

    return tree


def func3():
    pass
