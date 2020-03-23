from aiohttp import web
import logging
from settings import config
from db import close_pg, init_pg
import json

import db

async def index(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.question.select())
        records = await cursor.fetchall()
        questions = [dict(q) for q in records]
        return web.json_response()


app = web.Application()
app['config'] = config
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
app.add_routes([web.get('/', index)])



if __name__ == '__main__':
    web.run_app(app)