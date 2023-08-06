from alembic.config import Config
from alembic import command

from jija import drivers


class SQLAlchemyDriver(drivers.DatabaseDriver):
    def __init__(self, engine, migrator_url: str = None):
        self.__engine = engine
        self.__url = migrator_url or self.__engine.url

    @property
    def engine(self):
        return self.__engine

    async def get_connection(self):
        raise NotImplementedError()

    async def migrate(self):
        if not self._is_alembic_inited():
            self._init_alembic()
            print(
                'Alembic is inited. Fill target_metadata in migrations/env.py file. Then run "migrate" command again.'
            )
            return

        config = self._get_alembic_config()
        command.revision(config, autogenerate=True)

    async def update(self):
        if not self._is_alembic_inited():
            print('Alembic is not inited. Run "migrate" command first.')
            exit(1)

        config = self._get_alembic_config()
        command.upgrade(config, 'head')

    @staticmethod
    def _is_alembic_inited():
        from jija.config import StructureConfig
        return StructureConfig.PROJECT_PATH.joinpath('migrations').exists()

    def _init_alembic(self):
        config = self._get_alembic_config()
        command.init(config, directory='migrations')

    def _get_alembic_config(self):
        from jija.config import StructureConfig

        alembic_cfg = Config('alembic.ini')

        alembic_cfg.set_main_option('script_location', StructureConfig.PROJECT_PATH.joinpath('migrations').as_posix())
        alembic_cfg.set_main_option('sqlalchemy.url', self.__url)

        return alembic_cfg
