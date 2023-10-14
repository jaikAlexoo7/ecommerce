from django.shortcuts import render,redirect
from cart.models import Cart,Account,Order
from shop.models import Product
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def add_to_cart(request,p):
    product=Product.objects.get(pname=p)
    user=request.user
    try:
        cart=Cart.objects.get(user=user,product=product)
        if(cart.quantity<cart.product.stock):
            cart.quantity+=1
        cart.save()
    except Cart.DoesNotExist:
        cart=Cart.objects.create(product=product,user=user,quantity=1)
        cart.save()
    return redirect('cart:cart_view')

@login_required
def cart_view(request):
    total_amount = 0
    user=request.user
    try:
        cart=Cart.objects.filter(user=user)

        for i in cart:
            total_amount += i.quantity * i.product.price
    except:
        pass
    return render(request,'cartview.html',{'cart':cart,'total':total_amount})

@login_required
def cart_remove(request,p):
    product=Product.objects.get(pname=p)
    user=request.user
    try:
        cart=Cart.objects.get(user=user,product=product)
        if(cart.quantity>1):
            cart.quantity-=1
            cart.save()

        else:
            cart.delete()
    except:
        pass
    return redirect('cart:cart_view')

@login_required
def full_remove(request,p):
    product = Product.objects.get(pname=p)
    user = request.user
    try:
        cart = Cart.objects.get(user=user, product=product)
        cart.delete()
    except:
        pass
    return redirect('cart:cart_view')


@login_required
def order_form(request):
    if(request.method=="POST"):
        a=request.POST['a']
        p=request.POST['p']
        n=request.POST['n']
        user=request.user
        cart=Cart.objects.filter(user=user)
        total=0
        for i in cart:
            total+=i.quantity*i.product.price

        acct=Account.objects.get(acctnumber=n)
        if(acct.balance>total):
            acct.balance=acct.balance-total
            acct.save()
            for i in cart:
                o=Order.objects.create(user=user,product=i.product,phone=p,address=a,noofitems=i.quantity,order_status="Paid")
                o.save()
                i.product.stock=i.product.stock-i.quantity
                i.product.save()
            cart.delete()
            msg="Order placed succesfully"

            return render(request,'orderconfirm.html',{'msg':msg})
        else:
            msg="Transaction failed,insuffient Balance"
            return render(request, 'orderconfirm.html', {'msg': msg})
    return render(request,'orderform.html')

def order_status(request):
    user=request.user
    orders = Order.objects.filter(user=user)
    return render(request,'orderstatus.html',{'orders':orders})
