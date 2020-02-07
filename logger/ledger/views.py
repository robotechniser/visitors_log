from django.shortcuts import render

from ledger.models import Member, MemberLoginInstance
from ledger.forms import LoginLogoutForm, SignUpForm, OTPVerificationForm

from datetime import datetime as dt
import uuid

from .helper import *

def MemberLoginGetContext():
    """To shorten the code in MemberLogin()"""
    pass

def MemberLogin(request):
    date = dt.now()
    todays_date = dt.strptime(dt.strftime(dt.now(), '%d/%m/%Y') + " 00:00", '%d/%m/%Y %H:%M')
    mem_login_list = []

    if request.method == 'POST': # POST
        form = LoginLogoutForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            pwd = form.cleaned_data['password']
            # Case Sensitive
            mem_obj = Member.objects.filter(name__exact=name)

            if mem_obj: # Name Matched
                if not mem_obj[0].is_active: # Account inactive
                    login_error = "Your account is not active! Please contact an Admin!"
                    mem_login_list = MemberLoginInstance.objects.filter(login_timestamp__gte=todays_date).order_by('-login_timestamp')
                    login_list = getPage(request, mem_login_list)
                    num_logins_total = MemberLoginInstance.objects.filter(login_timestamp__gte=todays_date).count()
                    num_logged_in = MemberLoginInstance.objects.filter(logged_out=False).count()
                    context = {
                        'login_error': login_error,
                        'date': date,
                        'form': form,
                        'num_logins_total': num_logins_total,
                        'num_logged_in': num_logged_in,
                        'login_list': login_list,
                    }

                    return render(request, 'base.html', context)

                else: # Account active
                    mem = MemberLoginInstance.objects.filter(member__exact=mem_obj[0]).order_by('logged_out')

                    if not mem: # To handle the first login
                        verifier = PBKDF2PasswordHasher()
                        if verifier.verify(password=pwd, encoded=mem_obj[0].hashed_secret_key):
                            mem_obj[0].login_count += 1
                            mem_obj[0].save()
                            # Creating new object/entry of/for MemberLoginInstance
                            mem_inst = MemberLoginInstance.objects.create(member=mem_obj[0], logged_out=False)
                            # Limiting to logins performed today
                            mem_login_list = MemberLoginInstance.objects.filter(login_timestamp__gte=todays_date).order_by('-login_timestamp')
                            login_list = getPage(request, mem_login_list)
                            num_logins_total = MemberLoginInstance.objects.filter(login_timestamp__gte=todays_date).count()
                            num_logged_in = MemberLoginInstance.objects.filter(logged_out=False).count()
                            context = {
                                'date': date,
                                'form': form,
                                'num_logins_total': num_logins_total,
                                'num_logged_in': num_logged_in,
                                'login_list': login_list,
                            }

                            return render(request, 'base.html', context)
                    
                        else: # Wrong Password
                            login_error = "Please check your password!"
                            mem_login_list = MemberLoginInstance.objects.filter(login_timestamp__gte=todays_date).order_by('-login_timestamp')
                            login_list = getPage(request, mem_login_list)
                            num_logins_total = MemberLoginInstance.objects.filter(login_timestamp__gte=todays_date).count()
                            num_logged_in = MemberLoginInstance.objects.filter(logged_out=False).count()
                            context = {
                                'login_error': login_error,
                                'date': date,
                                'form': form,
                                'num_logins_total': num_logins_total,
                                'num_logged_in': num_logged_in,
                                'login_list': login_list,
                            }

                            return render(request, 'base.html', context)

                    else:
                        verifier = PBKDF2PasswordHasher()
                        if verifier.verify(password=pwd, encoded=mem_obj[0].hashed_secret_key):
                            if mem[0].logged_out: # Logging in
                                mem_obj[0].login_count += 1
                                mem_obj[0].save()
                                # Creating new object/entry of/for MemberLoginInstance
                                mem_inst = MemberLoginInstance.objects.create(member=mem[0].member, logged_out=False)
                                # Limiting to logins performed today
                                mem_login_list = MemberLoginInstance.objects.filter(login_timestamp__gte=todays_date).order_by('-login_timestamp')
                            else: # Logging out
                                mem[0].logout_timestamp = dt.now()
                                mem[0].logged_out = True
                                mem[0].save()
                                # Limiting to logins performed today
                                mem_login_list = MemberLoginInstance.objects.filter(login_timestamp__gte=todays_date).order_by('-login_timestamp')
                            login_list = getPage(request, mem_login_list)
                            num_logins_total = MemberLoginInstance.objects.filter(login_timestamp__gte=todays_date).count()
                            num_logged_in = MemberLoginInstance.objects.filter(logged_out=False).count()
                            context = {
                                'date': date,
                                'form': form,
                                'num_logins_total': num_logins_total,
                                'num_logged_in': num_logged_in,
                                'login_list': login_list,
                            }

                            return render(request, 'base.html', context)

                        else: # Wrong Password
                            login_error = "Please check your password!"
                            mem_login_list = MemberLoginInstance.objects.filter(login_timestamp__gte=todays_date).order_by('-login_timestamp')
                            login_list = getPage(request, mem_login_list)
                            num_logins_total = MemberLoginInstance.objects.filter(login_timestamp__gte=todays_date).count()
                            num_logged_in = MemberLoginInstance.objects.filter(logged_out=False).count()
                            context = {
                                'login_error': login_error,
                                'date': date,
                                'form': form,
                                'num_logins_total': num_logins_total,
                                'num_logged_in': num_logged_in,
                                'login_list': login_list,
                            }

                            return render(request, 'base.html', context)
                
            else: # Name not matched
                login_error = "Username not found!"
                mem_login_list = MemberLoginInstance.objects.filter(login_timestamp__gte=todays_date).order_by('-login_timestamp')
                login_list = getPage(request, mem_login_list)
                num_logins_total = MemberLoginInstance.objects.filter(login_timestamp__gte=todays_date).count()
                num_logged_in = MemberLoginInstance.objects.filter(logged_out=False).count()
                context = {
                    'login_error': login_error,
                    'date': date,
                    'form': form,
                    'num_logins_total': num_logins_total,
                    'num_logged_in': num_logged_in,
                    'login_list': login_list,
                }

                return render(request, 'base.html', context)

    else: # GET and others
        form = LoginLogoutForm()
    
    mem_login_list = MemberLoginInstance.objects.filter(login_timestamp__gte=todays_date).order_by('-login_timestamp')
    login_list = getPage(request, mem_login_list)
    num_logins_total = MemberLoginInstance.objects.filter(login_timestamp__gte=todays_date).count()
    num_logged_in = MemberLoginInstance.objects.filter(logged_out=False).count()
    context = {
        'date': date,
        'form': form,
        'num_logins_total': num_logins_total,
        'num_logged_in': num_logged_in,
        'login_list': login_list,
    }

    return render(request, 'base.html', context)

