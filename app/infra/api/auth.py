from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from config import config

API_KEY = config.api_key
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def get_api_key(request_header_key: str = Security(api_key_header)) -> str:

    """ 
    Verify api key from header request.

    :param request_header_key: header request
    :return request_header_key: api key
    """
    
    if request_header_key == API_KEY:
        return request_header_key
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API Key.")
