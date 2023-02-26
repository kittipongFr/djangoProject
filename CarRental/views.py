from django.db.models.functions import TruncDay, TruncMonth, TruncYear, TruncWeek, ExtractYear, ExtractDay, ExtractWeek, ExtractMonth
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
import calendar
import datetime

from django.urls import reverse

from CarRental.models import *
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger, )
import os
from django.db.models import Count
from django.db.models import Q, Subquery, OuterRef
from calendar import month_name
from django.contrib import messages
from django.contrib.auth.models import User
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def test(request):
    carType = CarType.objects.all().order_by('type_id')
    return render(request,'1.1/index.html',{"carType":carType})

def home(request):
    provinces = Provinces.objects.all().order_by('name_th')
    carType = CarType.objects.all().order_by('type_id')
    context = {"provinces": provinces,'carType':carType}
    return render(request, 'home.html', context)


@login_required
def Memberlist(request,pageNo):
    user_status = request.session['userStatus']
    if user_status == 'admin':
        mem = Member.objects.all()
        mem_page = Paginator(mem, 5)
        context = {'mem': mem_page.page(pageNo)}
        return render(request, 'backend/memberlist.html', context)
    else:
        return redirect('backend_index')

@login_required
def Member_add(request):
    user_status = request.session['userStatus']
    if user_status == 'admin':
        pv = Provinces.objects.all().order_by('name_th')
        if request.method == 'POST':
            mem_Id = request.POST['mem_id']
            vMem_id = Member.objects.filter(mem_id=mem_Id)
            if vMem_id:
                context = {'eror': True,'pv': pv}
                return render(request, 'backend/memberAdd.html', context)
            else:
                memId = request.POST['mem_id']
                name = request.POST['name']
                email = request.POST['email']
                tel = request.POST['tel']
                password = request.POST['tel']
                province = Provinces.objects.get(id=request.POST['province'])
                Member(mem_id=memId,name=name,email=email,tel=tel,provinces=province).save()
                user = User.objects.create_user(memId, email, password)
                user.first_name = name
                user.is_staff = False
                user.save()
                return redirect('Memberlist',pageNo = 1)
        else:
            context = {'pv':pv}
            return render(request, 'backend/memberAdd.html',context)
    else:
        return redirect('backend_index')


@login_required
def memberedit(request):
    user_status = request.session['userStatus']
    if user_status == 'member':
        provinces = Provinces.objects.all().order_by('name_th')
        mem = get_object_or_404(Member,mem_id = request.session['userId'])
        user = User.objects.get(username = request.session['userId'])
        if request.method == "POST":
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.first_name = request.POST['name']
            user.save(force_update=bool)
            # User.objects.filter(username='example').update(email='new_email@example.com')
            mem.mem_id = request.POST['username']
            mem.name = request.POST['name']
            mem.tel = request.POST['tel']
            mem.provinces = Provinces.objects.get(id=request.POST['province'])
            mem.save(force_update=bool)
            return redirect('home')
        else:
            context = {'mem':mem,'provinces':provinces}
            return render(request,'memEdit.html',context)
    else:
        return redirect('home')


@login_required
def memChangePassword(request):
    user_status = request.session['userStatus']
    if user_status == 'member':
        userId = request.session.get('userId')
        if request.method == 'POST':
            user = authenticate(username=userId, password=request.POST['oldPassword'])
            if user:
                if request.POST['newPassword'] == request.POST['confirmPassword']:
                    user.set_password(request.POST['newPassword'])

                    user.save()
                    success_message = 'เปลี่ยนรหัสผ่านใหม่เรียบร้อย'
                    return render(request, 'memChangePass.html', {'success': success_message})
                else:
                    error_message = 'รหัสผ่านใหม่กับรหัสที่ยืนยันไม่ตรงกัน'
                    return render(request, 'memChangePass.html', {'error': ''})
            else:
                error_message = 'รหัสผ่านเดิมไม่ถูกต้อง'
                return render(request, 'memChangePass.html', {'error0': error_message})
        else:
            return render(request, 'memChangePass.html')
    else:
        return redirect('home')














