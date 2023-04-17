from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as admin_user
from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from .models import User
import jwt
from .serializers import userSerializer
from rest_framework.decorators import api_view

# Create your views here.

@api_view(["POST"])
def signUp(request):
    try:
        name = request.data['username']
        email = request.data['email']
        phone = request.data['phone']
        password = request.data['password']
    except:
        return Response({'status':'Please provide the particular details mentioned above'})

    if len(name) < 4 :
        return Response({'status':'Name should be minimum of 4 letters'})
    
    if len(password) < 6 :
        return Response({'status':'Password should be minimum of 6 characters'})
    
    check_user = User.objects.all()
    for i in check_user:
        if i.email == email:
            return Response({'status':'Email already exists'})
        elif i.phone == phone:
            return Response({'status':'Phone Number already exists'})
    user = User.objects.create(name = name,
           email = email,
           phone = phone,
           password = password )
    user.save()
    return Response({'status': 'Success'}) 



@api_view(['POST'])
def user_login(request):
    try:
        email = request.data['email']
        password = request.data['password']
    except:
        return Response({'status':'Please provide the mentioned details'})
    
    try:
        user = User.objects.get(email=email,password=password)
        if user is not None:
            # print('kkkkkkkkkkkk')
            if user.is_superuser is False:
                payload = {
                    'email':user.email,
                    'password':user.password,

                }
                jwt_token = jwt.encode(payload, 'secret', algorithm='HS256')
                # print(jwt_token,"toooooooooooken")
                return Response({'status' : "Success",'payload' : payload ,'user_jwt': jwt_token,'id':user.id})
    except:
        if User.DoesNotExist:
            return Response("Email or Password is Wrong")



@api_view(['POST'])   
def verify_token(request):
    token  = request.data['token']
    decoded = jwt.decode(token, 'secret', algorithms='HS256')
    print(decoded.get('email'),'Yes iam back////.......')
    user = User.objects.get(email=decoded.get('email'))
    serializer = userSerializer(user,many=False)

    if user:
        return Response(serializer.data)
    else:
        return Response({'status' : 'Token Invalid'})



@api_view(['GET'])
def profile_view(request,id):
    user = User.objects.get(id=id)
    serializer = userSerializer(user,many=False)
    return Response(serializer.data)


@api_view(["POST"])
def addImage(request,id):
    user = User.objects.get(id=id)
    user.image = request.data['image']
    user.save()
    serializer = userSerializer(user,many=False)
    return Response(serializer.data)
    


@api_view(['GET'])
def user_list(request):
    user = User.objects.all()
    serializer = userSerializer(user,many=True)
    print(serializer.data)
    return Response(serializer.data)



@api_view(['POST'])
def admin_login(request):
    try:
        email = request.data['email']
        password =str(request.data['password']) 
        
    except:
        return Response({'status': "Please provide the details"})
    try:
        print('try block.....')
        user = admin_user.objects.get(email=email)
        # user=admin_user.objects.all()
        # print(user,'userrrrrrrrrrrr')
        if user is not None:
            print('kkkkkkkkkkkk')
            if user.is_superuser is True:
                payload = {
                    'email':user.email,
                    'password':user.password,
                }
                jwt_token = jwt.encode(payload, 'secret', algorithm='HS256')
                # print(jwt_token,"toooooooooooken")
                return Response({'status' : "Success",'payload' : payload ,'admin_jwt': jwt_token})
            else:
                return Response({'status' : 'Not a superuser'})
    except:
        if User.DoesNotExist:
            return Response("Email or Password is Wrong")
        

@api_view(['GET'])
def edit_user(request,id):
    user = User.objects.get(id=id)
    serializer = userSerializer(user,many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def update_user(request,id):
    user = User.objects.get(id=id)
    user.name = request.data["username"]
    user.email = request.data["email"]
    user.save()
    return Response("User Updated")


@api_view(['GET'])
def delete_user(request,id):
    user = User.objects.get(id=id)
    user.delete()
    return Response("User deleted")