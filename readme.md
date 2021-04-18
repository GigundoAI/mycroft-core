# mycroft-lib

mycroft lib is a repackaged version of mycroft-core

It is aimed at developers and makers interested in building on top of the 
mycroft stack, if you are a end-user that just wants to install mycroft 
please see the [official repository](https://github.com/MycroftAI/mycroft-core/) instead

* [Changes](#changes)
* [Install](#install)
    - [Bus](#bus)
    - [Enclosure/GUI](#enclosure-gui)
    - [STT](#stt)
    - [TTS](#tts)
    - [Audio Service](#audio-service)
    - [Skills](#skills)
    

## Changes

mycroft-lib tries to be a drop-in replacement for mycroft-core, most 
changes are just cleanup and moving imports around, however there are some 
notable new features:

- [puretryout's XDG PR](https://github.com/MycroftAI/mycroft-core/pull/2803) has been merged early
- [backend](https://github.com/HelloChatterbox/mycroft-lib/pull/9) is optional / can be disabled in .conf
- [msm](https://github.com/HelloChatterbox/mycroft-lib/pull/24) is optional / can be disabled in .conf
- [padatious](https://github.com/HelloChatterbox/mycroft-lib/pull/23) is optional / can be disabled in .conf
- lingua_franca [0.4.x](https://github.com/MycroftAI/mycroft-core/pull/2772) support has been merged early
- lingua_franca can be replaced with [lingua_nostra](https://github.com/HelloChatterbox/lingua-nostra)


## Install

The main assumption of mycroft-lib is that you may want to run only some 
pieces of the mycroft stack, this means the requirements vary wildly 
depending on the use case.

eg, if you are making a web chatbot you do not want the audio stack at all

by default mycroft-lib will only install the bare minimum requirements 
common to all individual mycroft services

```bash
pip install mycroft-lib==2021.4.2a14
```

you can perform a full install with
```bash
pip install mycroft-lib[all]==2021.4.2a14
```

### Additional requirements

#### Bus

if you want to run the messagebus (instead of connecting to an existing one)
```bash
pip install mycroft-lib[bus]==2021.4.2a14
```

#### Enclosure/GUI

if you want to run the enclosure service in order to connect mycroft-gui

```bash
pip install mycroft-lib[enclosure]==2021.4.2a14
```

#### STT

if you want to perform speech recognition
```bash
pip install mycroft-lib[stt]==2021.4.2a14
```

to install optional STT engines (google cloud)
```bash
pip install mycroft-lib[stt_engines]==2021.4.2a14
```

#### TTS
to install optional TTS engines (gTTS)
```bash
pip install mycroft-lib[tts_engines]==2021.4.2a14
```

#### Audio Service

if you want to install optional audio backends (vlc + pychromecast)
```bash
pip install mycroft-lib[audio_engines]==2021.4.2a14
```

#### Skills

the skills service is the most customizable

a minimal install will only require [adapt](https://github.com/MycroftAI/adapt) and [padaos](https://github.com/MycroftAI/padaos), in this case 
msm will be disabled and padatious replaced with padaos
```bash
pip install mycroft-lib[skills_minimal]==2021.4.2a14
```

a regular install will include padatious and msm
```bash
pip install mycroft-lib[skills]==2021.4.2a14
```

mycroft-lib supports both [lingua_franca](https://github.com/MycroftAI/lingua-franca) and [lingua_nostra](https://github.com/HelloChatterbox/lingua-nostra)

if both packages are installed preference is given to [lingua_nostra](https://github.com/HelloChatterbox/lingua-nostra)

you must install **only one** of these manually

```bash
pip install mycroft-lib[lingua_nostra]==2021.4.2a14
```
or
```bash
pip install mycroft-lib[lingua_franca]==2021.4.2a14
```