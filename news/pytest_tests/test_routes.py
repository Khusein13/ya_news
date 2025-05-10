import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_news_home_access(client):
    response = client.get(reverse('news:home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_news_detail_access(client, news):
    response = client.get(reverse('news:detail', kwargs={'pk': news.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_comment_edit_access(client, comment):
    client.force_login(comment.author)
    response = client.get(reverse('news:edit', kwargs={'pk': comment.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_comment_delete_access(client, comment):
    client.force_login(comment.author)
    response = client.get(reverse('news:delete', kwargs={'pk': comment.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_comment_edit_redirect_anonymous(client, comment):
    response = client.get(reverse('news:edit', kwargs={'pk': comment.pk}))
    assert response.status_code == 302
    assert response.url.startswith('/auth/login/')


@pytest.mark.django_db
def test_comment_delete_redirect_anonymous(client, comment):
    response = client.get(reverse('news:delete', kwargs={'pk': comment.pk}))
    assert response.status_code == 302
    assert response.url.startswith('/auth/login/')


@pytest.mark.django_db
def test_comment_edit_access_other_user(client, news, comment):
    other_user = User.objects.create_user(username='otheruser', password='password')
    client.force_login(other_user)
    response = client.get(reverse('news:edit', kwargs={'pk': comment.pk}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_comment_delete_access_other_user(client, news, comment):
    other_user = User.objects.create_user(username='otheruser', password='password')
    client.force_login(other_user)
    response = client.get(reverse('news:delete', kwargs={'pk': comment.pk}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_registration_login_logout_access(client):
    response = client.get(reverse('users:login'))
    assert response.status_code == 200

    response = client.get(reverse('users:logout'))
    assert response.status_code == 200

    response = client.get(reverse('users:signup'))
    assert response.status_code == 200
