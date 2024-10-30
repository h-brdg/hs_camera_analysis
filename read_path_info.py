import configparser
import os
#import from find_mount_point import find_mount_point

def read_path_info():
    try:
        config_ini = configparser.ConfigParser()
        config_ini.read('camera_config.ini', encoding='utf-8')
        config_dict = {'data_dir': config_ini['Paths']['data_dir'],
                       'tiff_dir': config_ini['Paths']['tiff_dir'],
                       'module_dir': config_ini['Paths']['module_dir'],
                       'result_dir': config_ini['Paths']['result_dir']}
    except:
        print('Problem reading camera_config.ini')
        config_dict = {}
    return config_dict

'''
def get_config():
    mp_path = find_mount_point()
    config_dict = read_path_info()
    for key in config_dict.keys():
        config_dict[key] = os.path.join(mp_path, config_dict[key])
    return config_dict
'''

if __name__ == '__main__':
    print(read_path_info())
#    print(get_config())

