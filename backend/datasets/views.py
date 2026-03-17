from django.http import JsonResponse
from .models import Dataset

def dataset_preview(request, id):
    dataset = Dataset.objects.get(id=id)
    return JsonResponse({
        'name': dataset.name,
        'sample_data': dataset.sample_data[:10],  # First 10 samples
    })