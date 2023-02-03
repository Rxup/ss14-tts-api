# ss14-tts-api

### запуск в докере
```
docker build . -t ss14-tts-api:latest
docker rm -f ss14tts
docker run -it -d --name ss14tts -p 5000:5000 ss14-tts-api:latest
```

просмотр логов в докере:
```
docker logs ss14tts -f
```

### запуск без docker

windows: https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe

!!! выше версии 3.9 не работет !!!

```
pip3 install -r ./requirements.txt --extra-index-url https://download.pytorch.org/whl/cu116
python ss14tts.py
```

### Прочие

конфиг:

```
[tts]
api_url="http://127.0.0.1:5000/tts"
api_token="test"
enabled=true
```


файл с бесплатными голосами:
> tts-voices.yml

копирнуть в /Resources/Prototypes/Corvax
