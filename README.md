# HS Camera Analysis

Analysis scripts for data obtained from the ACS and GX series high-speed cameras by nac Image Technology Inc.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Scripts](#scripts)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This repository contains Python scripts for analyzing data captured by the ACS and GX series high-speed cameras manufactured by nac Image Technology Inc. These scripts are designed to facilitate the processing and analysis of high-speed camera data for research and development purposes.

## Features
- Data extraction and preprocessing
- Frame-by-frame analysis and Time-averaged analysis
- Intensity of each channel and the ratio of two channels
- Visualization of high-speed camera data
  
## Installation
To use the scripts in this repository, you need to have Python installed on your system. You can install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage
1. Clone the repository:
    ```bash
    git clone https://github.com/h-brdg/hs_camera_analysis.git
    cd hs_camera_analysis
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure camera_config.ini, trim_info.custom.ini and coeff_info.ini

4. (Optional) Run the crop-adjustment-aiding script to configure trim_info.custom.ini :
    ```bash
    python adjust_trim_info.py
    ```

5. Run the gui plotting script:
    ```bash
    python plot_gui.py
    ```

## Scripts
- `adjust_trim_info.py`: Script for checking the trimming information.
- `plot_gui.py`: Main Script for analyzing and visualizing the high-speed camera data.

## Contributing
We welcome contributions to improve the scripts and add new features. Please fork the repository and submit your pull requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
