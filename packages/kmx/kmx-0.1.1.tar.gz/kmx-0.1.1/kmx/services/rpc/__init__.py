from typing import Protocol, Any, Optional


class RpcCaller(Protocol):
    """ """
    async def rpc_call(self, rpc_to: str, rpc_name: str, rpc_timeout: Optional[int] = None,
                       rpc_response_model: Optional[Any] = None, **params) -> Optional[Any]:
        """ """


class RpcWorker(Protocol):
    """ ДОделать """
