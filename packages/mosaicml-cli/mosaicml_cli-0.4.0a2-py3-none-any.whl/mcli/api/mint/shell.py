"""
connection engine to MINT
"""

from __future__ import annotations

import asyncio
import logging
import shutil
import ssl
import sys
from typing import Dict, Optional, cast

from websockets.client import WebSocketClientProtocol
from websockets.client import connect as ws_connect
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK, InvalidStatusCode

from mcli.api.exceptions import MintException
from mcli.api.mint import tty
from mcli.proto.mint_pb2 import MINTMessage, TerminalSize, UserInput
from mcli.utils.utils_logging import FAIL, WARN
from mcli.utils.utils_message_decoding import MessageDecoder

logger = logging.getLogger(__name__)


class MintShell:
    """Interactive shell into MINT (Mosaic Interactive service)

    Args:
        api_key: The user's API key. If not specified, the value of the $MOSAICML_API_KEY
            environment variable will be used. If that does not exist, the value in the
            user's config file will be used. The key is authenticated in MINT through MAPI
        endpoint: The MINT URL to hit for all requests. If not specified, the value of the
            $MOSAICML_MINT_ENDPOINT environment variable will be used. If that does not
            exist, the default setting will be used.
    """
    api_key: str
    endpoint: str

    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
    ):
        self._load_from_environment(api_key, endpoint)

        self._loop = asyncio.get_event_loop_policy().get_event_loop()

    def _load_from_environment(self, api_key: Optional[str] = None, endpoint: Optional[str] = None) -> None:
        # pylint: disable-next=import-outside-toplevel
        from mcli import config
        conf = config.MCLIConfig.load_config(safe=True)
        if api_key is None:
            api_key = conf.api_key

        if not api_key:
            api_key = ''

        self.api_key = api_key

        if endpoint is None:
            endpoint = conf.mint_endpoint
        self.endpoint = endpoint

    @property
    def header(self) -> Dict[str, str]:
        return {"Authorization": self.api_key}

    async def _connect(self, uri: str):
        """
        Connection helper

        Given a uri, connects to a websocket and streams data in the terminal shell
        """
        # setup tty and save old settings. if settings aren't reset, the terminal will likely become non-responsive

        shell_tty = tty.TTY()

        async def read_stdin(ws: WebSocketClientProtocol):
            """Reads the stdin and write to the websocket
            """
            while True:
                char = sys.stdin.read()
                if char:
                    message = MINTMessage(user_input=UserInput(input=char))
                    await ws.send(message.SerializeToString())
                else:
                    # This can be very short, since its main purpose is to not block the event loop
                    await asyncio.sleep(0.01)

        async def write_stdout(ws: WebSocketClientProtocol):
            """Reads from the websocket and writes to stdout
            """
            decoder = MessageDecoder()
            async for msg in ws:
                if msg:
                    decoded = decoder.decode(cast(bytes, msg))
                    sys.stdout.write(decoded)
                    sys.stdout.flush()

        async def monitor_terminal_size(ws: WebSocketClientProtocol):
            """Monitors terminal size and sends it to the server when it changes

            This sends the width x height tuple as a byte string so MINT can parse it
            """
            size = None
            while True:
                new_size = shutil.get_terminal_size()
                if new_size != size:
                    message = MINTMessage(terminal_size=TerminalSize(width=new_size.columns, height=new_size.lines))
                    await ws.send(message.SerializeToString())
                    size = new_size
                await asyncio.sleep(0.1)

        connect_params = {
            "uri": uri,
            "extra_headers": self.header,
            # Useful for debugging. If logging is set to DEBUG level, this will log debug statements
            "logger": logger,
            # Set the close timeout to a small value. When the server closes connection, it often
            # does not respond to the client's close request. This keeps the waiting to a minimum.
            # If we start having reasons for the client to initiate the close, we may need to modify
            # this value.
            "close_timeout": 0.25,
            # Give enough time for MINT to get a connection from the agent
            "open_timeout": 30,
        }
        if uri.startswith("wss:"):
            connect_params["ssl"] = ssl.SSLContext(ssl.PROTOCOL_TLS)

        try:
            async with ws_connect(**connect_params) as ws:
                # Start the read and write tasks to run until the connection closes
                consumer_task = asyncio.create_task(write_stdout(ws))
                producer_task = asyncio.create_task(read_stdin(ws))
                monitor_task = asyncio.create_task(monitor_terminal_size(ws))
                done, pending = await asyncio.wait(
                    [consumer_task, producer_task, monitor_task],
                    return_when=asyncio.FIRST_COMPLETED,
                )
                # Retrieve the results from the completed task(s) in case they errored
                await asyncio.gather(*done)
                # Cancel any remaining tasks
                for task in pending:
                    task.cancel()

        except ConnectionClosedOK:
            pass
        except ConnectionClosedError as e:
            raise MintException("MINT Shell unexpectedly closed") from e
        except OSError as e:
            if "Errno 61" in str(e):  # https://bugs.python.org/issue29980
                e = MintException(f'Could not connect to {self.endpoint}')
            raise e
        except InvalidStatusCode as e:
            raise MintException(f"Failed to run mint websocket with status code {e.status_code}") from e
        finally:
            shell_tty.reset()

    def connect(self, run_name: str, rank: int = 0) -> int:
        """
        Connect to a run using the MINT Shell

        args:
            run_name (str): Name of run to connect to
            rank (int): Integer of node rank. By default, selects the first.
        """
        if not tty.TTY_SUPPORTED:
            logger.warning(f'{WARN} MCLI Connect does not currently support TTY for your OS')

        uri = f"{self.endpoint}/{run_name}/{rank}"

        try:
            self._loop.run_until_complete(self._connect(uri))
        except MintException as e:
            logger.error(f'{FAIL} {e}')
            return 1
        return 0
