from django.shortcuts import render

import mimetypes
import os
from datetime import date
from urllib import request

from django.db import connection
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.template.smartif import key

UPLOAD_FOLDER = 'static/uploads/'


def index(request):
    return render(request, 'HomePage.html')


def AdminHomePage(request):
    return render(request, 'Admin/AdminHomePage.html')

def AdminHomePage1(request):
    return render(request, 'Admin/AdminHomePage1.html')


def AgencyHome(request):
    return render(request, 'Agency/AgencyHome.html')

def AgencyHome1(request):
    return render(request,'Agency/AgencyHome1.html')

def Agencysignup(request):
    if request.method == 'POST':
        agency_id = request.POST['agency']
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        cursor = connection.cursor()

        cursor.execute("select * from agency where agency_id='" + agency_id + "'  ")
        pins = cursor.fetchone()
        print(pins)
        flag = 'error'
        if pins == None:
            cursor = connection.cursor()
            flag = "ok"
            cursor.execute("insert into agency values('" + agency_id + "','" + name + "','" + address + "','" + phone + "','" + email + "','" + password + "','request' )")
            return HttpResponse(
                "<script>alert('Submited, wait for request');window.location='/login';</script>")
        else:
            flag = "error"
            return HttpResponse("<script>alert('Id Already Exits...!');window.location='/login';</script>")
        print(flag)
    return render(request, "agency/Agencysignup.html")


def login(request):
    return render(request, "login.html")

def logout(request):
    return render(request, "login.html")


def login1(request):
    if request.method == "POST":
        name = request.POST['un']
        password = request.POST['pass']
        request.session['lid'] = name

        cursor = connection.cursor()
        cursor.execute("select * from agency where  status = 'approved' ")
        ta = cursor.fetchall()
        cursor.execute("select count(agency_id) from agency where agency.status='request'")
        total = cursor.fetchone()
        c = total[0]
        request.session['count'] = c
        print(c)
        cursor.execute("select * from login where admin_id='" + name + "' and password='" + password + "'")
        print("select * from login where admin_id='" + name + "' and password='" + password + "'")
        pins = cursor.fetchone()
        flag = 'error'
        if pins == None:
            print("not admin")
            cursorF = connection.cursor()
            cursorF.execute("select * from agency where agency_id ='" + name + "' and password='" + password + "' and status = 'approved' ")

            print("select * from agency where agency_id ='" + name + "' and password='" + password + "' and status = 'approved' ")
            res = cursorF.fetchone()
            if res is not None:
                n = res[1]
                request.session['name']=n
                status = res[6]
                print(status)
                request.session['hid'] = name
                if (status == 'pending'):
                    return "<script>alert('Pending please wait');window.location='/';</script>"
                elif (status == 'rejected'):
                    return "<script>alert('Your Request Rejected');window.location='/';</script>"
                elif (status == 'approved'):
                    return redirect("/AgencyHome1")
            return HttpResponse("<script>alert('invalid');window.location='/';</script>")
        else:
            flag = "admin"
            print("this is admin")
    if flag == "admin":
        return redirect("/AdminHomePage1", {'data': ta})
    if flag == "res":
        return redirect("/AgencyHome1")
    if flag == "error":
        return HttpResponse("<script>alert('invalid');window.location='login';</script>")

    return HttpResponse("<script>alert('invalid');window.location='login';</script>")





def addCategory(request):
    if request.method == "POST":
        category_name = request.POST['category_name']
        cursor = connection.cursor()
        cursor.execute("insert into category values(null,'" + category_name + "')")
        return HttpResponse("<script>alert('Category Added');window.location='/AdminHomePage1';</script>")
    return render(request, "Admin/addCategory.html")


