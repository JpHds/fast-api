import uvicorn
from fastapi import FastAPI
from clientes import clientes_router

app = FastAPI()

@app.get("/")
def oi_eu_sou_programador() ->str :
    return "oi"

app.include_router(clientes_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
    