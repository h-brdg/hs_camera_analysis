#!/usr/bin/env python3

import os
import re

#%% misc
def strip_params(raw_str):
    c = r': (.*)'
    strip_str = re.search(c, raw_str)
    return strip_str.group(1)

def separate_size(raw_str):
    c = r'(\d+)x(\d+)'
    sep_str = re.search(c, raw_str)
    return sep_str.group(1, 2)

def get_params(lines_strip, param_key):
    list_rownum = [i for i, line_s in enumerate(lines_strip) if param_key in line_s]
    return strip_params(lines_strip[list_rownum[0]])

#%% read_conv_info
def read_conv_info(shot_no, tiff_dir):
    config_path = os.path.join(tiff_dir, str(shot_no)+'_tif.txt')
    with open(config_path, 'r', encoding='cp932') as ftxt:
        lines = ftxt.readlines()
#    print(lines)
    lines_strip = [line.strip() for line in lines ]
#    print(lines_strip)
    
#     list_rownum = [i for i, line_s in enumerate(lines_strip) if 'Frame_Rate' in line_s]
# #    print(list_rownum)
#     print(list_rownum[0])
#     print(lines_strip[list_rownum[0]])
    params_dict = {'frame_rate': 0,
                   'frame_size_x': 0,
                   'frame_size_y': 0,
                   'shutter_speed': 0,
                   'sensor_filter': 0,
                   'top_frame': 0,
                   'bottom_frame': 0
                   }
    try:
        params_dict['frame_rate'] = get_params(lines_strip, 'Frame_Rate')
        #print('Read Frame_Rate')
    except:
        print('Problem Reading Frame_Rate')
        
    try:
        params_dict['frame_size_x'] = separate_size(get_params(lines_strip, 'Frame_SRC_Size'))[0]
        #print('Read Frame_Size by MLink')
    except:
        try:
            params_dict['frame_size_x'] = separate_size(get_params(lines_strip, 'Frame_Size'))[0]
            #print('Read Frame_Size by HXLink')
        except:
            print('Problem Reading Frame_Size_x')

    try:
        params_dict['frame_size_y'] = separate_size(get_params(lines_strip, 'Frame_SRC_Size'))[1]
        #print('Read Frame_Size by MLink')
    except:
        try:
            params_dict['frame_size_y'] = separate_size(get_params(lines_strip, 'Frame_Size'))[1]
            #print('Read Frame_Size by HXLink')
        except:
            print('Problem Reading Frame_Size_x')

    try:
        params_dict['shutter_speed'] = get_params(lines_strip, 'ShutterSpeed ')
        #print('Read Shutter_Speed by MLink')
    except:
        try:
            params_dict['shutter_speed'] = get_params(lines_strip, 'Shutter_SRC_Speed')
            #print('Read Shutter_Speed by HXLink')
        except:
            print('Problem Reading Shutter_Speed')
            
    try:
        params_dict['sensor_filter'] = get_params(lines_strip, 'Sensor Filter')
        #print('Read Frame_Rate')
    except:
            print('Problem Reading Sensor Filter')
            
    try:
        params_dict['top_frame'] = get_params(lines_strip, 'TopFrame')
        params_dict['bottom_frame'] = get_params(lines_strip, 'BottomFrame')
    except:
            print('Problem Reading Frames')
    
    #print('Read params from ' + str(shot_no) + '_tif.txt: \n' + str(params_dict))
    return params_dict
    

#%%
if __name__ == "__main__":
    shot_no = 255704
    #shot_no = 252930
    tiff_dir = '/media/satoshi/SSD-ST/PRC/Data/Camera/tiff'
    print(read_conv_info(shot_no, tiff_dir))
