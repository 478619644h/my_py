# !/usr/bin/python

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
     Body : dict = None
     SysHead : dict = None

@app.post('/rb/inq/single/acct')
def calculate(request_data: Item):
    a = request_data
    a.SysHead["tranRetInfAry"] = [{
        "retCd":"000001",
        "retMsg":"success"
    }]
    print(a)
    return a


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app=app,
                host="0.0.0.0",
                port=10009,
                workers=1)