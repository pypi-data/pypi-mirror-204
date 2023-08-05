class DataNotFoundError(Exception):
    datum_id: int = None

    def __init__(self, datum_id):
        self.datum_id = datum_id
        self.message = f"Data with id {datum_id} was not found."
        super().__init__(self.message)
