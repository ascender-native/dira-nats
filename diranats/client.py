import json
# from app.settings import NATS_SERVER
from diracore.main import config
from .logging import MicroserviceLogger

from nats.aio.client import Client as NATSClient
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers


class NATSMessagingClient:

    # -------------------------------------------------------------------------
    # CLASS CONSTRUCTOR
    # -------------------------------------------------------------------------
    def __init__(self, logger: MicroserviceLogger):
        """
        Create instances of NATSMessagingClient

        **WARNING** this class is not Thread Safe. If multiple threads are used,
        each thread needs to have its own instance of this class.

        :param logger: Injected through dependency inversion. Implementation of
                       the logger to be used by this class.
        """
        self._nats_client = NATSClient()
        self._connected = self._connect()
        self._logger = logger
        self._response = None

    # -------------------------------------------------------------------------
    # PROPERTY CONNECTED
    # -------------------------------------------------------------------------
    @property
    def connected(self) -> bool:
        """
        If there is an active connection with NATS server this will return True
        :return:
        """
        return self._connected

    # -----------------------------------------------------------------------------
    # BROADCAST WITH LOOP
    # -----------------------------------------------------------------------------
    async def __broadcast_with_loop(self, message: dict, subject: str):
        """

        :param message:
        :param subject:
        :return:
        """
        try:
            self._connected = await self._connect()
            await self._nats_client.publish(
                subject,
                json.dumps(message).encode()
            )
            await self._nats_client.close()
            self._connected = False
        except ErrTimeout as et:
            self._logger.error(message=str(et))
        except ErrConnectionClosed as ecc:
            self._logger.error(message=str(ecc))
        except Exception as ex:
            self._logger.error(message=str(ex))

    # -----------------------------------------------------------------------------
    # REQUEST
    # -----------------------------------------------------------------------------
    async def submit_message_with_response(self, message: dict,
                                           subject: str) -> dict | None:
        """
        Submits a message that requires a response from the subscriber.

        :param message: JSON serializable dictionary.
        :param subject: Subject in which the message will be published.
        :return: Response dictionary or None
        """
        try:
            self._connected = await self._connect()
            response = await self._nats_client.publish(
                subject,
                json.dumps(message).encode()
            )
            await self._nats_client.close()
            self._connected = False
            return json.loads(response.data.decode())
        except ErrTimeout as et:
            self._logger.error(message=str(et))
        except ErrConnectionClosed as ecc:
            self._logger.error(message=str(ecc))
        except Exception as ex:
            self._logger.error(message=str(ex))
        finally:
            return None

    # -----------------------------------------------------------------------------
    # BROADCAST MESSAGE
    # -----------------------------------------------------------------------------
    async def broadcast_message(self, message: dict, subject: str):
        """

        :param message:
        :param subject:
        :return:
        """
        await self.__broadcast_with_loop(
            message=message,
            subject=subject
        )

    # -------------------------------------------------------------------------
    # METHOD CONNECT
    # -------------------------------------------------------------------------
    async def _connect(self):
        """

        :return:
        """
        try:
            await self._nats_client.connect(
                servers=[config('nats.url')]
            )
            return True
        except ErrNoServers as ens:
            self._logger.error(message=str(ens))
        except Exception as e:
            self._logger.error(message=str(e))
        finally:
            return False

