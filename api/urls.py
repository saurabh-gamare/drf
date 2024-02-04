from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    # path('student_detail/<int:pk>', views.get_student_detail, name='student_detail'),
    # path('student_list/', views.get_student_list, name='student_list')
    path('model_object_serializer/<int:pk>', views.model_object_serializer, name='model_object_serializer'),
    path('post_request_serializer', views.post_request_serializer, name='post_request_serializer'),

    path('product_create_list_api', views.ProductCreateListAPI.as_view(), name='product_create_list_api'),
    path('product_get_update_destroy_api/<int:pk>', views.ProductGetUpdateDestroy.as_view(), name='product_get_update_destroy_api'),

    path('product_create_list_mixin_api', views.ProductCreateListMixinAPI.as_view(), name='product_create_list_mixin_api'),
    path('product_get_update_destroy_mixin_api/<int:pk>', views.ProductGetUpdateDestroyMixin.as_view(), name='product_get_update_destroy_mixin_api'),

    path('product_detail_api_view/<int:pk>', views.ProductDetailApiView.as_view(), name='product_detail_api_view'),
    path('product_create_api_view', views.ProductCreateApiView.as_view(), name='product_create_api_view'),
    path('product_list_api_view', views.ProductListApiView.as_view(), name='product_list_api_view'),
    path('product_update_api_view/<int:id>', views.ProductUpdateApiView.as_view(), name='product_update_api_view'),
    path('product_delete_api_view/<int:id>', views.ProductDeleteApiView.as_view(), name='product_delete_api_view'),
    path('product_list_create_api_view', views.ProductListCreateApiView.as_view(), name='product_list_create_api_view'),

    path('register_customer', views.RegisterCustomer.as_view(), name='register_customer'),
    path('login_customer', views.LoginCustomer.as_view(), name='login_customer'),

    # Generate Auth Token
    path('api-token-auth', auth_views.obtain_auth_token)
]
