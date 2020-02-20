
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.core.mail import send_mail
from django.conf import settings

import math, random

def getPage(request, mem_login_list):
    """For Pagination"""
    page = request.GET.get('page', 1)
    paginator = Paginator(mem_login_list, 25) # Paginating - 25, per page

    try:
        login_list = paginator.page(page)
    except PageNotAnInteger:
        login_list = paginator.page(1)
    except EmptyPage:
        login_list = paginator.page(paginator.num_pages)
    
    return login_list


def getOTP():
    super_secret_key = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    super_secret_len = len(super_secret_key)
    OTP = ""
    for i in range(6) : 
        OTP += super_secret_key[math.floor(random.random() * super_secret_len)] 
  
    return OTP

def getHashedKey(password, OTP):
    """Separate function, in order to make changes down the line"""
    gen = PBKDF2PasswordHasher()
    return gen.encode(password=password, salt=OTP)

def mail(email, OTP):
    subject = settings.EMAIL_SUBJECT_PREFIX + ' OTP for Sign up or Password Change'
    body = 'Hello,\n\nYour OTP for sign up or password change verification is ' + OTP + '. Click on "Verify OTP" at the MLab Log Homepage and enter it in.\n\nRegards,\nClub Coordinator\nRTC, NISER'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, body, email_from, recipient_list, fail_silently=False)