def viewCategory(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    pin = cursor.fetchall()
    print(pin)
    return render(request, "Admin/viewCategory.html", {'data': pin})


def deleteCategory(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from category where category_id='" + str(id) + "'")
    return HttpResponse("<script>alert('Deleted Succesfully');window.location='/viewCategory';</script>")


def editCategory(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from category where category_id='" + str(id) + "'")
    pin = cursor.fetchall()
    print(pin)
    return render(request, "Admin/editCategory.html", {'data': pin})


def updatecategory(request, id):
    if request.method == "POST":
        category_name = request.POST['category_name']
        cursor = connection.cursor()
        cursor.execute(
            "update category set category_name='" + category_name + "' where   category_id  ='" + str(id) + "'")
        return HttpResponse("<script>alert('Updated');window.location='/viewCategory';</script>")
    return render(request, "Admin/editCategory.html")


def view_agency_request(request):
    cursor = connection.cursor()
    cursor.execute("select * from agency where status='request'")
    pin = cursor.fetchall()
    print(pin)
    return render(request, "Admin/view_agency_request.html", {'data': pin})


def approveagency(request, sid):
    cursor = connection.cursor()
    cursor.execute("update agency set status='approved' where agency_id='" + str(sid) + "'")
    return redirect("/view_agency_request")

def view_profile_detail(request):
    vid = request.session['hid']
    cursor = connection.cursor()
    cursor.execute("select * from  agency where agency_id='"+str(vid)+"'")
    data = cursor.fetchall()
    return render(request, "view_profile_detail.html", {'data':data})

def view_profile_edit(request,id):
    request.session['viewedit']=id
    cursor = connection.cursor()
    cursor.execute(" select * from agency where agency_id='"+str(id)+"'")
    data =cursor.fetchall()
    return render(request, "Agency/view_profile.html",{'data':data})

def view_profile(request):
    if request.method == 'POST':
        id = request.session['viewedit']
        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        password = request.POST['password']
        cursor = connection.cursor()
        cursor.execute("update agency set name='"+name+"',address='"+address+"', email='"+email+"',password='"+password+"'where agency_id='"+str(id)+"'")
        return HttpResponse("<script>alert('updated');window.location='/AgencyHome1';</script>")

    return redirect("view_profile_detail")

def view_approved_agency(request):
    cursor = connection.cursor()
    cursor.execute("select * from agency where status='approved'")
    pin = cursor.fetchall()
    print(pin)
    return render(request, "Admin/view_approved_agency.html", {'data': pin})

def delete_agency(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from agency where agency_id ='"+str(id)+"'")
    return HttpResponse("<script>alert('deleted');window.location='/view_approved_agency';</script>")


def ViewcompliantAdmin(request):
    cursor = connection.cursor()
    cursor.execute("select * from complaints ")
    pin = cursor.fetchall()
    return render(request, "Admin/ViewcompliantAdmin.html", {'data': pin})


def Reply(request, id):
    if request.method == "POST":
        reply = request.POST['TxtReply']
        cursor = connection.cursor()
        cursor.execute("update complaints set reply='" + reply + "' where idcomplaints='" + str(id) + "' ")
        return HttpResponse("<script>alert('Replayed');window.location='/ViewcompliantAdmin';</script>")
    return render(request, "Admin/Reply.html")


def register_driver(request):
    if request.method == 'POST':
        name = request.POST['name']
        licence_no = request.POST['licence_no']
        address = request.POST['address']
        driver_id = request.POST['driver_id']
        password = request.POST['password']
        agency_id = request.POST['agency_id']
        cursor = connection.cursor()
        cursor.execute(
            "insert into driver_details values(null,'" + name + "','" + licence_no + "','" + address + "','" + driver_id + "','" + password + "','" + agency_id + "')")
        return HttpResponse("<script>alert('Registered');window.location='/AgencyHome1';</script>")
    return render(request, "Agency/register_driver.html")


def view_drivers(request):
    cursor = connection.cursor()
    cursor.execute("select * from  driver_details ")
    data = cursor.fetchall()
    return render(request, "Agency/view_drivers.html", {'data': data})


def viewBookingDetials(request):
    hid = request.session['hid']
    cursor = connection.cursor()
    cursor.execute("select * from  booking_details where agency_id='"+str(hid)+"' and status='request' ")
    data = cursor.fetchall()
    return render(request, "Agency/viewBookingDetials.html", {'data': data})


def Selectdrivers(request,id,aid):
    request.session['bid']=id
    cursor = connection.cursor()
    cursor.execute("select * from  driver_details where agency_id='"+str(aid)+"' ")
    data = cursor.fetchall()
    return render(request, "Agency/Selectdrivers.html", {'data': data})


def AssignDriver(request,div):
    hid = request.session['hid']
    bid=request.session['bid']
    if request.method == 'POST':
        timing = request.POST['timing']
        agency_id = str(hid)
        diver_id = str(div)
        idbooking_details =str(bid)
        cursor = connection.cursor()
        cursor.execute("insert into driver_duty values(null,'" + timing + "','" + agency_id + "','" + idbooking_details + "','" + diver_id + "')")
        cursor.execute("update booking_details set status='Assigned' where idbooking_details='" + str(bid) + "' ")
        return HttpResponse("<script>alert('Assigned');window.location='/viewAssigned';</script>")
    return render(request, "Agency/AssignDriver.html")


def viewAssigned(request):
    cursor = connection.cursor()
    cursor.execute("SELECT d.iddriver_duty,d.timing,d.agency_id,c.category_name,d.diver_id FROM driver_duty as d join booking_details as b join category as c on d.idbooking_details=b.idbooking_details  and b.category_id=c.category_id")
    data = cursor.fetchall()
    return render(request, "Agency/viewAssigned.html", {'data': data})


def delete_assigned(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from  driver_duty where iddriver_duty = '" + str(id) + "'")
    return HttpResponse("<script>alert('Deleted');window.location='/viewAssigned';</script>")



def delete_driver(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from  driver_details where iddriver_details = '" + str(id) + "'")
    data = cursor.fetchone()
    return redirect("/view_drivers")


def edit_driver(request, id):
    request.session['eid'] = id
    cursor = connection.cursor()
    cursor.execute("select * from driver_details where iddriver_details = '" + str(id) + "' ")

    data = cursor.fetchone()
    return render(request, "Agency/edit_driver.html", {'data': data})


def update_driver(request):
    a = request.session['eid']
    print(a)
    if request.method == 'POST':
        name = request.POST['name']
        licence_no = request.POST['licence_no']
        address = request.POST['address']
        driver_id = request.POST['driver_id']
        password = request.POST['password']
        agency_id = request.POST['agency_id']
        cursor = connection.cursor()
        print(str(a))

        print("update driver_details set_name ='" + name + "',set_licence_no='" + licence_no + "',set_address='" + address + "',set_driver_id='" + driver_id + "', set_password='" + password + "',set_agency_id='" + agency_id + "' where iddriver_details ='" + str(a) + "'")

        cursor.execute("update driver_details set name ='" + name + "',licence_no='" + licence_no + "',address='" + address + "',driver_id='" + driver_id + "', password='" + password + "',agency_id='" + agency_id + "' where iddriver_details ='" + str(a) + "'")
        return HttpResponse("<script>alert('updated');window.location='/AgencyHome1';</script>")
    return render(request, "Agency/edit_driver.html")


def view_category(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    data = cursor.fetchall
    return render(request, "Agency/view_category.html", {'data': data})


def set_ammount_details(request, id):
    if request.method == 'POST':
        hid = request.session['hid']
        agency_id = str(hid)
        category_id = str(id)
        rate_per_kg = request.POST['rate_per_kg']
        cursor = connection.cursor()
        cursor.execute("insert into agency_rate values(null,'" + agency_id + "','" + category_id + "','" + rate_per_kg + "')")
        return HttpResponse("<script>alert('updated');window.location='/AgencyHome1';</script>")
    return render(request, "Agency/set_ammount_details.html")

def view_booking(request):
    cursor = connection.cursor()
    cursor.execute("select booking_details.*,category.category_name from booking_details join category on booking_details.category_id=category.category_id")
    data = cursor.fetchall()
    return render(request, "Agency/view_booking.html",{'data':data})

# def waste_collection_details(request):
#     cursor = connection.cursor()
#     cursor.execute("select * from ")
#     return render(request,"waste_collection_details.html")

def complaint_view(request):
    cursor = connection.cursor()
    cursor.execute("select * from complaints")
    data = cursor.fetchall()
    return render(request, "Agency/complaint_view.html", {'data':data})
