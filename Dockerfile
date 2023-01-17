FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
RUN python -m venv venv
RUN . venv/bin/activate
ADD requirements.txt .
RUN pip3 install -r ./requirements.txt --extra-index-url https://download.pytorch.org/whl/cu116
RUN yes | pip3 uninstall torchaudio
RUN pip3 install soundfile torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
ADD ss14tts.py .
ADD wsgi.py .
RUN pip3 install gevent
EXPOSE 5000
VOLUME [ "/root/.cache/torch/hub/" ]
ENTRYPOINT [ "python", "wsgi.py" ]