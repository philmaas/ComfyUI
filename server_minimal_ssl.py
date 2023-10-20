import asyncio
import websockets
import ssl

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"
    
    await websocket.send(greeting)
    print(f"> {greeting}")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('/etc/letsencrypt/live/showrunner-alpha.com/fullchain.pem', 
                           '/etc/letsencrypt/live/showrunner-alpha.com/privkey.pem')

start_server = websockets.serve(hello, "0.0.0.0", 7860, ssl=ssl_context)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
