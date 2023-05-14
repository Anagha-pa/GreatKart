from store.models import Product
from .models import Category

def menu_links(request):
    links = Category.objects.all()
    product = Product.objects.all()
    return dict(links=links,product=product)
