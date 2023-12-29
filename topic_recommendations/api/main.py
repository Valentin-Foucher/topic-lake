import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from topic_recommendations.infra.db.core import init_db


from topic_recommendations.app.main_router import router
from topic_recommendations.config import load_config
init_db()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(router)


@app.get('/', status_code=status.HTTP_204_NO_CONTENT)
async def root():
    pass





if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, log_config=load_config('../../log_config.yaml'))
