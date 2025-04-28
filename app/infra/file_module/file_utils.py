import csv
import os
import shutil

from typing import List

from app.exceptions import (
    NoFilesFoundException, 
    MultipleFilesException, 
    FilePathDoesNotExistsException,
    FormatFileIsNotValidException,
    NoHeaderException,
    ColumnNotFoundException,
    FileEmptyException
)


class FileUtils:

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.columns = ["year", "title", "studios", "producers", "winner"]
        self.INPUT_DIR = f"{self.filepath}/input"
        self.PROCESSED_DIR = f"{self.filepath}/processed"
        self.valid_format = ".csv"

    def parse_producers(self, producers_str: str) -> List[str]:

        producers_str = producers_str.replace(" and ", ",")
        
        return [producer.strip() for producer in producers_str.split(",") if producer.strip()]

    def create_folders(self):
        """ Cria as pastas necessárias para o gerenciamento do arquivo. """

        folders_path = [self.filepath, self.INPUT_DIR, self.PROCESSED_DIR]

        for folder in folders_path:

            if not os.path.exists(folder):
                os.makedirs(folder)

    def read_csv(self, filename: str) -> List[dict]:
        """ Consome o arquivo. """

        if not filename.endswith(self.valid_format):
            raise FormatFileIsNotValidException(f"Arquivo {filename} não está no formato {self.valid_format}")
    
        with open(f"{self.INPUT_DIR}/{filename}", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")

            if reader.fieldnames is None:
                raise NoHeaderException("Arquivo sem cabeçalho.")
            
            missing_columns = [col for col in self.columns if col not in reader.fieldnames]

            if missing_columns:
                raise ColumnNotFoundException(f"Algumas das seguintes colunas: {', '.join(missing_columns)} não foi encontrada.")
            
            # rows = [row for row in reader]
            
            rows = []

            for row in reader:

                award = {
                    'year': str(row.get('year')).strip(),
                    'title': row.get('title').strip(),
                    'studios': row.get('studios').strip(),
                    'producers': self.parse_producers(row.get('producers')),
                    'winner': row.get('winner','').lower().strip()
                }
                
                rows.append(award.copy())

            if not rows:
                raise FileEmptyException("Arquivo vazio")

        return rows
    
    def move_file(self, filename: str):
        """ Move o arquivo processado para a pasta /processed """

        fullpath_file = f"{self.INPUT_DIR}/{filename}"
        destination = f"{self.PROCESSED_DIR}/{filename}"

        shutil.move(fullpath_file, destination)

    def validate_filepath(self):
        """ Valida se os diretórios existem para o gerenciamento do arquivo """

        if not os.path.exists(self.INPUT_DIR):
            raise FilePathDoesNotExistsException(f"Diretório '{self.INPUT_DIR}' não existe.")
        
        if not os.path.exists(self.PROCESSED_DIR):
            raise FilePathDoesNotExistsException(f"Diretório '{self.PROCESSED_DIR}' não existe.")
        
    def get_files(self) -> List[str]:

        return [f for f in os.listdir(self.INPUT_DIR) if f.endswith(self.valid_format)]


    def get_filename(self) -> str:
        """Busca os arquivos na pasta de input. """

        files = self.get_files()

        if len(files) == 0:
            raise NoFilesFoundException(f"Nenhum arquivo encontrado no diretório '{self.INPUT_DIR}'.")
        
        if len(files) > 1:
            raise MultipleFilesException("Multiplos arquivos encontrados no diretório. É esperado apenas um.")

        return files[0]
