from collections.abc import AsyncIterator

import asyncio
from aiokafka import AIOKafkaConsumer

from kmx.models import MessageEnvelope

from kmx.services.logger import Logger
from kmx.services.logger.dummy import DummyLogger


class KafkaMessageConsumer:
    """ """

    def __init__(self, kafka_url: str, group_id: str, logger: Logger = None):
        """ """
        self._kafka_url = kafka_url
        self._group_id = group_id
        self._consumer: AIOKafkaConsumer = None  # noqa
        self._logger = logger or DummyLogger()

    async def start(self, topics: list[str]):
        """ """
        if self._consumer is not None:
            self._logger.info('Stopping current consumer')
            await self._consumer.stop()

        self._consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=self._kafka_url,
            group_id=self._group_id,
            auto_offset_reset='earliest'
        )
        self._logger.info(f'Kafka consumer created for bootstrap_servers `{self._kafka_url}` and topics `{", ".join(topics)}`')
        await self._consumer.start()

    async def stop(self):
        if self._consumer is not None:
            await self._consumer.stop()
            self._consumer = None

    async def consume_messages(self) -> AsyncIterator[MessageEnvelope]:
        """ """
        self._logger.info('Start consuming messages')
        async for message in self._consumer:
            self._logger.debug(f'Consumed message `{message.value}`')
            try:
                message_envelope = MessageEnvelope.parse_raw(message.value)
            except:
                self._logger.exception(f'Cannot parse message envelope from `{message.value}`')
            else:
                await self._consumer.commit()
                yield message_envelope
