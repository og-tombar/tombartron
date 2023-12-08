<img width="1135" alt="TOMBARTRON" src="https://github.com/og-tombar/TOMBARtron/assets/134632821/9985c4d8-ef83-408a-8149-659f0f8755e2">

# Welcome to TOMBARTRON!

The current release of this project is an early work-in-progress, showcasing a Python application designed for 3D modeling and visualization of musical instruments. TOMBARTRON is entirely coded in Python and utilizes Pygame and PyOpenGL for rendering 3D graphics, along with [Py-MeltySynth by Nobuaki Tanaka](https://github.com/sinshu/py-meltysynth) for audio synthesis. Although the project remains unfinished, most of the 3D graphics engine had been implemented and can be used reliably.

<p align="center">
  <img width="600" alt="TOMBARTRON in Action" src="https://github.com/og-tombar/TOMBARtron/assets/134632821/0d977e52-1e8f-47bd-b6e5-7aae6af0a42b">
</p>

# How does it work?

The current version has the following capabilities:

- 3D modeling of musical instruments using PyOpenGL, with the ability to render 3D scenes to video using Pygame.
- Rendering existing MIDI compositions to audio files, using [Py-MeltySynth](https://github.com/sinshu/py-meltysynth) and SoundFont libraries.
- Merging separate video and audio into a combined video using MoviePy.
- Uploading the resulting video to YouTube via the YouTube API.

# To-Do List
## Audio
- [ ] Implement procedural music composition logic.
- [ ] Develop a MIDI sequencer class that supports playback and communication with graphic modules for real-time animation.

## Graphics
- [ ] Finalize the keyboard model, including buttons, text, and other visual elements.
- [ ] Model additional musical instruments (e.g., guitars, drums, etc.).
