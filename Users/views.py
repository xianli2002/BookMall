from django.shortcuts import render

def cart(request):
    return render(request,'cart.html')
def detail(request):
    return render(request,'detail.html')
def index(request):
    return render(request,'index.html')
def list(request):
    return render(request,'list.html')
def login(request):
    return render(request,'login.html')
def place_order(request):
    return render(request,'place_order.html')
def register(request):
    return render(request,'register.html')
def user_center_info(request):
    return render(request,'user_center_info.html')
def user_center_order(request):
    return render(request,'user_center_order.html')
def user_center_site(request):
    return render(request,'user_center_site.html')

def test():
    pass
# Create your views here.
