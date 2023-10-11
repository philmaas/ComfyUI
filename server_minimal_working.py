from aiohttp import web
import json
import aiohttp
import ssl

class Server:
    def __init__(self):
        self.app = web.Application()
        self.app.add_routes([web.get('/ws', self.websocket_handler)])
        self.sockets = set()
    
    async def send(self, event, data, ws=None):
        message = {"type": event, "data": data}
        if ws:
            await ws.send_json(message)
        else:
            for websocket in self.sockets:
                await websocket.send_json(message)
    
    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        self.sockets.add(ws)
        
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                print(f"Received message: {msg.data}")
                
                msg_data = json.loads(msg.data)
                message_str = msg_data.get("data", {}).get("payload", "")
                
                await self.send("event", message_str)
                
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print(f'ws connection closed with exception {ws.exception()}')
            
        self.sockets.remove(ws)
        return ws


        # SSL Context Setup
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile='/etc/ssl/private/certificate.crt', keyfile='/etc/ssl/private/private.key')
        # Note: Ensure the paths to the cert and key files are correct and are generated before starting the server.
# Initialize and run the server
server = Server()
web.run_app(server.app, port=7860, ssl_context=ssl_context)