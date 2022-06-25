#!/bin/sh
set -e

if [ "$1" = 'telegram' ]; then
  exec python bot_tg.py
elif [ "$1" = 'vk' ]; then
  exec python bot_vk.py
elif [ "$1" = 'manage-intents' ]; then
  exec python manage_intents.py
else
  exec "$@"
fi
