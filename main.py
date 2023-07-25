from fastapi import FastAPI

from routers.instagram import router as inst_router


def init_routes(app_: FastAPI) -> None:
    app_.include_router(inst_router)


def create_app() -> FastAPI:
    app_ = FastAPI()
    init_routes(app_)
    return app_


app = create_app()


@app.on_event('shutdown')
async def shutdown() -> None:
    print('Shutdown')
