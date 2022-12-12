from .models import Cartegory

def menu_links(self):
    links=Cartegory.objects.all()
    return dict(links=links)