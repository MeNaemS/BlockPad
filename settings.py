from dynaconf import Dynaconf
from schemas.config import Config, Dotenv
from adaptix import Retort

# Загружаем .env
raw_dotenv = Dynaconf(dotenv_path=".env", load_dotenv=True, envvar_prefix="DYNACONF_")
dotenv = Dotenv(
    config_path=raw_dotenv.config_path,
    config_file=raw_dotenv.config_file,
    shapes_path=raw_dotenv.shapes_path
)

# Загружаем JSON с конфигами
raw_settings = Dynaconf(
    settings_files=[
        f"{dotenv.config_path}/{dotenv.config_file}",
        f"{dotenv.config_path}/{dotenv.shapes_path}",
    ]
)

# Используем Adaptix для приведения к модели Config
retort = Retort()
settings: Config = retort.load(raw_settings, Config)

