from django.urls import path, include
from rest_framework_nested import routers
from images.api import views

router = routers.SimpleRouter()
router.register(r'', views.ImageView)

image_nested_router = routers.NestedSimpleRouter(router, r'', lookup='image')
image_nested_router.register(r'tags', views.ImageTagView)
image_nested_router.register(r'tags-bulk', views.ImageTagBulkView)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(image_nested_router.urls)),
]
