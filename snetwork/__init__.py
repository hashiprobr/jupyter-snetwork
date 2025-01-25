# Copyright (c) 2024 Marcelo Hashimoto
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0


from jchannel.server import Server
from snetwork.renderer import Renderer


async def start(host='localhost', port=8889, url: str | None = None, heartbeat=30, timeout=3) -> Renderer:
    server = Server(host, port, url, heartbeat)
    renderer = Renderer(server, timeout)
    await renderer._start()
    return renderer
