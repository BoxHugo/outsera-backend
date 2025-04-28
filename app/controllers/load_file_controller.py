from app.application.read_file_use_case import ReadFileUseCase
from app.application.add_db_use_case import AddDB
from app.infra.logger_module.log_utils import LogUtils


class LoadFileController:

    @classmethod
    def run(cls):

        log = LogUtils("load file")

        log.info("Iniciando...\nCarregando arquivo...")
        rows = ReadFileUseCase.run(log)

        log.info("Adicionando os registros no banco de dados")
        AddDB.run(log, rows)

        log.info("Arquivo carregado com sucesso.")
