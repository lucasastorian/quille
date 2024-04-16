import os
import certifi
import logging
import datetime
import aiohttp_cors
from aiohttp import web
from dotenv import load_dotenv
from aiohttp_sse import sse_response

from utils.utils import now
from assistant.assistant import Assistant

os.environ['SSL_CERT_FILE'] = certifi.where()
app = web.Application()


def route(method, path):
    def decorator(handler):
        app.router.add_route(method, path, handler)
        return handler

    return decorator


def setup_cors(app: web.Application):
    # Create a default CORS config
    cors = aiohttp_cors.setup(app, defaults={
        "http://localhost:4200": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*",
        )
    })

    # Apply the CORS config to every route in the app
    for route in list(app.router.routes()):
        cors.add(route)


@route('POST', '/stream')
async def stream(request):
    """Prompts the earnings call analyst"""
    body = await request.json()

    chain = Assistant(messages=body['messages'], document=body['document'])

    logging.info(f"{datetime.datetime.utcnow().isoformat()}: Prompting Assistant")

    async with sse_response(request) as sse_queue:
        await chain.call(sse_queue=sse_queue)
        print(f"{datetime.datetime.utcnow().isoformat()} - Completion of Assistant Stream")
        await sse_queue.send("0\n\n")


if __name__ == '__main__':
    load_dotenv(dotenv_path=".env")
    setup_cors(app)
    web.run_app(app, port=8080)
