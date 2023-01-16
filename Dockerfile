FROM pytorch/pytorch:latest
ADD requirements.txt .
RUN pip3 install -r ./requirements.txt
ADD run.py .
EXPOSE 5000
CMD ["python","run.py"]
ENTRYPOINT [ "pyton","run.py" ]