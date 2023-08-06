import aiomcrcon
import websockets
from mcqq_tool.mcrcon import RconCLIENTS, RconClient, remove_rcon_client, rcon_connect, rcon_send_msg_to_qq
from nonebot import logger, get_bot

from .utils import plugin_config


async def ws_client(websocket):
    """WebSocket"""
    try:
        server_name = websocket.request_headers["x-self-name"].encode('utf-8').decode('unicode_escape')
    except KeyError:
        logger.error("[MC_QQ_Rcon]丨未获取到该服务器的名称")
        await websocket.close(1008, "[MC_QQ_Rcon]丨未获取到该服务器的名称")
    else:
        for client in RconCLIENTS:
            if server_name == client.server_name:
                logger.error(f"[MC_QQ_Rcon]丨[Server:{server_name}] 已连接至WebSocket服务器，无需重复连接。")
                await websocket.close(1008, f"[MC_QQ_Rcon]丨[Server:{server_name}] 已连接至WebSocket服务器，无需重复连接。")
        try:
            mcrcon_connect = aiomcrcon.Client(
                websocket.remote_address[0],
                plugin_config.mc_qq_rcon_rcon_dict[server_name],
                plugin_config.mc_qq_rcon_password
            )
            await rcon_connect(client=mcrcon_connect, server_name=server_name)
        except KeyError:
            logger.error(f"[MC_QQ_Rcon]丨[Server:{server_name}] 的 Rcon 端口未获取")
        else:
            RconCLIENTS.append(
                RconClient(server_name=server_name, websocket=websocket, rcon=mcrcon_connect)
            )
            logger.success(f"[MC_QQ_Rcon]丨[Server:{server_name}] 已连接至 WebSocket 服务器")

        try:
            async for message in websocket:
                await rcon_send_msg_to_qq(
                    bot=get_bot(),
                    message=message,
                    server_list=plugin_config.mc_qq_rcon_servers_list,
                    display_server_name=plugin_config.mc_qq_display_server_name
                )
        except websockets.WebSocketException as e:
            await remove_rcon_client(server_name=server_name)
            logger.error(f"[MC_QQ_Rcon]丨[Server:{server_name}] 的 WebSocket 连接已断开：{e}")
        except ConnectionRefusedError:
            logger.error(f"[MC_QQ_Rcon]丨[Server:{server_name}] 的 Rcon 未开启或连接信息错误")
            logger.error(f"[MC_QQ_Rcon]丨[Server:{server_name}] 的 WebSocket 连接已断开")
        else:
            if websocket.closed:
                await remove_rcon_client(server_name=server_name)


async def start_ws_server():
    """启动 WebSocket 服务器"""
    global ws
    ws = await websockets.serve(ws_client, plugin_config.mc_qq_ws_ip, plugin_config.mc_qq_rcon_ws_port)
    logger.success("[MC_QQ_Rcon]丨WebSocket 服务器已开启")


async def stop_ws_server():
    """关闭 WebSocket 服务器"""
    global ws
    ws.close()
    logger.success("[MC_QQ_Rcon]丨WebSocket 服务器已关闭")
