import os
import subprocess
from datetime import datetime
import csv
import random
import textwrap

account_name = 'quotes.musaic'
input_path = os.path.join(os.path.dirname(__file__), 'input')
output_path = os.path.join(os.path.dirname(__file__), 'output')

def cleaned_sentence(sentence: str, is_filename: bool = False) -> str:
  max_line_length = 20 
  sentence = sentence.replace('\'', " ")
  if not is_filename: 
    lines = textwrap.wrap(sentence, width=max_line_length)
    sentence = '\n'.join(lines)
  return sentence
  

def generate_video(theme: str, first_part: str, second_part: str, video_path: str):
  duration = 11.5

  # Checks duration of video 
  command = f'ffprobe -i {video_path} -show_entries format=duration -v quiet -of csv="p=0"'
  result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  current_duration = float(result.stdout.strip())
  if current_duration < duration:
    print('Video should durate more than 11,5 sec')
    return

  # Generates video
  output_file = os.path.join(output_path, f'{cleaned_sentence(first_part, True)}.mp4')
  subprocess.run(f'ffmpeg -i {video_path} -t {duration} -vf "\
    drawtext=text=\'{cleaned_sentence(theme.upper())}\':x=(w-tw)/2:y=(h-th)/5:fontsize=w/20:fontcolor=white:fontfile={os.path.join(input_path, "fonts/Poppins/Poppins-Regular.ttf")},\
    drawtext=text=\'{cleaned_sentence(first_part)}\':x=(w-tw)/2:y=(h-th)/2:fontsize=w/10:fontcolor=white:fontfile={os.path.join(input_path, "fonts/KudryashevDisplay/fontspring-demo-kdp45.otf")}:enable=\'between(t,0,9)\':box=1:boxcolor=black:boxborderw=10:line_spacing=10,\
    drawtext=text=\'{cleaned_sentence(second_part)}\':x=(w-tw)/2:y=(h-th)/2:fontsize=w/10:fontcolor=white:fontfile={os.path.join(input_path, "fonts/KudryashevDisplay/fontspring-demo-kdp45.otf")}:enable=\'between(t,10,{duration})\':box=1:boxcolor=black:boxborderw=10:line_spacing=10,\
    drawtext=text=\'@{account_name}\':x=(w-tw)/2:y=4*(h-th)/5:fontsize=w/25:fontcolor=white:fontfile={os.path.join(input_path, "fonts/Poppins/Poppins-Regular.ttf")}" -c:v libx264 -c:a copy \'{output_file}\'', 
    shell= True, stderr=subprocess.DEVNULL
  )
  if not os.path.exists(output_file) or (os.path.exists(output_file) and os.path.getsize(output_file) == 0):
    raise Exception(f'Generating {first_part} not succeeded !')

if not os.path.exists(output_path):
  os.mkdir(output_path)

with open('data.csv', 'r') as csv_file:
  # Reads inputs
  video_folder = os.path.join(input_path, 'videos')
  file_list = list(filter(lambda filename: filename.lower().endswith('.mp4'), os.listdir(video_folder)))
  # Reads CSV
  csv_reader = csv.reader(csv_file, delimiter=';')
  next(csv_reader)
  for row in csv_reader:
    theme, first_part, second_part = row
    video_path = os.path.join(video_folder, random.choice(file_list))
    try:
      generate_video(theme, first_part, second_part, video_path)
    except Exception as e:
      print(e)