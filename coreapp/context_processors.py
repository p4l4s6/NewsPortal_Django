from coreapp.models import Category


def main_menu(request):
    return {
        "menus": Category.objects.all().filter(is_active=True).filter(is_menu=True)
    }