def SignUp(request):
    date = dt.now()

    if request.method == 'POST': # POST
        form = SignUpForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['password']
            forgot_pwd = form.cleaned_data['forgot_password']
            # Case Sensitive
            mem_obj = Member.objects.filter(name__exact=name).filter(email__exact=email)

            if mem_obj and forgot_pwd: # Forgotten Password Case
                OTP = getOTP()
                mem_obj[0].hashed_secret_key = getHashedKey(pwd, OTP)
                mem_obj[0].is_active = False # False, till OTP is verified
               
                mem_obj[0].save()
                # Sending mail with OTP
                mail(mem_obj[0].email, OTP)

                message = "A 6-digit OTP has been mailed to your entered mail ID. You will have to verify the OTP, before logging in with your new password."
                context = {
                    'message': message,
                    'date': date,
                    'form': form,
                }

                return render(request, 'signup.html', context)
            
            elif mem_obj and not forgot_pwd: # Error
                message = "User/Email already exists. If you've forgotten your password, please check the checkbox."
                context = {
                    'message': message,
                    'date': date,
                    'form': form,
                }

                return render(request, 'signup.html', context)

            elif not mem_obj and not forgot_pwd: # Sign Up Case
                OTP = getOTP()
                # Creating a new member
                new_mem = Member.objects.create(name=name, email=email, hashed_secret_key=getHashedKey(pwd, OTP), is_active=False)
                # Sending mail with OTP
                mail(new_mem.email, OTP)

                message = "A 6-digit OTP has been mailed to your entered mail ID. If it does not arrive in a few minutes, check your email and your spam folder."
                context = {
                    'message': message,
                    'date': date,
                    'form': form,
                }

                return render(request, 'signup.html', context)


            else: # "not mem_obj and forgot_pwd" | Error
                message = "User does not exist."
                context = {
                    'message': message,
                    'date': date,
                    'form': form,
                }

                return render(request, 'signup.html', context)

    else: # GET
        form = SignUpForm()

    context = {
        'date': date,
        'form': form,
    }

    return render(request, 'signup.html', context)



def Verify(request):
    date = dt.now()
    if request.method == 'POST': # POST
        form = OTPVerificationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            OTP =  form.cleaned_data['OTP']

            mem_obj = Member.objects.filter(email__exact=email)

            if mem_obj: # Member found
                prev_key = mem_obj[0].hashed_secret_key
                saved_OTP = prev_key[prev_key.index("$", prev_key.index("$")+1)+1:prev_key.rindex("$")]

                if OTP == saved_OTP: # Verified
                    mem_obj[0].is_active = True
                    mem_obj[0].save()

                    message = "OTP verified successfully. Account activated! Please go to the homepage to login again!"
                    context = {
                        'message': message,
                        'form': form,
                    }

                    return render(request, 'verify.html', context)
                
                else: # Not verified
                    message = "Wrong OTP entered! Please check your OTP and try again, or if the error persists, try changing the password again."
                    context = {
                        'message': message,
                        'form': form,
                    }

                    return render(request, 'verify.html', context)
            
            else: # Member not found
                message = "Member not found in database. Please check your inputs!"
                context = {
                    'message': message,
                    'form': form,
                }

                return render(request, 'verify.html', context)

    else: # GET and others
        form = OTPVerificationForm()

    context = {
        'date': date,
        'form': form,
    }

    return render(request, 'verify.html', context)