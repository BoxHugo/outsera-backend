class FileProcessingException(Exception):
    """ Erro ao processar arquivo """

    pass


class MultipleFilesException(Exception):
    """ Quando existe mais de um arquivo na pasta de input """

    pass


class NoFilesFoundException(Exception):
    """ Quando não foi encontrado arquivos na pasta de input """

    pass


class FilePathDoesNotExistsException(Exception):
    """ Quando o diretório dos inputs não foi encontrado """

    pass


class FormatFileIsNotValidException(Exception):
    """ Formato do arquivo não é válido """

    pass


class NoHeaderException(Exception):
    """ Arquivo sem cabeçalho """

    pass


class ColumnNotFoundException(Exception):
    """ Coluna obrigatória não encontrada """

    pass

class FileEmptyException(Exception):
    """ Arquivo vazio """

    pass
