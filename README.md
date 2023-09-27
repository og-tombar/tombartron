<img width="1135" alt="tombartron" src="https://github.com/og-tombar/TOMBARtron/assets/134632821/9985c4d8-ef83-408a-8149-659f0f8755e2">

# Welcome to TOMBARTRON!

This project represents an early work-in-progress, serving as a second iteration of TOMBARTRON. The original TOMBARTRON was prototyped using Max-MSP-Jitter in 2020. Much like its predecessor, the current version aims to be a tool for generating music videos instantly and effortlessly.

TOMBARTRON is entirely written in Python and leverages Pygame, PyOpenGL for rendering 3D graphics, and [Py-MeltySynth by Nobuaki Tanaka](https://github.com/sinshu/py-meltysynth) for audio synthesis.

# Important Disclaimers

- It is crucial to note that this project is still in its early stages, and a significant portion of the code is yet to be developed.
- In 2020, I successfully created a working prototype with most of the music related capabilities described below using Max-MSP-Jitter. Unfortunately, GitHub doesn't support the display of Max-MSP-Jitter code in a readable format, which is why the 2020 version's code is absent from this repository.
- To provide context, I will include a content sample generated by the 2020 TOMBARTRON version at the end of this document.
- However, it is worth mentioning that much of the graphics engine infrastructure is already implemented in this project and can be reliably utilized (see the .gif below).

<p align="center">
  <img width="600" alt="TOMBARTRON in Action" src="https://github.com/og-tombar/TOMBARtron/assets/134632821/0d977e52-1e8f-47bd-b6e5-7aae6af0a42b">
</p>

# How does it work?

Once completed, TOMBARTRON will have the capability to generate music videos from start to finish with a single click. This comprehensive process includes:

- Complete music composition, including instrumentation and orchestration, with the option for randomized or non-randomized composition parameters such as form, key, meter, and tempo. This is achieved using a simple rule-based AI.
- Rendering compositions to file, converting MIDI to audio with the [Py-MeltySynth](https://github.com/sinshu/py-meltysynth) and SoundFont libraries.
- Modular modeling of 3D musical instruments using PyOpenGL and animating them to align with the music. This is possible as each model component is rendered separately and can be controlled accordingly.
- Rendering the 3D PyOpenGL scene, which contains animated instruments, into a video using Pygame. Subsequently, this video is combined with the audio file using MoviePy.
- Uploading the resulting video to YouTube via the YouTube API, with options for randomized or non-randomized parameters such as title, description, category, and tags.

# To-Do List
## Audio
- [ ] Implement a MIDI sequencer class supporting playback and communication with graphic modules for real-time animation.
- [ ] Implement music composition logic, from high-level parameters to full orchestration of multi-instrumental compositions.

## Graphics
- [ ] Complete the keyboard model, including buttons, text, and other visual elements.
- [ ] Model additional musical instruments (e.g. guitars, drums, etc.).

# TOMBARTRON 2020 (Max-MSP-Jitter) Content Sample
<p align="center">
  <img src="https://github.com/og-tombar/tombartron/assets/134632821/a026c546-38b3-47ad-9db2-14ad1639f057" alt="TOMBARTRON 2020 Sample">
</p>
