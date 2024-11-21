FROM nvidia/cuda:12.6.2-runtime-ubuntu22.04

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev python-is-python3 wget git&& \
    rm -rf /var/lib/apt/lists/*

ARG DEBIAN_FRONTEND=noninteractive

RUN mkdir /app
WORKDIR /app

RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu124
RUN pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124

RUN git clone https://github.com/comfyanonymous/ComfyUI.git

WORKDIR /app/ComfyUI

RUN pip install -r requirements.txt

COPY comfy.settings.json /app/ComfyUI/user/default

RUN mkdir /app/http-server
WORKDIR /app/http-server
COPY requirements.txt /app/http-server
RUN pip install -r requirements.txt

WORKDIR /app/ComfyUI

WORKDIR /app/ComfyUI/models/checkpoints
RUN wget "https://civitai.com/api/download/models/113479?type=Model&format=SafeTensor&size=pruned&fp=fp16" --content-disposition

WORKDIR /app/ComfyUI/models/vae
RUN wget "https://civitai.com/api/download/models/311162?type=Model&format=SafeTensor" --content-disposition

WORKDIR /app/http-server
COPY call_comfyui_unsecure.py /app/http-server
COPY main.py /app/http-server
CMD exec functions-framework --target=main_handle

WORKDIR /app/ComfyUI
ENTRYPOINT ["python", "main.py"]

#ENTRYPOINT ["python", "main.py", "--listen"]
