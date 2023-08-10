import os
import subprocess
import csv
import random
import textwrap
from music import create_model, generate_long_audio

account_name = 'quotes.musaic'
input_path = os.path.join(os.path.dirname(__file__), 'input')
hashtags_path = os.path.join(os.path.dirname(__file__), 'hashtags')
output_path = os.path.join(os.path.dirname(__file__), 'video_output')

def cleaned_sentence(sentence: str, is_filename: bool = False) -> str:
  max_line_length = 20 
  sentence = sentence.replace('\'', " ")
  if not is_filename: 
    lines = textwrap.wrap(sentence, width=max_line_length)
    sentence = '\n'.join(lines)
  return sentence

def generate_video(theme: str, first_part: str, second_part: str, video_path: str, audio_path: str, duration: int):
  # Checks duration of video 
  command = f'ffprobe -i {video_path} -show_entries format=duration -v quiet -of csv="p=0"'
  result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  current_duration = float(result.stdout.strip())
  if current_duration < duration:
    raise Exception('Video should durate more than 11,5 sec')

  # Generates video
  output_file = ''
  with open(os.path.join(hashtags_path, 'quotes.txt'), 'r') as quotes:
    output_file = os.path.join(output_path, f'{cleaned_sentence(first_part, True)} {quotes.readline()}.mp4')
  subprocess.run(f'ffmpeg -i {video_path} -i {audio_path} -t {duration} -vf "\
    drawtext=text=\'{cleaned_sentence(theme.upper())}\':x=(w-tw)/2:y=(h-th)/5:fontsize=w/20:fontcolor=white:fontfile={os.path.join(input_path, "fonts/Poppins/Poppins-Regular.ttf")},\
    drawtext=text=\'{cleaned_sentence(first_part)}\':x=(w-tw)/2:y=(h-th)/2:fontsize=w/10:fontcolor=white:fontfile={os.path.join(input_path, "fonts/KudryashevDisplay/fontspring-demo-kdp45.otf")}:enable=\'between(t,0,9)\':box=1:boxcolor=black:boxborderw=10:line_spacing=10,\
    drawtext=text=\'{cleaned_sentence(second_part)}\':x=(w-tw)/2:y=(h-th)/2:fontsize=w/10:fontcolor=white:fontfile={os.path.join(input_path, "fonts/KudryashevDisplay/fontspring-demo-kdp45.otf")}:enable=\'between(t,10,{duration})\':box=1:boxcolor=black:boxborderw=10:line_spacing=10,\
    drawtext=text=\'@{account_name}\':x=(w-tw)/2:y=4*(h-th)/5:fontsize=w/25:fontcolor=white:fontfile={os.path.join(input_path, "fonts/Poppins/Poppins-Regular.ttf")}" -c:v libx264 -c:a aac \'{output_file}\'', 
    shell= True, stderr=subprocess.DEVNULL
  )
  if not os.path.exists(output_file) or (os.path.exists(output_file) and os.path.getsize(output_file) == 0):
    raise Exception(f'Generating {first_part} not succeeded !')

if not os.path.exists(output_path):
  os.mkdir(output_path)

data_path = os.path.join(input_path, 'data.csv')
with open(data_path, 'r') as csv_file:
  duration = 11.5
  # Reads inputs
  video_folder = os.path.join(input_path, 'videos')
  file_list = list(filter(lambda filename: filename.lower().endswith('.mp4'), os.listdir(video_folder)))
  # Reads CSV
  csv_reader = csv.reader(csv_file, delimiter=';')
  next(csv_reader)
  # Create song model
  print('Generating model...')
  model = create_model()
  sentence = 'chill love piano song'
  for row in csv_reader:
    theme, first_part, second_part = row
    print(f'Generating {first_part}')
    audio_path = os.path.join(os.path.dirname(__file__), 'music_output', generate_long_audio(model, sentence, duration, topk=250, topp=0, temperature=1.0, cfg_coef=3.0, overlap=10, fade=False))
    video_path = os.path.join(video_folder, random.choice(file_list))
    try:
      generate_video(theme, first_part, second_part, video_path, audio_path, duration)
    except Exception as e:
      print(e)