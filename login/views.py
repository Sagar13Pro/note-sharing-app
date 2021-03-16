from datetime import datetime 
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from .models import Note,Users
from .forms import RegisterForm, NoteForm
from django.urls import reverse
from django.contrib import messages
from passlib.hash import pbkdf2_sha256 as kdf
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

'''STARTED BLOCK'''
# views for New SingIn Page ANd SignUp Page.
def SignIn(request):
    return render(request, "SignIn.html")

def SignUp(request):
    return render(request, "SignUp1.html")

def Notes(request):
    if request.session.get("session_email"):
        return render(request, "create_note.html")
    return HttpResponseRedirect(reverse("login"))

def Dashboard(request):
    if request.session.get('session_email'):
        note = list(Note.objects.filter(creator_id = Users.objects.get(email = request.session.get('session_email'))).values())
        for item in note:
            item['password'] = Note.set_PasswordDecrypt(item['password'])
        return render(request, "dashboard.html",
                      {
                          "users": Users.objects.get(email=request.session.get('session_email')),
                          "notes": note
                      })
    return HttpResponseRedirect(reverse('login'))

def Edit(request,id = None):
    if request.session.get('session_email'):
        editNote = Note.objects.get(id=id)
        #print(type(editNote.secured_content))
        msg = Note.set_PasswordDecrypt(editNote.secured_content)
        passwd = Note.set_PasswordDecrypt(editNote.password)
        return render(request,"Edit.html",{'editNote':editNote,'secured_content':msg,'passwd':passwd})
    return HttpResponseRedirect(reverse('login'))

def Share(request,id = None):
    if request.session.get('session_email'):
        shareNote = Note.objects.get(id=id)
        return render(request,"share.html",{'shareNote':shareNote,'date':datetime.now()})
    return HttpResponseRedirect(reverse('login'))

def SharedView(request, id = None):
    try:
        Notes = Note.objects.get(id=id)
        if Notes.expiry_time > datetime.now():
            if len(request.POST) > 0:
                print(len(request.POST))
                if Note.set_PasswordDecrypt(Notes.password) == request.POST["password"]:
                    return render(request,"sharedView.html",{
                    "sharedNote":Notes,
                    "matched":True,
                    "secured_content": Note.set_PasswordDecrypt(Notes.secured_content)
                    })
                else:
                    messages.error(request,"It seems you entered incorrect password.")
                    return HttpResponseRedirect(reverse('note_shared_view',args=(id,)))
            if Notes.isset_Password:
                passCheck = Note.objects.get(id=id)
                return render(request,"sharedView.html",{'passCheck':passCheck.isset_Password,'id':id})
            else:
                getSecured = Note.set_PasswordDecrypt(Notes.secured_content)
                return render(request,"sharedView.html",{
                    "sharedNote":Notes,
                    "matched":False,
                    "secured_content":getSecured
                    })
        else:
            return render(request, "sharedView.html",{'err':'The link Has been Expired . Ask The Owner to reshare.'})
    except Exception as er:
        print('Exception:::',er)
        return render(request, "sharedView.html",{'err':'The Note has been not found.'})
    
    
def Logout(request):
    if request.session.get("session_email"):
        request.session.flush()
    return HttpResponseRedirect(reverse("login"))

#User Registration Store Function
def Save(request):
    try:
        if request.method == 'POST':
            # Validation of fields in forms.py passed by users
            details = RegisterForm(request.POST)
            if details.is_valid():
                if not Users.objects.filter(email=details.data["email"]):
                    user = Users.objects.create(
                        firstName=details.data["firstName"],
                        lastName=details.data["lastName"],
                        email=details.data["email"],
                        mobileNo=details.data["mobileNo"],
                        password=kdf.hash(
                            details.data["password"],
                            rounds=1200,
                            salt_size=32)
                    )
                    print(user)
                    messages.success(
                        request, 'Your Registration has been done successfully.', 'success'
                    )
                    return HttpResponseRedirect(reverse('login'))
                else:
                    print('else')
                    messages.error(
                        request, 'OPPS! The email already been taken.'
                    )
                    return HttpResponseRedirect(reverse('registration'))
            else:
                print(details.errors)
                return render(request, "SignUp1.html", {
                    'form': details
                })
    except Exception as err:
        print('Error--------',err,'-----------')
        messages.error( request, 'OPPS! Something went Wrong.')
        return HttpResponseRedirect(reverse('registration'))

#validate user while logging
def ValidateUser(request):
    if request.method == 'POST':
        getUser = Users.objects.filter(email=request.POST["email"])
        if len(getUser) == 1 and kdf.verify(request.POST['pass'], getUser.values()[0]['password']):
            request.session['session_email'] = Users.objects.get(
                email=request.POST["email"]).email
            print(request.session.get('session_email'))
            return HttpResponseRedirect(reverse('user_dashboard'))
        else:
            messages.error(
                request, 'OPPS! Your credentails doesn\'t matched with our records.'
            )
            return HttpResponseRedirect(reverse('login'))

#Creation of Note and Store
def create_note(request):
    if request.method == 'POST':
            try:
                user = Users.objects.get(email=request.session.get("session_email"))
                note_valid = NoteForm(request.POST)
                print(note_valid.data)
                if note_valid.is_valid():
                    Note.objects.create(
                    title = note_valid.data['title'],
                    secured_content = Note.set_PasswordEncrypt(note_valid.data['secured_content']),
                    password = Note.set_PasswordEncrypt(note_valid.data['password']),
                    isset_Password = note_valid.data['isset_Password'],
                    creator = user)
                    messages.success(request,"Note successfully created with title: %s" % note_valid.data['title'])
                else:
                    print(note_valid.errors)
                    return render(request, 'create_note.html', {'noteform':note_valid})
            except Exception as Error:
                print('Error: ',Error)
            return HttpResponseRedirect(reverse('note_view'))

