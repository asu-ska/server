from typing import Any
from msgspec import Struct
from litestar import Litestar, get, post
from litestar.controller import Controller
from litestar.handlers import HTTPRouteHandler
import uvicorn

# ==========================================
# 1. Слой данных (Схемы/DTO)
# ==========================================
# Используем ультрабыстрый msgspec.Struct вместо Pydantic
class User(Struct):
    id: int
    name: str
    email: str

class UserCreate(Struct):
    name: str
    email: str


# ==========================================
# 2. Контроллер (Слой бизнес-логики)
# ==========================================
# Группировка эндпоинтов в класс упрощает модернизацию и тестирование
class UserController(Controller):
    path = "/users"

    # Имитация базы данных для примера
    _db: list[dict[str, Any]] = [
        {"id": 1, "name": "Алексей", "email": "alex@example.com"}
    ]

    @get()
    async def get_users(self) -> list[User]:
        """Получить список всех пользователей."""
        # Litestar автоматически преобразует словари в объекты User
        return [User(**u) for u in self._db]

    @post()
    async def create_user(self, data: UserCreate) -> User:
        """Создать нового пользователя."""
        new_id = len(self._db) + 1
        new_user = {"id": new_id, "name": data.name, "email": data.email}
        self._db.append(new_user)
        return User(**new_user)


# ==========================================
# 3. Базовый эндпоинт (Healthcheck)
# ==========================================
@get("/")
async def index() -> dict[str, str]:
    return {"status": "ok", "message": "Сервер Litestar успешно запущен"}


# ==========================================
# 4. Инициализация приложения
# ==========================================
# Подключаем контроллеры и функции через список route_handlers
app = Litestar(
    route_handlers=[index, UserController],
)


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=443,
        reload=True,
        ssl_keyfile="localhost-key.pem",
        ssl_certfile="localhost-cert.crt"
    )
