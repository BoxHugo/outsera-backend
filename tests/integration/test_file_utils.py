import pytest
from app.infra.file_module.file_utils import FileUtils
from app.exceptions import (
    FormatFileIsNotValidException,
    ColumnNotFoundException,
    FileEmptyException,
    NoHeaderException,
    NoFilesFoundException,
    FilePathDoesNotExistsException
)
from tests.conftest import create_csv

def test_read_valid_csv(setup_folders):
    """ Testa leitura do arquivo """

    fu = FileUtils(str(setup_folders))
    fu.create_folders()

    content = "year;title;studios;producers;winner\n1980;Test Movie;Studio;Producer 1;yes"
    create_csv(setup_folders / "input", "file.csv", content)

    rows = fu.read_csv("file.csv")

    assert rows[0]['title'] == "Test Movie"
    assert rows[0]['producers'] == ["Producer 1"]

def test_read_invalid_format(setup_folders):
    """ Testa o formato do arquivo """

    fu = FileUtils(str(setup_folders))
    fu.create_folders()

    content = "any content"
    create_csv(setup_folders / "input", "file.txt", content)

    with pytest.raises(FormatFileIsNotValidException):
        fu.read_csv("file.txt")

def test_missing_columns_csv(setup_folders):
    """ Verifica as colunas obrigatórias """

    fu = FileUtils(str(setup_folders))
    fu.create_folders()

    # studios faltando
    content = "year;title;producers;winner\n1980;Test Movie;Producer;yes"  
    create_csv(setup_folders / "input", "file.csv", content)

    with pytest.raises(ColumnNotFoundException):
        fu.read_csv("file.csv")

def test_empty_csv_file(setup_folders):
    """ Verifica se o arquivo está vazio """

    fu = FileUtils(str(setup_folders))
    fu.create_folders()

    content = "year;title;studios;producers;winner\n"
    create_csv(setup_folders / "input", "empty.csv", content)

    with pytest.raises(FileEmptyException):
        fu.read_csv("empty.csv")

def test_no_header_csv(setup_folders):
    """ Verifica se tem cabeçalho """

    fu = FileUtils(str(setup_folders))
    fu.create_folders()

    content = "1980;Test Movie;Studio;Producer;yes\n"
    create_csv(setup_folders / "input", "noheader.csv", content)

    with pytest.raises(NoHeaderException):
        fu.read_csv("noheader.csv")

def test_no_file_found(setup_folders):
    """ Verifica se o arquivo existe """

    fu = FileUtils(str(setup_folders))
    fu.create_folders()

    with pytest.raises(NoFilesFoundException):
        fu.get_filename()

def test_directory_not_found(tmp_path):
    """ Verifica se o diretório existe """

    wrong_path = tmp_path / "wrong_dir"
    fu = FileUtils(str(wrong_path))

    with pytest.raises(FilePathDoesNotExistsException):
        fu.validate_filepath()
