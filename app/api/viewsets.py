from imp import get_magic
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status , filters , generics , mixins ,viewsets
from app.api.serializers import GuestSerializer,MovieSerializer,ReservationSerializer
from ..models import Guest, Movie, Reservation
from rest_framework.views import APIView
from django.http import Http404
# function based views 
# GET POST
@api_view(['GET' , 'POST'])
def FBV_LIST(request):
    if request.method=='GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests , many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GuestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status =status.HTTP_201_CREATED)
        return Response(serializer.data , status = status.HTTP_400_BAD_REQUEST)
# PK ( GET PUT DELETE)
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request,pk):
    try:
        guest = Guest.objects.get(id=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = GuestSerializer(guest , many=False)
        return Response(serializer.data)
    elif request.method == 'PUT': 
        serializer = GuestSerializer(guest , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        
# CBV class based views
# LIST AND CREATE ( GET - POST )
class CBV_LIST(APIView):
    def get(self,request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests , many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.data , status=status.HTTP_400_BAD_REQUEST)

# (CBV) DELETE UPDATE GET => PK
class CBV_PK(APIView): 
    def get_object(self,pk):
        try:
            return Guest.objects.get(id=pk)
        except Guest.DoesNotExist:
            raise Http404
    
    def get(self,request,pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest,many=False)
        return Response(serializer.data)
    def put(self,request,pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    def delete(self,pk,request):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# MIXINS DRY ( don't repeat yourself) GET - POST 
class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)

# MIXINS GET PUT DELETE => PK
class mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin , generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self,request,pk):
        return self.retrieve(request)
    def put(self,request,pk):
        return self.update(request)
    def delete(self,request,pk):
        return self.destroy(request)

# GENERICS
# GET - POST 
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

# GENERICS GET - PUT - DELETE => pk
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

# VIEWSETS
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

# Find Movie Using Filter (To check it in POSTMAN)
@api_view(['GET'])
def find_movie(request):
    data = request.data
    movie = Movie.objects.filter(
        hall = data['hall'],
        movie = data['movie'],
    )
    serializer = MovieSerializer(movie,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def reservation(request):
    data = request.data
    movie = Movie.objects.get(
        hall = data['hall'],
        movie = data['movie'],
    )
    guest = Guest.objects.create(
        name = data['name'],
        mobile = data['mobile']
    )
    reservation = Reservation.objects.create(
        guest = guest,
        movie = movie,
    )
    return Response(status=status.HTTP_201_CREATED)