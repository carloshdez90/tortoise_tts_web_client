import os
import io
import sys
from time import time
from datetime import datetime

import torch
import torchaudio

sys.path.append('../../tortoise-tts/tortoise/')
from api import TextToSpeech, MODELS_DIR
from utils.audio import load_audio, load_voices
from utils.text import split_and_recombine_text

# Get voices available in tortoise-tts lib
def get_voices():
    voices = sorted(os.listdir('../../tortoise-tts/tortoise/voices'))
    return dict(zip(voices, voices))

def get_quality():
    values = ["ultra_fast", "fast", "standard", "high_quality"]
    return dict(zip(values, values))

def get_candidates():
    return list(range(1,6))

def generate_tts(voice='mol', text = 'Hello world', preset='fast', candidates = 1):
    
    output_path = 'results/'
    model_dir = MODELS_DIR
    seed=None
    produce_debug_state=False
    cvvp_amount=.0
    os.makedirs(output_path, exist_ok=True)

    # Preparing the input text
    text = ' '.join(text.splitlines())

    if '|' in text:
        print("Found the '|' character in your text, which I will use as a cue for where to split it up. If this was not"
              "your intent, please remove all '|' characters from the input.")
        texts = text.split('|')
    else:
        texts = split_and_recombine_text(text)

    tts = TextToSpeech(models_dir=model_dir)

    selected_voices = voice.split(',')
    seed = int(time()) if seed is None else seed
    result_outpath = os.path.join(output_path, datetime.now().strftime("%Y-%d-%m_%H-%M"))
    os.makedirs(result_outpath, exist_ok=True)
    
    for k, selected_voice in enumerate(selected_voices):
        if '&' in selected_voice:
            voice_sel = selected_voice.split('&')
        else:
            voice_sel = [selected_voice]
        voice_samples, conditioning_latents = load_voices(voice_sel)

        all_parts = []
        for j, text in enumerate(texts):
            gen = tts.tts_with_preset(text, voice_samples=voice_samples, conditioning_latents=conditioning_latents,
                                      preset=preset, k=candidates, use_deterministic_seed=seed)
            if candidates == 1:
                gen = gen.squeeze(0).cpu()
                torchaudio.save(os.path.join(result_outpath, f'{j}.wav'), gen, 24000)
            else:
                candidate_dir = os.path.join(result_outpath, str(j))
                os.makedirs(candidate_dir, exist_ok=True)
                for k, g in enumerate(gen):
                    torchaudio.save(os.path.join(candidate_dir, f'{k}.wav'), g.squeeze(0).cpu(), 24000)
                gen = gen[0].squeeze(0).cpu()
            all_parts.append(gen)

        if candidates == 1:
            full_audio = torch.cat(all_parts, dim=-1)
            torchaudio.save(os.path.join(result_outpath, 'combined.wav'), full_audio, 24000)

        # Combine each candidate's audio clips.
        if candidates > 1:
            audio_clips = []
            for candidate in range(candidates):
                for line in range(len(texts)):
                    wav_file = os.path.join(result_outpath, str(line), f"{candidate}.wav")
                    audio_clips.append(load_audio(wav_file, 24000))
                audio_clips = torch.cat(audio_clips, dim=-1)
                torchaudio.save(os.path.join(result_outpath, f"combined_{candidate:02d}.wav"), audio_clips, 24000)
                audio_clips = []

    return {"status": "done"}