#!/usr/bin/env python3

"""
Reads the tiff file in [shot_no]_tif.zip

"""

import os
import zipfile
import numpy as np
import tifffile

def load_tiff(shot_no, tiff_dir, frame_tgt=0, num_frames=0):
    with zipfile.ZipFile(os.path.join(tiff_dir, str(shot_no) + '_tif.zip'), 'r') as zf:
        
        if (num_frames == 0):
            num_frames = len(zf.namelist())-frame_tgt
        
        img_list = []
        for i,fn in enumerate(range(frame_tgt, frame_tgt + num_frames)):
            target_tiff = str(shot_no) + '_' + str(fn).zfill(8) + '.tif'
            try:
                with tifffile.TiffFile(zf.open(target_tiff)) as tif:
                    img = tif.asarray()
                    
                    # print(str(img.shape))
                    #print(type(img))
                    #plt.imshow(img)
                    
                    img_list.append(img)
            except KeyError as ke:
                print('Error: ' + str(ke))
                break
    #img_array = np.array(img_list).transpose(1,2,0)
    img_array = np.array(img_list)
    return img_array

#%% Test
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import read_config_info
    shot_no = 256221
    frame_tgt=3000
    num_frames=1
    config_dict = read_config_info.read_config_info()
    tiff_dir = config_dict['tiff_dir']
    img_array = load_tiff(shot_no, tiff_dir, frame_tgt, num_frames)
    #img_array = tiff_reader(shot_no, tiff_dir)
    print(img_array.shape)
    print(img_array.dtype)
    plt.imshow(img_array[0,:,:])
