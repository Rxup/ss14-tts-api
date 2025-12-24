#!/bin/bash

pkg_lib_path="/usr/local/lib/ffmpeg/ffmpeg-n6.1.1-1-g61b88b4dda-linux64-gpl-6.1"
#BIN_PATH="/usr/local/bin"
BIN_PATH="./bin"

mkdir -p $BIN_PATH

ls -s $pkg_lib_path

# Создаем символические ссылки
ln -sv "${pkg_lib_path}/bin/ffmpeg" "${BIN_PATH}/ffmpeg"
ln -sv "${pkg_lib_path}/bin/ffplay" "${BIN_PATH}/ffplay"
ln -sv "${pkg_lib_path}/bin/ffprobe" "${BIN_PATH}/ffprobe"

echo "Установлен FFmpeg версии ${latest_version}"

"${BIN_PATH}/ffmpeg" -version