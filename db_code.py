from sqlalchemy import select
from db_settings import *
from models import Announcement


async def get_announcements():
    """
    Функция получения всех объявлений из ДБ
    """
    async with engine_table.begin() as session:
        result = await session.execute(select(Announcement))
        announcements = result.fetchall()
        if announcements:
            results = [{
                'id': announcement.id,
                'title': announcement.title,
                'description': announcement.description,
                'author': announcement.author,
                'created_at': announcement.created_at.isoformat(),
            } for announcement in announcements]
        else:
            response_data = {'message': 'Announcement not found'}
            return response_data
    return results


async def send_new_announcement(new_announcement):
    """
    Функция создания нового объявления
    """
    try:
        async with Session() as session:
            session.add(new_announcement)
            await session.commit()
        response_data = {'message': 'Announcement created successfully'}
        return response_data
    except Exception as e:
        print(f"Error occurred: {e}")


async def delete_announcement_id(id_announcement):
    """
    Функция удаления объявления по id
    """
    async with Session() as session:
        result = await session.execute(select(Announcement).where(Announcement.id == int(id_announcement)))
        announcement = result.scalars().first()
        if announcement:
            await session.delete(announcement)
            await session.commit()
            response_data = {'message': 'Announcement delete successfully'}
            return response_data
        else:
            response_data = {'error': 'Announcement no delete successfully'}
            return response_data


async def update_announcement_id(id_announcement, data):
    """
    Функция обновления конкретного объявления
    """
    async with Session() as session:
        try:
            result = await session.execute(select(Announcement).where(Announcement.id == int(id_announcement)))
            announcement = result.scalars().first()
            if not announcement:
                response_data = {'error': 'Announcement not found'}
                return response_data
            announcement.title = data['title']
            announcement.description = data['description']
            announcement.author = data['author']
            await session.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
            response_data = {'error': 'Announcement not found'}
            return response_data
    response_data = {'message': 'Announcement updated successfully'}
    return response_data
