from django.db.models import Max
from .models import Order, Product, User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer, OrderCreateSerializer, UserSerializer
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from .filters import ProductFilter, InStockFilterBackend, OrderFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# Classsbased Api view
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by("pk")
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, InStockFilterBackend]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price", "stock"]
    #pagination_class = PageNumberPagination
    # pagination_class.page_size = 2
    # pagination_class.page_query_param = "pagenum"
    # pagination_class.page_size_query_param = "size"
    # pagination_class.max_page_size = 4
    pagination_class = LimitOffsetPagination
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        
        return super().get_permissions()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items", "items__product")
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    
    def get_serializer_class(self):
        # Can also check if POST: if self.request.method == "POST": or if self.request.method in ["POST", "PUT", "PATCH"]: or self.request.method == "PUT"
        if self.action == "create" or self.action == "update":
            return OrderCreateSerializer
        
        return super().get_serializer_class()
    
    def get_queryset(self):        
        qs = super().get_queryset()
        user = self.request.user

        if not user.is_authenticated:
            return qs.none()

        if not user.is_staff:
            qs = qs.filter(user=user)

        return qs
        
    # @action(detail=False, methods=['get'], url_path="user-orders", permission_classes=[IsAuthenticated])
    # def user_orders(self, request):
    #     orders = self.get_queryset().filter(user=request.user)
    #     serializer = self.get_serializer(orders, many=True)
    
    #     return Response(serializer.data)
    
    
    

# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.filter(stock__gt=0)
#     serializer_class = ProductSerializer
    
    
# class ProductCreateAPIView(generics.CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
#     def create(self, request, *args, **kwargs):
#         print(request.data)
#         return super().create(request, *args, **kwargs)
    

# Functionbase Api views
# @api_view(["GET"])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
    
#     return Response(serializer.data)

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"
    
    def get_permissions(self):        
        self.permission_classes = [AllowAny]
        
        if self.request.method in ["PUT","PATCH","DELETE"]:
            self.permission_classes = [IsAdminUser]
        
        return super().get_permissions()
    

# @api_view(["GET"])
# def product_detail(request,pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
    
#     return Response(serializer.data)

# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related("items", "items__product")
#     serializer_class = OrderSerializer
    
# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related("items", "items__product")
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         qs = super().get_queryset()
        
#         return qs.filter(user=self.request.user)
    
        
        

# @api_view(["GET"])
# def order_list(request):
#     orders = Order.objects.prefetch_related("items", "items__product")
#     serializer = OrderSerializer(orders, many=True)
    
#     return Response(serializer.data)


class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer(
            {
                "products":products,
                "count":len(products),
                "max_price":products.aggregate(max_price=Max("price"))["max_price"]
            }
        )
        
        return Response(serializer.data)



class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
    