@login_required
def backend_index(request):
    user_status = request.session['userStatus']
    if user_status == 'owner':
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        last_Day = Rent.objects.filter(Q(rent_date=yesterday) & Q(own_id=request.session['userId'])).annotate(
            day=TruncDay('rent_date')).values('day').annotate(count=Count('rent_id')).annotate(
            total=Sum(F('price') * F('amount'))).order_by('day')
        car = Car.objects.filter(own_id=request.session['userId'])
        reportDay = Rent.objects.filter(Q(rent_date=datetime.date.today()) & Q(own_id=request.session['userId'])).annotate(
            day=TruncDay('rent_date')).values('day').annotate(count=Count('rent_id')).annotate(total=Sum(F('price') * F('amount'))).order_by('day')
        list_rent = Rent.objects.filter(Q(rent_date=datetime.date.today()) & Q(own_id=request.session['userId'])).filter(status__in='1,2,3,4,5')
        countRent = Rent.objects.filter(Q(own_id=request.session['userId']),
                            Q(status='1') | Q(status='2') | Q(status='3') | Q(status='4')).annotate(count=Count('rent_id'))
        this_year = timezone.now().year
        sales_by_month = Rent.objects.filter(Q(own_id=request.session['userId']) & Q(rent_date__year=this_year)).annotate(
            month=ExtractMonth('rent_date')
        ).values('month').annotate(
            total=Sum(F('price') * F('amount'))
        ).order_by('month')

        x = [month_name[sale['month']] for sale in sales_by_month]
        y = [sale['total'] for sale in sales_by_month]

        ##percent DAY
        amount_today = Rent.objects.filter(Q(own_id=request.session['userId']) & Q(rent_date=datetime.date.today())).aggregate(
            total_today=models.Sum(F('price') * F('amount')))['total_today'] or 0
        amount_yesterday = Rent.objects.filter(Q(own_id=request.session['userId']) & Q(rent_date=yesterday)).aggregate(
            total_yesterday=models.Sum(F('price') * F('amount')))['total_yesterday'] or 0

        if amount_today != 0:
            if amount_yesterday != 0:
                per = ((amount_today - amount_yesterday) / amount_yesterday) * 100

                p = '{:.2f}'.format(per)
                if amount_today > amount_yesterday:

                    percent = "+" + str(p) + "%"
                else:

                    percent = str(p) + "%"
            else:
                percent = "+100%"
        else:
            if amount_yesterday != 0:

                per = ((amount_today - amount_yesterday) / amount_yesterday) * 100
                p = '{:.2f}'.format(per)
                if amount_today > amount_yesterday:

                    percent = "+" + str(p) + "%"
                else:
                    percent = str(p) + "%"
            else:
                percent = "+0%"
        ##percent MONTH
        today = datetime.date.today()
        first_day_of_month = today.replace(day=1)
        last_day_of_previous_month = first_day_of_month - datetime.timedelta(days=1)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
        this_month_data = Rent.objects.filter(
            Q(own_id=request.session['userId']) & Q(rent_date__gte=first_day_of_month, rent_date__lte=today))
        last_month_data = Rent.objects.filter(
            Q(own_id=request.session['userId']) & Q(rent_date__gte=first_day_of_previous_month,
                                                    rent_date__lte=last_day_of_previous_month))
        this_month_total = this_month_data.aggregate(total_month=models.Sum(F('price') * F('amount')))['total_month'] or 0
        last_month_total = last_month_data.aggregate(total_lmonth=models.Sum(F('price') * F('amount')))['total_lmonth'] or 0
        if this_month_total != 0:
            if last_month_total != 0:
                d = (this_month_total / last_month_total) * 100
                df = '{:.2f}'.format(d)
                if this_month_total > last_month_total:
                    percentM = "+" + str(df) + "%"
                else:
                    percentM = str(df) + "%"
            else:
                percentM = "+100%"
        else:
            if last_month_total != 0:
                d = (this_month_total - last_month_total) / last_month_total * 100
                df = '{:.2f}'.format(d)
                if this_month_total > last_month_total:
                    percentM = "+" + str(df) + "%"
                else:
                    percentM = str(df) + "%"

            else:
                percentM = "+0%"

        ##percent YEAR
        todays = datetime.date.today()
        start_of_this_year = todays.replace(month=1, day=1)
        start_of_last_year = start_of_this_year - datetime.timedelta(days=365)
        this_year_data = Rent.objects.filter(
            Q(own_id=request.session['userId']) & Q(rent_date__gte=start_of_this_year, rent_date__lte=todays))
        last_year_data = Rent.objects.filter(Q(own_id=request.session['userId']) & Q(rent_date__gte=start_of_last_year,rent_date__lte=start_of_this_year - datetime.timedelta(days=1)))
        this_year_total = this_year_data.aggregate(thisYtotal=Sum(F('price') * F('amount')))['thisYtotal'] or 0
        last_year_total = last_year_data.aggregate(lastYtotal=Sum(F('price') * F('amount')))['lastYtotal'] or 0
        if this_year_total != 0:
            if last_year_total != 0:
                dn = (this_year_total - last_year_total) / last_year_total * 100
                dff = '{:.2f}'.format(dn)
                if this_year_total > last_year_total:
                    percentY = "+" + str(dff) + "%"
                else:
                    percentY = str(dff) + "%"
            else:
                percentY = "+100%"
        else:
            if last_year_total != 0:
                dn = (this_year_total - last_year_total) / last_year_total * 100
                dff = '{:.2f}'.format(dn)
                if this_year_total > last_year_total:
                    percentY = "+" + str(dff) + "%"
                else:
                    percentY = str(dff) + "%"
            else:
                percentY = "+0%"
        context = {'car': car, 'list_rent': list_rent, 'reportDay': reportDay, 'lastDay': last_Day, 'percent': percent,
                   'this_month_total': this_month_total,'countRent':countRent
            , 'this_year_total': this_year_total, 'percentY': percentY, 'percentM': percentM, 'x': x, 'y': y}
        return render(request, 'backend/index.html', context)
    elif user_status == "admin":
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        last_Day = Rent.objects.filter(Q(rent_date=yesterday) ).annotate(
            day=TruncDay('rent_date')).values('day').annotate(count=Count('rent_id')).annotate(
            total=Sum(F('price') * F('amount'))).order_by('day')
        car = Car.objects.all()
        reportDay = Rent.objects.filter(
            Q(rent_date=datetime.date.today()) ).annotate(
            day=TruncDay('rent_date')).values('day').annotate(count=Count('rent_id')).annotate(
            total=Sum(F('price') * F('amount'))).order_by('day')
        list_rent = Rent.objects.filter(Q(rent_date=datetime.date.today()))
        countRent = Rent.objects.filter(
                                        Q(status='1') | Q(status='2') | Q(status='3') | Q(status='4')).annotate(
            count=Count('rent_id'))

        #
        this_year = timezone.now().year
        sales_by_month = Rent.objects.filter(
           Q(rent_date__year=this_year)).annotate(
            month=ExtractMonth('rent_date')
        ).values('month').annotate(
            total=Sum(F('price') * F('amount'))
        ).order_by('month')

        x = [month_name[sale['month']] for sale in sales_by_month]
        y = [sale['total'] for sale in sales_by_month]

        ##percent DAY
        amount_today = \
            Rent.objects.filter( Q(rent_date=datetime.date.today())).aggregate(
                total_today=models.Sum(F('price') * F('amount')))['total_today'] or 0
        amount_yesterday = Rent.objects.filter(  Q(rent_date=yesterday)).aggregate(
            total_yesterday=models.Sum(F('price') * F('amount')))['total_yesterday'] or 0

        if amount_today != 0:
            if amount_yesterday != 0:
                per = ((amount_today - amount_yesterday) / amount_yesterday) * 100
                p = '{:.2f}'.format(per)
                if amount_today > amount_yesterday:

                    percent = "+" + str(p) + "%"
                else:

                    percent = str(p) + "%"
            else:
                percent = "+100%"
        else:
            if amount_yesterday != 0:
                per = ((amount_today - amount_yesterday) / amount_yesterday) * 100
                p = '{:.2f}'.format(per)
                if amount_today > amount_yesterday:

                    percent = "+" + str(p) + "%"
                else:

                    percent = str(p) + "%"
            else:
                percent = "+0%"

        ##percent MONTH
        today = datetime.date.today()
        first_day_of_month = today.replace(day=1)
        last_day_of_previous_month = first_day_of_month - datetime.timedelta(days=1)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
        this_month_data = Rent.objects.filter(
             Q(rent_date__gte=first_day_of_month, rent_date__lte=today))
        last_month_data = Rent.objects.filter(
            Q(rent_date__gte=first_day_of_previous_month,
                                                    rent_date__lte=last_day_of_previous_month))
        this_month_total = this_month_data.aggregate(total_month=models.Sum(F('price') * F('amount')))[
                               'total_month'] or 0
        last_month_total = last_month_data.aggregate(total_lmonth=models.Sum(F('price') * F('amount')))[
                               'total_lmonth'] or 0
        if this_month_total != 0:
            if last_month_total != 0:
                d = (this_month_total - last_month_total) / last_month_total * 100
                df = '{:.2f}'.format(d)
                if this_month_total > last_month_total:
                    percentM = "+" + str(df) + "%"
                else:
                    percentM = str(df) + "%"
            else:
                percentM = "+100%"
        else:
            if last_month_total != 0:
                d = (this_month_total - last_month_total) / last_month_total * 100
                df = '{:.2f}'.format(d)
                if this_month_total > last_month_total:
                    percentM = "+" + str(df) + "%"
                else:
                    percentM = str(df) + "%"

            else:
                percentM = "+0%"

        ##percent YEAR
        todays = datetime.date.today()
        start_of_this_year = todays.replace(month=1, day=1)
        start_of_last_year = start_of_this_year - datetime.timedelta(days=365)
        this_year_data = Rent.objects.filter(
              Q(rent_date__gte=start_of_this_year, rent_date__lte=todays))
        last_year_data = Rent.objects.filter( Q(rent_date__gte=start_of_last_year,rent_date__lte=start_of_this_year - datetime.timedelta(
                                                                                         days=1)))
        this_year_total = this_year_data.aggregate(thisYtotal=Sum(F('price') * F('amount')))['thisYtotal'] or 0
        last_year_total = last_year_data.aggregate(lastYtotal=Sum(F('price') * F('amount')))['lastYtotal'] or 0
        if this_year_total != 0:
            if last_year_total != 0:
                dn = (this_year_total - last_year_total) / last_year_total * 100
                dff = '{:.2f}'.format(dn)
                if this_year_total > last_year_total:
                    percentY = "+" + str(dff) + "%"
                else:
                    percentY = str(dff) + "%"
            else:
                percentY = "+100%"
        else:
            if last_year_total != 0:
                dn = (this_year_total - last_year_total) / last_year_total * 100
                dff = '{:.2f}'.format(dn)
                if this_year_total > last_year_total:
                    percentY = "+" + str(dff) + "%"
                else:
                    percentY = str(dff) + "%"
            else:
                percentY = "+0%"
        context = {'car': car, 'list_rent': list_rent, 'reportDay': reportDay, 'lastDay': last_Day, 'percent': percent,
                   'this_month_total': this_month_total, 'countRent': countRent
            , 'this_year_total': this_year_total, 'percentY': percentY, 'percentM': percentM, 'x': x, 'y': y}
        return render(request, 'backend/index.html', context)

    else:
        return redirect('home')

