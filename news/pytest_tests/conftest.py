import pytest
from django.urls import reverse
from news.models import News, Comment  # Убедитесь в правильном импорте
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


@pytest.fixture
def news(db):
    """Создание фикстуры для объектов News."""
    return News.objects.create(title="Test Title", text="Test Content", date=timezone.now())


@pytest.fixture
def author_user(db):
    """Создание фикстуры для авторизованного пользователя."""
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def comment(db, news, author_user):
    """Создание фикстуры для объектов Comment."""
    return Comment.objects.create(news=news, author=author_user, text="Test Comment")
