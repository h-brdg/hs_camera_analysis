#!/usr/bin/env python3

import numpy as np

from calc_int import calc_int
from calc_ratio import calc_ratio

def calc_avg(shot_no, line_ch, frame_tgt=0, num_frames=0, avg_time=10):
    
    if len(line_ch) == 1:
        mode = 'int'
        print('Mode: int')
        camera_dict_avg = calc_int(shot_no, line_ch, frame_tgt, num_frames)
    elif len(line_ch) == 2:
        mode = 'ratio'
        print('Mode: ratio')
        camera_dict_avg = calc_ratio(shot_no, line_ch, frame_tgt, num_frames)
    else:
        print('Error: Invalid line_ch')
        return None
    
    
#%% Average
    frame_rate = int(camera_dict_avg['frame_rate'])
    frame_start = int(camera_dict_avg['frame_start'])
    num_frames_per_block = int(avg_time * frame_rate / 1000)
    total_time = int(camera_dict_avg['data_size'][0])*1000/frame_rate
    num_avg_block = int(total_time / avg_time)
    # print(num_frames_per_block)
    # print(total_time)
    # print(num_avg_block)
    avg_data = np.zeros((num_avg_block,) + camera_dict_avg['trimmed_size'])
    # print(avg_data.shape)
    avg_time_list = []
    for j in range(num_avg_block): # j starts at 0
        avg_data[j] = np.mean(camera_dict_avg['data'][(num_frames_per_block*j):(num_frames_per_block*(j+1)-1),:,:], axis=0)
        # block_start_time = (frame_start + num_frames_per_block*j)/frame_rate * 1000
        block_start_time = frame_start/frame_rate * 1000 + j*avg_time
        avg_time_list = np.append(avg_time_list,block_start_time)
        
    camera_dict_avg.update({'data_avg': avg_data})
    camera_dict_avg.update({'avg_time': avg_time})
    camera_dict_avg.update({'avg_time_list': avg_time_list})
    
    return camera_dict_avg
    
#%% Test
if __name__ == "__main__":
    import time
    import matplotlib.pyplot as plt
    
    shot_no = 256221
    line_ch = '1'
    line_ch = ('1','2')
    # frame_tgt = 0
    # num_frames = 0
    # avg_time = 10
    
    frame_tgt = 11000
    num_frames = 100
    avg_time = 0.5
    
    camera_dict_avg = calc_avg(shot_no, line_ch, frame_tgt, num_frames, avg_time)
    
    # Plot each averaged frame in 'data_avg'
    avg_data = camera_dict_avg['data_avg']
    num_blocks = avg_data.shape[0]
    
    plt.figure(figsize=(10, 10))
    
    for i in range(num_blocks):
        plt.subplot(int(np.ceil(np.sqrt(num_blocks))), int(np.ceil(np.sqrt(num_blocks))), i + 1)
        plt.imshow(avg_data[i], cmap='gray')
        plt.title(f"Frame {i}")
        plt.axis('off')  # Hide axes for a cleaner look
    
    plt.tight_layout()
    plt.suptitle(f"Averaged Frames for Shot {shot_no}", fontsize=16)
    plt.subplots_adjust(top=0.9)
    plt.show()