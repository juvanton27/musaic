# Prerequisite
## Install ffmpeg
### on macOS
sudo brew install ffmpeg
### on Linux
sudo apt install ffmpeg
## Install all pip3 requirements
pip3 install -r requirements.txt
## Install Nvidia driver (Ubuntu with GPU)
sudo ubuntu-drivers autoinstall

# Define environments variables
In Chrome, search chrome://version and whereis chromedriver
USER_DATA_DIR=<path>
CHROMEDRIVER_PATH=<path>

# Starting application
python3 main.py <time_in_seconds> <project_number>
