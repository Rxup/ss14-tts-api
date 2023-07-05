FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
VOLUME [ "/root/.cache/" ]
VOLUME [ "/workspace/voices" ]
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends curl libsndfile1 && rm -rf /var/lib/apt/lists/*
RUN python -m venv venv
RUN . venv/bin/activate
ADD requirements.txt .
RUN pip3 install -r ./requirements.txt --extra-index-url https://download.pytorch.org/whl/cu116
RUN yes | pip3 uninstall torchaudio
RUN pip3 install torchaudio==0.13.1+cu116 soundfile --extra-index-url https://download.pytorch.org/whl/cu116
ADD ss14tts.py .
ADD wsgi.py .
COPY src src/
RUN pip3 install gevent
RUN python -c "from ss14tts import app"
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl --fail http://localhost:5000/health || exit 1
EXPOSE 5000
ENTRYPOINT [ "python", "wsgi.py" ]
