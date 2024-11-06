#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1
from tqdm import tqdm

from camera_reader_mt import camera_reader
from calc_int import calc_int
# import hampel_filter


def plot_camera_int_frame(shot_no, line_ch, frame_tgt, num_frames):
    camera_dict_int = calc_int(shot_no, line_ch, frame_tgt, num_frames)
    
    dir_out = os.path.join(camera_dict_int['result_dir'], 'int', str(shot_no) + '_ch' + str(line_ch))
    os.makedirs(dir_out, exist_ok=True)

#%%
    zaxis = np.linspace(0, len(camera_dict_int['data'][0,0,:]), len(camera_dict_int['data'][0,0,:])+1)
    xaxis = np.linspace(0, len(camera_dict_int['data'][0,:,0]), len(camera_dict_int['data'][0,:,0])+1)
    ppmm = 112/(int(camera_dict_int["diam_flange"]))  # mm per pixel
    # X axis ... 0 on the center line.
    xaxis = len(xaxis)/2 - xaxis
    # Convert to cm
    xaxis *= float(ppmm) / 10
    zaxis *= float(ppmm) / 10
    # Z axis ... 1100 cm at the corner.
    zaxis = zaxis + 1095 - zaxis[-1]
    
    # max intensity
    ymax = np.max(camera_dict_int['data'])
    print('ymax = ' + str(ymax))
    
#%% Hampel filter to detect outlier and set ymax accordingly
    # ymax, ymax_arg, hampel_fig = hampel_filter.filter_ymax(camera_dict['data'], hw_size=2, thr=3)
    # hampel_fig.savefig(os.path.join(dir_out, 'hampel_' + str(shot_no) + '_' + str(line_ch)))
    # hampel_fig.close()
    #ymax = 100000

#%% Save fig
    for i, img in tqdm(enumerate(camera_dict_int['data']),total = num_frames, desc='Saving figs...'):
        
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        
        # Draw the figure
        ax_img = ax.imshow(img, extent=[zaxis[0], zaxis[-1], xaxis[-1], xaxis[0]], vmax=ymax, vmin=0, cmap='jet')
        
        # Color bar
        divider = mpl_toolkits.axes_grid1.make_axes_locatable(ax)
        cax = divider.append_axes('right', size='4%', pad='2%')
        fig.colorbar(ax_img, cax=cax)
        
        # Title
        time_quot = int(((frame_tgt + i) // (int(camera_dict_int["frame_rate"])/100)) * 10) # quotient
        time_quot += 50 # TEX 10
        time_rem =  int((frame_tgt + i) % (int(camera_dict_int["frame_rate"])/100)) # remainder
        filler = len(str(camera_dict_int["frame_rate"]))
        ax.set_title('#'+str(shot_no)+'_ch' + str(line_ch) +'\n@' + str(time_quot) + ' ms + ' + str(time_rem).zfill(filler) + ' / ' + str(camera_dict_int["frame_rate"]) + " ms", fontsize=16)

        # Ticks
        ax.set_xticks([1060, 1070, 1080, 1090])
        ax.set_yticks([-10, -5, 0, 5, 10])
        
        # Labels
        # ax.set_xlabel('Z coord. (cm)')
        # ax.set_ylabel('X corrd. (cm)')
        
        # Fonts
        # fig.subplots_adjust(left=0.2, wspace=0.2)
        # font = {'family': 'Arial'}
        # plt.rc('font', **font)
        
        plt.savefig(os.path.join(dir_out, str(shot_no) + '_ch' + str(line_ch) + '_'  + str(frame_tgt + i).zfill(6) + 'by' + str(camera_dict_int['frame_rate'])))
        # plt.show()
        
        plt.close(fig)    
    
#%% Test
if __name__ == "__main__":
    import time
    
    time_sta = time.time()
    shot_li = [256221]
    frame_tgt=10000
    num_frames=100
    #flg_rot=False
    # line_li = ['all']
    line_li = ['1']
    for shot_no in shot_li:
        for line_ch in line_li:
            plot_camera_int_frame(shot_no, line_ch, frame_tgt, num_frames)
    time_end = time.time()
    print('Time spent: ' + str(time_end-time_sta) + ' (s)')
    #print(camera_dict['frame_rate'])
