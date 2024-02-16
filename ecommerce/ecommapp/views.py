from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View 
from ecommapp.forms import UserRegister,UserLogin,CartForm,OrderForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# from django.views.generic import TemplateView,CreateView
from django.contrib.auth.models import User
from ecommapp.models import Products,Cart,Orders
from django.core.mail import send_mail,settings
# from django.urls import reverse_lazy
# Create your views here.
class HomeView(View):
    def get(self,request):
        data=Products.objects.all()
        return render(request,'index.html',{"product":data})

class UserRegisterView(View):
    def get(self,request,*args,**kwargs):
        form=UserRegister()
        return render(request,'user_register.html',{"form":form})
    def post(self,request,*args,**kwargs):
        form = UserRegister(request.POST)
        if(form.is_valid()):
             User.objects.create_user(**form.cleaned_data)
            #  messages.success(request,'Registration Successfull')
             messages.success(request,'registration successfully')
            #  return redirect('log_view')     
             return redirect('home_view')     
        else:
            messages.error(request,'Registration failed')
            return redirect('reg_view')
            
            
# class UserRegisterView(CreateView):
#     model=User
#     template_name="user_register.html"
#     form_class=UserRegister
#     success_url=reverse_lazy('home_view')
#     def form_valid(self,form):
#         messages.success(self.request,'Registraion Successful')
#         return super().form_valid(form)


class UserLoginView(View):
    def get(self,request,*args,**kwargs):
        form=UserLogin()
        return render(request,"user_login.html",{'form':form})
    def post(self, request,*args,**kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if (user):
            login(request,user)
            messages.success(request,'Login Successfull')
            return redirect('home_view')
        else:
            login(request,user)
            messages.error(request,'Login faild')
            return redirect('log_view')

class UserLogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        
        messages.success(request,'logout successfully')
        return redirect('home_view')
        # return HttpResponse("successfully logout")

class ProductDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        product=Products.objects.get(id=id)
        # filter used to get data based on a condioion here we use get method to get id
        return render(request,'product_detail.html',{"product":product})


class AddToCartView(View):
    def get(self,request,*args,**kwargs):
         form=CartForm()
         id=kwargs.get('id')
         product=Products.objects.get(id=id)
         return render(request,'addtocart.html',{'form':form,'product':product})
    def post(self,request,*args,**kwargs):
        user=request.user
        form =Cart(request.POST)
        id= kwargs.get('id')
        p=Products.objects.get(id=id)
        q= request.POST.get('quantity')
        Cart.objects.create(user=user,quantity=q,product=p)
        return redirect('home_view') 

class CartListView(View):
    def get(self,request,*args,**kwargs):
        cart=Cart.objects.filter(user=request.user).exclude(status='order-placed')
        return render(request,'cart_list.html',{'cart':cart})

class PlaceOrder(View):
    def get(self,request,*args,**kwargs):
        form=OrderForm()
        return render(request,"place_order.html",{'form':form})
    def post(self,request,*args,**kwargs):
        cart_id=kwargs.get('cart_id')
        cart=Cart.objects.get(id=cart_id)
        # to get id frrom Cars 
        user=request.user
        address=request.POST.get('address')
        email=request.POST.get('email')
        Orders.objects.create(user=user,cart=cart,address=address,email=email)
        send_mail("confirmation","your order has been placed successfully",settings.EMAIL_HOST_USER,[email])
        cart.status="order-placed"
        cart.save()
        return redirect('home_view')

class CartDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        data=Cart.objects.get(id=id)
        data.delete()
        return redirect('cart_list_view')



        
    
        



    