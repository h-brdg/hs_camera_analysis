#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1
from tqdm import tqdm

from calc_avg import calc_avg
# import hampel_filter


def plot_camera_int_frame(shot_no, line_ch, frame_tgt, num_frames, avg_time):
    camera_dict_int_avg = calc_avg(shot_no, line_ch, frame_tgt, num_frames, avg_time)
    
    dir_out = os.path.join(camera_dict_int_avg['result_dir'], 'int', str(shot_no) + '_ch' + str(line_ch) + '_avg_' + str(avg_time))
    os.makedirs(dir_out, exist_ok=True)

#%%
    zaxis = np.linspace(0, len(camera_dict_int_avg['data_avg'][0,0,:]), len(camera_dict_int_avg['data_avg'][0,0,:])+1)
    xaxis = np.linspace(0, len(camera_dict_int_avg['data_avg'][0,:,0]), len(camera_dict_int_avg['data_avg'][0,:,0])+1)
    ppmm = 112/(int(camera_dict_int_avg["diam_flange"]))  # mm per pixel
    # X axis ... 0 on the center line.
    xaxis = len(xaxis)/2 - xaxis
    # Convert to cm
    xaxis *= float(ppmm) / 10
    zaxis *= float(ppmm) / 10
    # Z axis ... 1100 cm at the corner.
    zaxis = zaxis + 1095 - zaxis[-1]
    
    # max intensity
    ymax = np.max(camera_dict_int_avg['data_avg'])
    print('ymax = ' + str(ymax))
    
#%% Hampel filter to detect outlier and set ymax accordingly
    # ymax, ymax_arg, hampel_fig = hampel_filter.filter_ymax(camera_dict['data'], hw_size=2, thr=3)
    # hampel_fig.savefig(os.path.join(dir_out, 'hampel_' + str(shot_no) + '_' + str(line_ch)))
    # hampel_fig.close()
    #ymax = 100000

#%% Save fig
    for i, img in tqdm(enumerate(camera_dict_int_avg['data_avg']), total=camera_dict_int_avg['data_avg'].shape[0], desc='Saving figs...'):
        
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        
        # Draw the figure
        ax_img = ax.imshow(img, extent=[zaxis[0], zaxis[-1], xaxis[-1], xaxis[0]], vmax=ymax, vmin=0, cmap='plasma')
        
        # Color bar
        divider = mpl_toolkits.axes_grid1.make_axes_locatable(ax)
        cax = divider.append_axes('right', size='4%', pad='2%')
        fig.colorbar(ax_img, cax=cax)
        
        # Title
        time_quot = camera_dict_int_avg["avg_time_list"][i] # quotient
        time_quot = round(time_quot, 2)
        ax.set_title('#'+str(shot_no)+'_ch' + str(line_ch) +'\n@' +  str(time_quot) + 'ms-' + str(time_quot+avg_time) + 'ms', fontsize=16)

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
        
        # plt.savefig(os.path.join(dir_out, str(shot_no) + '_ch' + str(line_ch) + '_'  + str(time_quot) + 'ms-' + str(time_quot+avg_time) + 'ms.svg'))
        num_frames_per_block = int(avg_time * int(camera_dict_int_avg['frame_rate']) / 1000)
        plt.savefig(os.path.join(dir_out, str(shot_no) + '_ch' + str(line_ch) + '_'  + str(frame_tgt+num_frames_per_block*i) + '-'  + str(frame_tgt+num_frames_per_block*(i+1)-1) + '.svg'))

        # plt.show()
        
        plt.close(fig)    
    
#%% Test
if __name__ == "__main__":
    import time
    
    time_sta = time.time()
    shot_li = [256221]
    frame_tgt=0
    num_frames=0
    avg_time = 0.5
    #flg_rot=False
    # line_li = ['all']
    line_li = ['1', '2', '4']
    for shot_no in shot_li:
        for line_ch in line_li:
            plot_camera_int_frame(shot_no, line_ch, frame_tgt, num_frames, avg_time)
    time_end = time.time()
    print('Time spent: ' + str(time_end-time_sta) + ' (s)')
    #print(camera_dict['frame_rate'])
