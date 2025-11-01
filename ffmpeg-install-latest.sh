#!/bin/bash

# URL для получения информации о последней версии
api_url="https://api.github.com/repos/BtbN/FFmpeg-Builds/releases"

# Получаем информацию о последнем релизе и выбранном файле
#latest_version=$(curl -s $api_url | jq -r '.[0].tag_name')
#file_name="ffmpeg-master-latest-linux64-gpl-shared.tar.xz"
#file_info=$(curl -s $api_url | jq --arg file "$file_name" '.[0].assets | map(select(.name == $file))[0]')

# Формируем URL для скачивания файла
#download_url=$(echo $file_info | jq -r '.browser_download_url')

file_name=ffmpeg-n6.0.1-linux64-gpl-shared-6.0.tar.xz
download_url=https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2023-11-30-12-55/ffmpeg-n6.0.1-linux64-gpl-shared-6.0.tar.xz

# Временная директория
temp_dir="/tmp/ffmpeg_temp"

# Создаем временную директорию, если она не существует
mkdir -p $temp_dir

# Скачиваем файл
wget $download_url -O /tmp/$file_name

stat /tmp/$file_name
ls -s $temp_dir

# Распаковываем архив
tar -xf /tmp/$file_name -C $temp_dir

# Указываем пути
#pkg_path="$temp_dir/ffmpeg-master-latest-linux64-gpl-shared"
ls -s $temp_dir
cat /etc/*release*
pkg_path="$temp_dir/ffmpeg-n6.0.1-linux64-gpl-shared-6.0"
pkg_lib_path="/usr/local/lib/ffmpeg"
#BIN_PATH="/usr/local/bin"
BIN_PATH="./bin"

# Создаем директорию, если она не существует
mkdir -p $pkg_lib_path
mkdir -p $BIN_PATH

ls -s $pkg_path

# Копируем файлы
cp -r $pkg_path/* $pkg_lib_path/

# Создаем символические ссылки
ln -sv "${pkg_lib_path}" "${pkg_lib_path}"
ln -sv "${pkg_lib_path}/bin/ffmpeg" "${BIN_PATH}/ffmpeg"
ln -sv "${pkg_lib_path}/bin/ffplay" "${BIN_PATH}/ffplay"
ln -sv "${pkg_lib_path}/bin/ffprobe" "${BIN_PATH}/ffprobe"

# Очищаем временную директорию
rm -rf $temp_dir

echo "Установлен FFmpeg версии ${latest_version}"

"${BIN_PATH}/ffmpeg" -version