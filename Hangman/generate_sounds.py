import wave
import struct
import math

def generate_tone(filename, frequency, duration, volume=0.5, sample_rate=44100):
    num_samples = int(sample_rate * duration)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(num_samples):
            # Sine wave formula
            sample = volume * math.sin(2 * math.pi * frequency * (i / sample_rate))
            # Convert to 16-bit integer
            sample_int = int(sample * 32767.0)
            wav_file.writeframesraw(struct.pack('<h', sample_int))

# Correct: short high pitch
generate_tone('Correct.wav', 800.0, 0.1)

# Wrong: short low pitch
generate_tone('Wrong.wav', 150.0, 0.3)

# Win: Arpeggio up (simulated with standard notes)
def generate_arpeggio(filename, freqs, duration_per_note, volume=0.5, sample_rate=44100):
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for freq in freqs:
            num_samples = int(sample_rate * duration_per_note)
            for i in range(num_samples):
                sample = volume * math.sin(2 * math.pi * freq * (i / sample_rate))
                sample_int = int(sample * 32767.0)
                wav_file.writeframesraw(struct.pack('<h', sample_int))

generate_arpeggio('Win.wav', [440, 554, 659, 880], 0.15) # A4, C#5, E5, A5

# Loose: Arpeggio down
generate_arpeggio('Loose.wav', [300, 250, 200, 150, 100], 0.2)
