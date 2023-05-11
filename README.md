# ss14-tts-api

### Запуск в докере
```
docker build . -t ss14-tts-api:latest
docker rm -f ss14tts
docker run -it -d --name ss14tts -p 5000:5000 ss14-tts-api:latest
```

Просмотр логов в докере:
```
docker logs ss14tts -f
```

### Запуск без docker

Windows: https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe

!!! Выше версии 3.9 не работет !!!

```
pip3 install -r ./requirements.txt --extra-index-url https://download.pytorch.org/whl/cu116
python ss14tts.py
```
### Конфигурация

Файл:
```
config.ini
```
___P.S все переменные у докера находятся в Dockerfile-е!___

Пример конфиг файла для английской модели (Там 100+ спикеров, для теста прописал только 4):

```
language = en
model_id = v3_en
speakers = en_0, en_1, en_2, random
```

language - язык модели\
model_id ~~Как ни странно~~ - Название модели\
speakers - массив спикеров\
Язык и model_id брать отсюда:
```
https://models.silero.ai/models/tts/
```
Спикеров брать отсюда:
```
https://github.com/snakers4/silero-models#v3
```

___После изменения модели в конфиге файл model.pt удалить!___
### Прочее

Конфигурация сервера:

```
[tts]
api_url="http://127.0.0.1:5000/tts"
api_token="test"
enabled=true
```


файл с бесплатными голосами:
> tts-voices.yml

Копирнуть в /Resources/Prototypes/Corvax
