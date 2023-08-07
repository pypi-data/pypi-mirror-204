from typing import Union

from fastapi import APIRouter, Header

from lnhub_rest.core.collaborator._crud import sb_select_collaborator
from .utils import (
    extract_access_token,
    get_supabase_client,
)

router = APIRouter(prefix="/instance/collaborator")


@router.get("/{account_handle}/{name}")
def is_collaborator(
    instance_id: str,
    account_id: str,
    authentication: Union[str, None] = Header(default=None),
):
    access_token = extract_access_token(authentication)
    supabase_client = get_supabase_client(access_token)

    try:
        collaborator = sb_select_collaborator(instance_id, account_id, supabase_client)
        if collaborator is None:
            return False
        else:
            return True
    finally:
        supabase_client.auth.sign_out()
