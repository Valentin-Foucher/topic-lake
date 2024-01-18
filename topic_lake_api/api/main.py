import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from topic_lake_api.api.utils.app_utils import add_error_handlers, add_routers, lifespan
from topic_lake_api.config import load_config


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

add_routers(app)
add_error_handlers(app)


@app.get('/', status_code=status.HTTP_204_NO_CONTENT)
async def root():
    pass


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, log_config=load_config('log_config.yaml'))
