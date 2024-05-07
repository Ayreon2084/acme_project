from django.urls import path

from . import views

app_name = 'pages'

# # 1. FBV.
# urlpatterns = [
#     path('', views.homepage, name='homepage'),
# ]

# # 2. CBV.
urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
]
