from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
GUI_ROOT = PROJECT_ROOT / "GUI"
RESOURCE_ROOT = GUI_ROOT / "Resources"

THEME_PATH = str(GUI_ROOT / "Themes.json")
DATABASE_PATH = str(PROJECT_ROOT / "database.db")
FEN_STRING_PATH = str(PROJECT_ROOT / "fenString.txt")
BOARD_IMAGE_PATH = str(PROJECT_ROOT / "board.png")


def resource_path(*parts):
    return str(RESOURCE_ROOT.joinpath(*parts))
