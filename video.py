from datetime import datetime
import os

import numpy as np
import plotly.graph_objects as go
import tqdm
from scipy.io import wavfile


def generate_video(audio_path):
  PATH = "./music_output"

  # Configuration
  FPS = 30
  FFT_WINDOW_SECONDS = 0.25  # how many seconds of audio make up an FFT window

  # Note range to display
  FREQ_MIN = 10
  FREQ_MAX = 1000

  # Output size. Generally use SCALE for higher res, unless you need a non-standard aspect ratio.
  RESOLUTION = (1920, 1080)
  AUDIO_FILE = audio_path

  fs, data = wavfile.read(os.path.join(PATH, AUDIO_FILE))  # load the data
  # audio = data.T[0] # this is a two channel soundtrack, get the first track
  audio = data  # this is a two channel soundtrack, get the first track
  FFT_WINDOW_SIZE = int(fs * FFT_WINDOW_SECONDS)
  AUDIO_LENGTH = len(audio) / fs

  def plot_fft(p, xf, fs, dimensions=(960, 540)):
    layout = go.Layout(
      autosize=False,
      width=dimensions[0],
      height=dimensions[1],
      font={"size": 24},
      xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
      plot_bgcolor="rgba(0,0,0,0)",
      paper_bgcolor="rgba(0,0,0,0)",
    )

    fig = go.Figure(
      layout=layout,
      layout_xaxis_range=[FREQ_MIN, FREQ_MAX],
      layout_yaxis_range=[0, 1],
    )
    fig.add_trace(
      go.Scatter(
        x=xf,
        y=p,
        line=dict(color="rgb(0,0,0)", width=5, shape="spline", smoothing=1.3),
      )
    )

    return fig

  def extract_sample(audio, frame_number):
    end = frame_number * FRAME_OFFSET
    begin = int(end - FFT_WINDOW_SIZE)

    if end == 0:
      # We have no audio yet, return all zeros (very beginning)
      return np.zeros((np.abs(begin)), dtype=float)
    elif begin < 0:
      # We have some audio, padd with zeros
      return np.concatenate(
        [np.zeros((np.abs(begin)), dtype=float), audio[0:end]]
      )
    else:
      # Usually this happens, return the next sample
      return audio[begin:end]

  # Hanning window function
  window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, FFT_WINDOW_SIZE, False)))

  xf = np.fft.rfftfreq(FFT_WINDOW_SIZE, 1 / fs)
  FRAME_COUNT = int(AUDIO_LENGTH * FPS)
  FRAME_OFFSET = int(len(audio) / FRAME_COUNT)

  # Pass 1, find out the maximum amplitude so we can scale.
  mx = 0
  for frame_number in range(FRAME_COUNT):
    sample = extract_sample(audio, frame_number)

    fft = np.fft.rfft(sample * window)
    fft = np.abs(fft).real
    mx = max(np.max(fft), mx)

  # print(f"Max amplitude: {mx}")

  # Pass 2, produce the animation
  for frame_number in tqdm.tqdm(range(FRAME_COUNT)):
    sample = extract_sample(audio, frame_number)

    fft = np.fft.rfft(sample * window)
    fft = np.abs(fft) / mx

    fig = plot_fft(fft.real, xf, fs, RESOLUTION)
    fig.write_image(f"./frames/frame{frame_number}temp.png", scale=2)
    os.system(
      f'ffmpeg -i ./image.png -i ./frames/frame{frame_number}temp.png -filter_complex "[1:v]scale=1920x1080[bg];[0:v][bg]overlay=format=auto" ./frames/frame{frame_number}.png 2> /dev/null'
    )

  output_path = f"./video_output/video_{datetime.now().timestamp()}.mp4"
  os.system(
    f"ffmpeg -y -r {FPS} -f image2 -s 1920x1080 -i ./frames/frame%d.png -i './music_output/'{AUDIO_FILE} -c:v libx264 -pix_fmt yuv420p {output_path} 2> /dev/null"
  )
  print(f"Video saved to {output_path}")
  print("\n")
  return output_path
