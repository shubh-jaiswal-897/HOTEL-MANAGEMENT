
from django.http import HttpResponse
from django.shortcuts import render
from datetime import  datetime
from django.db import connection


from .models import *



# Create your views here.

def index(request):
    data=tbl_category.objects.all().order_by('-id')[0:12]
    pdata=tbl_product.objects.all().order_by('-id')[0:12]
    sdata=tbl_slider.objects.all().order_by('-id')[0:3]
    md={"cdata":data,"productdata":pdata,"sliderdata":sdata}
    return render(request,'index.html',md)

def Food(request):
    cid=request.GET.get('pid')
    if cid is not None:
        pdata=tbl_product.objects.all().filter(category=cid)
    else:
        pdata = tbl_product.objects.all().order_by('-id')
    cdata=tbl_category.objects.all().order_by('-id')

    mydict={"categorydata":cdata,"productdata":pdata}
    return render(request,'Food.html',mydict)

def about(request):
    return render(request,'about.html')

def contact(request):
    mydict={}
    if request.method == "POST":
        a=request.POST.get('name')
        b=request.POST.get('email')
        c=request.POST.get('mobile')
        d=request.POST.get('subject')
        e=request.POST.get('msg')
        contactus(Name=a,Email=b,Mobile=c,Subject=d,Message=e).save()
        return HttpResponse("<script>('Data Save Successfully');location.href='/contact/'</script>")

        #mydict={"name":a,"email":b,"mobile":c,"subject":d,"message":e,}

    return render(request,'contact.html',mydict)

def login(request):
    if request.method=="POST":
        email=request.POST.get('userid')
        passwd=request.POST.get('passwd')
        x=tbl_register.objects.all().filter(email=email,password=passwd).count()
        if x==1:
            y=tbl_register.objects.all().filter(email=email)
            request.session['userpic']=str(y[0].picture)
            request.session['username']=str(y[0].name)
            request.session['user']=email
            cartitems=tbl_cart.objects.all().filter(userid=email).count()
            request.session['cartitems']=cartitems
            return HttpResponse("<script>alert('you are login successfully');location.href='/login/';</script>")
        else:
            return HttpResponse("<script>alert('your userid or password is incorrect...');location.href='/login/';</script>")
    return render(request,'login.html')

def booktable(request):
    if request.method=="POST":
        name=request.POST.get('name')
        mobile=request.POST.get('mobile')
        email=request.POST.get('email')
        people=request.POST.get('people')
        bdate=request.POST.get('bdate')
        btime=request.POST.get('btime')
        ftype=request.POST.get('foodtype')
        etype=request.POST.get('eventtype')
        tbl_booktable(name=name,email=email,mobile=mobile,date_of_booking=bdate,time_of_booking=btime,no_of_people=people,type_of_event=etype,type_of_food=ftype,booking_date=datetime.now().date()).save()
        return HttpResponse("<script>alert('Your table booked successfully..');location.href='/booktable/'</script>")

    return render(request,'booktable.html')

def register(request):
    mydict = {}
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        passwd=request.POST.get('passwd')
        address=request.POST.get('address')
        mobile=request.POST.get('mobile')
        city=request.POST.get('city')
        pincode=request.POST.get('pincode')
        picture=request.FILES['fu']
        x=tbl_register.objects.all().filter(email=email).count()
        if x==1:
            return HttpResponse("<script>alert('You are already registered...');""location.href='register'</script>")
        else:
           tbl_register(name=name,email=email,password=passwd,address=address,mobile=mobile,city=city,pincode=pincode,picture=picture).save()
           return HttpResponse("<script>alert('Thanks for register with us....'); location.href='/register/'</script>")

    return render(request,'register.html',mydict)



def faqs(request):
     return render(request,'faqs.html')

def home(request):
    return render(request,'home.html')


def logout(request):
    if request.session.get('user'):
        del request.session['user']
        return HttpResponse("<script>alert('Now you are logout');location.href='/login/'</script>")
    return render(request,'logout.html')

def cart(request):
    user=request.session.get('user')
    if user:
        pid=request.GET.get('pid')
        pimage=request.GET.get('pimage')
        pprice=float(request.GET.get('pprice'))
        pname=request.GET.get('pname')
        pquantity=int(request.GET.get('pquantity'))
        total_price=pprice*pquantity
        if pquantity>0:
            tbl_cart(userid=user,product_id=pid,product_image=pimage,product_price=pprice,quantity=pquantity,total_price=total_price,product_name=pname,added_date=datetime.now().date()).save()
            cartitems = tbl_cart.objects.all().filter(userid=user).count()
            request.session['cartitems'] = cartitems
            return HttpResponse("<script>alert('Your Item is added successfully in cart...');location.href='/home/'</script>")
        else:
            return HttpResponse("<script>alert('Please Increase your item quantity');location.href='/home/'</script>")

    return render(request,'cart.html')