@login_required
def reportQD(request):
    user_status = request.session['userStatus']
    if user_status == 'owner':
        day = request.GET.get('day')
        if request.method == 'GET':
            if day != '':
                reportDay = Rent.objects.filter(
                    Q(rent_date=day) & Q(own_id=request.session['userId'])).annotate(
                    date=TruncDay('rent_date')).values('date').annotate(count=Count('rent_id')).annotate(
                    total=Sum(F('price') * F('amount'))).order_by('date')
                list_rent = Rent.objects.filter(Q(rent_date=day) & (Q(own_id=request.session['userId'])))
                context = {'reportDay': reportDay, 'list_rent': list_rent}
                return render(request, 'backend/reportQ.html', context)
            else:
                return redirect('backend_index')
        else:
            return redirect('backend_index')
    elif user_status == 'admin':
        day = request.GET.get('day')
        if request.method == 'GET':
            if day != '':
                reportDay = Rent.objects.filter(
                    Q(rent_date=day)).annotate(
                    date=TruncDay('rent_date')).values('date').annotate(count=Count('rent_id')).annotate(
                    total=Sum(F('price') * F('amount'))).order_by('date')
                list_rent = Rent.objects.filter(Q(rent_date=day) )
                context = {'reportDay': reportDay, 'list_rent': list_rent}
                return render(request, 'backend/reportQ.html', context)
            else:
                return redirect('backend_index')
        else:
            return redirect('backend_index')

    else:
        return redirect('home')

@login_required
def reportQY(request):
    user_status = request.session['userStatus']
    if user_status == 'owner':
        years = request.GET.get('year')
        if request.method == 'GET':
            if years != '':

                reportDay = Rent.objects.filter(
                    Q(rent_date__year=years) & Q(own_id=request.session['userId'])).annotate(
                    date=ExtractYear('rent_date')).values('date').annotate(count=Count('rent_id')).annotate(
                    total=Sum(F('price') * F('amount'))).order_by('date')
                list_rent = Rent.objects.filter(Q(rent_date__year=years) & Q(own_id=request.session['userId']))
                context = {'reportDay': reportDay, 'list_rent': list_rent}
                return render(request, 'backend/reportQ.html', context)
            else:
                return redirect('backend_index')
        else:
            return redirect('backend_index')
    elif user_status == 'admin':
        years = request.GET.get('year')
        if request.method == 'GET':
            if years != '':

                reportDay = Rent.objects.filter(
                    Q(rent_date__year=years) ).annotate(
                    date=ExtractYear('rent_date')).values('date').annotate(count=Count('rent_id')).annotate(
                    total=Sum(F('price') * F('amount'))).order_by('date')
                list_rent = Rent.objects.filter(Q(rent_date__year=years) )
                context = {'reportDay': reportDay, 'list_rent': list_rent}
                return render(request, 'backend/reportQ.html', context)
            else:
                return redirect('backend_index')
        else:
            return redirect('backend_index')

    else:
        return redirect('home')

