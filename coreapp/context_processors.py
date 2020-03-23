from hitcount.models import HitCount

from coreapp.models import Category, Comment, Advertisement


def main_menu(request):
    return {
        "menus": Category.objects.all().filter(is_active=True).filter(is_menu=True),
        "comments": Comment.objects.all().order_by('-updated_at')[:5],
        "popular": HitCount.objects.all().order_by('-hits')[:4],
        "ad": Advertisement.objects.last(),
    }
