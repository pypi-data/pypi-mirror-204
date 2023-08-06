from typing import Optional, Any

import json
import uuid

from aioredis import Redis
from pydantic import BaseModel

from kmx.exceptions import RpcTimeout, RpcRemoteError, RpcError
from kmx.models import RpcResult


class RedisRpcCaller:
    """ """
    def __init__(self, redis: Redis, timeout: Optional[int] = None):
        self.redis = redis
        self.timeout = timeout if timeout > 0 else 5

    async def rpc_call(self, rpc_to: str, rpc_name: str, rpc_timeout: Optional[int] = None,
                       rpc_response_model: Optional[Any] = None, **params) -> Optional[Any]:
        """ """
        rpc_call_uid = str(uuid.uuid4()).replace('-', '')
        expire_key = f'kmx:rpc_expiry_key:{rpc_call_uid}'
        queue_name = f'kmx:{rpc_to}:rpc_queue'
        results_key = f'kmx:rpc_result:{rpc_call_uid}'
        timeout = rpc_timeout or self.timeout

        rpc_query = {
            'rpc_call_uid': rpc_call_uid,
            'rpc_to': rpc_to,
            'rpc_name': rpc_name,
            'data': self.prepare_rpc_params(**params)
        }

        await self.redis.setex(expire_key, timeout, 1)
        await self.redis.rpush(queue_name, json.dumps(rpc_query).encode())

        async with self.redis:
            result_message = await self.redis.blpop(results_key, timeout)

        if result_message is None:
            raise RpcTimeout(f'Timeout for {rpc_to}.{rpc_name} ({timeout} sec)')

        _, message = result_message

        try:
            result = RpcResult.parse_raw(message)
        except Exception as e:
            raise RpcError(f'Unknown rpc result: {message} (expected RpcResult value)')

        if result.error:
            raise RpcRemoteError(result.error)

        return self.parse_rpc_result(result, rpc_response_model)

    @staticmethod
    def prepare_rpc_params(**kwargs) -> dict:
        """ """
        if len(kwargs) == 1 and 'params' in kwargs:
            # поддержка устаревшего вызова, когда в параметрах передается одно значение "params"
            params = kwargs['params']
            return params.dict() if isinstance(params, BaseModel) else params

        params = {}
        for key, value in kwargs.items():
            params[key] = value.dict() if isinstance(value, BaseModel) else value

        return params

    @staticmethod
    def parse_rpc_result(rpc_worker_result: RpcResult, rpc_response_model: Any):
        """ """
        if rpc_response_model is not None and issubclass(rpc_response_model, BaseModel):
            return rpc_response_model.parse_obj(rpc_worker_result.data)

        if '__rpc_raw_result__' in rpc_worker_result.data:
            return rpc_worker_result.data['__rpc_raw_result__']

        return rpc_worker_result.data