@login_required
def reportQM(request):
    user_status = request.session['userStatus']
    if user_status == 'owner':
        months = request.GET.get('month')
        if request.method == 'GET':
            if months != '':
                year, month = months.split('-')
                y = int(year)
                m = str(month)
                reportDay = Rent.objects.filter(
                    Q(rent_date__year=y) & Q(rent_date__month=m) & Q(own_id=request.session['userId'])).annotate(
                    date=TruncMonth('rent_date')).values('date').annotate(count=Count('rent_id')).annotate(
                    total=Sum(F('price') * F('amount'))).order_by('date')
                list_rent = Rent.objects.filter(
                    Q(rent_date__year=y) & Q(rent_date__month=m) & (Q(own_id=request.session['userId'])))
                context = {'reportDay': reportDay, 'list_rent': list_rent}
                return render(request, 'backend/reportQ.html', context)
            else:
                return redirect('backend_index')
        else:
            return redirect('backend_index')
    elif user_status == 'admin':
        months = request.GET.get('month')
        if request.method == 'GET':
            if months != '':
                year, month = months.split('-')
                y = int(year)
                m = str(month)
                reportDay = Rent.objects.filter(
                    Q(rent_date__year=y) & Q(rent_date__month=m)).annotate(
                    date=TruncMonth('rent_date')).values('date').annotate(count=Count('rent_id')).annotate(
                    total=Sum(F('price') * F('amount'))).order_by('date')
                list_rent = Rent.objects.filter(
                    Q(rent_date__year=y) & Q(rent_date__month=m) )
                context = {'reportDay': reportDay, 'list_rent': list_rent}
                return render(request, 'backend/reportQ.html', context)
            else:
                return redirect('backend_index')
        else:
            return redirect('backend_index')

    else:
        return redirect('home')

@login_required
def backend_Rent(request, pageNo):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        rent = Rent.objects.filter(Q(own_id=request.session['userId']),
                                   Q(status='1') | Q(status='2') | Q(status='3') | Q(status='4')).order_by('-rent_date')
        rent_page = Paginator(rent, 5)
        context = {'rent': rent_page.page(pageNo)}
        return render(request, 'backend/billRent.html', context)
    else:
        return redirect('home')

@login_required
def backend_RentHistory(request, pageNo):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        rent = Rent.objects.filter(Q(own_id=request.session['userId']),
                                   Q(status='5') | Q(status='6') | Q(status='7')).order_by('-rent_date')
        rent_page = Paginator(rent, 5)
        context = {'rent': rent_page.page(pageNo)}
        return render(request, 'backend/RentHistory.html', context)
    else:
        return redirect('home')

@login_required
def backend_Cartype(request, pageNo):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        types = CarType.objects.all().order_by('type_id')
        type_page = Paginator(types, 5)
        context = {'type': type_page.page(pageNo)}
        return render(request, 'backend/carType.html', context)
    else:
        return redirect('home')


@login_required
def backend_Car(request, pageNo):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        car = Car.objects.all().filter(own_id=request.session['userId']).order_by('-car_id')
        car_page = Paginator(car, 5)
        context = {'car': car_page.page(pageNo)}
        return render(request, 'backend/car.html', context)
    else:
        return redirect('home')


@login_required
def backend_Car_add(request):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':

        types = CarType.objects.all()
        provinces = Provinces.objects.all().order_by('name_th')
        add = Adress.objects.filter(own_id=request.session['userId'])
        if request.method == 'POST':
            cid = request.POST.get("id")
            vCar_id = Car.objects.filter(car_id=cid)
            if vCar_id:
                context = {'eror': True, 'types': types, 'provinces': provinces,'add':add}
                return render(request, 'backend/carAdd.html', context)
            else:
                car_id = request.POST['id']
                brand = request.POST['brand']
                model = request.POST['model']
                gear = request.POST['gear']
                seat = request.POST['seat']
                desc = request.POST['desc']
                address = Adress.objects.get(id=request.POST.get('add'))
                type = CarType.objects.get(type_id=request.POST.get('type'))
                price = request.POST['price']
                province = Provinces.objects.get(id=request.POST.get('province'))
                own = Owner.objects.get(own_id=request.POST.get('own'))
                image = request.FILES.get('img')
                Car(car_id=car_id, brand=brand, car_model=model, type_id=type, price=price, provinces=province,
                    own_id=own, gearType=gear, seat=seat, img=image,desc=desc,address=address).save()
                imgpath = image.name
                point = imgpath.rfind('.')
                ext = imgpath[point:]
                imgNames = imgpath.split('/')
                imgName = imgNames[len(imgNames) - 1]
                newImg = car_id + "_" + str(datetime.date.today()) + ext

                car = get_object_or_404(Car, car_id=car_id)
                car.img = 'static/image/cars/' + newImg
                car.save()
                if os.path.exists('static/image/cars/' + newImg):
                    os.remove('static/image/cars/' + newImg)  # file exits, delete it
                os.rename('static/image/cars/' + imgName, 'static/image/cars/' + newImg)
                return redirect('backend_Car', pageNo=1)
        else:
            context = {'types': types, 'provinces': provinces,'add':add}
            return render(request, 'backend/carAdd.html', context)
    else:
        return redirect('home')


@login_required
def backend_Car_edit(request, car_id):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        car = get_object_or_404(Car, car_id=car_id)
        types = CarType.objects.all()
        provinces = Provinces.objects.all().order_by('name_th')
        add = Adress.objects.filter(own_id=request.session['userId'])
        if request.method == 'POST':
            car.brand = request.POST['brand']
            car.car_model = request.POST['model']
            car.seat = request.POST['seat']
            car.gearType = request.POST['gear']
            car.type_id = CarType.objects.get(type_id=request.POST.get('type'))
            car.price = request.POST['price']
            car.address = Adress.objects.get(id=request.POST['add'])
            car.provinces = Provinces.objects.get(id=request.POST.get('province'))
            car.own = Owner.objects.get(own_id=request.POST.get('own'))
            car.desc = request.POST['desc']
            if request.FILES.get('img') is None:
                img = car.img
            else:
                img = request.FILES.get('img')
            car.img = img
            car.save(force_update=bool)
            if request.FILES.get('img') == img:
                imgpath = img.name
                point = imgpath.rfind('.')
                ext = imgpath[point:]
                imgNames = imgpath.split('/')
                imgName = imgNames[len(imgNames) - 1]
                newImg = car_id + "_" + str(datetime.date.today()) + ext
                car = get_object_or_404(Car, car_id=car_id)
                car.img = 'static/image/cars/' + newImg
                car.save()
                if os.path.exists('static/image/cars/' + newImg):
                    os.remove('static/image/cars/' + newImg)  # file exits, delete it
                os.rename('static/image/cars/' + imgName, 'static/image/cars/' + newImg)
            return redirect('backend_Car', pageNo=1)
        else:
            # return render(request,'')
            context = {'types': types, 'provinces': provinces, 'car': car,'add':add}
            return render(request, 'backend/carEdit.html', context)
    else:
        return redirect('home')


