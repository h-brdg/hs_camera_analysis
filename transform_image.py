import numpy as np
import cv2

import read_coeff_info
import read_trim_info


def transform_image(shot_no, line_ch, tiff_dir, img_array, flg_rot):
    
    #(left, right, top, bottom, rot_90, rot_deg, tra_x, tra_y) = read_trim_info.read_trim_info(shot_no, line_ch, tiff_dir)
    tra_dict = read_trim_info.read_trim_info(shot_no, line_ch, tiff_dir)
    (left, right, top, bottom, rot_90, rot_deg, tra_x, tra_y) = (tra_dict['left'], tra_dict['right'], tra_dict['top'], tra_dict['bottom'], tra_dict['rot_90'], tra_dict['rot_deg'], tra_dict['tra_x'], tra_dict['tra_y'])
    #%% Rotate
    img_array = np.rot90(img_array, int(rot_90), axes=(1,2))
    
    if (flg_rot):
        frames, rows, cols, = img_array.shape
        mat_rot = cv2.getRotationMatrix2D(center=[(int(left)+int(right))/2, (int(top)+int(bottom))/2], angle=float(rot_deg), scale=1)
        mat_tra = np.array([[1, 0, float(tra_x)],
                       [0, 1, float(tra_y)]], dtype=float)
        for i in range(frames):
            img_array[i,:,:] = cv2.warpAffine(img_array[i,:,:], mat_rot, (cols,rows), flags=cv2.INTER_CUBIC) #INTER_LANCZOS4,INTER_NEAREST,INTER_CUBIC 	
            img_array[i,:,:] = cv2.warpAffine(img_array[i,:,:], mat_tra, (cols,rows), flags=cv2.INTER_CUBIC)
    
    #%% Trim
    img_array = img_array[:,int(top):int(bottom), int(left):int(right)]
    
    #%% Flip
    if (line_ch == '1' or line_ch == '3'):
        img_array = np.flip(img_array, axis=1)
    
    #%% Coeff
    coeff = read_coeff_info.read_coeff_info(shot_no, line_ch, tiff_dir)
    img_array = img_array*coeff
      
    #%% Return
    return img_array, tra_dict, coeff
