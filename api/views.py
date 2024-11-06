from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
# from api.models import Student
# from api.serializers import StudentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Product, Track, Album
from .serializers import ProductSerializer, TrackSerializer, AlbumSerializer
from rest_framework import generics, authentication
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.permissions import BasePermission, SAFE_METHODS, \
    IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import CustomPermissionClass
# from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
# from rest_framework.pagination import LimitOffsetPagination
from .paginations import CustomPagination


# Create your views here.

# def get_student_detail(request, pk):
#     student_detail = Student.objects.get(id=pk)
#     student_detail = StudentSerializer(student_detail)
#     return JsonResponse(student_detail.data)
#
# def get_student_list(request):
#     student_list = Student.objects.all()
#     student_list = StudentSerializer(student_list, many=True)
#     return JsonResponse(student_list.data, safe=False)


@api_view(['GET'])
def model_object_serializer(request, pk):
    details = Product.objects.get(id=pk)
    # print(details)
    serialized_data = {}
    print(details, 'details')
    if details:
        print(details.price, 'price')
        serialized_data = ProductSerializer(details).data
        # print(serialized_data)
    return Response(serialized_data)


@api_view(['POST'])
def post_request_serializer(request):
    print(request.data)
    print(type(request.data))
    serialized_data = ProductSerializer(data=request.data)
    # here data keyword should be passed as request.data is a request
    if serialized_data.is_valid(raise_exception=True):
        return Response(serialized_data.data)


##########  API VIEWS START ###########
class ProductCreateListAPI(APIView):

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # request_data = request.data
            # response = Product(
            #         title = request_data.get('title'),
            #         content = request_data.get('content'),
            #         price = request_data.get('price')
            #     )
            # response.save()
            response = serializer.save()  # inbuilt method create() will be called from serializers.py
            return Response({
                'product_id': response.id
            })

    def get(self, request):
        instance = Product.objects.filter(price__lt=50)
        # instance = Product.objects.all()

        paginator = CustomPagination()
        result = paginator.paginate_queryset(instance, request)

        serializer = ProductSerializer(result, many=True)
        serializer_data = serializer.data
        # for data in serializer_data:
        #     if float(data.get('price')) > 10:
        #         tags = 'Premium'
        #     else:
        #         tags = 'Basic'
        #     data['tags'] = tags

        # Instead of above code we can use get_<attribute_name> in serializers.py
        # return Response(serializer_data)
        return paginator.get_paginated_response(serializer_data)

    # Here, only create and list api combinations can be used because these 2 apis dont require pk


class ProductGetUpdateDestroy(APIView):

    def get(self, request, pk):
        instance = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk):
        # method 1
        # data = request.data
        # Product.objects.filter(id=pk).update(
        #         title=data.get('title')
        #     )
        # return Response({
        #     'product_id': pk
        # })

        # method 2
        # instance = Product.objects.get(id=pk)
        # request_data = request.data
        # instance.title = request_data.get('title')
        # instance.content = request_data.get('content')
        # instance.save()
        # return Response({
        #     'pk': pk
        # })

        # method3 (Preferred method)
        instance = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = serializer.save()  # inbuilt method update() will be called from serializers.py
            return Response({
                'pk': pk
            })

    def delete(self, request, pk):
        instance = Product.objects.get(id=pk)
        instance.delete()
        return Response({
            'product_id': pk
        })

    # Here, only retrieve, update and delete api combinations can be used because these 3 apis require pk


##########  API VIEWS END ###########


##########  GENERIC VIEWS START ###########
class ProductDetailApiView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CustomPermissionClass]

    # for modifying the response, retrieve() method is used
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # get_object() is used as only single data is fetched
        # instance = self.get_queryset() # get_queryset() will be used for multiple data
        serializer = self.get_serializer(instance)
        print(serializer)
        # we cannot use serializer.validated_data in get apis as its already saved in db
        # and that means the data was already validated
        data = dict(serializer.data)
        data.pop('price')
        data.pop('sale_price')
        return Response({'response': data})


class ProductCreateApiView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # for doing things with serializer like modifying the request data and saving data in db,
    # perform_create() method is used
    def perform_create(self, serializer):
        print(self.request.data)
        validated_data = serializer.validated_data
        title = validated_data.get('title')
        content = validated_data.get('content')
        if not content:
            content = title
        instance = serializer.save(content=content)
        return instance.id

    # for modifying the response, create() method is used
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            product_id = self.perform_create(serializer)
            return Response({
                'product_id': product_id
            })


