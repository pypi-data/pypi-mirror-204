import websockets
from mcqq_tool.mcqq import Client, CLIENTS, send_msg_to_qq, remove_client
from nonebot import logger, get_bot

from .utils import plugin_config


async def ws_client(websocket: websockets.WebSocketServerProtocol):
    """WebSocket"""
    try:
        server_name = websocket.request_headers["x-self-name"].encode('utf-8').decode('unicode_escape')
    except KeyError as e:
        # 服务器名为空
        logger.error(f"[MC_QQ]丨未获取到该服务器的名称，连接断开：{e}")
        await websocket.close(1008, "[MC_QQ]丨未获取到该服务器的名称，连接断开")
        return
    else:
        for client in CLIENTS:
            # 重复连接
            if server_name == client.server_name:
                logger.error(f"[MC_QQ]丨[Server:{server_name}] 已连接至 WebSocket 服务器，无需重复连接")
                await websocket.close(1008, f"[MC_QQ]丨[Server:{server_name}] 已连接至 WebSocket 服务器，无需重复连接")
                return

        CLIENTS.append(Client(server_name=server_name, websocket=websocket))
        logger.success(f"[MC_QQ]丨[Server:{server_name}] 已连接至 WebSocket 服务器")
        try:
            async for message in websocket:
                await send_msg_to_qq(
                    bot=get_bot(),
                    message=message,
                    server_list=plugin_config.mc_qq_servers_list,
                    display_server_name=plugin_config.mc_qq_display_server_name
                )
        except websockets.WebSocketException as e:
            # 移除当前客户端
            await remove_client(server_name=server_name)
            logger.error(f"[MC_QQ]丨[Server:{server_name}] 的 WebSocket 连接已断开：{e}")
        else:
            if websocket.closed:
                await remove_client(server_name=server_name)
                logger.error(f"[MC_QQ]丨[Server:{server_name}] 的 WebSocket 连接已断开")


async def start_ws_server():
    """启动 WebSocket 服务器"""
    global ws
    ws = await websockets.serve(ws_client, plugin_config.mc_qq_ws_ip, plugin_config.mc_qq_ws_port)
    logger.success("[MC_QQ]丨WebSocket 服务器已开启")


async def stop_ws_server():
    """关闭 WebSocket 服务器"""
    global ws
    ws.close()
    logger.success("[MC_QQ]丨WebSocket 服务器已关闭")
