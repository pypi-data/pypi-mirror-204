from aiokafka import AIOKafkaProducer

from kmx.models import MessageEnvelope
from kmx.services.logger import Logger
from kmx.services.logger.dummy import DummyLogger


class KafkaMessageProducer:
    """ """
    def __init__(self, kafka_url: str, logger: Logger = None):
        self._kafka_url = kafka_url
        self._producer: AIOKafkaProducer = None  # noqa
        self._logger = logger or DummyLogger()

    async def start(self):
        if self._producer is not None:
            self._logger.info('Stopping current producer')
            await self._producer.stop()

        self._producer = AIOKafkaProducer(bootstrap_servers=self._kafka_url)
        self._logger.info(f'Kafka producer created for bootstrap_server `{self._kafka_url}`')
        await self._producer.start()

    async def stop(self):
        if self._producer is not None:
            await self._producer.stop()
            self._producer = None

    async def send_message(self, message: MessageEnvelope):
        """ """
        self._logger.debug(f'producing message: {message}')
        await self._producer.send_and_wait(topic=message.receiver, value=message.json(ensure_ascii=False).encode())
