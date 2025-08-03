from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello FastAPI.'}


@app.get('/item/{item_id}')
async def read_item(item_id: int):
    return {'item id': item_id}


@app.get('/user/me')
async def read_current_user():
    return {'user_id': 'the current user.'}


@app.get('/user/{user_id}')
async def read_user(user_id: int):
    return {'user_id': user_id}