@login_required
def backend_Car_delete(request, car_id):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        car = get_object_or_404(Car, car_id=car_id)
        img = car.img.name  # รูปสินค้าเดิม
        if request.method == 'POST':
            car.delete()
            # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
            # ใน table db เก็บ /products/xxx.xx
            if os.path.exists(img):  # file exits, delete it
                os.remove(img)
            return redirect('backend_Car', pageNo=1)
        else:
            context = {'car': car}
            return render(request, 'backend/carDelete.html', context)
    else:
        return redirect('home')


@login_required
def backend_Type_add(request):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        if request.method == 'POST':
            tid = request.POST.get("id")
            v_type = CarType.objects.filter(type_id=tid)
            if v_type:
                context = {'eror': True}
                return render(request, 'backend/typeAdd.html', context)
            tname = request.POST.get("type")
            v_typename = CarType.objects.filter(type_name=tname)
            if v_typename:
                context = {'eror1': True}
                return render(request, 'backend/typeAdd.html', context)
            else:
                type_id = request.POST['id']
                type_name = request.POST['type']
                image = request.FILES.get('img')
                CarType(type_id=type_id, type_name=type_name, picture=image).save()
                imgpath = image.name
                point = imgpath.rfind('.')
                ext = imgpath[point:]
                imgNames = imgpath.split('/')
                imgName = imgNames[len(imgNames) - 1]
                newImg = type_id + "_" + str(datetime.date.today()) + ext

                types = get_object_or_404(CarType, type_id=type_id)
                types.picture = 'static/image/types/' + newImg
                types.save()
                if os.path.exists('static/image/types/' + newImg):
                    os.remove('static/image/types/' + newImg)  # file exits, delete it
                os.rename('static/image/types/' + imgName, 'static/image/types/' + newImg)
                return redirect('backend_Cartype', pageNo=1)
        else:
            return render(request, 'backend/typeAdd.html')
    else:
        return redirect('home')


@login_required
def backend_Type_edit(request, type_id):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        type = get_object_or_404(CarType, type_id=type_id)
        if request.method == 'POST':
            if request.FILES.get('img') is None:
                img = type.picture
            else:
                img = request.FILES.get('img')
            type.type_name = request.POST.get("type")
            type.picture = img
            type.save(force_update=bool)
            if request.FILES.get('img') == img:
                imgpath = img.name
                point = imgpath.rfind('.')
                ext = imgpath[point:]
                imgNames = imgpath.split('/')
                imgName = imgNames[len(imgNames) - 1]
                newImg = type_id + "_" + str(datetime.date.today()) + ext
                type = get_object_or_404(CarType, type_id=type_id)
                type.picture = 'static/image/types/' + newImg
                type.save()
                if os.path.exists('static/image/types/' + newImg):
                    os.remove('static/image/types/' + newImg)  # file exits, delete it
                os.rename('static/image/types/' + imgName, 'static/image/types/' + newImg)
            return redirect('backend_Cartype', pageNo=1)
        else:
            # return render(request,'')
            context = {'type': type}
            return render(request, 'backend/typeEdit.html', context)
    else:
        return redirect('home')


@login_required
def backend_Type_delete(request, type_id):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        type = get_object_or_404(CarType, type_id=type_id)
        img = type.picture.name  # รูปสินค้าเดิม
        if request.method == 'POST':
            type.delete()
            # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
            # ใน table db เก็บ /products/xxx.xx
            if os.path.exists(img):  # file exits, delete it
                os.remove(img)
            return redirect('backend_Cartype', pageNo=1)
        else:
            context = {'type': type}
            return render(request, 'backend/typeDelete.html', context)
    else:
        return redirect('home')



def Owner_Register(request):
    province = Provinces.objects.all().order_by('name_th')
    if request.method == 'POST':
        oid = request.POST.get("id")
        v_own = Owner.objects.filter(own_id=oid)
        own_email = request.POST.get("email")
        user = User.objects.filter(username=oid)
        v_email = Owner.objects.filter(email=own_email)
        if v_own or user:
            context = {'eror': True, 'province': province}
            return render(request, 'signUpOwn.html', context)
        elif v_email:
            context = {'eror1': True, 'province': province}
            return render(request, 'signUpOwn.html', context)
        else:
            own_id = request.POST['id']
            email = request.POST['email']
            password = request.POST['password']
            tel = request.POST['tel']
            name = request.POST['name']
            address = request.POST['address']
            provinces = Provinces.objects.get(id=request.POST.get('province'))
            bday = request.POST['bday']
            Owner(own_id=own_id, email=email, tel=tel, name=name, address=address,
                  provinces=provinces, birthdate=bday).save()
            user = User.objects.create_user(own_id, email, password)
            user.first_name = name
            user.is_staff = True
            user.save()
        return redirect('backend_index')
    else:
        context = {'province': province}
        return render(request, 'signUpOwn.html', context)



def Member_Register(request):
    province = Provinces.objects.all().order_by('name_th')
    if request.method == 'POST':
        mid = request.POST.get("id")
        v_mem = Member.objects.filter(mem_id=mid)
        user = User.objects.filter(username=mid)
        mem_email = request.POST.get("email")
        v_email = Member.objects.filter(email=mem_email)
        if v_mem or user:
            context = {'eror': True, 'province': province}
            return render(request, 'signUpMem.html', context)
        elif v_email:
            context = {'eror1': True, 'province': province}
            return render(request, 'signUpMem.html', context)
        else:
            m_id = request.POST['id']
            email = request.POST['email']
            password = request.POST['password']
            tel = request.POST['tel']
            name = request.POST['name']
            provinces = Provinces.objects.get(id=request.POST.get('province'))
            Member(mem_id=m_id, email=email, tel=tel, name=name, provinces=provinces).save()
            user = User.objects.create_user(m_id, email, password)
            user.first_name = name
            user.is_staff = False
            user.save()
            return redirect('signIn')
    else:
        context = {'province': province}
        return render(request, 'signUpMem.html', context)



