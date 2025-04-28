"""Main API"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints.routers import routers
from config import config
from app.controllers.load_file_controller import LoadFileController


app = FastAPI(
    title="Projeto Golden Raspeberry Api",
    version="0.0.1",
    description="""
        ## Api - Desafio técnico Golden Raspberry Awards.

        Este projeto tem como objetivo resolver o desafio técnico Golden Raspberry Awards. que possibilita a leitura da lista de indicados e vencedores da categoria Pior Filme do Golden Raspberry Awards.
            
        *Desenvolvido por Francisco Hugo S. Rosa.*
        """
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(routers, prefix=config.api_version)

@app.on_event("startup")
async def startup_event():

    from app.infra.db.session import create_all_tables

    create_all_tables()

    LoadFileController.run()

if __name__ == "__main__":

    uvicorn.run(app, host=config.host_api, port=int(config.port_api))
