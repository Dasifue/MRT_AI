import io
import cv2

import numpy as np
from PIL import Image
from celery import shared_task
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Results


@shared_task
def predict_tumor(result_id):

    print(f"Получение записи №{result_id}")
    result = get_object_or_404(Results, id=result_id)
    print(f"Запись найдена: {result}")

    print(f"Получение МРТ")
    with open(result.mrt_picture.path, "rb") as file:
        img = Image.open(io.BytesIO(file.read()))
    print("Файл найден")

    print(f"Начало анализа...")
    opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img = cv2.resize(opencvImage,(150,150))
    img = img.reshape(1,150,150,3)
    p = settings.MODEL().predict(img)
    p = np.argmax(p,axis=1)[0]

    if p==0:
        diagnosis = 'Glioma Tumor'
    elif p==1:
        diagnosis = 'No Tumor'
    elif p==2:
        diagnosis = 'Meningioma Tumor'
    else:
        diagnosis = 'Pituitary Tumor'
    print(f"Анализ завершён. Результат: {diagnosis}")

    result.diagnosis = diagnosis
    result.save(update_fields=['diagnosis'])
