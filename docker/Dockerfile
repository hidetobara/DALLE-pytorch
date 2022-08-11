# FROM pytorch/pytorch:1.10.0-cuda11.3-cudnn8-devel
FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu20.04

RUN apt -y update && apt -y install git vim less python3-pip
RUN pip3 install torch==1.8.2 torchvision==0.9.2 torchaudio==0.8.2 --extra-index-url https://download.pytorch.org/whl/lts/1.8/cu111
RUN pip3 install axial_positional_embedding einops>=0.3.2 ftfy packaging pillow regex rotary-embedding-torch taming-transformers-rom1504 tokenizers torch>=1.6 torchvision transformers tqdm youtokentome WebDataset

RUN pip3 install git+https://github.com/openai/DALL-E.git
# RUN pip3 install git+https://github.com/openai/CLIP.git

# RUN pip3 install beautifulsoup4

WORKDIR /work
