from myapp.config import Config, load_config
from myapp.db import DbHandler
from myapp.db.mdb import MariaDbRepository
from myapp.logger.logger import log


class Container:
    config: Config
    db_hnd: DbHandler


# _container: Container | None = None


def new_container() -> Container:
    global _container

    c = Container()

    # load config
    try:
        c.config = _init_config()
    except Exception as e:
        raise RuntimeError(f"config loading error..{e}") from e

    # init database
    c.db_hnd = _init_database(c.config)

    # _container = c
    return c


def _init_config() -> Config:
    return load_config(".")


def _init_database(cfg: Config) -> DbHandler:
    repo = MariaDbRepository(
        user=cfg.db_user,
        pw=cfg.db_passwd,
        dbname=cfg.db_name,
        host=cfg.db_address,
        port=cfg.db_port,
    )
    try:
        repo.init()
    except Exception as e:
        log.error("Db Init err.. {}", str(e))
    return repo