class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # pagination_class = CustomPagination
    # If there are no customizations in the api then just add 'pagination_class' attribute
    # But if there are modifications then make changes for paginator as below

    # for custom query, use the get_queryset method. Similary we can do this for get_object method
    def get_queryset(self):
        # queryset = Product.objects.filter(price__gt=15)
        # queryset = Product.objects.select_related('user').filter(user__email='sg35.user@gmail.com')
        queryset = Product.objects.all()
        return queryset

    # for modifying the response, list() method is used
    def list(self, request, *args, **kwargs):
        print(request.user)
        instance = self.get_queryset()

        paginator = CustomPagination()
        results = paginator.paginate_queryset(instance, request)

        serializer = self.get_serializer(results, many=True)
        product_list = []
        data = list(serializer.data)
        # for details in data:
        #     if float(details.get('sale_price')) < 50:
        #         product_list.append(details)
        # return Response(data)
        return paginator.get_paginated_response(data)


class ProductUpdateApiView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    permission_classes = [CustomPermissionClass]

    def perform_update(self, serializer):
        data = serializer.validated_data  # validated request data
        price = 20 if data.get('price') > 20 else data.get('price')
        serializer.save(price=price)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            print(kwargs)
            return Response({
                'product_id': kwargs.get('id')
            })


class ProductDeleteApiView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    # If there's no need, then do not overwrite destroy method
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # In perform_destroy method, we pass instance as the parameter instead of serializer
        self.perform_destroy(instance)
        return Response({})


# This api can run list and create apis both
class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = [authentication.SessionAuthentication]
    # authentication_classes = [authentication.TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    # permission_classes = [CustomPermissionClass]

    def perform_create(self, serializer):
        data = serializer.validated_data
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user)
        print(queryset.values())
        return queryset

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        return Response(list(serializer.data))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            serializer_data = dict(serializer.data)
            content = serializer_data.get('content') if serializer_data.get('content') else 'Anything'
            return Response({
                'content': content
            })


# Similar APIs
# RetrieveUpdateAPIView
# RetrieveDestroyAPIView
# RetrieveUpdateDestroyAPIView

##########  GENERIC VIEWS END ###########



##########  MIXINS API VIEWS START ###########
class ProductCreateListMixinAPI(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        instance = Product.objects.filter(price__lt=50)
        serializer = ProductSerializer(instance, many=True)
        return Response({
            'product_details': serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)  # This is nothing but serializer.save()
            return Response({
                'msg': 'Product Added!'
            })

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductGetUpdateDestroyMixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


##########  MIXINS API VIEWS END ###########

class RegisterCustomer(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = serializer.save()
            token, created = Token.objects.get_or_create(user=response)
            return Response({
                'token': str(token)
            })

        # The token returned must be used in headers when calling other APIs
        # Authorization: Token 8cbea44c2773d908ad59551f7d4fe77e13cb8047
        # A prefix named 'Token' must be used


class LoginCustomer(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer_data = serializer.data
            username = serializer_data.get('username')
            password = serializer_data.get('password')
            user = authenticate(username=username, password=password)
            # here user object is returned
            if not user:
                return Response({
                    'status': 401,
                    'message': 'Invalid Credentials',
                    'data': {}
                })
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 200,
                'message': 'Success',
                'data': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            })

        # The token returned must be used in headers when calling other APIs
        # Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkzNDI1MjQyLCJpYXQiOjE2OTM0MjQ5NDIsImp0aSI6ImM4MGZkNGFkZDIxZDQxZTNhMzU1YWZkNGM5ZGExOTliIiwidXNlcl9pZCI6MzF9.tAVHkXc6ZQSQa9_3FhVXWZqnlC7JWa54hrEd89iPD3Q
        # A prefix named 'Bearer' must be used



class ListTracks(APIView):

    def get(self, request):
        instance = Track.objects.all()
        serializer = TrackSerializer(instance, many=True)
        return Response(serializer.data)
    

class ListAlbums(APIView):

    def get(self, request):
        instance = Album.objects.all()
        serializer = AlbumSerializer(instance, many=True)
        return Response(serializer.data)
