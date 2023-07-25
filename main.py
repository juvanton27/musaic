import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from music import create_model, generate_long_audio, generate_music_sentence
from video import generate_video
from bot import create_bot, upload_video

def main(counter: int, customCounter: bool = False):
  print(f'Project {counter}')
  print("Generating model ...")
  model = create_model()

  print("Cleaning frame repository ...")
  folders=['frames', 'music_output', 'video_output']
  for folder in folders:
    if not os.path.exists(folder):
      os.mkdir(folder)
  os.system("rm ./frames/*.png")
  load_dotenv()

  print("Generating music sentence ...")
  sentence = generate_music_sentence()

  print("Generating music ...")
  audio_path = generate_long_audio(model, sentence, int(sys.argv[1]), topk=250, topp=0, temperature=1.0, cfg_coef=3.0, overlap=10)

  print("Generating video ...")
  video_path = generate_video(audio_path)

  max_attemps = 3
  attempt = 1
  bot = None
  title = f'Lazy Project #{counter} - Musaic'
  while attempt <= max_attemps:
    try:
      print(f'Try {attempt}')
      print("Generating bot ...")
      bot = create_bot()

      print("Uploading video ...")
      upload_video(bot, video_path, title)
      break
    except Exception as e:
      print(e)
      attempt += 1
      if bot is not None:
        bot.quit()
  
  if attempt > max_attemps:    
    with open('error.log', 'a') as file:
      file.write(f'{count} => {datetime.now().isoformat()}: {title}')
  else: 
    if not customCounter:
      with open('service.log', 'a') as file:
        file.write(f'{count} => {datetime.now().isoformat()}: {title}')
    print('Job success !')

if __name__ == '__main__':
  log_path = 'service.log'
  count = 0
  customCounter = False
  if len(sys.argv) == 2:
    try:
      with open(log_path, 'r') as file:
        lines = file.readlines()
        if len(lines) == 0:
          count = 1
        else: 
          count = int(lines.pop().split(' ')[0])+1
    except FileNotFoundError:
      with open(log_path, 'w') as file:
        count = 0
  if len(sys.argv) == 3:
    count = sys.argv[2]
    customCounter = True
  main(count, customCounter)