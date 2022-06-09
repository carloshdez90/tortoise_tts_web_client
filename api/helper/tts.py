import os

# Get voices available in tortoise-tts lib
def get_voices():
    voices = os.listdir('../../tortoise-tts/tortoise/voices')

    return voices

def get_quality():
    return ["ultra_fast", "fast", "standard", "high_quality"]

def get_candidates():
    return list(range(1,6))