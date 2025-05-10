import pytest
from django.urls import reverse
from news.models import News
from django.utils import timezone
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_news_count_on_home_page(client):
    for i in range(15):
        News.objects.create(title=f'News {i}', text='Content', date=timezone.now().date())

    response = client.get('/')
    assert len(response.context['news_list']) <= 10


@pytest.mark.django_db
def test_news_sorting_on_home_page(client):
    News.objects.create(title='Old News', text='Old Content', date=timezone.now().date() - timezone.timedelta(days=2))
    News.objects.create(title='Recent News', text='Recent Content', date=timezone.now().date())
    News.objects.create(title='Another Recent News', text='Another Recent Content', date=timezone.now().date() - timezone.timedelta(days=1))

    response = client.get('/')
    news_titles = [news.title for news in response.context['news_list']]
    assert news_titles == ['Recent News', 'Another Recent News', 'Old News']


@pytest.mark.django_db
def test_comments_order_on_news_detail_page(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    news = News.objects.create(title='Test News', text='Test Content', date=timezone.now())

    response = client.get(f'/news/{news.pk}/')
    assert response.status_code == 200
    assert response.context['object'] == news

    comments_list = response.context.get('comments_list', [])
    assert len(comments_list) == 0


@pytest.mark.django_db
def test_comment_form_access_for_anonymous_user(client):
    news = News.objects.create(title='Test News', text='Test Content', date=timezone.now())
    response = client.get(f'/news/{news.pk}/')
    assert response.status_code == 200
    assert 'comment_form' not in response.content.decode()


@pytest.mark.django_db
def test_comment_form_access_for_authenticated_user(client):
    user = User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')
    news = News.objects.create(title='Test News', text='Test Content', date=timezone.now())
    response = client.get(f'/news/{news.pk}/')
    assert response.status_code == 200
    assert '<h3>Оставить комментарий:</h3>' in response.content.decode()
