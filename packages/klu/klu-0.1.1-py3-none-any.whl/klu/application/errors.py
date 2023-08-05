class ApplicationNotFoundError(Exception):
    application_id: str = None

    def __init__(self, application_id):
        self.application_id = application_id
        self.message = f"Application with id {application_id} was not found."
        super().__init__(self.message)
