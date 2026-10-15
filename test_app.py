import pytest
from models import User
from app import create_app, db
from bs4 import BeautifulSoup


@pytest.fixture
def app():

    app = create_app()
    # Configuración en memoria
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    # Activa de modo testing.
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app  # Punto de ejecución de la prueba.
        db.drop_all()  # Borra tablas y limpia de datos basura.


@pytest.fixture
def client(app):

    return app.test_client()


@pytest.fixture
def temp_user(app):

    with app.app_context():
        user = User(user_name="james", email="ellogos@gmail.com",
                    password_hash="cualquiercosa")
        db.session.add(user)
        db.commit()

        return user


# Test Menu
def test_menu(client):

    response = client.get("/menu")
    assert response.status_code == 200

    html = BeautifulSoup(response.get_data(as_text=True), "html.parser")

    assert html.title.string == "SPOT · Menú"
    assert html.find("h1").get_text(strip=True) == "LAS ESPECIALES"
    assert html.find("img") is not None
