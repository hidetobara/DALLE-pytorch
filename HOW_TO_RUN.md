# docker build
docker build -t dalle ./docker

# docker run
docker run  -it --rm --mount src="/c/obara/DALLE-pytorch/",target=/work,type=bind dalle /bin/bash
### --gpus all
