from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView , ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.parsers import FormParser , MultiPartParser , JSONParser , FileUploadParser
from .serializers import UserRegistrationSerializer, UserLoginSerializer , AddAdvisorSerializer , BookingSerializer
from .models import User , Advisor, Booking
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from django.utils.encoding import iri_to_uri, uri_to_iri

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        data=request.data
        if data.get('email')=="" or data.get('name')=="" or data.get('password')=="":
            status_code = status.HTTP_400_BAD_REQUEST
            '''
            response = {
                'success' : 'False',
                'status code' : status_code,
                'message': 'Submit all values',
                }
            '''
            return Response(status=status_code)
        else:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            try:
                user=User.objects.get(email=data.get('email'))
                payload = JWT_PAYLOAD_HANDLER(user)
                jwt_token = JWT_ENCODE_HANDLER(payload)
                update_last_login(None, user)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    'User with given email and password does not exists'
                )
            status_code = status.HTTP_201_CREATED
            response = {
                'token' : jwt_token,
                'User_id':user.id,
                }
            
            return Response(response, status=status_code)

class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        data=request.data
        if data.get('email')=="" or data.get('password')=="":
            status_code = status.HTTP_400_BAD_REQUEST
            '''
            response = {
                'success' : 'False',
                'status code' : status_code,
                'message': 'Submit all values',
                }
            '''
            return Response(status=status_code)
        else:
            email = data.get("email", None)
            password = data.get("password", None)
            user = authenticate(email=email, password=password)
            if user is None:
                status_code=status.HTTP_401_UNAUTHORIZED
                '''
                response = {
                'success' : 'False',
                'status code' : status_code,
                'message': 'Username or password incorrect',
                }'''
                return Response(status=status_code)    
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            response = {
                'token' : serializer.data['token'],
                'User_id':user.id,
                }
            status_code = status.HTTP_200_OK

            return Response(response, status=status_code)
            
class AddAdvisorView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AddAdvisorSerializer
    parser_classes=(JSONParser,FormParser,MultiPartParser)
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid() and request.data['advisor_name'] !="" and request.data['advisor_photo_url'] != "":
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class AdvisorListView(ListAPIView):
    queryset=Advisor.objects.all()
    serializer_class=AddAdvisorSerializer
    permission_classes = (IsAuthenticated,)

class CallBookView(CreateAPIView):
    serializer_class=BookingSerializer
    permission_classes = (IsAuthenticated,)
    def post(self,request,user_id,advisor_id):
        serializer = self.serializer_class(data={"user":user_id, "advisor":advisor_id, "time":request.data.get('booking_time')})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CallBookListView(RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)

    def get(self,request,user_id):
        query=Booking.objects.filter(user_id=user_id)
        res=[]
        for q in query:
            dic={}
            dic["advisor_id"]=q.advisor.id
            dic["advisor_name"]=q.advisor.advisor_name
            dic["advisor_photo_url"]=q.advisor.advisor_photo_url.url
            dic["Booking_id"]=q.id
            dic["booking_time"]=str(q.time)
            res.append(dic)
        #response={"data":res}
        print(res)
        return Response(res,status=status.HTTP_200_OK)