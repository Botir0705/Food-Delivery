from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.log_in, name='log_in'),
    path('index/', views.index, name='index'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log_out/', views.log_out, name='log_out'),
    path('restaurant/<int:pk>', views.restaurant, name='restaurant'),
    path('<int:id>/', views.categories, name='categories'),
    path('halal/', views.halal, name='halal'),
    path('add/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove/<int:pk>', views.remove_from_cart, name='remove'),
    path('checkout/', views.checkout, name='checkout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)