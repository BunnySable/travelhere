from django.shortcuts import render, redirect
from travelapp.models import Travel, Cart, Profile, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import razorpay
from django.core.mail import send_mail

# catagories = Travel.objects.values('type').distinct()

# Create your views here.
def home(request):
    # print('after login in home:'),request.user.is_authernticated
    context = {}
    data = Travel.objects.all()
    context['travels'] = data
    catagories = Travel.objects.values('catagory').distinct()
    context['types']=catagories
    return render(request,'index.html',context)    

def register(request):
    if request.method == "GET":
        return render(request,'register.html')
    else:
        context={}
        u = request.POST['username']
        e = request.POST['email']
        p = request.POST['password']
        cp = request.POST['confirmpassword']

        if u=='' or e=='' or p=='' or cp=='':
            context['error']='please fill all details'
            return render(request,'register.html',context)
        elif p != cp:
            context['error']= 'Password and confirm Password must be same'
            return render(request,'register.html',context)
        elif User.objects.filter(username=u).exists():
            context['error']= 'Username already exist. enter unique username'
            return render(request,'register.html',context)
        else :
            user = User.objects.create(username=u, email=e)
            user.set_password(p)
            user.save()
            # context['success']='Rgistered successfully !! Please Login'
            # return render(request, 'login.html',context)
            messages.success(request,'Registeration Successfully!! please Login')
            return redirect('/login')


def userlogin(request):
    if request.method =="GET":
        return render(request,'login.html')
    else:
        context={}
        u=request.POST['username']
        p=request.POST['password']
        user = authenticate(username=u,password=p)
        if user is None:
            print('worng details')
            context['error']='kindly enter corret details to login'
            return render(request,'login.html',context)
        else:
            print('successful authentication')
            print(request.user.is_authenticated)
            login(request,user)  # session login 
            messages.success(request,'Logged in successfully !!')
            return redirect('/')
        
def userLogout(request):
    logout(request)
    messages.success(request,'logout successful !!')
    return redirect('/')

def aboutus(request):
    logout(register)
    
    return render(request,'aboutus.html')

def contactus(request):
    return render(request,'contactus.html')

def travelDetails(request,travelid):
    data = Travel.objects.get(id = travelid)
    context ={}
    context['travel'] = data 
    return render(request, 'details.html', context)

def searchByCatagory(request,searchBy):
    data = Travel.objects.filter(catagory = searchBy)
    context = {}
    context['travels']=data
    return render(request,'index.html',context)

# def searchByRange(request):
#     minprice=request.GET['min']
#     maxprice=request.GET['max']
#     c1=Q(price__gte=minprice)
#     c2=Q(price__lte=maxprice)
#     data=Cloth.objects.filter(c1 & c2)
#     context={}
#     context['cloths']=data
#     return render(request,'index.html',context)

# def sortTravelByPrice(request,dir):

#     if dir == 'asc':
#         col='price'
#     else:
#         col='price'
#     data = Travel.objects.all().order_by(col)
#     context = {}
#     context['pets']=data
#     return render(request,'index.html',context)

# def addToCart(request,travelid):
#     user = request.user
#     travel = Travel.objects.get(id = travelid)
#     cart = Cart.objects.create(travelid = travel, uid = user)
#     cart.save()
#     messages.success(request,'travel added to cart successfully !!')
#     return redirect('/')

def addToCart(request,travelid):
    userid=request.user.id
    if userid:
        travel=Travel.objects.get(id = travelid)
        cart=Cart.objects.create(travelid=travel,uid=request.user)
        cart.save()
        messages.success(request,'Item Added To Cart')
        return redirect('/')
    else:
        messages.error(request,'Please Login')
        return redirect('/login')
    
def showMyCart(request):
    userid = request.user.id
    data = Cart.objects.filter(uid = userid)
    context = {}
    context['cartlist']= data
    count = len(data)
    total =0
    for cart in data:
        total += cart.travelid.price   #*cart.quantity
    context['count']=count
    context['total']=total
    return render(request,'cart.html',context)

def removeCart(request,cartid):
    cart = Cart.objects.filter(id = cartid)
    cart.delete()
    messages.error(request,'Travel Remove from the cart successfully !!')
    return redirect('/mycart')

def updateQuantity(request,cartid,oprn):
    if oprn =='incr':
        cart = Cart.objects.filter(id = cartid)
        qty = cart[0].quantity
        cart.update(quantity =qty+1)
        return redirect('/mycart')
    else:
        cart = Cart.objects.filter(id = cartid)
        qty = cart[0].quantity
        cart.update(quantity =qty-1)
        return redirect('/mycart')

def confirmOrder(request):
    userid=request.user.id
    data = Cart.objects.filter(uid = userid)
    context={}
    context['cartlist']=data
    count=len(data)
    total=0
    for cart in data:
        total+=cart.travelid.price*cart.quantity
    context['count']=count
    context['total']=total
    return render(request,'confirmorder.html',context)

def makePayment(request):
    userid=request.user.id
    data = Cart.objects.filter(uid = userid)
    total=0
    for cart in data:
        total+=cart.travelid.price*cart.quantity
    client = razorpay.Client(auth=("rzp_test_QPXTPF1KYwWdC0", "QrLzjZkppijznBLWFiAnmDSt"))

    data = { "amount": total*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    # context['profile']=Profile.objects.get(id = userid)
    return render(request,'pay.html',context)

def placeOrder(request,oid):
    '''
    1. userid
    2. card Fetch
    3. isnsert order details
    4. cart clear
    5. send gmail
    6. hoome --> 'order placed'
    '''
    userid=request.user.id
    # user=User.objects.get(id=userid)
    cartlist = Cart.objects.filter(uid = userid)
    for cart in cartlist:
        # travel=Travel.objects.get(id=cart.clothid)
        order=Order.objects.create(orderid=oid,userid=cart.uid,travelid=cart.travelid,quantity=cart.quantity)
        order.save()
    cartlist.delete()
    # sending email
    msg = "Thank you for placing the order. Your order id is: "+oid
    send_mail(
        "Order placed successfully !!",
        msg,
        "ganeshsable247@gmail.com",
        [request.user.email],
        fail_silently=False,
    )
    messages.success(request,'Order Placed Successfully!!!')
    return redirect('/')


def editProfile(request):
    if request.method=='GET':
        userid=request.user.id
        context={}
        # context['profile']=Profile.objects.get(id = userid)
        return render(request,'profile.html',context)
    else:
        fn=request.POST['firstname']
        ln=request.POST['lastname']
        m=request.POST['mobile']
        a=request.POST['address']

        userid = request.user.id
        user = User.objects.filter(id=userid)
        user.update(first_name=fn,last_name=ln)

        profile=Profile.objects.create(id = user[0], mobile = m,address = a)
        profile.save()
        messages.success(request,'Profile Updated!!!')
        # return render(request,'profile.html')
        return redirect("/")
    