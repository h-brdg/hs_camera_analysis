#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import os

def search_section(shot_no, search_ini):
    #search_ini = configparser.ConfigParser()
    #search_ini.read('trim_info.ini', encoding='utf-8')
    tgt_section = 'DEFAULT'
    for section_name in search_ini.sections():
        try:
            if ((int(shot_no) >= int(search_ini[section_name]['shot_beg'])) and (int(shot_no) <= int(search_ini[section_name]['shot_end']))):
                tgt_section = section_name
        except: pass
    return tgt_section

def read_trim_info(shot_no, line_type, tiff_dir):
    trim_ini = configparser.ConfigParser()
    
    # Check if custom ini file exists
    if os.path.exists('trim_info_custom.ini'):
        ini_file = 'trim_info_custom.ini'
        trim_ini.read(ini_file, encoding='utf-8')
        info_sect = search_section(shot_no, trim_ini)
        if info_sect == 'DEFAULT':
            ini_file = 'trim_info.ini'
            trim_ini.read(ini_file, encoding='utf-8')
            print('Reading from trim_info.ini')
        else:
            print('Reading from trim_info_custom.ini')

        
    else:
        ini_file = 'trim_info.ini'
        trim_ini.read(ini_file, encoding='utf-8')
        info_sect = search_section(shot_no, trim_ini)
        print('Reading from trim_info.ini')
    
    if (line_type=='all'):
        (info_left, info_right, info_top, info_bottom, rot_deg, tra_x, tra_y) = ('left_4', 'right_4', 'top', 'bottom', 'rot_deg_ch1', 'tra_x_ch1', 'tra_y_ch1')
    elif (line_type=='4'): #n21ps
        (info_left, info_right, info_top, info_bottom, rot_deg, tra_x, tra_y) = ('left', 'right', 'top_ch4', 'bottom_ch4', 'rot_deg_ch4', 'tra_x_ch4', 'tra_y_ch4')
    elif (line_type=='3'): #natom
        (info_left, info_right, info_top, info_bottom, rot_deg, tra_x, tra_y) = ('left', 'right', 'top_ch3', 'bottom_ch3', 'rot_deg_ch3', 'tra_x_ch3', 'tra_y_ch3')
    elif (line_type=='2'): #hb
        (info_left, info_right, info_top, info_bottom, rot_deg, tra_x, tra_y) = ('left', 'right', 'top_ch2', 'bottom_ch2', 'rot_deg_ch2', 'tra_x_ch2', 'tra_y_ch2')
    elif (line_type=='1'): #ha
        (info_left, info_right, info_top, info_bottom, rot_deg, tra_x, tra_y) = ('left', 'right', 'top_ch1', 'bottom_ch1', 'rot_deg_ch1', 'tra_x_ch1', 'tra_y_ch1')
    
    tra_dict = {'diam_flange':trim_ini[info_sect]['diam_flange'],
                'left':trim_ini[info_sect][info_left],
                'right':trim_ini[info_sect][info_right],
                'top':trim_ini[info_sect][info_top],
                'bottom':trim_ini[info_sect][info_bottom],
                'rot_90':trim_ini[info_sect]['rot_90'],
                'rot_deg':trim_ini[info_sect][rot_deg],
                'tra_x':trim_ini[info_sect][tra_x],
                'tra_y':trim_ini[info_sect][tra_y]}
    #print(tra_dict)
    return(tra_dict)

#%% Test
if __name__ == "__main__":
    import read_config_info
    shot_no = 252930
    line_ch= 'all'
    config_dict = read_config_info.read_config_info()
    tiff_dir = config_dict['tiff_dir']
    print('tra_dict: ' + str(read_trim_info(shot_no, line_ch, tiff_dir)))

