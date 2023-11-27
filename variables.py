from pathlib import Path

ROOT_DIR = Path(__file__).parent

FILES_DIR = ROOT_DIR / '_img/'
WINDOW_ICON_PATH = FILES_DIR / 'icone2.png'


if __name__ == '__main__':
    print(ROOT_DIR)
    print(FILES_DIR)
    print(WINDOW_ICON_PATH)