def userSignin(request):
    if request.method == 'POST':
        userName = request.POST.get("userName")
        userPass = request.POST.get("userPass")
        user = authenticate(request, username=userName, password=userPass)
        if user is not None:
            login(request, user)

            if user.is_staff == 1 and user.is_superuser == 1:
                user = User.objects.filter(username=userName).first()
                request.session['userId'] = user.username
                request.session['userName'] = user.first_name
                request.session['userStatus'] = 'admin'
                return redirect('home')
            elif user.is_staff == 1 and user.is_superuser == 0:
                own = Owner.objects.filter(own_id=userName).first()
                request.session['userId'] = own.own_id
                request.session['userName'] = own.name
                request.session['userStatus'] = 'owner'
                return redirect('backend_index')
            else:
                mem = Member.objects.filter(mem_id=userName).first()
                request.session['userId'] = mem.mem_id
                request.session['userName'] = mem.name
                request.session['userStatus'] = 'member'
                return redirect('home')
        else:
            error_message = 'Invalid login credentials. Please try again.'
            return render(request, 'signIn.html', {'error_message': error_message})
    else:
        data = {'userName': '', 'eror0': True}
        return render(request, 'signIn.html', data)


@login_required
def userLogout(request):
    del request.session["userId"]
    del request.session["userName"]
    del request.session["userStatus"]
    logout(request)
    return redirect('home')


@login_required
def bankOwn_add(request):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        banks = Bank.objects.all()
        if request.method == 'POST':
            bank_num = request.POST.get("b_num")
            Vbank = OwnBank.objects.filter(bank_num=bank_num)
            if Vbank:
                context = {'eror': True, 'bank': banks}
                return render(request, 'backend/bankAdd.html', context)
            else:
                name = request.POST['name']
                b_num = request.POST['b_num']
                branch = request.POST['branch']
                bank = Bank.objects.get(id=request.POST.get('bank'))
                oid = Owner.objects.get(own_id=request.POST.get('oid'))
                OwnBank(bank_num=b_num, branch=branch, bank_id=bank, own_id=oid, name=name).save()
            return redirect('backend_Bank', pageNo=1)
        else:
            context = {'bank': banks}
            return render(request, 'backend/bankAdd.html', context)
    else:
        return redirect('home')


@login_required
def backend_Bank(request, pageNo):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        bank = OwnBank.objects.all().filter(own_id=request.session['userId'])
        bank_page = Paginator(bank, 5)
        context = {'bank': bank_page.page(pageNo)}
        return render(request, 'backend/bank.html', context)
    else:
        return redirect('home')


@login_required
def backend_Bank_edit(request, id):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        bank = get_object_or_404(OwnBank, id=id)
        bankall = Bank.objects.all()
        if request.method == 'POST':
            bank.bank_num = request.POST['b_num']
            bank.name = request.POST['name']
            bank.branch = request.POST['branch']
            bank.bank_id = Bank.objects.get(id=request.POST.get('bank'))
            bank.own_id = Owner.objects.get(own_id=request.POST.get('oid'))
            bank.save(force_update=bool)
            return redirect('backend_Bank', pageNo=1)
        else:
            context = {'bank': bank, 'banks': bankall}
            return render(request, 'backend/bankEdit.html', context)
    else:
        return redirect('home')


@login_required
def backend_Bank_delete(request, id):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        bank = get_object_or_404(OwnBank, id=id)
        if request.method == 'POST':
            bank.delete()
            # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
            # ใน table db เก็บ /products/xxx.xx
            return redirect('backend_Bank', pageNo=1)
        else:
            context = {'bank': bank}
            return render(request, 'backend/bankdelete.html', context)
    else:
        return redirect('home')


@login_required
def backend_RentDetails(request, rent_id):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        rents = get_object_or_404(Rent, rent_id=rent_id)
        context = {'rents': rents}
        return render(request, 'backend/rentDetail.html', context)
    else:
        return redirect('home')


@login_required
def backend_RentHistoryDetails(request, rent_id):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        rents = get_object_or_404(Rent, rent_id=rent_id)
        context = {'rents': rents}
        return render(request, 'backend/RentHistoryDetail.html', context)
    else:
        return redirect('home')


@login_required
def rentConfirm(request, rent_id, car_id):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        rent = get_object_or_404(Rent, rent_id=rent_id)
        car = Car.objects.get(car_id=car_id)
        own = get_object_or_404(Owner, own_id=request.session.get('userId'))
        confirm = Confirms()
        confirm.rent_id = rent
        confirm.own = own
        confirm.save()
        rent.status = '2'
        rent.save()
        car.status = 1
        car.save()
        return redirect('backend_RentDetails', rent_id=rent_id)
    else:
        return redirect('home')


@login_required
def rentReject(request, rent_id,car_id):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        rent = get_object_or_404(Rent, rent_id=rent_id)
        car = get_object_or_404(Car, car_id=car_id)
        own = get_object_or_404(Owner, own_id=request.session.get("userId"))
        if request.method == 'POST':
            comment = request.POST['comment']
            reject = Reject()
            reject.rent = rent
            reject.own = own
            reject.comment = comment
            reject.save()
            rent.status = "7"
            rent.save()
            car.status = 0
            car.save()
            return redirect('backend_RentDetails', rent_id=rent.rent_id)
        else:
            context = {'rent': rent, 'list': list}
            return render(request, 'backend/Reject.html', context)
    else:
        return redirect('home')


@login_required
def backend_Accepts(request, rent_id):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        rents = get_object_or_404(Rent, rent_id=rent_id)
        own = get_object_or_404(Owner, own_id=request.session.get('userId'))
        # if Payment.DoesNotExist:
        pays = Payment.objects.filter(rent_id=rent_id)
        if request.method == 'POST':
            accept = Accepts()
            accept.rent = rents
            accept.own = own
            accept.save()
            rents.status = "4"
            rents.save()
            return redirect('backend_RentDetails', rent_id=rents.rent_id)
        else:
            context = {'rents': rents, 'pays': pays}
            return render(request, 'backend/Accepts.html', context)
    else:
        return redirect('home')
    # else:
    #     context = {'rents': rents}
    #     return render(request, 'backend/Accepts.html', context)


