FROM pytorch/pytorch:2.3.1-cuda11.8-cudnn8-runtime
VOLUME [ "/root/.cache/" ]
VOLUME [ "/workspace/voices" ]
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends curl wget jq libsndfile1 sox libsox-dev libsox-fmt-all libavdevice-dev && rm -rf /var/lib/apt/lists/*
RUN python -m venv venv
RUN . venv/bin/activate
ADD requirements.txt .
RUN pip3 install -r ./requirements.txt --extra-index-url https://download.pytorch.org/whl/cu116
ADD ss14tts.py .
ADD wsgi.py .
ADD *.wav .
COPY src src/
RUN pip3 install gevent
RUN ldconfig
ADD ffmpeg-install-latest.sh .
RUN bash ./ffmpeg-install-latest.sh
RUN rm ./ffmpeg-install-latest.sh
ADD test.py .
RUN python test.py
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl --fail http://localhost:5000/health || exit 1
EXPOSE 5000
ENTRYPOINT [ "python", "wsgi.py" ]
