import datetime
import random
import os

import torch
import torchaudio
from audiocraft.models import musicgen

styles = [
    "Pop",
    "Rock",
    "Jazz",
    "Hip-hop",
    "R&B",
    "Classique",
    "Country",
    "Reggae",
    "Electro",
    "Funk",
    "Soul",
    "Blues",
    "Métal",
    "Punk",
    "Indie",
    "Folk",
    "Latino",
    "Rap",
    "Disco",
    "Gospel",
]
melodies = [
    "Simple",
    "Complex",
    "Arpeggiated",
    "Syncopated",
    "Ornamented",
    "Repetitive",
    "Harmonic",
    "Contrapuntal",
    "Imitative",
    "Modal",
    "Pentatonic",
    "Bluesy",
    "Jazzy",
    "Folk-inspired",
    "Dissonant",
    "Melancholic",
    "Ethereal",
    "Uplifting",
    "Cinematic",
]
percussions = [
    "bongo",
    "conga",
    "djembé",
    "cajon",
    "tambourin",
    "maracas",
    "shaker",
    "timbales",
    "darbouka",
    "tabla",
]
rhythms = [
    "Rock",
    "Jazz",
    "Blues",
    "Reggae",
    "Salsa",
    "Funk",
    "Hip-hop",
    "R&B",
    "Country",
    "Pop",
    "Classique",
    "Électro",
    "Soul",
    "Disco",
    "Folk",
    "Rap",
    "Métal",
    "Punk",
    "Latino",
    "Indie",
]
contexts = [
    "Relaxing at home",
    "Driving in the car",
    "Working out at the gym",
    "Partying with friends",
    "Studying or focusing",
    "Walking in nature",
    "Cooking or baking",
    "Having a romantic dinner",
    "Chilling by the pool",
    "Getting ready for a night out",
]

def create_model():
  return musicgen.MusicGen.get_pretrained('melody', device='cuda')

def generate_music_sentence():
  style = styles[random.randint(0, len(styles) - 1)]
  melodie = melodies[random.randint(0, len(melodies) - 1)]
  percussion = percussions[random.randint(0, len(percussions) - 1)]
  rhythm = rhythms[random.randint(0, len(rhythms) - 1)]
  context = contexts[random.randint(0, len(contexts) - 1)]

  description = f"Lofi song with {style} style with {melodie} melody, {percussion} percussion, and {rhythm} rythm, for {context}"
  print(description)
  return description

def generate_long_audio(
  model, text, duration, topk=250, topp=0, temperature=1.0, cfg_coef=3.0, overlap=5
):
  topk = int(topk)

  output = None
  segment_duration = duration
  nth_segment = 0
  nb_segment = int(duration/30)

  while duration > 0:
    nth_segment+=1
    print(f'Segment {nth_segment}/{nb_segment}')

    if output is None:  # first pass of long or short song
      if segment_duration > model.lm.cfg.dataset.segment_duration:
        segment_duration = model.lm.cfg.dataset.segment_duration
      else:
        segment_duration = duration
    else:  # next pass of long song
      if duration + overlap < model.lm.cfg.dataset.segment_duration:
        segment_duration = duration + overlap
      else:
        segment_duration = model.lm.cfg.dataset.segment_duration

    # print(f'Segment duration: {segment_duration}, duration: {duration}, overlap: {overlap}')

    model.set_generation_params(
      use_sampling=True,
      top_k=topk,
      top_p=topp,
      temperature=temperature,
      cfg_coef=cfg_coef,
      duration=min(segment_duration, 30),  # ensure duration does not exceed 30
    )

    if output is None:
      next_segment = model.generate(descriptions=[text], progress=True)
      duration -= segment_duration
    else:
      last_chunk = output[:, :, -overlap * model.sample_rate :]
      next_segment = model.generate_continuation(
        last_chunk, model.sample_rate, descriptions=[text], progress=True
      )
      duration -= segment_duration - overlap

    if output is None:
      output = next_segment
    else:
      output = torch.cat(
        [output[:, :, : -overlap * model.sample_rate], next_segment], 2
      )

  audio_output = output.detach().cpu().float()[0]
  filename = f"music_{datetime.datetime.now().timestamp()}.wav"
  output_path = f"music_output/{filename}"
  torchaudio.save(output_path, audio_output, sample_rate=32000)
  print(f"Song saved to {output_path}")
  return filename
