import os
import sys

from music import create_model, generate_long_audio, generate_music_sentence
from video import generate_video
from bot import create_bot, upload_video

def main(counter: int):
  print(f'Project {counter}')
  print("Generating model ...")
  model = create_model()

  print("Cleaning frame repository ...")
  os.system("rm ./frames/*.png")

  print("Generating music sentence ...")
  sentence = generate_music_sentence()

  print("Generating music ...")
  audio_path = generate_long_audio(model, sentence, int(sys.argv[2]), topk=250, topp=0, temperature=1.0, cfg_coef=3.0, overlap=10)

  print("Generating video ...")
  video_path = generate_video(audio_path)

  max_attemps = 3
  attempt = 1
  bot = None
  while attempt <= max_attemps:
    try:
      print(f'Try {attempt}')
      print("Generating bot ...")
      bot = create_bot()

      print("Uploading video ...")
      upload_video(bot, video_path, f'Lazy Project #{counter} - Musaic')
      break
    except Exception as e:
      attempt += 1
      if bot is not None:
        bot.quit()
  
  if attempt > max_attemps:    
    with open('error.log', 'a') as file:
      file.write(f'Project {counter} => {video_path}\n')
  else: 
    print('Job success !')

if __name__ == '__main__':
  counter = int(sys.argv[1])
  while True:
    main(counter)
    counter += 1