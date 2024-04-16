import s13
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

client = TestClient(app=s13.app)


def test_item_post():
    model_in = s13.DataIn(name="test", qty=12, address="test_address")
    response = client.post(
        "/add-item", headers={"Active": "true"}, json=jsonable_encoder(model_in)
    )
    assert response.status_code == 201
    assert len(response.json()) == 2


def test_item_post_inactive():
    model_in = s13.DataIn(name="test", qty=12, address="test_address")
    response = client.post(
        "/add-item", headers={"Active": "no"}, json=jsonable_encoder(model_in)
    )
    assert response.status_code == 406
    assert len(response.json()) == 1


def test_item_post_long_name():
    dict_in = dict(name="t" * 11, qty=12, address="test_address")
    response = client.post(
        "/add-item", headers={"Active": "yes"}, json=jsonable_encoder(dict_in)
    )
    assert response.status_code == 422
    assert len(response.json()) == 1


def test_item_get():
    response = client.get("/get-item/3")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_item_get_not_found():
    response = client.get("/get-item/8")
    assert response.status_code == 404
    assert len(response.json()) == 1


def test_item_get_out_of_index():
    response = client.get("/get-item/11")
    assert response.status_code == 422
    assert len(response.json()) == 1
