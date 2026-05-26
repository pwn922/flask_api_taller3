class ImportCsvError(Exception):
    def __init__(self, message: str, detail: str = ""):
        self.message = message
        self.detail = detail
        super().__init__(self.message)


class EmptyFileError(ImportCsvError):
    def __init__(self):
        super().__init__(
            message="El archivo CSV está vacío",
            detail="empty_file",
        )


class InvalidColumnsError(ImportCsvError):
    def __init__(self):
        super().__init__(
            message="Las columnas del CSV no coinciden con la estructura esperada",
            detail="invalid_columns",
        )


class InvalidCsvFormatError(ImportCsvError):
    def __init__(self):
        super().__init__(
            message="El archivo no es un CSV válido",
            detail="invalid_csv_format",
        )
