# -*- coding: utf-8 -*-

import read_conv_info
import configparser

def search_section(shot_no, search_ini):
    #search_ini = configparser.ConfigParser()
    #search_ini.read('coeff_info.ini', encoding='utf-8')
    tgt_section = 'DEFAULT'
    for section_name in search_ini.sections():
        try:
            if ((int(shot_no) >= int(search_ini[section_name]['shot_beg'])) and (int(shot_no) <= int(search_ini[section_name]['shot_end']))):
                tgt_section = section_name
        except: pass
    return tgt_section

def read_coeff_info(shot_no, line_ch, tiff_dir):
    
    #%% Read Params
    cam_params = read_conv_info.read_conv_info(shot_no, tiff_dir)
    frame_rate = int(cam_params['frame_rate'])
    shutter_speed = cam_params['shutter_speed']
    
    coeff_ini = configparser.ConfigParser()
    coeff_ini.read('coeff_info.ini', encoding='utf-8')

    info_sect = search_section(shot_no, coeff_ini)
#    frame_size_x = int(cam_params['frame_size_x'])
#    frame_size_y = int(cam_params['frame_size_y'])
    
    #%% Coeff
    
    if shutter_speed == 'OPEN':
        shutter_coeff = 1
    else:
        shutter_coeff = 1 #temp

    # Camera relative response coefficient
    if line_ch == "4": # CH4
        #response_coeff = 1/(0.535*0.75)
        #response_coeff = 1 / 12.79
        response_rate = coeff_ini[info_sect]['response_rate_ch4']
    elif line_ch == "3": # CH3
        #response_coeff = 1/(0.119*1)
        #response_coeff = 1 / 78.63
        response_rate = coeff_ini[info_sect]['response_rate_ch3']
    elif line_ch == "2": # CH2
        #response_coeff = 1/(0.881*1)
        #response_coeff = 1 / 25.28
        response_rate = coeff_ini[info_sect]['response_rate_ch2']
    elif line_ch == "1": # CH1, ND Filter OD=0.8
        #response_coeff = 1/(0.850*pow(10, -0.8)*0.75)
        #response_coeff = 1 / 2.57
        response_rate = coeff_ini[info_sect]['response_rate_ch1']
    elif line_ch == "all":
        #response_coeff = 1
        response_rate = coeff_ini[info_sect]['response_rate']
      
    coeff = (1/float(response_rate))*shutter_coeff*(frame_rate/1000)
    # (frame_rate/1000): Relative to 1000 fps
      
    #%% Return
    return coeff

#%% Test
if __name__ == "__main__":
    import read_config_info
    shot_no = 252930
    line_ch = '1'
    config_dict = read_config_info.read_config_info()
    tiff_dir = config_dict['tiff_dir']
    print('coeff: ' + str(read_coeff_info(shot_no, line_ch, tiff_dir)))
