import wave
import struct
import math

# Generates a sound wave and saves it as a .wav file
def generate_tone(filename, freq, duration, func=math.sin, fade_out=0.0):
    sample_rate = 44100 # Standard CD audio quality
    num_samples = int(duration * sample_rate)
    max_amp = 32767.0 # Max volume for 16-bit audio
    
    with wave.open(filename, 'w') as wav_file:
        # Set up a mono channel, 16-bit audio file
        wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))
        
        for i in range(num_samples):
            t = float(i) / sample_rate # Current time in seconds
            value = func(2.0 * math.pi * freq * t) # Get wave value at this time
            
            # Apply fade out if we set one, to avoid popping noises at the end
            if fade_out > 0:
                fade = max(0.0, 1.0 - (t / fade_out))
                value *= fade
                
            # Pack the amplitude into binary format and write to the file
            packed_value = struct.pack('h', int(value * max_amp * 0.1)) # Keep volume low at 10%
            wav_file.writeframes(packed_value)

# Creates a retro 8-bit sounding square wave
def square(t):
    return 1.0 if math.sin(t) > 0 else -1.0

print("Generating move.wav")
# Generate a quick, low blip for moving pieces
generate_tone('move.wav', 440, 0.05, square, 0.05)

print("Generating rotate.wav")
# Generate a slightly higher blip for rotating pieces
generate_tone('rotate.wav', 880, 0.05, square, 0.05)

print("Generating clear.wav")
# Generate a longer, higher pitch for clearing lines
generate_tone('clear.wav', 1320, 0.2, square, 0.2)

print("Generating game_over.wav")
# Custom function to create a "falling pitch" game over sound
def generate_game_over(filename):
    sample_rate = 44100
    duration = 1.0
    num_samples = int(duration * sample_rate)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            # Start at 400Hz and slide down to 100Hz
            freq = 400 - 300 * t
            value = square(2.0 * math.pi * freq * t)
            fade = max(0.0, 1.0 - t) # Fade out over the whole second
            
            packed_value = struct.pack('h', int(value * 32767.0 * 0.15 * fade))
            wav_file.writeframes(packed_value)

generate_game_over('game_over.wav')
print("Sounds generation complete.")
