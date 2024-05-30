"""
The main script that initiates and runs the FastAPI application.
This module sets up the application configuration including database
 connection, static files routing and API routes.
"""

from functools import partial

import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api.api_v1.api import api_router
from app.config.init_settings import init_setting
from app.config.settings import setting
from app.core.lifecycle import lifespan
from app.core.utils import custom_generate_unique_id, custom_openapi

app: FastAPI = FastAPI(
    debug=True,
    openapi_url=f"{setting.API_V1_STR}{init_setting.OPENAPI_FILE_PATH}",
    openapi_tags=init_setting.TAGS_METADATA,
    lifespan=lifespan,
    generate_unique_id_function=custom_generate_unique_id,
)
app.openapi = partial(custom_openapi, app)  # type: ignore
app.mount(
    init_setting.IMAGES_PATH,
    StaticFiles(directory=init_setting.IMAGES_DIRECTORY),
    name=init_setting.IMAGES_APP,
)
app.include_router(api_router, prefix=setting.API_V1_STR)


@app.get(
    "/",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_class=RedirectResponse,
)
async def redirect_to_docs() -> RedirectResponse:
    """
    Redirects the user to the /docs endpoint for API documentation.
    ## Response:
    - `return:` **The redirected response**
    - `rtype:` **RedirectResponse**
    """
    return RedirectResponse("/docs")


@app.get("/health", response_class=JSONResponse)
async def check_health() -> JSONResponse:
    """
    Check the health of the application backend.
    ## Response:
    - `return:` **The JSON response**
    - `rtype:` **JSONResponse**
    """
    return JSONResponse({"status": "healthy"})


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=f"{setting.SERVER_HOST}",
        port=setting.SERVER_PORT,
        reload=setting.SERVER_RELOAD,
        log_level=setting.SERVER_LOG_LEVEL,
    )
