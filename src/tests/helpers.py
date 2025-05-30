import random
import string
from uuid import uuid4

DINUM_SIREN = "130025265"


def random_group():
    """Generate random group data."""
    return {
        "name": f"Test Group {''.join(random.choices(string.ascii_lowercase, k=5))}",
        "organisation_siren": DINUM_SIREN,
        "admin_email": f"admin_{random.randint(1000, 9999)}@example.com",
        "scopes": "read maintain",
        "contract": "datapass_test",
    }


def random_user():
    """Generate a random user for testing."""
    return {"email": f"test_{uuid4()}@example.com", "sub_pro_connect": f"sub_{uuid4()}"}


def random_name():
    """Generate a random name."""
    return f"Test Name {''.join(random.choices(string.ascii_lowercase, k=5))}"


def create_group(client):
    """Create a group for testing."""
    new_group_data = random_group()
    response = client.post("/groups/", json=new_group_data)
    assert response.status_code == 201
    group = response.json()
    assert group["name"] == new_group_data["name"]
    new_group_data["id"] = group["id"]
    return new_group_data
