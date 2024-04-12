import uvicorn
from starlette import status

from topic_lake_api.api.utils.app_utils import init_app
from topic_lake_api.config import load_config

app = init_app()


@app.get('/', status_code=status.HTTP_204_NO_CONTENT)
async def root():
    pass


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, log_config=load_config('log_config.yaml'))
