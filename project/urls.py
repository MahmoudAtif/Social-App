"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from project.users import urls as users_urls_v1
from project.friends import urls as friends_urls_v1
from project.posts import urls as posts_urls_v1
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls.i18n import i18n_patterns


schema_view = get_schema_view(
    openapi.Info(
        title="User-Authentication Api",
        default_version='v1',
        description="A description of your API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('api/users/v1/', include((users_urls_v1, 'users'))),
    path('api/users/v1/auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('api/friends/v1/', include((friends_urls_v1, 'friends'))),
    path('api/posts/v1/', include((posts_urls_v1, 'posts'))),
    prefix_default_language=False
)


if settings.DEBUG:
    urlpatterns += [
        path(
            'api-docs/',
            schema_view.with_ui(
                'swagger',
                cache_timeout=0
            ),
            name='schema-swagger-ui'
        ),
        path(
            'redoc/',
            schema_view.with_ui(
                'redoc',
                cache_timeout=0
            ),
            name='schema-redoc'
        ),
        path('__debug__/', include('debug_toolbar.urls')),
    ]

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
