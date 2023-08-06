"""Define an object that handles the connection to the Websocket"""
import asyncio
import json
from typing import Callable
from websockets.client import connect
from websockets.exceptions import ConnectionClosed, InvalidStatusCode, ConnectionClosedError
from .exceptions import (
    InvalidApiToken, WebsocketException, NoCardsFound, RequestLimitReached, AlreadyConnected
)
from .utils import (
    handle_settings,
    handle_charge_points,
    handle_status,
    handle_grid,
    handle_setting_change,
    handle_session_messages,
    get_dummy_message,
    get_exception
)

URL = "wss://motown.bluecurrent.nl/haserver"
BUTTONS = ("START_SESSION", "STOP_SESSION", "SOFT_RESET", "REBOOT")

class Websocket:
    """Class for handling requests and responses for the BlueCurrent Websocket Api."""
    _connection = None
    _has_connection = False
    auth_token = None
    receiver = None
    receive_event = None
    receiver_is_coroutine = None

    def __init__(self):
        pass

    def get_receiver_event(self):
        """Return cleared receive_event when connected."""

        self._check_connection()
        if self.receive_event is None:
            self.receive_event = asyncio.Event()

        self.receive_event.clear()
        return self.receive_event

    async def validate_api_token(self, api_token: str):
        """Validate an api token."""
        await self._connect()
        await self._send({"command": "VALIDATE_API_TOKEN", "token": api_token})
        res = await self._recv()
        await self.disconnect()

        if res['object'] == 'ERROR':
            raise get_exception(res)

        if not res.get("success"):
            raise InvalidApiToken
        self.auth_token = "Token " + res["token"]
        return True

    async def get_email(self):
        """Return the user email"""
        if not self.auth_token:
            raise WebsocketException("token not set")
        await self._connect()
        await self.send_request({"command": "GET_ACCOUNT"})
        res = await self._recv()
        await self.disconnect()

        if res['object'] == 'ERROR':
            raise get_exception(res)

        if not res.get("login"):
            raise WebsocketException('No email found')
        return res['login']

    async def get_charge_cards(self):
        """Get the charge cards."""
        if not self.auth_token:
            raise WebsocketException("token not set")
        await self._connect()
        await self.send_request({"command": "GET_CHARGE_CARDS"})
        res = await self._recv()
        await self.disconnect()
        cards = res.get("cards")

        if res['object'] == 'ERROR':
            raise get_exception(res)

        if len(cards) == 0:
            raise NoCardsFound
        return cards

    async def connect(self, api_token: str):
        """Validate api_token and connect to the websocket."""
        if self._has_connection:
            raise WebsocketException("Connection already started.")
        await self.validate_api_token(api_token)
        await self._connect()

    async def _connect(self):
        """Connect to the websocket."""
        try:
            self._connection = await connect(URL)
            self._has_connection = True
        except Exception as err:
            self.check_for_server_reject(err)
            raise WebsocketException(
                "Cannot connect to the websocket.") from err

    async def send_request(self, request: dict):
        """Add authorization and send request."""
        if not self.auth_token:
            raise WebsocketException("Token not set")

        request["Authorization"] = self.auth_token
        await self._send(request)

    async def loop(self, receiver: Callable):
        """Loop the message_handler."""

        self.receiver = receiver
        self.receiver_is_coroutine = asyncio.iscoroutinefunction(receiver)

        # Needed for receiving updates
        await self._send({"command": "HELLO", "Authorization": self.auth_token})

        while True:
            stop = await self._message_handler()
            if stop:
                break

    async def _message_handler(self):
        """Wait for a message and give it to the receiver."""

        message: dict = await self._recv()

        # websocket has disconnected
        if not message:
            return True

        object_name = message.get("object")

        if not object_name:
            raise WebsocketException("Received message has no object.")

        # handle ERROR object
        if object_name == "ERROR":
            raise get_exception(message)

        # if object other than ERROR has an error key it will be send to the receiver.
        error = message.get("error")

        # ignored objects
        if (("RECEIVED" in object_name and not error)
                or object_name == "HELLO" or "OPERATIVE" in object_name):
            return False
        if object_name == "CHARGE_POINTS":
            handle_charge_points(message)
        elif object_name == "CH_STATUS":
            handle_status(message)
        elif object_name == "CH_SETTINGS":
            handle_settings(message)
        elif "GRID" in object_name:
            handle_grid(message)
        elif object_name in ('STATUS_SET_PUBLIC_CHARGING', 'STATUS_SET_PLUG_AND_CHARGE'):
            handle_setting_change(message)
        elif any(button in object_name for button in BUTTONS):
            handle_session_messages(message)
        else:
            return False

        self.handle_receive_event()

        await self.send_to_receiver(message)

        # Fix for api sending old start_datetime
        if object_name == 'STATUS_START_SESSION' and not error:
            await self.send_to_receiver(get_dummy_message(message['evse_id']))

    async def send_to_receiver(self, message):
        """Send data to the given receiver."""
        if self.receiver_is_coroutine:
            await self.receiver(message)
        else:
            self.receiver(message)

    async def _send(self, data: dict):
        """Send data to the websocket."""
        self._check_connection()
        try:
            data_str = json.dumps(data)
            await self._connection.send(data_str)
        except (ConnectionClosed, InvalidStatusCode) as err:
            self.handle_connection_errors(err)

    async def _recv(self):
        """Receive data from de websocket."""
        self._check_connection()
        try:
            data = await self._connection.recv()
            return json.loads(data)
        except (ConnectionClosed, InvalidStatusCode) as err:
            self.handle_connection_errors(err)

    def handle_connection_errors(self, err):
        """Handle connection errors."""
        if self._has_connection:
            self._has_connection = False
            self.handle_receive_event()
            self.check_for_server_reject(err)
            raise WebsocketException("Connection was closed.")

    async def disconnect(self):
        """Disconnect from de websocket."""
        self._check_connection()
        if not self._has_connection:
            raise WebsocketException("Connection is already closed.")
        self._has_connection = False
        self.handle_receive_event()
        await self._connection.close()

    def _check_connection(self):
        """Throw error if there is no connection."""
        if not self._connection:
            raise WebsocketException("No connection with the api.")

    def handle_receive_event(self):
        "Set receive_event if it exists"
        if self.receive_event is not None:
            self.receive_event.set()

    def check_for_server_reject(self, err):
        """Check if the client was rejected by the server"""
        if isinstance(err, InvalidStatusCode) and err.headers.get('x-websocket-reject-reason'):
            if 'Request limit reached' in err.headers.get('x-websocket-reject-reason'):
                raise RequestLimitReached("Request limit reached") from err
            if 'Already connected' in err.headers.get('x-websocket-reject-reason'):
                raise AlreadyConnected("Already connected")
        if isinstance(err, ConnectionClosedError) and err.code == 4001:
            raise RequestLimitReached("Request limit reached") from err
