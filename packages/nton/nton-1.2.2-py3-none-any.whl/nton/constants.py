import shutil
import sys
import tempfile
from pathlib import Path

from appdirs import AppDirs


class Directories:
    app_dirs = AppDirs("nton", "rlaphoenix")
    root = Path(__file__).resolve().parent  # root of package/src
    user_configs = Path(app_dirs.user_config_dir)
    data = Path(app_dirs.user_data_dir)
    cache = Path(app_dirs.user_cache_dir)
    logs = Path(app_dirs.user_log_dir)
    temp = Path(tempfile.gettempdir()) / "rlaphoenix-nton"
    output = Path.home() / "Desktop" / "NTON"
    assets = root / "assets"


class Binaries:
    nstool = shutil.which("nstool")
    hacbrewpack = shutil.which("hacbrewpack")
    hptnacp = shutil.which("hptnacp")
    magick = shutil.which("magick")


class Files:
    keys_home = (Path.home() / ".switch" / "prod.keys")
    keys_cwd = Path("./prod.keys").absolute()
    keys = keys_cwd if keys_cwd.is_file() else keys_home


for binary, path in vars(Binaries).items():
    if binary.startswith("__"):
        continue
    if not path:
        print(
            f"!! {binary} cannot be found! Please place it in the current working directory or"
            "put it's path in your PATH Environment Variable, or put the binary."
        )
        sys.exit(1)

if not Files.keys.is_file():
    print(f"!! prod.keys is missing! Please place it in the current working directory or at \"{Files.keys_home}\"")
    sys.exit(1)
