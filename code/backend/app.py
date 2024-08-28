from aiohttp import web
from aiohttp.web import Request, Response
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.integration.aiohttp import (
    CloudAdapter,
    ConfigurationBotFrameworkAuthentication,
)
from bots.assistant_bot import AssistantBot
from bots.utils_bot import BotUtils
from core.config import settings as CONFIG
from utils import enable_logging


def init_app() -> web.Application:
    # Create cloud adapter
    adapter = CloudAdapter(ConfigurationBotFrameworkAuthentication(CONFIG))
    adapter.on_turn_error = BotUtils.on_error

    # Create bot
    bot = AssistantBot()

    # Create app
    app = web.Application(middlewares=[aiohttp_error_middleware])

    # Listen for incoming requests on /api/messages
    async def messages(req: Request) -> Response:
        return await adapter.process(req, bot)

    # Add route to app
    app.router.add_post("/api/messages", messages)


if __name__ == "__main__":
    # Enable logging
    enable_logging()

    # Create app
    app = init_app()

    try:
        web.run_app(app, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error
