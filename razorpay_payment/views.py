import os
from .keyconfig import *

from django.contrib.auth.decorators import login_required

from payments.settings import LOGIN_REDIRECT_URL
from razorpay_payment.models import Records
import razorpay
from allauth import socialaccount

from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import Donation_Form
from .models import Records
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


@login_required
def success_transaction_list(request):
    transactions = Records.objects.filter(user=request.user ).all()
    success_transactions = transactions.filter(completed=True).all()
    context={
        'transactions': success_transactions
    }
    return render(request, 'razorpay_payment/transactions.html', context)


@login_required
def failed_transaction_list(request):
    transactions = Records.objects.filter(user=request.user ).all()
    failed_transactions = transactions.filter(completed=False).all()
    context={
        'transactions': failed_transactions
    }
    return render(request, 'razorpay_payment/transactions.html', context)

def payment(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            d_form=Donation_Form(request.POST)
            amount = int(request.POST['amount'])*100
            current_user=request.user
            d_form.instance.user=current_user
            d_form.save()
            
            if d_form.is_valid:
                x=1
                client = razorpay.Client(auth=(razorpaykey, razorpaysecret))
                response = client.order.create({'amount':amount,'currency':'INR','payment_capture':1})
                print(response)
                order_id=response['id']
                
                d_form.instance.order_id=order_id
                print(order_id)
                
                d_form.save()
                context =  {
                'response':response,
                'amount':amount/100,
                'x':x,
                'razorpaykey':os.getenv('razorpaykey')

                }


        else:
            x=0
            d_form=Donation_Form()
            context =  {
                'd_form':d_form,
                'x':x,

                }

    
        return render(request,"razorpay_payment/payment.html",context)
    else:
        return render(request, template_name="razorpay_payment/home.html")


# def take_amount(request):
#     if request.method=="POST":
#         d_form = Donation_Form(request.POST)
#
#     d_form = Donation_Form
#     context={
#         'd_form': d_form
#     }

@csrf_exempt
def payment_success(request):
    # print(request.POST)
    # print("hello")
    if request.method =="POST":
        print(request.POST)
        razorpay_payment_id=request.POST["razorpay_payment_id"]
        razorpay_order_id=request.POST["razorpay_order_id"]
        razorpay_signature=request.POST["razorpay_signature"]
        org_name=request.POST["org_name"]

        current_order=Records.objects.filter(order_id=razorpay_order_id)[0]
        current_order.completed=True
        current_order.razorpay_payment_id=razorpay_payment_id
        current_order. razorpay_signature= razorpay_signature
        current_order.org_name=org_name
        current_order.save()

        
    return HttpResponse("<h1>Done payment hurray</h1><a href='/'>Home</a>")


def home_page(request):
    return render(request, template_name="razorpay_payment/home.html")


# def testview(request):
#     if request.method=="POST":
#         d_form=Donation_Form(request.POST,instance=request.user)
#         current_user=request.user
#         d_form.instance.user=current_user
#         amount = request.POST['amount']
#
#         if d_form.is_valid:
#             print(amount)
#             d_form.save()
#             return redirect('/')
#
#     else:
#         d_form=Donation_Form(instance=request.user)
#
#         context =  {
#         'd_form':d_form,
#         }
#
#         return render(request,"razorpay_payment/test.html",context)
    
