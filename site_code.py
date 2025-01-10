from datetime import datetime
from aiohttp import web
from db_code import get_announcements, send_new_announcement, delete_announcement_id, update_announcement_id
from models import Announcement

routes = web.RouteTableDef()


@routes.get("/")
async def start_page(request: web.Request):
    """Стартовая страница для http://127.0.0.1:5000"""
    with open(file='./templates/index.html', mode='rb') as f:
        index_html = f.read()
    return web.Response(body=index_html, content_type='text/html')


@routes.get(path='/announcements')
async def load_announcements(request: web.Request):
    """Получаем список всех объявлений"""
    results = await get_announcements()
    return web.json_response(data=results, status=200)


async def validate_data(data, required_fields):
    """Проверяет наличие всех обязательных полей/ Валидация"""
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"{field} is required"
    return True, None


@routes.post(path='/announcement')
async def create_announcement(request: web.Request):
    """Создание объявления"""
    data = await request.json()
    required_fields = ['title', 'description', 'author']
    is_valid, error_message = await validate_data(data, required_fields)
    if not is_valid:
        return web.json_response(data={"error": error_message}, status=201)
    else:
        new_announcement = Announcement(
            title=data['title'],
            description=data['description'],
            author=data['author'],
            created_at=datetime.now()
        )
        # Сохранение в базу данных
        response_data = await send_new_announcement(new_announcement)
        return web.json_response(data=response_data, status=201)


@routes.delete(path='/announcement/{id:\\d+}')
async def delete_announcement(request: web.Request):
    """Удаление объявления по ID"""
    announcement_id = request.match_info['id']
    announcement_data = await delete_announcement_id(announcement_id)
    if 'message' in announcement_data:
        return web.json_response(data=announcement_data,
                                 status=201)
    else:
        return web.json_response(data=announcement_data, status=409)


@routes.patch(path='/announcement/{id:\\d+}')
async def update_announcement(request: web.Request):
    """Обновление текста объявления по ID"""
    data = await request.json()
    required_fields = ['title', 'description', 'author']
    is_valid, error_message = await validate_data(data, required_fields)
    announcement_id = request.match_info['id']
    if not is_valid:
        return web.json_response(data={"error": error_message}, status=201)
    else:
        response_data = await update_announcement_id(announcement_id, data)
        return web.json_response(data=response_data, status=200)



app = web.Application()
app.add_routes(routes)  # Автоматически собираем router. Методы уже определены.

web.run_app(app, host='127.0.0.1', port=5000)
