# HOLMES V

HOLMES V (formerly [mycroft-lib](https://mycroft.ai/trademark/)) is a repackaged version of [mycroft-core](https://github.com/MycroftAI/mycroft-core/)

`Mike, alias Adam Selene, alias Simon Jester, alias Mycroft Holmes, officially an augmented HOLMES IV system, is a supercomputer empowered to take control of Lunar society, which achieved self-awareness`

`HOLMES V` is named after the `HOLMES IV` system from the novel `The Moon is a Harsh Mistress` by `Robert Heinlein`, It is the system the next generation of voice assistants will be built on top of

It is aimed at developers and makers interested in building on top of the mycroft stack, if you are a end-user that just wants to install mycroft please see the [official repository](https://github.com/MycroftAI/mycroft-core/) instead


- [HOLMES V](#holmes-v)
  * [Features](#features)
  * [Objectives](#objectives)
  * [Compatibility](#compatibility)
  * [Install](#install)
    + [Additional requirements](#additional-requirements)
      - [Skills](#skills)
      - [Bus](#bus)
      - [Enclosure/GUI](#enclosure-gui)
      - [STT](#stt)
      - [TTS](#tts)
      - [Audio Service](#audio-service)
      
  
## Features

HolmesV tries to be a drop-in replacement for mycroft-core, most changes are just cleanup and moving imports around, however there are some notable new features:

- [XDG compliant](https://github.com/HelloChatterbox/HolmesV/pull/32)
- [internet_connection](https://github.com/HelloChatterbox/HolmesV/pull/28) is optional / can be disabled in .conf
- [backend](https://github.com/HelloChatterbox/HolmesV/pull/9) is optional / can be disabled in .conf
- [msm](https://github.com/HelloChatterbox/HolmesV/pull/24) is optional / can be disabled in .conf
- [padatious](https://github.com/HelloChatterbox/HolmesV/pull/23) is optional / can be disabled in .conf
- lingua_franca [0.4.x](https://github.com/MycroftAI/mycroft-core/pull/2772)
- lingua_franca can be replaced with [lingua_nostra](https://github.com/HelloChatterbox/lingua-nostra)


## Objectives

- facilitate the development of projects on top of the mycroft-core
- repackage mycroft-core as a library that can be easily distributed
- modularize mycroft-core into small reusable components
- minimize the amount of dependencies required for a given setup
- maximize the amount of platforms HolmesV can be used on
- do not break the established mycroft-core API other projects rely on
- transparently load skills developed for mycroft-core
- transparently integrate with any project developed to interface with mycroft-core
- maximize customization options to account for unforeseen use cases and applications
- enhancements should be done as a .conf option when possible
- it should always be possible to run HolmesV with the same exact configuration as mycroft-core, given that all system requirements are met
- versioning should indicate the state of HolmesV synchronization with mycroft-core
   - main version number is the date of last sync with dev branch on mycroft-core
   - alpha releases indicate the objectives above are not yet 100% achieved
   - beta releases indicate all objectives above are meet


## Compatibility

**you can not install HolmesV side by side with mycroft-core**, it is meant to replace it! 

Because it is a drop in replacement that means `import mycroft` would conflict between both versions

HolmesV runs skills made for mycroft-core and interfaces with all known mycroft projects, see the [æwesome-mycroft-community](https://github.com/ChanceNCounter/awesome-mycroft-community) for a selection of projects that you can integrate with HolmesV
 

## Install

The main assumption of HolmesV is that you may want to run only some pieces of the mycroft stack, this means the requirements vary wildly depending on the use case.

eg, if you are making a web chatbot you do not want the audio stack at all

by default HolmesV will only install the bare minimum requirements common to all individual mycroft services

```bash
pip install HolmesV==2021.5.6a2
```

if you want the exact same stack as mycroft-core
```bash
pip install HolmesV[mycroft]==2021.5.6a2
```

you can perform a full recommended install with
```bash
pip install HolmesV[all]==2021.5.6a2
```

differences between `HolmesV[all]` and `HolmesV[mycroft]`:
- replaces msm with mock-msm
- replaces lingua_franca with lingua_nostra


### Additional requirements

#### Skills

the skills service is the most customizable

- msm needs to be explicitly installed, automatically disabled if unavailable
- lingua_franca needs to be explicitly installed

HolmesV supports both [lingua_franca](https://github.com/MycroftAI/lingua-franca) and [lingua_nostra](https://github.com/HelloChatterbox/lingua-nostra)

skills can use either of these packages directly, both are properly configured internally, however HolmesV gives preference to [lingua_nostra](https://github.com/HelloChatterbox/lingua-nostra)

a minimal install will only require [adapt](https://github.com/MycroftAI/adapt), [padaos](https://github.com/MycroftAI/padaos) and [lingua_nostra](https://github.com/HelloChatterbox/lingua-nostra)

```bash
pip install HolmesV[skills_minimal]==2021.5.6a2
```

a regular install will also include padatious
```bash
pip install HolmesV[skills]==2021.5.6a2
```


#### Bus

if you want to run the messagebus (instead of connecting to an existing one)
```bash
pip install HolmesV[bus]==2021.5.6a2
```

#### Enclosure/GUI

if you want to run the enclosure service in order to connect mycroft-gui

```bash
pip install HolmesV[enclosure]==2021.5.6a2
```

#### STT

if you want to perform speech recognition
```bash
pip install HolmesV[stt]==2021.5.6a2
```

to install optional STT engines (google cloud)
```bash
pip install HolmesV[stt_engines]==2021.5.6a2
```

#### TTS
to install optional TTS engines (gTTS)
```bash
pip install HolmesV[tts_engines]==2021.5.6a2
```

#### Audio Service

if you want to install optional audio backends (vlc + pychromecast)
```bash
pip install HolmesV[audio_engines]==2021.5.6a2
```

