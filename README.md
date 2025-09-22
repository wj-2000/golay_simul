# Code for Golay Metalens Project

## Getting started

The code provided in the folder demonstrates the generation of the Golay metalens aperture and phase information, as well as the wave propagation simulations used in this study. This file shows the instructions on how to run the code. 

## Prerequisites

### Minimum Requirements

- Python ≥ 3.8 (3.8.10 used in testing)
- NumPy ≥ 1.21 (1.24.3 verified)
- OpenCV ≥ 4.5 (4.9.0 verified)
- PyTorch ≥ 2.0 (CPU: 2.7.1 verified)

### Tested Environment

The following specific versions were fully validated:
- Python 3.8.10
- NumPy 1.24.3
- OpenCV 4.9.0 
- PyTorch (CPU-only) 2.7.1

> **Note**: The code is expected to work with newer versions of these packages. Exact version matching is not required, but significant version differences (e.g., PyTorch 1.x) may cause compatibility issues.

## Installation guide

1. Download and unzip the entire project folder (typically takes 3-5 minutes).
2. Execute the code directly from the project folder. The guide for running the code is introduced in the following session.

## Running the code

1. To generate phase and amplitude for the center aperture and the Golay metalens:
-- Run "generate_aperture_file.ipynb". 
-- Expected output: Phase and amplitude arrays for the center aperture and the Golay metalens. 

2. To simulate point spread function of the center aperture and the Golay metalens:
-- Open the code in the current folder.
-- In the terminal:
   - For Windows, run: `bash autorun.sh`
   - For Linux, first make the script executable: `chmod 777 autorun.sh`, then run: `./autorun.sh`
-- Expected output: The point spread function of the center aperture and the Golay metalens.

> **Note**: For memory-constrained systems (e.g., consumer desktops), we recommend scaling down the aperture diameter by a minimum factor of 10. For full-scale processing, server deployment is advised due to high memory requirements.

3. To visualize the point spread function and the modular transfer function of the center aperture and the Golay metalens: 
-- Run plot_psf_mtf.ipynb
-- Expected output: Plots showing the point spread function the modular transfer function of the center aperture and the Golay metalens.

## License
This code is made available for academic and research purposes only. Redistribution or commercial use is not permitted without prior permission from the authors.
