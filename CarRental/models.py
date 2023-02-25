from django.contrib.auth.models import User
from django.db import models
import uuid
from django.utils import timezone
from django.db.models import F, Sum, Count
import datetime


class Geographies(models.Model):
    name= models.CharField(max_length=30,default="")
    def __str__(self):
        return self.name
class Provinces(models.Model):
    code  = models.CharField(max_length=30,default="")
    name_th = models.CharField(max_length=30,default="")
    name_en = models.CharField(max_length=30,default="")
    geography_id = models.ForeignKey(Geographies,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.name_th

class Member(models.Model):
    mem_id = models.CharField(primary_key=True, max_length=13, default="")
    name = models.CharField(max_length=60,default="")
    provinces = models.ForeignKey(Provinces, on_delete=models.CASCADE, default=None)
    email = models.CharField(max_length=50,default="")
    tel = models.CharField(max_length=10, default="")
    img = models.ImageField(upload_to='static/image/Member/', default="")
    def __str__(self):
        return str(self.mem_id) +" : "+self.name

class Owner(models.Model):
    own_id = models.CharField(primary_key=True, max_length=13, default="")
    name = models.CharField(max_length=60,default="")
    address = models.CharField(max_length=100, default="")
    provinces = models.ForeignKey(Provinces, on_delete=models.CASCADE, default=None)
    email = models.CharField(max_length=50,default="")
    tel = models.CharField(max_length=10, default="")
    password = models.CharField(max_length=35, default="")
    linkLocation = models.URLField(max_length=200,default="")
    birthdate = models.DateField(blank=True, default='', null=True)
    img = models.ImageField(upload_to='static/image/Owner/', default="",blank=True,null=True)
    def __str__(self):
        return self.own_id +" : "+self.name

class Bank(models.Model):
    bank_name = models.CharField(max_length=20,default="")
    img = models.ImageField(upload_to='static/image/Bank/', default="")
    def __str__(self):
        return self.bank_name

class OwnBank(models.Model):
    bank_id = models.ForeignKey(Bank, on_delete=models.CASCADE, default=None)
    bank_num = models.CharField(max_length=20, default="")
    name = models.CharField(max_length=30, default="")
    branch = models.CharField(max_length=30, default="")
    own_id = models.ForeignKey(Owner,on_delete=models.CASCADE,default=None)
    def __str__(self):
        return self.bank_num + " : "+self.own_id.name

class Adress(models.Model):
    own_id = models.ForeignKey(Owner,on_delete=models.CASCADE,default=None)
    name = models.CharField(max_length=100,default="")
    province = models.ForeignKey(Provinces,on_delete=models.CASCADE,default=None)
    location = models.URLField(max_length=200,default="")
    def __str__(self):
        return str(self.id)

class CarType(models.Model):
    type_id = models.CharField(primary_key=True, max_length=8, default="")
    type_name = models.CharField( max_length=20,unique=True, default="")
    picture = models.ImageField(upload_to='static/image/types/', default="")
    def __str__(self):
        return self.type_name

class Car(models.Model):
    car_id = models.CharField(primary_key=True, max_length=8, default="")
    brand = models.CharField(max_length=20,default="")
    car_model = models.CharField(max_length=30,default="")
    gearType = models.CharField(max_length=30,default="")
    seat = models.CharField(max_length=30,default="")
    img = models.ImageField(upload_to='static/image/cars/', default="")
    price = models.FloatField(default=0.00)
    status = models.IntegerField(default=0)
    desc = models.CharField(max_length=800,default="")
    address = models.ForeignKey(Adress, on_delete=models.CASCADE, default=None)
    type_id = models.ForeignKey(CarType, on_delete=models.CASCADE, default=None)
    provinces = models.ForeignKey(Provinces, on_delete=models.CASCADE, default=None)
    own_id = models.ForeignKey(Owner, on_delete=models.CASCADE, default=None)
    def getStatus(self):
        if self.status == 0:
            return 'ว่าง'
        elif self.status == 1:
            return 'ไม่ว่าง'
        elif self.status == 2:
            return 'ไม่พร้อมใช้งาน'

    def gettotal(self):
        total = Rent.objects.filter(car=self).aggregate(total=Sum(F('price')*F('amount')))
        # return count['count']
        return total['total']




class Rent(models.Model):
    rent_id = models.CharField(primary_key=True, max_length=13, default="")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=None)
    rent_date = models.DateField(blank=True, default='', null=True)
    return_date = models.DateField(blank=True, default='', null=True)
    amount = models.IntegerField(default=0)
    status = models.CharField(max_length=3,default="")
    mem_id = models.ForeignKey(Member, on_delete=models.CASCADE, default=None)
    own_id = models.ForeignKey(Owner,on_delete=models.CASCADE,default=None)
    price = models.FloatField(default=0.00)


    def newRentId(self):
        yy = str(datetime.date.today().strftime('%y'))
        mm = str(datetime.date.today().strftime('%m'))
        lastRent = Rent.objects.last()
        if lastRent:
            lastId = int(lastRent.rent_id[9:])
        else:
            lastId = 0
        id = str(lastId+1)
        id=id.zfill(6)
        newId  = "RN-"+ yy + mm + id
        self.rent_id = newId
        return newId

    def getStatus(self):
        if self.status == '1':
            return 'รอการยืนยัน'
        elif self.status == '2':
            return 'ยืนยันแล้ว **รอแจ้งชำระ**'
        elif self.status == '3':
            return 'ชำระแล้ว **รอยืนยันการชำระ**'
        elif self.status == '3.1':
            return 'ชำระแล้ว ยอดไม่ถูกต้องโปรดตรวจสอบแล้วแจ้งชำระใหม่!!'
        elif self.status == '4':
            return 'เรียบร้อยเข้ารับรถไปใช้ไปได้เลย'
        elif self.status == '5':
            return 'การเช่าเสร็จสิ้น'
        elif self.status == '6':
            return 'ยกเลิก'
        elif self.status == '7':
            return 'ปฎิเสธ'




    def getTotalrent(self):
        total = self.price*self.amount
        return total
    def getVat(self):
        vat = (self.price*self.amount)*0.07
        return vat
    def getAfterVat(self):
        after = (self.price*self.amount)-((self.price*self.amount)*0.07)
        return after


