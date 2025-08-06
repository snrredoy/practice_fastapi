from fastapi import FastAPI, Query
from pydantic import BaseModel, AfterValidator
from typing import Annotated
import random


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