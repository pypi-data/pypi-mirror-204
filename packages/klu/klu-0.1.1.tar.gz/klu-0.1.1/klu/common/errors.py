class UnknownKluError(Exception):
    def __init__(self):
        self.message = "Unknown error in Klu SDK. Please contact the support team."
        super().__init__(self.message)


class UnknownKluAPIError(Exception):
    def __init__(self, status: int, message: str):
        self.message = (
            f"Unknown error in Klu API.\nstatus_code: {status},\nmessage: {message}"
        )
        super().__init__(self.message)


class WorkspaceNotFoundError(Exception):
    def __init__(self):
        self.message = "Workspace not found for provided API key."
        super().__init__(self.message)