@login_required
def incompleteTransfer(request, rent_id):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        rent = get_object_or_404(Rent, rent_id=rent_id)
        rent.status = '3.1'
        rent.save()
        return redirect('backend_RentDetails', rent_id=rent_id)
    else:
        return redirect('home')


@login_required
def rentSuccess(request, rent_id, car_id):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        rent = get_object_or_404(Rent, rent_id=rent_id)
        car = Car.objects.get(car_id=car_id)
        rent.status = '5'
        rent.save()
        car.status = 0
        car.save()
        return redirect('backend_RentDetails', rent_id=rent_id)
    else:
        return redirect('home')


# import  requests,json
# def sendNotify(message):
#     url = "https://notify-api.line.me/api/notify"
#     LINE_ACCESS_TOKEN = "EeaOnlRFpgRVebZlSA9XQli2Qlc4mk0jJgsZVCAIhkv"  # token from your line notify web
#     LINE_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded', "Authorization": "Bearer " + LINE_ACCESS_TOKEN}
#     return requests.post(url, headers=LINE_HEADERS, data=message)
#
# def sendLineMessage(request):
#     sMessage = "Django Message for You"  # ข้อความที่ต้องการส่ง
#     sendNotify(sMessage)
#     messages.add_message(request, messages.INFO, "Send Message to Line Notify was Successfully.")
#     return redirect('home')

@login_required
def pdfReceipt(request, rent_id):
    pdfmetrics.registerFont(TTFont('THSarabunNew', 'thsarabunnew-webfont.ttf'))
    # pdfmetrics.registerFont(TTFont('THSarabunNew-Bold', 'thsarabunnew_bold-webfont.ttf'))
    template = get_template('pdfReceipt.html')
    rent = Rent.objects.filter(rent_id=rent_id).first()
    pay = Payment.objects.filter(rent_id=rent_id).first()
    context = {"rent": rent, 'pay': pay}
    html = template.render(context)
    response = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("<h1><b>เกิดข้อผิดพลาด!!!</b> ไม่สามารถสร้างเอกสาร PDF ได้...</h2>", status=400)


# @login_required
# def gg(request):
#     day = request.GET.get('day')
#     if request.method == 'GET':
#         if day != '':
#             reportDay = Rent.objects.filter(
#                 Q(rent_date=day) & Q(own_id=request.session['userId'])).annotate(
#                 date=TruncDay('rent_date')).values('date').annotate(count=Count('rent_id')).annotate(
#                 total=Sum(F('price') * F('amount'))).order_by('date')
#             list_rent = Rent.objects.filter(Q(rent_date=day) & (Q(own_id=request.session['userId'])))
#             context = {'reportDay': reportDay, 'list_rent': list_rent}
#             return render(request, 'backend/reportQ.html', context)
#         else:
#             return redirect('backend_index')
#     else:
#         return redirect('backend_index')


@login_required
def showCarAll(request):
    today = str(datetime.date.today())
    rental_start_date = request.POST.get('rc_date')
    rental_end_date = request.POST.get('rt_date')
    pv = request.POST.get('provinces')
    type = request.POST.get('type')
    price = request.POST.get('price')
    if request.method == 'POST':
        if today > rental_start_date:
            return redirect('home')
        elif rental_end_date >= rental_start_date:
            # if request.POST.get('type') == "0":
            request.session['rent_date'] = rental_start_date
            request.session['return_date'] = rental_end_date
            request.session['province'] = pv
            if price:
                request.session['price'] = price
            else:
                price = "0-10000"
                request.session['price'] = "0-10000"
            if type:
                request.session['type'] = type
            else:
                type = "0"
                request.session['type'] = "0"
            if type != "0" and price != "0-10000":
                mnP,mxP = price.split('-')
                province_one = Provinces.objects.all().filter(id=pv).first()
                type_one = CarType.objects.filter(type_id=type).first()
                overlapping_rentals = Rent.objects.filter(
                    Q(rent_date__lte=rental_end_date) & Q(return_date__gte=rental_start_date)
                ).exclude(Q(status='5') | Q(status='6') | Q(status='7')).values('car_id')
                cars = Car.objects.exclude(
                    car_id__in=overlapping_rentals.values('car_id')
                ).filter(Q(provinces=pv) & Q(type_id=type) & Q(price__range=(mnP,mxP))).order_by('type_id')
                provinces = Provinces.objects.all().order_by('name_th')
                carType = CarType.objects.all().order_by('type_id')

            elif type != "0":
                type_one = CarType.objects.filter(type_id=type).first()
                province_one = Provinces.objects.filter(id=pv).first()
                overlapping_rentals = Rent.objects.filter(
                    Q(rent_date__lte=rental_end_date) & Q(return_date__gte=rental_start_date)
                ).exclude(Q(status='5') | Q(status='6') | Q(status='7')).values('car_id')
                cars = Car.objects.exclude(
                    car_id__in=overlapping_rentals.values('car_id')
                ).filter(Q(provinces=pv) & Q(type_id=type)).order_by('type_id')
                provinces = Provinces.objects.all().order_by('name_th')
                carType = CarType.objects.all().order_by('type_id')
            elif price != '0-10000':
                mnP, mxP = price.split('-')
                type_one = CarType.objects.filter(type_id=type).first()
                province_one = Provinces.objects.filter(id=pv).first()
                overlapping_rentals = Rent.objects.filter(
                    Q(rent_date__lte=rental_end_date) & Q(return_date__gte=rental_start_date)
                ).exclude(Q(status='5') |  Q(status='6') | Q(status='7')).values('car_id')
                cars = Car.objects.exclude(
                    car_id__in=overlapping_rentals.values('car_id')
                ).filter(Q(provinces=pv) & Q(price__range=(mnP,mxP))).order_by('type_id')
                provinces = Provinces.objects.all().order_by('name_th')
                carType = CarType.objects.all().order_by('type_id')

            else:
                province_one = Provinces.objects.all().filter(id=pv).first()
                type_one = CarType.objects.filter(type_id=type).first()
                overlapping_rentals = Rent.objects.filter(
                    Q(rent_date__lte=rental_end_date) & Q(return_date__gte=rental_start_date)
                ).exclude(Q(status='5') | Q(status='6')| Q(status='7')).values('car_id')
                cars = Car.objects.exclude(
                    car_id__in=overlapping_rentals.values('car_id')
                ).filter(provinces=pv).order_by('type_id')
                provinces = Provinces.objects.all().order_by('name_th')
                carType = CarType.objects.all().order_by('type_id')

            context = {'car': cars, 'provinces': provinces, 'carType': carType, 'province_one': province_one,'type_one':type_one}
            if not cars:
                context['no_cars_message'] = "ไม่พบรถให้เช่าในช่วงเวลาและสถานที่ที่คุณค้นหา โปรดลองอีกครั้ง!!"
            return render(request, 'showCarAll.html', context)
        else:
            del request.session['rent_date']
            del request.session['return_date']
            del request.session['province']
            del request.session['type']
            del request.session['price']
            return redirect('home')
    else:
        return redirect('home')