class Payment(models.Model):
    pay_id = models.CharField(max_length=13, default="")
    pay_total = models.FloatField(default=0.00)
    pay_date = models.DateField(blank=True, default='', null=True)
    slip_img = models.ImageField(upload_to='static/image/Slip/', default="")
    bank = models.ForeignKey(OwnBank,on_delete=models.CASCADE,default=None)
    rent_id = models.ForeignKey(Rent,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.pay_id+" : "+str(self.pay_total)






class Confirms(models.Model):
    rent_id = models.ForeignKey(Rent, on_delete=models.CASCADE, default=None)
    own = models.ForeignKey(Owner, on_delete=models.CASCADE, default=None)
    c_date = models.DateTimeField(auto_now_add = True)
    comment = models.CharField(max_length=200, default="",null=True,blank=True)

class Transfers(models.Model):
    rent_id = models.ForeignKey(Rent, on_delete=models.CASCADE, default=None)
    t_date = models.DateTimeField(auto_now_add = True)
    pay_num = models.CharField(max_length=35, default="")
    bank = models.ForeignKey(OwnBank,on_delete=models.CASCADE,default=None)
    slip = models.ImageField(upload_to ='static/bills/', default="")
    comment = models.CharField(max_length=200, default="",null=True,blank=True)

class Accepts(models.Model):
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE, default=None)
    own = models.ForeignKey(Owner, on_delete=models.CASCADE, default=None)
    a_date =models.DateTimeField(auto_now_add = True)
    comment = models.CharField(max_length=200, default="",null=True,blank=True)


class Cancel(models.Model):
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE, default=None)
    mem = models.ForeignKey(Member, on_delete=models.CASCADE, default=None)
    cdate = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=200, default="")

class Reject(models.Model):
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE, default=None)
    own = models.ForeignKey(Owner, on_delete=models.CASCADE, default=None)
    rdate = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=200, default="")

















