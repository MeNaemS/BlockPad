from dynaconf import Dynaconf
from schemas.config import Config, Dotenv
<<<<<<< HEAD
=======

>>>>>>> 5ed53aa9690a25eafc51ca89f3f362346ab756fa
dotenv: Dotenv = Dynaconf(dotenv_path='.env', load_dotenv=True, envvar_prefix='DYNACONF_')
settings: Config = Dynaconf(
    settings_files=[
        f'{dotenv.config_path}/{dotenv.config_file}',
        f'{dotenv.config_path}/{dotenv.shapes_path}'
    ]
)
<<<<<<< HEAD

=======
>>>>>>> 5ed53aa9690a25eafc51ca89f3f362346ab756fa
