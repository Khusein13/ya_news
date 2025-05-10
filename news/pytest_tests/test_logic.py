import pytest
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from news.models import News, Comment


@pytest.mark.django_db
def test_anonymous_user_cannot_submit_comment(client):
    news = News.objects.create(title='Test News', text='Test Content', date=timezone.now())
    response = client.post(reverse('news:edit', args=[news.pk]), {'text': 'This is a comment'})
    assert response.status_code == 302
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_authenticated_user_can_submit_comment(client):
    user = User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')
    news = News.objects.create(title='Test News', text='Test Content', date=timezone.now())
    response = client.post(reverse('news:detail', args=[news.pk]), {'text': 'This is a comment'})
    assert response.status_code == 302
    assert Comment.objects.filter(news=news, author=user, text='This is a comment').exists()


@pytest.mark.django_db
def test_authenticated_user_can_edit_own_comment(client):
    user = User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')
    news = News.objects.create(title='Test News', text='Test Content', date=timezone.now())
    comment = Comment.objects.create(news=news, author=user, text='Original comment')
    response = client.post(reverse('news:edit', args=[comment.pk]), {'text': 'Updated comment'})
    assert response.status_code == 302
    comment.refresh_from_db()
    assert comment.text == 'Updated comment'
