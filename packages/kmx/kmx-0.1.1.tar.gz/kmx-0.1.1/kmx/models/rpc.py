from typing import Optional
from pydantic import BaseModel, root_validator


class RpcQuery(BaseModel):
    """ """
    rpc_call_uid: str
    rpc_to: str
    rpc_name: str
    data: dict
    timeout: int = 5


class RpcResult(BaseModel):
    """ """

    rpc_call_uid: str
    data: Optional[dict] = None
    error: Optional[str] = None

    @root_validator
    def check_data_and_error(cls, values):
        """ """
        if values['data'] is not None and values['error'] is not None:
            raise ValueError('Both `data` and `error` cannot be not None')
        return values
