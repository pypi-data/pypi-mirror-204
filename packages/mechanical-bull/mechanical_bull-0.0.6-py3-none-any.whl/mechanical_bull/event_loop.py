import asyncio

import bovine
import json

import logging

logger = logging.getLogger(__name__)


async def handle_connection(client, handlers):
    event_source = await client.event_source()
    logger.info("Connected")
    async for event in event_source:
        if not event:
            return
        if event and event.data:
            data = json.loads(event.data)
            logger.debug(event.data)

            for handler in handlers:
                await handler(client, data)


async def loop(client_config, handlers):
    async with bovine.BovineClient(client_config) as client:
        while True:
            await handle_connection(client, handlers)
            logger.info("Disconnected from server, reconnecting in 10 seconds")
            await asyncio.sleep(10)
