from rest_framework import viewsets
from .serializers import ImageSerializer
from ..models import Image
from io import BytesIO
from rest_framework.response import Response
from django.core.files import File
from celery import shared_task, current_app
import os
from django.conf import settings
from django.shortcuts import render
from django.views import View
from rest_framework import status
from ..tasks import algorithm_image
from django.http import JsonResponse
from rest_framework.decorators import api_view
import time


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all().order_by('-uploaded')
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            context = {}
            image_uploaded = serializer.validated_data['picture']
            image_name = str(serializer.validated_data['picture'])
            file_path = os.path.join(settings.IMAGES_DIR, image_name)

            with open(file_path, 'wb+') as fp:
                for chunk in image_uploaded:
                    fp.write(chunk)

            result = algorithm_image.delay(file_path)

            return JsonResponse({"task_id": result.id,
                                 "task_status": result.status},
                                status=status.HTTP_201_CREATED)


@api_view(('GET',))
def get_status(request, task_id):
    task = current_app.AsyncResult(task_id)
    context = {'task_status': task.status, 'task_id': task.id}

    if task.status == 'PENDING':
        time.sleep(1)
        return Response({**context}, status=status.HTTP_201_CREATED)
    else:
        response_data = ImageSerializer(Image.objects.get(pk=task.get()))
        return Response({**context, **response_data.data}, status=status.HTTP_201_CREATED)
