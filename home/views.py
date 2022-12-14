from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import response

from django.db.models import Q
from django.core.paginator import Paginator

from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import BlogSerializer

from . models import Blog


class PublicView(APIView):
    def get(self, request):
        try:
            blogs = Blog.objects.all().order_by('?')

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search) | Q(description__icontains = search))

            
            page_number = int(request.GET.get('page', 1))
            paginator = Paginator('blogs',1)

            serializer = BlogSerializer(blogs, many = True)

            return Response({
                'data':serializer.data,
                'message':'venues fetched successfully'
            },status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            

            return Response({
                'data' : {},
                'message' : 'something went wrongly'
            },status=status.HTTP_400_BAD_REQUEST)



class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user = request.user)

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search) | Q(description__icontains = search))


            serializer = BlogSerializer(blogs, many=True)

            return Response({
                'data':serializer.data,
                'message':'venues fetched successfully'
            },status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            

            return Response({
                'data' : {},
                'message' : 'something went wrongly'
            },status=status.HTTP_400_BAD_REQUEST)



    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    'data' : serializer.errors,
                    'message' : 'something went wrong'
                },status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                    'data' : serializer.data,
                    'message' : 'venue entry successfully'
                },status=status.HTTP_201_CREATED)
            
        except Exception as e:
            

            return Response({
                'data' : {},
                'message' : 'something went wrongly'
            },status=status.HTTP_400_BAD_REQUEST)

    
    def patch(self, request):
        try:
            data = request.data
            

            blog = Blog.objects.filter(uid = data.get('uid'))

            if not blog.exists():
                return response({
                    'data':{},
                    'message':"invalid venue card uid"
                }, status=status.HTTP_401_UNAUTHORIZED)


            if request.user != blog[0].user:
                return response({
                    'data':{},
                    'message':"you are not authorized to change this blog"
                }, status=status.HTTP_401_UNAUTHORIZED)

            serializer = BlogSerializer(blog[0],data=data, partial = True)

            if not serializer.is_valid():
                return Response({
                    'data' : serializer.errors,
                    'message' : 'something went wrong'
                },status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                    'data' : serializer.data,
                    'message' : 'venue details updated successfully'
                },status=status.HTTP_201_CREATED)
        
        
        except Exception as e:
            

            return Response({
                'data' : {},
                'message' : 'something went wrongly'
            },status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            data = request.data
            

            blog = Blog.objects.filter(uid = data.get('uid'))

            if not blog.exists():
                return response({
                    'data':{},
                    'message':"invalid venue card uid"
                }, status=status.HTTP_401_UNAUTHORIZED)


            if request.user != blog[0].user:
                return response({
                    'data':{},
                    'message':"you are not authorized to change this venue details"
                }, status=status.HTTP_401_UNAUTHORIZED)

            blog[0].delete()

            return Response({
                    'data' : {},
                    'message' : 'venue deleted successfully'
                },status=status.HTTP_202_ACCEPTED)
            
        except Exception as e:
            

            return Response({
                'data' : {},
                'message' : 'something went wrongly'
            },status=status.HTTP_400_BAD_REQUEST)