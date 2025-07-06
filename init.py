import os
from colorama import Fore, Back, Style, init
import logging
from datetime import datetime
import sys

# Инициализация colorama
init(autoreset=True)

# Настройка логирования с UTF-8
def setup_logging():
    logging.basicConfig(
        filename='system_info.log',
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8'  # Явное указание кодировки
    )
    # Для старых версий Python (менее 3.9) используем хак:
    if sys.version_info < (3, 9):
        handler = logging.FileHandler('system_info.log', encoding='utf-8')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S'))
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.INFO)

setup_logging()

def log_info(message):
    """Логирует информацию и выводит её в консоль"""
    # Удаляем цветовые коды для лог-файла
    clean_message = re.sub(r'\x1b\[[0-9;]*m', '', message)
    logging.info(clean_message)
    print(message)

def windows_collect_info():
    """Собирает информацию о системе Windows"""
    def get_wmic_data(query, description):
        """Получает данные из WMIC и форматирует их"""
        try:
            result = os.popen(f"wmic {query}").read()
            # Исправляем кодировку вывода WMIC
            if sys.stdout.encoding != 'utf-8':
                result = result.encode(sys.stdout.encoding, errors='replace').decode('utf-8', errors='replace')
            return f"{Fore.GREEN}{description}:\n{result.strip()}"
        except Exception as e:
            return f"{Fore.RED}Ошибка при получении {description}: {str(e).encode('utf-8', errors='replace').decode('utf-8')}"

    # Получаем информацию
    sections = [
        ("cpu get name", "cpu"),
        ("memorychip get capacity", "ram"),
        ("path win32_videocontroller get name", "gpu"),
        ("diskdrive get model,size", "hdd")
    ]

    for query, description in sections:
        info = get_wmic_data(query, description)
        log_info(info)

def system_definition():
    """Определяет систему и запускает сбор информации"""
    print(f"{Fore.CYAN}Hello user, pick your system:")
    print(f"{Fore.YELLOW}1. Windows")
    print(f"{Fore.YELLOW}2. Linux")
    
    try:
        pick = input(f"{Fore.WHITE}yout pick: ")
        if pick == "1":
            log_info("\nPick windows...\n")
            windows_collect_info()
        elif pick == "2":
            log_info("\nlinux not supported\n")
        else:
            log_info(f"{Fore.RED}ERROR")
    except Exception as e:
        log_info(f"{Fore.RED}ERROR: {str(e).encode('utf-8', errors='replace').decode('utf-8')}")

if __name__ == "__main__":
    import re
    try:
        system_definition()
    except Exception as e:
        logging.error(f"CRITICAL ERROR: {str(e).encode('utf-8', errors='replace').decode('utf-8')}")
        print(f"{Fore.RED}CRITICAL ERROR: {e}")
    finally:
        print(Style.RESET_ALL)