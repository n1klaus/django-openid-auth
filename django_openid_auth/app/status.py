from django.http import JsonResponse


def get_status(request):
    data = {"status": "100% UP!"}
    return JsonResponse(data)
