from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Records(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.PositiveIntegerField()
    time=models.DateTimeField(default=timezone.now)
    completed=models.BooleanField(default=False)
    order_id=models.CharField(max_length=25,blank=True)
    razorpay_payment_id=models.CharField( max_length=50,blank=True)
    razorpay_signature=models.CharField(max_length=100,blank=True)
    org_name=models.CharField(max_length=100,blank=True)




    def __str__(self):
        return self.order_id