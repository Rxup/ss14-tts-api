FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime 
ADD requirements.txt .
RUN pip3 install -r ./requirements.txt --extra-index-url https://download.pytorch.org/whl/cu116
ADD run.py .
EXPOSE 5000
CMD ["python","run.py"]
ENTRYPOINT [ "python","run.py" ]