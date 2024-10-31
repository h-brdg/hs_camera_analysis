import load_tiff
import read_conv_info
import transform_image 
import read_config_info
import numpy as np
from tqdm import tqdm
import concurrent.futures

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
    conv_dict = read_conv_info.read_conv_info(shot_no, tiff_dir)
    
    if num_frames == 0:
        num_frames = int(conv_dict['bottom_frame']) - int(conv_dict['top_frame']) - frame_tgt
    
    first_frame = load_tiff.load_tiff(shot_no, tiff_dir, frame_tgt, 1)
    first_frame, tra_dict, coeff = transform_image.transform_image(shot_no, line_ch, tiff_dir, first_frame, flg_rot)
    frame_shape = first_frame[0].shape
    estimated_size_gb = (num_frames * frame_shape[0] * frame_shape[1] * 4) / (1024 ** 3)

    # if True:   # For testing
    if estimated_size_gb > int(config_dict['mem_limit_size']):
        memmap_filename = 'trimmed_image.dat'
        trimmed_memmap = np.memmap(memmap_filename, dtype='float32', mode='w+', shape=(num_frames,) + frame_shape)
        camera_data = trimmed_memmap
        print("Using memmap due to large data size")
    else:
        camera_data = np.empty((num_frames,) + frame_shape, dtype='float32')
        print("Using in-memory array")

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

    camera_dict = {'data': camera_data, 'coeff': coeff, 'frame_start': frame_tgt}
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
    num_frames = 1000
    flg_rot = False
    line_ch = '2' 
    camera_dict = camera_reader(shot_no, line_ch, frame_tgt, num_frames, flg_rot)
    
    if camera_dict:
        plt.imshow(camera_dict['data'][0, :, :])
        plt.show()
    
    time_end = time.time()
    print('Time spent: ' + str(time_end - time_sta) + ' (s)')
