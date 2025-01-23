# Copyright (c) 2025 Marcelo Hashimoto
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0


import os
import asyncio

from importlib import metadata
from jchannel.channel import Channel
from jchannel.server import Server


class Renderer:
    _server: Server
    _channel: Channel
    _timeout: int

    def __init__(self, server: Server, timeout=3):
        try:
            url = os.environ['SNETWORK_CLIENT_URL']
        except KeyError:
            version = metadata.version('jupyter-snetwork')

            url = f'https://unpkg.com/jupyter-snetwork-client@{version}/dist/main.js'

        code = f'''
            (channel) => {{
                function loaded(name, url) {{
                    return new Promise((resolve, reject) => {{
                        const script = document.createElement('script');

                        script.addEventListener('load', () => {{
                            resolve();
                        }});

                        script.addEventListener('error', (event) => {{
                            console.error(event);

                            reject(`Could not load ${{name}}`);
                        }});

                        script.src = url;

                        document.head.appendChild(script);
                    }});
                }}

                if (!self.pixijsLoaded) {{
                    self.pixijsLoaded = loaded('PixiJS', 'https://pixijs.download/v8.7.0/pixi.min.js');
                }}

                if (!self.snetworkLoaded) {{
                    self.snetworkLoaded = self.pixijsLoaded.then(() => loaded('snetwork-client', '{url}'));
                }}

                return self.snetworkLoaded;
            }}
        '''

        self._server = server
        self._channel = Channel(server, code)
        self._timeout = timeout

    def start(self) -> asyncio.Task:
        return asyncio.create_task(self._start())

    def stop(self) -> asyncio.Task:
        return asyncio.create_task(self._stop())

    async def _start(self) -> None:
        await self._server.start()
        await self._channel.open(self._timeout)

    async def _stop(self) -> None:
        await self._channel.close()
        await self._server.stop()
