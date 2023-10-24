from aiohttp import web
import json
import aiohttp
import ssl
import asyncio

class Server:
    def __init__(self):
        self.app = web.Application()
        self.app.add_routes([web.get('/ws', self.websocket_handler)])
        self.sockets = set()

    async def index(self, request):
        """ Serve the main HTML page """
        content = """
        <html>
            <head>
                <title>WebSocket Test Page</title>
            </head>
            <body>
                <h1>Unity Rendering Service</h1>
                <script>
                    const ws = new WebSocket('wss://showrunner-alpha.com/ws');
                    ws.onmessage = event => {
                        console.log(event.data);
                    }
                    ws.onopen = () => {
                        ws.send(JSON.stringify({
                            action: "send_message",
                            data: {
                                payload: "Hello from the client!"
                            }
                        }));
                    }
                </script>
            </body>
        </html>
        """
        return web.Response(content_type='text/html', text=content)

    async def send(self, event, data, ws=None):
        message = {"type": event, "data": data}
        if ws:
            await ws.send_json(message)
        else:
            for websocket in self.sockets:
                await websocket.send_json(message)

    async def run_script(self, script_path, episode_id):
        if ws:
            print(f"Episode ID: {episode_id}")
        print(f"Episode ID: {episode_id}")
        # Ensure the bash script is executable
        # subprocess_run = await asyncio.create_subprocess_exec("chmod", "755", script_path)
        await subprocess_run.wait()

        # Print the episode_id
        print(f"Episode ID: {episode_id}")
        # Execute bash script asynchronously
        command_line = f"{script_path} {episode_id}"
        process = await asyncio.create_subprocess_shell(
            command_line, 
            stdout=asyncio.subprocess.PIPE, 
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()


    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        self.sockets.add(ws)
        
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                print(f"Received message: {msg.data}")
                
                msg_data = json.loads(msg.data)

                action = msg_data.get("action")
                if action == "call_function":
                    function_name = msg_data.get("function_name")
                    args = msg_data.get("args", {})

                    if function_name == "run_script":
                        print(args.get("episode_id"))
                        command_line = f"{args.get('script_path')} {args.get('episode_id')}"
                        process = await asyncio.create_subprocess_shell(
                            command_line, 
                            stdout=asyncio.subprocess.PIPE, 
                            stderr=asyncio.subprocess.PIPE
                        )
                        stdout, stderr = await process.communicate()


                else:
                    message_str = msg_data.get("data", {}).get("payload", "")
                    await self.send("event", message_str)
                
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print(f'ws connection closed with exception {ws.exception()}')
        
        self.sockets.remove(ws)
        return ws

    def __init__(self):
        self.app = web.Application()
        self.app.add_routes([
            web.get('/', self.index),
            web.get('/ws', self.websocket_handler)
        ])
        self.sockets = set()




# SSL Context Setup
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('/etc/letsencrypt/live/showrunner-alpha.com/fullchain.pem', 
                           '/etc/letsencrypt/live/showrunner-alpha.com/privkey.pem')
# Note: Ensure the paths to the cert and key files are correct and are generated before starting the server.
# Initialize and run the server
server = Server()
web.run_app(server.app, port=7860, ssl_context=ssl_context)