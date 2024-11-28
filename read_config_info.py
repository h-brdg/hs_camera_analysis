import configparser
import os
#import from find_mount_point import find_mount_point

def read_config_info():
    try:
        config_file = "camera_config_custom.ini" if os.path.exists("camera_config_custom.ini") else "camera_config.ini"
        config_ini = configparser.ConfigParser()
        config_ini.read(config_file, encoding='utf-8')
        config_dict = {'data_dir': config_ini['Paths']['data_dir'],
                       'tiff_dir': config_ini['Paths']['tiff_dir'],
                       'module_dir': config_ini['Paths']['module_dir'],
                       'result_dir': config_ini['Paths']['result_dir'],
                       'memmap_dir': config_ini['Paths']['memmap_dir'],
                       'mem_limit_size': config_ini['Settings']['mem_limit_size']
                      }
    except:
        print('Problem reading camera_config.ini')
        config_dict = {}
    return config_dict

'''
def get_config():
    mp_path = find_mount_point()
    config_dict = read_config_info()
    for key in config_dict.keys():
        config_dict[key] = os.path.join(mp_path, config_dict[key])
    return config_dict
'''

if __name__ == '__main__':
    print(read_config_info())
#    print(get_config())

