from .cart import Cart as CartUtil  # We'll define this utility below

def cart(request):
    return {'cart': CartUtil(request)}