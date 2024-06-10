from diracore.main import cli, click, config, app
from typing import Any

import shutil
import os
from importlib import util

@cli.command("nats.public")
def set_webhook_telegram():
    source_module = 'diranats.config.nats'
    destination_module = 'config'

    # Получите путь к исходному файлу
    source_file = get_module_path(source_module)

    # Убедитесь, что директория назначения существует
    destination_dir = os.path.dirname(get_module_path(destination_module))
    os.makedirs(destination_dir, exist_ok=True)

    # Копирование файла
    destination_file = os.path.join(destination_dir, os.path.basename(source_file))
    shutil.copy(source_file, destination_file)

def get_module_path(module_name):
    """Получить путь к файлу модуля."""
    spec = util.find_spec(module_name)
    if spec is None:
        raise ImportError(f"Модуль '{module_name}' не найден")
    return spec.origin