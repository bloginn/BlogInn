from blog.models import List


def getById(id):
    try:
        return List.objects.get(pk=id)
    except List.DoesNotExist:
        return False