@login_required
def carRentDetail(request,car_id):

    car = Car.objects.filter(car_id=car_id).first()
    if request.session['userId']:
        mem = Member.objects.filter(mem_id=request.session['userId']).first()
        if request.method == "POST":
            rent = Rent()
            rentId = rent.newRentId()
            rent_date = request.POST['rent_date']
            return_date = request.POST['return_date']
            mem_id = request.POST['mem']
            memId = Member.objects.get(mem_id=mem_id)
            status = "1"
            own = Owner.objects.get(own_id=request.POST['own'])
            price = request.POST['price']
            date1 = datetime.datetime.strptime(return_date, '%Y-%m-%d')
            date2 = datetime.datetime.strptime(rent_date, '%Y-%m-%d')
            amount = (date1 - date2).days + 1
            carId = car_id
            Rent(rent_id=rentId,rent_date=rent_date,return_date=return_date,status=status,mem_id=memId,own_id=own,car_id=carId,price=price,amount=int(amount)).save()
            car.status = 1
            car.save()
            url = reverse('memRent', args=[rentId])
            return redirect(url)

        else:
            context = {"car": car, 'mem': mem}
            return render(request, 'detail.html', context)
    else:
        return redirect('signIn')


@login_required
def memRent(request,rent_id):
    rent= Rent.objects.filter(rent_id=rent_id).first()
    pay = Payment.objects.filter(rent_id=rent_id)
    context = {'rents': rent,'pay':pay}
    return  render(request,'memRentDetail.html',context)

@login_required
def rentCancel(request,rent_id,car_id):
    rent = get_object_or_404(Rent, rent_id=rent_id)
    cars = get_object_or_404(Car,car_id=car_id)
    mem = get_object_or_404(Member, mem_id=request.session.get("userId"))
    if request.method == 'POST':
        comment = request.POST['comment']
        cancel = Cancel()
        cancel.rent = rent
        cancel.mem = mem
        cancel.comment = comment
        cancel.save()
        rent.status = "6"
        rent.save()
        cars.status = 0
        cars.save()
        return redirect('memRent', rent_id=rent.rent_id)
    else:
        context = {'rent': rent, 'list': list}
        return render(request, 'Cancel.html', context)


@login_required
def memRentList(request,pageNo):
    rent= Rent.objects.filter(mem_id=request.session['userId']).order_by("status")
    rent_page = Paginator(rent, 5)
    context = {'rent': rent_page.page(pageNo)}
    return  render(request,'rentList.html',context)

@login_required
def memPayment(request,rent_id):
    rent = get_object_or_404(Rent, rent_id=rent_id)
    bank = OwnBank.objects.filter(own_id=rent.own_id)
    # mem = get_object_or_404(Member, mem_id=request.session.get("userId"))
    if request.method == 'POST':
        payId = request.POST['pay_id']
        payTotal = request.POST['total']
        payDate = request.POST['date']
        bank = OwnBank.objects.get(bank_num=request.POST['bank'])
        rentId = Rent.objects.get(rent_id=rent_id)
        slip = request.FILES.get('slip')
        Payment(pay_id=payId,pay_total=payTotal,pay_date=payDate,bank=bank,rent_id=rentId,slip_img=slip).save()
        imgpath = slip.name
        point = imgpath.rfind('.')
        ext = imgpath[point:]
        imgNames = imgpath.split('/')
        imgName = imgNames[len(imgNames) - 1]
        newImg = payId + "_" + str(datetime.date.today()) + ext

        pay = get_object_or_404(Payment,pay_id = payId)
        pay.slip_img = 'static/image/Slip/' + newImg
        pay.save()
        if os.path.exists('static/image/Slip/' + newImg):
            os.remove('static/image/Slip/' + newImg)  # file exits, delete it
        os.rename('static/image/Slip/' + imgName, 'static/image/Slip/' + newImg)
        rent.status = "3"
        rent.save()

        return redirect('memRent', rent_id = rent.rent_id)
    else:
        context = {'rent': rent, 'bank': bank}
        return render(request, 'Payment.html', context)



@login_required
def backend_address(request):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        add = Adress.objects.filter(own_id=request.session['userId'])

        context = {'add': add}
        return render(request, 'backend/address.html', context)
    else:
        return redirect('home')

@login_required
def backend_address_add(request):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        pv = Provinces.objects.all().order_by('name_th')
        if request.method == 'POST':
            name = request.POST['name']
            location = request.POST['location']
            province = Provinces.objects.get(id=request.POST['province'])
            own = Owner.objects.get(own_id=request.session['userId'])
            Adress(name=name,location=location,province=province,own_id=own).save()
            return redirect('address')
        else:
            context = {'pv':pv}
            return render(request, 'backend/addressAdd.html',context)
    else:
        return redirect('home')

@login_required
def backend_address_edit(request,id):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        add = get_object_or_404(Adress, id=id)
        pv = Provinces.objects.all().order_by('name_th')
        if request.method == 'POST':
            name = request.POST['name']
            location = request.POST['location']
            province = Provinces.objects.get(id=request.POST['province'])
            own = Owner.objects.get(own_id=request.session['userId'])
            add.name = name
            add.location = location
            add.province = province
            add.own_id = own
            add.save(force_update=bool)
            return redirect('address')
        else:
            context = {'pv':pv,'add':add}
            return render(request, 'backend/addressEdit.html',context)
    else:
        return redirect('home')

@login_required
def backend_Address_delete(request, id):
    user_status = request.session['userStatus']
    if user_status == 'admin' or user_status == 'owner':
        add = get_object_or_404(Adress, id=id)
        add.delete()
        return redirect('address')
    else:
        return redirect('home')










