# Prerequisite

## Install ffmpeg
### on macOS
sudo brew install ffmpeg
### on Linux
sudo apt install ffmpeg

## Install python3 and all pip3 requirements
pip3 install -r requirements.txt

## Install Nvidia driver (Ubuntu with NVIDIA GPU)
sudo ubuntu-drivers autoinstall

# Define environments variables
In Chrome, search chrome://version and whereis chromedriver
USER_DATA_DIR=<path>
CHROMEDRIVER_PATH=<path>

# Starting application
```python3 main.py <time_in_seconds> <project_number>```
!!! You must be logged !!! If your credential aren't already in the browser, please run before :
```python3 login.py```
You'll have one minute to log as usual