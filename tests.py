from modules.all_utils import *
import modules.meltysynth as ms

import wave
import time

from array import array
from collections.abc import Sequence

def write_wav_file(
    sample_rate: int, left: Sequence[float], right: Sequence[float], path: str
) -> None:
    max_value = 0.0

    for t in range(len(left)):
        if abs(left[t]) > max_value:
            max_value = abs(left[t])

        if abs(right[t]) > max_value:
            max_value = abs(right[t])

    a = 0.99 / max_value

    data = array("h")

    for t in range(len(left)):
        sample_left = int(32768 * a * left[t])
        sample_right = int(32768 * a * right[t])

        data.append(sample_left)
        data.append(sample_right)

    wav = wave.open(path, "wb")
    wav.setframerate(sample_rate)
    wav.setnchannels(2)
    wav.setsampwidth(2)
    wav.writeframesraw(data)
    wav.close()


def simple_chord() -> None:
    print('Loading SoundFont...')
    sf2 = open(YAMAHA_C7_SF2_PATH, "rb")
    sound_font = ms.SoundFont(sf2)
    sf2.close()

    print('Creating synthesizer...')
    settings = ms.SynthesizerSettings(44100)
    synthesizer = ms.Synthesizer(sound_font, settings)

    print('Assigning notes to synthesizer...')
    synthesizer.note_on(0, 60, 100)
    synthesizer.note_on(0, 64, 100)
    synthesizer.note_on(0, 67, 100)

    # The output buffer (3 seconds).
    print('Creating buffers...')
    left = ms.create_buffer(3 * settings.sample_rate)
    right = ms.create_buffer(3 * settings.sample_rate)

    print('Rendering waveform...')
    start = time.time()
    synthesizer.render(left, right)
    end = time.time()

    # Print the time elapsed.
    print("Time elapsed: " + str(end - start))

    print('Saving WAV file...')
    # Save the waveform as a WAV file.
    write_wav_file(settings.sample_rate, left, right, OUTPUT_DIR_PATH + '/simple_chord.wav')


def main() -> None:
    simple_chord()


if __name__ == "__main__":
    main()