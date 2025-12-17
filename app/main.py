from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes import router
from app.domain.errors import ValidationError, ConflictError, InfrastructureError, DomainError
from app.infra.sql_models import Base
from app.db import engine


def create_app() -> FastAPI:
    app = FastAPI(title="Orders API")

    # Crear tablas
    Base.metadata.create_all(bind=engine)

    # Rutas
    app.include_router(router)

    # --- Manejo de errores: dominio vs infraestructura ---

    @app.exception_handler(ValidationError)
    def handle_domain_validation(_: Request, exc: ValidationError):
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    @app.exception_handler(ConflictError)
    def handle_domain_conflict(_: Request, exc: ConflictError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(InfrastructureError)
    def handle_infra(_: Request, exc: InfrastructureError):
        return JSONResponse(status_code=503, content={"detail": "Infrastructure error", "hint": str(exc)})

    @app.exception_handler(DomainError)
    def handle_domain_generic(_: Request, exc: DomainError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(SQLAlchemyError)
    def handle_sqlalchemy(_: Request, exc: SQLAlchemyError):
        # por si algo se coló sin envolver
        return JSONResponse(status_code=503, content={"detail": "Database error", "hint": str(exc)})

    return app


app = create_app()
