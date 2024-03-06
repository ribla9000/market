from django.urls import path
from market.views import payment, download_image

urlpatterns = [
    path("webhooks/yoo", payment, name="payment"),
    path("download/<str:path>", download_image, name='download_image')
]
