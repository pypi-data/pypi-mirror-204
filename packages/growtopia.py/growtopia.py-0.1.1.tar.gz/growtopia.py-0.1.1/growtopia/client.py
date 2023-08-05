__all__ = ("Client",)

import asyncio

import enet

from .context import Context
from .enums import EventID
from .event_pool import EventPool
from .protocol import Packet
from .utils import identify_packet


class Client(EventPool, enet.Host):
    def __init__(self, address: tuple[str, int] = None, **kwargs) -> None:
        EventPool.__init__(self)
        enet.Host.__init__(
            self,
            None,
            kwargs.get("max_peers", 1),
            kwargs.get("channels", 2),
            kwargs.get("in_bandwidth", 0),
            kwargs.get("out_bandwidth", 0),
        )

        self.compress_with_range_coder()
        self.checksum = enet.ENET_CRC32

        self.__address: tuple[str, int] = address
        self.__running: bool = False
        self.__peer: enet.Peer = None

    def start(self) -> None:
        self.__running = True
        self._event_loop.run_until_complete(self.run())

    async def stop(self) -> None:
        self.__running = False

    def send(self, packet: Packet = None, data: bytes = None) -> None:
        if data is not None:
            packet = Packet.from_bytes(data)

        if self.__peer is not None:
            self.__peer.send(0, packet.enet_packet)

    async def run(self) -> None:
        if self.__peer is None:
            self.__peer = self.connect(enet.Address(*self.__address), 2, 0)

        ctx = Context()
        ctx.client = self

        await self._dispatch(EventID.CLIENT_READY, ctx)

        while self.__running:
            event = self.service(0, True)

            if event is None:
                await asyncio.sleep(0)
                continue

            ctx = Context()
            ctx.event = event
            ctx.client = self

            if event.type == enet.EVENT_TYPE_CONNECT:
                ctx.peer = event.peer
                await self._dispatch(EventID.CONNECT, ctx)

            elif event.type == enet.EVENT_TYPE_RECEIVE:
                ctx.packet = Packet.from_bytes(event.packet.data)
                ctx.enet_packet = event.packet

                await self._dispatch(identify_packet(ctx.packet), ctx)
                await self._dispatch(EventID.RECEIVE, ctx)
            elif event.type == enet.EVENT_TYPE_DISCONNECT:
                await self._dispatch(EventID.DISCONNECT, ctx)

        await self._dispatch(EventID.CLIENT_CLEANUP, ctx)
