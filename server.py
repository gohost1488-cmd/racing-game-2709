"""AHVE Racing Server — racing-game-2709."""
import json, uuid, random, time, math
from aiohttp import web

players = {}

async def index(request):
    return web.FileResponse('index.html')

async def ws_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    pid = str(uuid.uuid4())[:8]
    players[pid] = {'id': pid, 'x': 100, 'y': 300, 'speed': 0, 'lap': 0, 'color': random.choice(['red','blue','green','yellow'])}
    await ws.send_json({'type': 'init', 'player_id': pid})
    
    async for msg in ws:
        data = json.loads(msg.data)
        p = players[pid]
        if data.get('accelerate'):
            p['speed'] = min(10, p['speed'] + 0.5)
        elif data.get('brake'):
            p['speed'] = max(0, p['speed'] - 0.5)
        p['x'] = (p['x'] + p['speed']) % 800
        if p['x'] < 1:
            p['lap'] += 1
        await ws.send_json({'type': 'state', 'players': list(players.values())})
    return ws

app = web.Application()
app.router.add_get('/', index)
app.router.add_get('/ws', ws_handler)
if __name__ == '__main__':
    web.run_app(app, port=5000)