def EditStore(request, id = None):
    if request.method == 'POST':
        contents = NoteForm(request.POST)
        if contents.is_valid():
            #print(contents)
            to_update = Note.objects.get(id=id)
            to_update.title = contents.data['title']
            to_update.secured_content = Note.set_PasswordEncrypt(contents.data['secured_content'])
            if  contents.data['isset_Password'] == 'False':
                to_update.isset_Password = contents.data['isset_Password']
                to_update.password = None
            else:
                if contents.data['password'].startswith('gAAAAA'):
                    print('ok')
                    to_update.isset_Password = contents.data['isset_Password']
                else:
                    to_update.password = Note.set_PasswordEncrypt(contents.data['password'])
                    to_update.isset_Password = contents.data['isset_Password']
            to_update.save()
            messages.success(request,'Hurray!! Your Note with id %d has been successfully updated.!!' % id)
            #args=(par1,) like this only it works
            return HttpResponseRedirect(reverse('note_edit',args=(id,)))
        else:
            print(contents.errors)
            messages.error(request,contents.errors)
            return HttpResponseRedirect(reverse('note_edit',args=(id,)))

#function for when user share a note to someone by setting expiry time
def ShareNote(request,id = None):
    if request.method == 'POST':
        try:
            note = Note.objects.get(id=id)
            note.expiry_time = request.POST['expiryTime']
            note.save()
            # noteLink = 'http://127.0.0.1:8000/user/note/shared/view/' + str(id)
            livelink = 'https://myvault-app.herokuapp.com/user/note/shared/view/' + str(id)
            print('Shared Note link:',livelink)
            send_mail(
                'Note Share Link',
                'Live Note Shared link: ' + livelink,
                settings.EMAIL_HOST_USER,
                [request.POST['emailto']]
                )
            messages.success(request, 'Your note has been shared to %s successfully. Also check in spam for mail' % request.POST['emailto'])
            return HttpResponseRedirect(reverse('user_dashboard'))
        except Exception as error:
            print(error)
            messages.error(request, 'OPPS! Something went Wrong!!')
            return HttpResponseRedirect(reverse('note_share',args=(id,)))

        
#Note Deletion Function 
def Delete(request,id = None):
    notes = Note.objects.get(id=id)
    if notes.expiry_time is not None:
         if notes.expiry_time > datetime.now():
            messages.info(request,"The Note is not expired.You can't Delete Now.")
            return HttpResponseRedirect(reverse('user_dashboard'))
         else:
            notes.delete()
            messages.success(request,"Your Note with id %d is Deleted Successfully!" % id)
            return HttpResponseRedirect(reverse('user_dashboard'))
    else:
        notes.delete()
        messages.success(request,"Your Note with id %d is Deleted Successfully!" % id)
        return HttpResponseRedirect(reverse('user_dashboard'))

def search_Result(request):
    query = str(request.POST['search_Query_title'])
    answer_notes = Note.objects.filter(title__icontains=query) 
    # Filtered by title , if no results found by tilte , then it will search by user's first name.
    #  As in models.py user_name is commented , that's why we used first_name field
    if len(answer_notes) == 0:
        try:
            user_instance = Users.objects.get(firstName = query)
            user_id = user_instance.id
            result = list(Note.objects.filter(creator=user_id))    # Filtered by user name
            for i in result:
                i.secured_content = Note.set_PasswordDecrypt(i.secured_content)
            return render(request, "search.html",
                        {
                            "users": Users.objects.get(email=request.session.get('session_email')),
                            "notes": result
                        })
        except:
            return render(request, "search.html")
    else:
        for i in answer_notes:     # please chech def edit ........... inside that i use code to decrypt code
            i.secured_content = Note.set_PasswordDecrypt(i.secured_content)
        return render(request, "search.html",
                {
                    "users": Users.objects.get(email=request.session.get('session_email')),
                    "notes": answer_notes
                })

def fg_pass(request):
    return render(request,'password_reset.html')

def resest_password(request,id):
    return render(request,'password_reset_confirm.html' , {'id':id})

def reset_done(request):
    if request.POST['new_pass'] == request.POST['confirm_pass']:
        id = request.POST['id']
        tmp = Users.objects.get(id=id)
        tmp.password = kdf.hash(request.POST['new_pass'],rounds=1200,salt_size=32)
        #tmp.password = request.POST['new_pass']
        tmp.save()
        return render(request, "password_reset_complete.html")
    else:
        return render(request,"password_reset_confirm.html" , {'err':'The Confirmation Password Doesn\'t Matched.'})

def validate_password(request):
    try:
        exist_user = Users.objects.get(email=request.POST['email'])
        password_Reset_link = "https://myvault-app.herokuapp.com/user/reset_password/" + str(exist_user.id)
        subject = 'Password Reset Link'
        message = 'Click on below link to reset password ' + password_Reset_link
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [exist_user.email, ] 
        send_mail(subject, message, email_from, recipient_list)
        return render(request, "password_reset_done.html",{'err':'Email HAs been Sent .please check your E-mail .'})
    except Exception as er:
        print('Exception:::',er)
        return render(request, "password_reset_done.html",{'err':'Something goes Wrong.'})
    

def search_Result_search(request):
     return render(request, "search.html")
