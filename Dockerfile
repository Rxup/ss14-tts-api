FROM python:3.9
ADD requirements.txt .
RUN pip3 install -r ./requirements.txt
ADD ../models.yml .
ADD run.py .
CMD ["python","run.py"]
ENTRYPOINT [ "pyton","run.py" ]