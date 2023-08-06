from httpx import codes


class BaseDetailedException(Exception):

    def __init__(self, detail: str, status_code: int):
        self.detail = detail
        self.status_code = status_code

    def __repr__(self) -> str:
        return f'{self.status_code}: {self.detail}'


class ClientError(BaseDetailedException):

    def __init__(self, detail: str = 'invalid request', status_code: int = codes.BAD_REQUEST):
        super().__init__(detail, status_code)
