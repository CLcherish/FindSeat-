# coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
import pymysql

# Create your views here.


def login(request):
    name = request.POST.get('uname')
    print(name)
    return render(request, 'seatview/login.html', name)


def login_check(request):
    print('1')
    uname = request.POST.get('uName')
    upwd = request.POST.get('uPwd')
    db = pymysql.connect('localhost', 'root', '123456',
                         'lseat', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM seatview_customer WHERE NAME = '%s' AND PWD = '%s'" % (
        uname, upwd)
    cursor.execute(sql)
    results = cursor.fetchall()
    print(uname, upwd)
    print(results)
    db.close()
    if len(results) >= 1:
        print('登录成功')
        request.session['isLogin'] = True
        request.session['uname'] = uname
        request.session['password'] = upwd
        return JsonResponse({'msg': 'ok'})
    else:
        print('登录失败')
        return JsonResponse({'msg': 'fail_user'})
    return HttpResponse(request, 'seatview/login.html')


def userInfo(request):
    print(request.session['uname'])
    return render(request, 'seatview/userInfo.html')


def show_message(request):
    username = request.session['uname']
    db = pymysql.connect('localhost', 'root', '123456',
                         'lseat', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT seatid FROM seatview_seat WHERE customername= '%s'" % username
    cursor.execute(sql)
    results = cursor.fetchall()
    db.commit()

    if len(results) > 0:
        seatIndex = results[0][0].replace('-', '_')
        print('超出索引')
        sql = "SELECT begintime,endtime FROM "+seatIndex+"Order"
        cursor.execute(sql)
        timeResults = cursor.fetchall()
        db.commit()

        begintime = timeResults[0][0]
        endtime = timeResults[0][1]
        return JsonResponse({'msg': username, 'pos': seatIndex, 'begintime': begintime, 'endtime': endtime})
    else:
        return JsonResponse({'msg': username, 'pos': '并没有预约', 'begintime': '无', 'endtime': '无'})


def register(request):
    return render(request, 'seatview/register.html')


def register_check(request):
    uname = request.POST.get('uname')
    upwd = request.POST.get('upwd')
    uphone = request.POST.get('uphone')
    db = pymysql.connect('localhost', 'root', '123456',
                         'lseat', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM seatview_customer WHERE NAME = '%s'" % uname
    cursor.execute(sql)
    results = cursor.fetchall()
    print(uname, upwd, uphone)
    if len(results) > 0:
        print('有人注册了')
        return JsonResponse({'msg': 'fail_user'})
    else:
        print('无人注册')
        sql = "INSERT INTO seatview_customer(name,pwd,uphone) VALUES('%s','%s','%s')" % (
            uname, upwd, uphone)
        cursor.execute(sql)
        db.commit()
        return JsonResponse({'msg': 'ok'})
    db.close()
    return render(request, 'seatview/register.html')

# def index(request):
#     return render(request,'seatview/index.html')


def seat(request):
    return render(request, 'seatview/seats.html')


def upload_seat(request):
    seatid = request.POST.get('seatid')
    status = request.POST.get('status')
    username = request.session['uname']
    begintime = request.POST.get('begintime')
    endtime = request.POST.get('endtime')
    seatIndex = seatid.replace('-', '_')
    print(seatid, status, seatIndex, username, begintime, endtime)
    db = pymysql.connect('localhost', 'root', '123456',
                         'lseat', charset='utf8')
    cursor = db.cursor()

    sql = "SELECT customername FROM seatview_seat WHERE customername='%s'" % username
    cursor.execute(sql)
    results = cursor.fetchall()
    print('是', len(results))
    db.commit()
    if len(results) < 1:
        sql = "INSERT INTO  seatview_seat(seatid,status,customername) VALUES('%s','%s','%s')" % (
            seatid, status, username)
        cursor.execute(sql)
        db.commit()

        print(len(results))
        print('101')
        sql = "create table if not exists "+seatIndex+"Comment" + \
            "(customer varchar(20),comment varchar(20));"
        cursor.execute(sql)
        sql = "create table if not exists "+seatIndex+"Order" + \
            "(username varchar(20),begintime varchar(6),endtime varchar(6));"
        cursor.execute(sql)
        sql = "INSERT INTO "+seatIndex+"Order" + \
            "(username,begintime,endtime) VALUES('%s','%s','%s');" % (
                username, begintime, endtime)
        cursor.execute(sql)
        db.commit()
        db.close()
        return JsonResponse({'msg': 'OK'})
    else:
        return JsonResponse({'msg': 'fail'})


def download_seat(request):
    db = pymysql.connect("localhost", "root", "123456",
                         "lseat", charset='utf8')
    cursor = db.cursor()
    sql = "SELECT seatid FROM seatview_seat  WHERE status ='%s'" % 'ordered'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        # for row in results:
        #    fname = row[0]
        #    print ("fname=%s" % fname,results)
    except:
        print("Error: unable to fetch data")
    db.close()
    return JsonResponse({'msg': results})
    # return render(request,'seatview/register.html')


def download_comment(request):
    seatid = request.POST.get('seatid')
    print(seatid)
    seatIndex = seatid.replace('-', '_')
    db = pymysql.connect("localhost", "root", "123456",
                         "lseat", charset='utf8')
    cursor = db.cursor()
    # 这里会因为找不到表报错
    sql = "SELECT * FROM " + seatIndex+"Comment"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        # for row in results:
        #    fname = row[0]
        #    print ("fname=%s" % fname,results)
        print(results)
    except:
        print("Error: unable to fetch data")
        return JsonResponse({'msg': (('null', 'null'),)})
    else:
        return JsonResponse({'msg': results})
    finally:
        db.close()


def download_ordertime(request):
    seatid = request.POST.get('seatid')
    print(seatid)
    seatIndex = seatid.replace('-', '_')
    db = pymysql.connect("localhost", "root", "123456",
                         "lseat", charset='utf8')
    cursor = db.cursor()
    # 这里会因为找不到表报错
    sql = "SELECT username,begintime,endtime FROM " + seatIndex+"Order"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        # for row in results:
        #    fname = row[0]
        #    print ("fname=%s" % fname,results)
        print(results)
    except:
        print("Error: unable to fetch data")
    db.close()
    return JsonResponse({'msg': results})


def cancel_reservation(request):
    username = request.session['uname']
    seatid = request.POST.get('pos')
    seatIndex = request.POST.get('pos').replace('-', '_')
    # print(seatid,seatIndex)
    db = pymysql.connect("localhost", "root", "123456",
                         "lseat", charset='utf8')
    cursor = db.cursor()
    sql = "DELETE FROM seatview_seat WHERE customername='%s'" % username
    cursor.execute(sql)
    # db.commit()
    sql = "DELETE FROM "+seatIndex+"Order"+" WHERE username='%s'" % username
    cursor.execute(sql)
    db.commit()
    db.close()
    return JsonResponse({'msg': username, 'pos': '并没有预约', 'begintime': '无', 'endtime': '无'})


def Submit_Commit(request):
    username = request.session['uname']
    textIndex = request.POST.get('comment')
    pos = request.POST.get('pos')
    print(username, '发表了', pos, '的评论：', textIndex)
    db = pymysql.connect("localhost", "root", "123456",
                         "lseat", charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO "+pos+"Comment" + \
        " VALUES('%s','%s')" % (username, textIndex)
    cursor.execute(sql)
    db.commit()
    db.close()
    return JsonResponse({'msg': 'OK'})
