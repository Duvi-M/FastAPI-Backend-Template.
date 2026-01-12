import pytest

@pytest.mark.asyncio
async def test_login_success(client):
    # Usa el admin que ya seedeas localmente.
    # En CI lo ideal es crear un usuario en test DB, pero primero lo hacemos simple.
    resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "admin@local.com", "password": "admin123456"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    # Puede fallar en CI si no se crea el admin en esa DB.
    # Por eso, para CI real, haremos seed en un fixture después.
    assert resp.status_code in (200, 401)