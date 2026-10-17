![Nuke](https://img.shields.io/badge/Nuke-17.1v2-F5B335?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11.11-3776AB?style=flat-square&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.7.1-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)

![SandText](https://raw.githubusercontent.com/andreaskrein/andreaskrein.github.io/05b6e969ea30bd65c65d150e31f9a9b03077aeb9/assets/SandText.png)
# FLUX.2[klein] 4B for Nuke
## Runs Flux 2 Klein 4B in an Inference node
### Installation
1. Place the content of this repo into a folder in your local Cattery directory,   
   for example `~.nuke/Cattery/flux-2-klein-4B-for-Nuke`

3. Download the image-to-image [model](https://huggingface.co/andreaskrein/flux-2-klein-4B_I2I_512px/resolve/main/flux-2-klein-4B_I2I_512px.cat) and the [text encoder](https://huggingface.co/andreaskrein/qwen-3/resolve/main/qwen-3.cat), and put them inside this folder as well

5. In Nuke, update the Cattery (**Cattery > Update**)
   
   ![Cattery menu](https://raw.githubusercontent.com/andreaskrein/andreaskrein.github.io/master/assets/Cattery.png)
***   
### Properties
![Properties](https://raw.githubusercontent.com/andreaskrein/andreaskrein.github.io/master/assets/flux-2-klein-4B-for-Nuke.png)
Enter your prompt, and press the button to encode it.   
You can change the seed, but steps and guidance are hardcoded at `steps=4` and `cfg=1` with FLUX.
