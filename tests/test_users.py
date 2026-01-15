from fastapi.testclient import TestClient
from app.main import app
from app import schema

client = TestClient(app)
# biz bu pytest bilan hohlagan codelarni test qila olamiz, assert orqali tekshiramiz
def test_root():
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'welcome to my fucking  world'

# def test_create_user():
#     res = client.post("/users/", json = {"email": "yellovvv@gmail.com", "password": "yello"})
#     print(res.json())

#     new_user = schema.UserOut(**res.json())
#     assert  new_user.email == "yellovvv@gmail.com"
#     # assert res.status_code == 201
