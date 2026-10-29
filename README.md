![Nuke](https://img.shields.io/badge/Nuke-17.1v2-F5B335?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11.11-3776AB?style=flat-square&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.7.1-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)

![SandText](https://raw.githubusercontent.com/andreaskrein/andreaskrein.github.io/05b6e969ea30bd65c65d150e31f9a9b03077aeb9/assets/SandText.png)
# FLUX.2[klein] 4B for Nuke
## Runs Flux 2 Klein 4B in an Inference node
Native, local, dependency-free image editing.
### Installation
1. Place the content of this repo into a folder in your local Cattery directory,   
   for example `~/.nuke/Cattery/flux-2-klein-4B-for-Nuke`

3. download the image-to-image [model](https://huggingface.co/andreaskrein/flux-2-klein-4B_I2I_512px/resolve/main/flux-2-klein-4B_I2I_512px.cat) and the [text encoder](https://huggingface.co/andreaskrein/qwen-3/resolve/main/qwen-3.cat), and put them inside this folder as well

5. in Nuke, update the Cattery (**Cattery > Update**)
   
   ![Cattery menu](https://raw.githubusercontent.com/andreaskrein/andreaskrein.github.io/master/assets/Cattery.png)
***   
### Properties
Connect an input and a reference image to the node. Enter your image editing prompt, and press the button to encode it. You can then change the seed. With FLUX 2, steps and guidance are hardcoded at `steps=4` and `cfg=1`.
![Properties](https://raw.githubusercontent.com/andreaskrein/andreaskrein.github.io/master/assets/flux-2-klein-4B-for-Nuke.png)

<!-- <img src="https://raw.githubusercontent.com/andreaskrein/andreaskrein.github.io/master/assets/handbag.png" width=256 height=256><img src="https://raw.githubusercontent.com/andreaskrein/andreaskrein.github.io/master/assets/output.png" width=256 height=256>![edit](https://raw.githubusercontent.com/andreaskrein/andreaskrein.github.io/master/assets/edit.png)) -->

### License
flux-2-klein-4b_I2I_512px.cat is an experimental implementation licensed under the Apache 2 License and is derived from **black-forest-labs/FLUX.2-klein-4B**. Although the Apache 2 License permits commercial use of the flux-2-klein-4b_I2I_512px.cat code, the underlying pre-trained models, associated training data, and dependencies may be subject to separate — including non-commercial — licensing restrictions that are not covered by this license. Users should consult the original Flux 2 klein 4B repository for further information on applicable licensing terms and are solely responsible for ensuring that their intended use complies with all relevant restrictions. **No legal responsibility is assumed by the author for your use of results generated with this implementation.**
