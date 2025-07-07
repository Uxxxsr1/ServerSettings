import os
import subprocess
import shutil
import sys
from pathlib import Path

def clone_and_run(repo_url, script_path, clone_dir="cloned_repo"):
    """
    Клонирует репозиторий и выполняет указанный скрипт из него
    
    :param repo_url: URL GitHub репозитория
    :param script_path: Путь к скрипту внутри репозитория
    :param clone_dir: Директория для клонирования (по умолчанию 'cloned_repo')
    """
    try:
        # Удаляем директорию, если она уже существует
        if os.path.exists(clone_dir):
            print(f"Удаляем существующую директорию {clone_dir}...")
            shutil.rmtree(clone_dir)
        
        # Клонируем репозиторий
        print(f"Клонируем репозиторий {repo_url}...")
        subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
        
        # Полный путь к скрипту
        full_script_path = Path(clone_dir) / script_path
        
        if not full_script_path.exists():
            raise FileNotFoundError(f"Скрипт {full_script_path} не найден в репозитории")
        
        print(f"Запускаем скрипт {full_script_path}...")
        
        # Переходим в директорию репозитория
        os.chdir(clone_dir)
        
        # Запускаем скрипт (предполагаем, что это Python скрипт)
        subprocess.run([sys.executable, str(script_path)], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Возвращаемся в исходную директорию
        os.chdir("..")

if __name__ == "__main__":
    # Пример использования
    if len(sys.argv) < 3:
        print("Использование: python clone_and_run.py <repo_url> <script_path> [clone_dir]")
        print("Пример: python clone_and_run.py https://github.com/user/repo.git scripts/main.py my_repo")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    script_path = sys.argv[2]
    clone_dir = sys.argv[3] if len(sys.argv) > 3 else "cloned_repo"
    
    clone_and_run(repo_url, script_path, clone_dir)
