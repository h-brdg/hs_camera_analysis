import load_tiff
import read_conv_info
import transform_image 
import read_config_info
import numpy as np
from tqdm import tqdm
import concurrent.futures
import os

def process_frame(shot_no, tiff_dir, i, line_ch, flg_rot):
    """Load and transform a single frame."""
    try:
        img_array = load_tiff.load_tiff(shot_no, tiff_dir, i, 1)
        img_array, tra_dict, coeff = transform_image.transform_image(shot_no, line_ch, tiff_dir, img_array, flg_rot)
        return i, img_array, tra_dict, coeff
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None

def camera_reader(shot_no, line_ch, frame_tgt=0, num_frames=0, flg_rot=False):
    config_dict = read_config_info.read_config_info()
    tiff_dir = config_dict['tiff_dir']
    memmap_dir = config_dict['memmap_dir']
    os.makedirs(memmap_dir, exist_ok=True)
    conv_dict = read_conv_info.read_conv_info(shot_no, tiff_dir)
    
    if num_frames == 0:
        num_frames = int(conv_dict['bottom_frame']) - (int(conv_dict['top_frame']) + frame_tgt)
    
    first_frame = load_tiff.load_tiff(shot_no, tiff_dir, frame_tgt, 1)
    first_frame, tra_dict, coeff = transform_image.transform_image(shot_no, line_ch, tiff_dir, first_frame, flg_rot)
    frame_shape = first_frame[0].shape
    estimated_size_mb = (num_frames * frame_shape[0] * frame_shape[1] * 4) / (1024 ** 2)

    if flg_rot:
        transformed = 'rot'
    else:
        transformed = 'org'
    memmap_filename = f'trimmed_{shot_no}_ch{line_ch}_tgt{frame_tgt}_{num_frames}frs_{transformed}.dat'
    memmap_path = os.path.join(memmap_dir, memmap_filename)

    if os.path.exists(memmap_path):
        camera_data = np.memmap(memmap_path, dtype='float32', mode='r+', shape=(num_frames,) + frame_shape)
        print(f"Using existing memmap file: {memmap_path}")
    else:
        if estimated_size_mb > int(config_dict['mem_limit_size']):
            trimmed_memmap = np.memmap(memmap_path, dtype='float32', mode='w+', shape=(num_frames,) + frame_shape)
            camera_data = trimmed_memmap
            print(f"Using memmap due to large data size: {memmap_path}")
        else:
            camera_data = np.empty((num_frames,) + frame_shape, dtype='float32')
            print("Using in-memory array for trimmed data")

        # Multi-threading for processing each frame
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_frame = {
                executor.submit(process_frame, shot_no, tiff_dir, i, line_ch, flg_rot): i 
                for i in range(frame_tgt, frame_tgt + num_frames)
            }
    
            for future in tqdm(concurrent.futures.as_completed(future_to_frame), total=num_frames, desc="Loading frames..."):
                result = future.result()
                if result is not None:
                    i, img_array, tra_dict, coeff = result
                    camera_data[i - frame_tgt] = img_array

    camera_dict = {'data': camera_data, 'coeff': coeff, 'frame_start': int(conv_dict['top_frame']) + frame_tgt}
    camera_dict.update(conv_dict)
    camera_dict.update(tra_dict)
    camera_dict.update(config_dict)
    camera_dict['data_size'] = (num_frames, *camera_dict['trimmed_size'])

    return camera_dict

#%% Test
if __name__ == "__main__":
    import time
    import matplotlib.pyplot as plt
    
    time_sta = time.time()
    shot_no = 256221
    frame_tgt = 0
    num_frames = 0
    flg_rot = False
    shot_li = [256221,256223]
    shot_li = [256221]
    line_ch_li = ('4', '2', '1')
    for shot_no in shot_li:
        for line_ch in line_ch_li:
                camera_dict = camera_reader(shot_no, line_ch, frame_tgt, num_frames, flg_rot)
    
    if camera_dict:
        plt.imshow(camera_dict['data'][0, :, :])
        plt.show()
    
    time_end = time.time()
    print('Time spent: ' + str(time_end - time_sta) + ' (s)')
