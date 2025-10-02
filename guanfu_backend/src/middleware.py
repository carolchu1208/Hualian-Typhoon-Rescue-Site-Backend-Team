from typing import Callable

from jose import JWTError
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from src.auth.dependencies import get_current_user
from src.database import get_db


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """ process request """
        # get token
        token = request.headers.get("Authorization")

        # verify token
        if token:
            try:
                if token.startswith("Bearer "):
                    token = token[7:]

                db_gen = get_db()
                db = next(db_gen)

                # get current user
                user = get_current_user(token, db)

                # insert user info in request
                request.state.user = user

            except JWTError as e:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid authentication credentials."},
                )
        else:
            request.state.user = None  # anonymous users

        """ process response """
        response = await call_next(request)
        return response