def orderhistory(request):
    oid=request.GET.get('oid')
    user=request.session.get('user')
    if user:
        data1=tbl_order.objects.all().filter(userid=user,status="pending")
        data2=tbl_order.objects.all().filter(userid=user,status="Accepted")
        data3=tbl_order.objects.all().filter(userid=user,status="Delivered")
        if oid is not None:
            tbl_order.objects.all().filter(id=oid).delete()
            return HttpResponse("<script>alert('Your order hava been canceld ');location.href='/orderhistory/'</script>")
        mydict={"porder":data1,"aorder":data2,"dorder":data3}

    return render(request,'orderhistory.html',mydict)

def myprofile(request):
    user=request.session.get('user')
    uinfo=""
    if user:
        uinfo=tbl_register.objects.all().filter(email=user)
        if request.method=="POST":
            name=request.POST.get('name')
            email=request.POST.get('email')
            mobile=request.POST.get('mobile')
            address=request.POST.get('address')
            city=request.POST.get('city')
            pincode=request.POST.get('pincode')
            passwd=request.POST.get('passwd')
            cpasswd=request.POST.get('cpasswd')
            picture=request.FILES['fu']
            if passwd==cpasswd:
                tbl_register(email=user,name=name,mobile=mobile,address=address,city=city,pincode=pincode,picture=picture,password=passwd).save()
                y = tbl_register.objects.all().filter(email=user)
                request.session['userpic'] = str(y[0].picture)
                request.session['username'] = str(y[0].name)
                return HttpResponse("<script>alert('Your Profile is update Successful..');location.href='/profile/'</script>")
            else:
                return HttpResponse("<script>alert('Confirm password is not matched..');location.href='/profile/'</script>")

    mydict={"userinfo":uinfo}
    return render(request,'myprofile.html',mydict)





def showcart(request):
    user=request.session.get('user')
    cid=request.GET.get('cid')
    data=""
    if user:
     data=tbl_cart.objects.all().filter(userid=user).order_by('-id')
     if cid is not None:
      tbl_cart.objects.all().filter(id=cid).delete()
      cartitems = tbl_cart.objects.all().filter(userid=user).count()
      request.session['cartitems']=cartitems
      return HttpResponse("<script>alert('You Items has been deleted from cart..');location.href='/showcart/'</script>")

    md={"cartdata":data}
    return render(request,'showcartitmes.html',md)


def cartforproduct(request):
    user = request.session.get('user')
    if user:
        pid = request.GET.get('pid')
        pimage = request.GET.get('pimage')
        pprice = float(request.GET.get('pprice'))
        pname = request.GET.get('pname')
        pquantity = int(request.GET.get('pquantity'))
        total_price = pprice * pquantity
        if pquantity > 0:
            tbl_cart(userid=user, product_id=pid, product_image=pimage, product_price=pprice, quantity=pquantity,
                     total_price=total_price, product_name=pname, added_date=datetime.now().date()).save()
            cartitems = tbl_cart.objects.all().filter(userid=user).count()
            request.session['cartitems'] = cartitems
            return HttpResponse("<script>alert('Your Item is added successfully in cart...');location.href='/Food/'</script>")
        else:
            return HttpResponse("<script>alert('Please Increase your item quantity');location.href='/Food/'</script>")

    return render(request,'pcart.html')

def order(request):
    user=request.session.get('user')
    msg=request.GET.get('msg')
    if user:
     if msg is not None:
        cursor=connection.cursor()
        cursor.execute("insert into user_tbl_order(userid,product_id,product_name,product_image,product_price,product_quantity,total_price,status,order_date) select '"+str(user)+"'userid,product_id,product_name,product_image,product_price,quantity,total_price,'pending','"+str(datetime.now().date())+"' from user_tbl_cart where userid='"+str(user)+"'")
        tbl_cart.objects.all().filter(userid=user).delete()
        cartitems =tbl_cart.objects.all().filter(userid=user).count()
        request.session['cartitems'] =cartitems
        return HttpResponse("<script>alert('Your order place successfully..');location.href='/orderhistory/'</script>")


    return render(request,'order.html')
