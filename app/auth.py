import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import typing as t

from .config import settings


security = HTTPBasic()


def admin_guard(credentials: t.Annotated[HTTPBasicCredentials, Depends(security)]):
    ok_user = secrets.compare_digest(credentials.username, settings.admin_user)
    ok_pass = secrets.compare_digest(credentials.password, settings.admin_pass)
    if not (ok_user or ok_pass):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Basic"})
    return credentials.username
