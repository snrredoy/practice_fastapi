from fastapi import FastAPI, Query, Path, Body, Cookie, Response, Header
from pydantic import BaseModel, AfterValidator, Field, HttpUrl, EmailStr
from typing import Annotated, Literal, Any
import random
from datetime import datetime, timedelta, time
from uuid import UUID
from fastapi.responses import JSONResponse, RedirectResponse

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


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get('/items/')
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@app.get('/items/{item_id}')
async def read_items(item_id: int , q: str | None = None):
    if q:
        return {'item_id': item_id, 'q': q}
    return {'item_id': item_id}


@app.get('/optional/{item_id}')
async def read_items(item_id: int , q: str | None = None, short: bool = False):
    item = {'item_id': item_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update({'description': 'This is an amezing item that has a long description.'})
    return item


@app.get('/item/{item_id}/user/{user_id}')
async def read_items(item_id: int , user_id: int, q: str | None = None, short: bool = False):
    item = {'item_id': item_id, 'user_id': user_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update({'description': 'This is an amezing item that has a long description.'})
    return item


@app.get('/required/{item_id}/user/{user_id}')
async def read_items(item_id: int , user_id: int, needy: str, q: str | None = None, short: bool = False):
    item = {'item_id': item_id, 'user_id': user_id, 'needy': needy}
    if q:
        item.update({'q': q})
    if not short:
        item.update({'description': 'This is an amezing item that has a long description.'})
    return item


class Product(BaseModel):
    name : str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str | None = None
    full_name: str | None = None

@app.post('/product/')
async def create_product(item: Product):
    item_dict = item.dict()
    if item.tax is not None: 
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    return item_dict


@app.put('/product/{product_id}')
async def update_product(product_id: int, product: Product, q: str | None = None):
    return {
        'product_id': product_id,
        **product.dict(),
        'q': q
    }


# path , query and body using one request and body is optional
@app.put('/update/{product_id}')
async def update_product(product_id: Annotated[int, Path(ge=0, le=100)], q: str | None = None, product: Product | None = None):
    results = {
        'product_id': product_id
    }
    if q:
        results.update({'q': q})
    if product:
        results.update({'product': product})
    return results


# path , query and multiple body using one request
@app.post('/add/{product_id}')
async def update_product(product_id: Annotated[int, Path(ge=0, le=100)], user: User, q: str | None = None, product: Product | None = None):
    results = {
        'product_id': product_id
    }
    if q:
        results.update({'q': q})
    if product:
        results.update({'product': product})
    if user:
        results.update({'user': user})
    return results


# singular body item and multiple body using one request
@app.post('/singular/{product_id}')
async def update_product(product_id: Annotated[int, Path(ge=0, le=100)], user: User,  importance: Annotated[int, Body()], q: str | None = None, product: Product | None = None):
    results = {
        'product_id': product_id
    }
    if q:
        results.update({'q': q})
    if product:
        results.update({'product': product})
    if user:
        results.update({'user': user})
    if importance:
        results.update({'importance': importance})
    return results
# not required using annotate and query , q can be none or str
# @app.get('/cards/')
# async def read_card(q: Annotated[str | None , Query(max_length=50)] = None):
#     results = {"cards": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# default value with non required, q is default str
# @app.get('/cards/')
# async def read_card(q: Annotated[str, Query(max_length=50)] = 'Name'):
#     results = {"cards": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# required query parameter, q must be str input
# @app.get('/cards/')
# async def read_card(q: Annotated[str, Query(max_length=50)]):
#     results = {"cards": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# required query parameter but q accept str or none
# @app.get('/cards/')
# async def read_card(q: Annotated[str | None, Query(max_length=50)]):
#     results = {"cards": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# non required query parameter but q accept list or none
# @app.get('/cards/')
# async def read_card(q: Annotated[list[str] | None, Query(max_length=50)] = None):
#     results = {"cards": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# non required query parameter but q accept list or default
# @app.get('/cards/')
# async def read_card(q: Annotated[list[str], Query(max_length=50)] = ['list', 'dict']):
#     results = {"cards": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# non required query parameter but q accept list or default(You can also use list directly instead of list[str])
# @app.get('/cards/')
# async def read_card(q: Annotated[list, Query(max_length=50)] = []):
#     results = {"cards": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# non required query parameter but q accept str or None
# @app.get('/cards/')
# async def read_card(q: Annotated[str | None, Query(title='Query String', description='This is query', max_length=50)] = None):
#     results = {"cards": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# non required query parameter but item-query accept str or None with deprecated
@app.get('/cards/')
async def read_card(q: Annotated[str | None, Query(alias='item-query', deprecated=True)] = None):
    results = {"cards": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_valid_id(id: str):
    if not id.startswith(('isbn-', 'imdb-')):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


@app.get('/search/')
async def read_val(id: Annotated[str | None, AfterValidator(check_valid_id)] = None):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {'id': id, 'name': item}


# Validate path parameter
# @app.get('/roll/{role_id}')
# async def read_roll(role_id: Annotated[int , Path(title='Put the valid roll')]):
#     item = {}
#     if role_id:
#         item.update({'role': role_id})
#     return item


# Validate path parameter
@app.get('/roll/{role_id}')
async def read_roll(role_id: Annotated[int , Path(title='Put the valid roll', ge=1)]):
    item = {}
    if role_id:
        item.update({'role': role_id})
    return item


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, ge=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal['created_at', 'updated_at'] = 'created_at'
    tags: list[str] = []


@app.get('/filter/', tags=['Filter with all model fields'])
async def read_filter(filter: Annotated[FilterParams, Query()]):
    return filter


class Images(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tags: list[str]
    images: list[Images] | None = None

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item] | None = None


@app.put('/update_item/{item_id}')
async def update_item(item_id: int, item: Item):
    results = {
        'item_id': item_id,
        'item': item
    }
    return results


@app.post('/offers/')
async def create_offer(offer: Offer):
    results = {
        'offer': offer
    }
    return results


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights


class Item1(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        'json_schema_extra':{
            'examples': [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }

@app.put('/item1/{item_id}')
async def update_item1(item_id: int, item: Item1):
    results = {'item_id': item_id, 'item': item}
    return results


class Item2(BaseModel):
    name: str = Field(examples=['Foo'])
    description: str = Field(default=None, examples=['A very nice Item'])
    price: float = Field(examples=[30.6])
    tax: float = Field(default=None, examples=[12.2])


@app.put('/item2/{item_id}')
async def update_item1(item_id: int, item: Item2):
    results = {'item_id': item_id, 'item': item}
    return results



@app.put("/item3/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }

@app.get("/set-cookie")
async def set_cookie(response: Response):
    response.set_cookie(key="ads_id", value="12345")
    return {"message": "Cookie set!"}

@app.get("/items_cookie/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}

@app.get('/item_header/')
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {'User agent': user_agent}


@app.get("/items_duplicate/")
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}


@app.post('/item_return')
async def create_item(item: Item) -> Item:
    return item

@app.get('/item_return_get')
async def read_item() -> list[Item]:
    return [
        Item(name='Alu', description='I am a good alu', price= 20, tags=['alu', 'sei sobji']),
        Item(name='Potol', description='Ami holam bici ala potol', price= 40, tags=['potol', 'bici ala potol'])
    ]


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(BaseModel):
    password: str

# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: str | None = None

class UserOut(BaseUser):
    username: str
    email: EmailStr
    full_name: str | None = None



# @app.post('/create_user/')
# async def create_user(user: UserIn) -> UserIn:
#     return user


# @app.post('/create_user/', response_model=UserOut)
# async def create_user(user: UserIn) -> Any:
#     return user


@app.post('/create_user/')
async def create_user(user: UserIn) -> BaseUser:
    return user


@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})



@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")


@app.get('/portal1', response_model=None)
async def read_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})


class Item4(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get('/item4/{item_id}', response_model=Item4, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


@app.get(
    "/item4/{item_id}/name",
    response_model=Item4,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/item4/{item_id}/public", response_model=Item4, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]