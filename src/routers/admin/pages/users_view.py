from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from templates.template_manager import Breadcrumb, template_manager

from ....dependencies import get_admin_read_service
from ....services.admin.read_service import AdminReadService

router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def users_explorer(
    request: Request, admin_service: AdminReadService = Depends(get_admin_read_service)
):
    """
    Allow admin to explore all groups
    """
    users = await admin_service.get_users()
    return template_manager.render(
        request,
        "utilisateurs.html",
        "Liste des utilisateurs",
        enforce_authentication=True,
        context={"users": users},
    )


@router.get("/{user_id}", response_class=HTMLResponse)
async def user_explorer(
    request: Request, user_id: int, admin_service=Depends(get_admin_read_service)
):
    """
    Allow admin to explore the detail of one specific group
    """
    group = await admin_service.get_user_details(user_id)

    return template_manager.render(
        request,
        "utilisateur.html",
        f"Utilisateur {user_id}",
        enforce_authentication=True,
        context=group,
        breadcrumbs=[Breadcrumb(path="/admin/users", label="Liste des utilisateurs")],
    )
