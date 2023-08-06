from django.http import JsonResponse


# Generic responses

def response_success(message: str = "The operation was completed successfully", status: int = 200) -> JsonResponse:
    return response_message(message, status)


def response_message(message: str, status: int = 200) -> JsonResponse:
    return response_object({"message": message}, status)


def response_object(obj: dict, status: int = 200) -> JsonResponse:
    return JsonResponse(obj, status=status)
