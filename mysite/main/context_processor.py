def categories(request):
    from .models import Category
    return {'category_set': Category.objects.all()}
