from app.infra.file_module.file_utils import FileUtils
from config import config
from typing import List, Dict



class ReadFileUseCase:

    @classmethod
    def run(cls, log: 'LogUtils') -> List[Dict]:
        
        file_module = FileUtils(config.bucketpath)

        log.info("Criando pastas utilizadas no gerenciamento do arquivo")
        file_module.create_folders()

        log.info("Validando pastas utilizadas no gerenciamento do arquivo")
        file_module.validate_filepath()

        log.info("Recuperando arquivo")
        filename = file_module.get_filename()

        log.info("Lendo arquivo")
        rows = file_module.read_csv(filename)

        log.info("Movendo arquivo para processados")
        # file_module.move_file(filename)

        log.info("Leitura finalizada.")
        return rows
