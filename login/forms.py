from django.forms import ModelForm
from .models import Users, Note
from re import match


class RegisterForm(ModelForm):
    class Meta:
        model = Users
        fields = [
            "firstName",
            "lastName",
            "email",
            "mobileNo",
            "password"
        ]
    # validation for form user registration

    def clean(self):
        #super(RegisterForm, self).clean()

        firstName = self.data['firstName']
        lastName = self.data['lastName']
        email = self.data['email']
        mobileNo = self.data['mobileNo']
        password = self.data['password']
        passwordConfirm = self.data["passwordConfirm"]

        # if len(firstName) < 5:
        #     self._errors["firstName"] = self.error_class([
        #         'Maximum 5 character required'
        #     ])
        # if len(lastName) < 5:
        #     self._errors["lastName"] = self.error_class([
        #         'Maximum 5 character required for last name'
        #     ])
        if email is not None:
            regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if not match(regex_email, email):
                self._errors["email"] = self.error_class([
                    'Please Provide a valid email address'
                ])
        if mobileNo is not None:
            try:
                if len(mobileNo) != 10:
                    self._errors["mobileNo"] = self.error_class([
                        'Mobile Number digits should be 10 only'
                    ])
                mobileNo = int(mobileNo)
            except:
                self._errors["mobileNo"] = self.error_class([
                    'Mobile Number should be the  digits.'
                ])
        if password is not None and passwordConfirm is not None:
            if len(password) < 8:
                self._errors["password"] = self.error_class([
                    'Password length must be 8 or greater than 8 characters'
                ])
            else:
                specialChar = ['!', '@', '#', '$', '^', '&', '*']
                if not any(char.isdigit() for char in password):
                    self._errors["digit"] = self.error_class([
                        'Password should have at least one digit.'
                    ])
                if not any(char.isupper() for char in password):
                    self._errors["upper"] = self.error_class([
                        'Password should have at least one uppercase character.'
                    ])
                if not any(char.islower() for char in password):
                    self._errors["lower"] = self.error_class([
                        'Password should have at least one lowercase character.'
                    ])
                if not any(char in specialChar for char in password):
                    self._errors["special"] = self.error_class([
                        'Password should have at least one special character.'
                    ])
                if password != passwordConfirm:
                    self._errors["passwordConfirm"] = self.error_class([
                        'Password Doesnt match'
                    ])
        print(type(self.cleaned_data))
        return self.cleaned_data

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = [
            "title",
            "secured_content",
            "password",
            "isset_Password",
        ]
    def clean(self):
        #super(NoteForm, self).clean()
        title = self.data['title']
        secured_content = self.data['secured_content']
        password = self.data['password']
        isset_Password = self.data['isset_Password']
        print("--------" + title + ' ' + secured_content + ' ' + password + ' '+ isset_Password +'---')
        
        if isset_Password == 'True':
            if len(password) < 8:
                    self._errors["password"] = self.error_class([
                        'Password length must be 8 or greater than 8 characters'
                    ])
            else:
                specialChar = ['!', '@', '#', '$', '^', '&', '*']
                if not any(char.isdigit() for char in password):
                        self._errors["digit"] = self.error_class([
                            'Password should have at least one digit.'
                        ])
                if not any(char.isupper() for char in password):
                        self._errors["upper"] = self.error_class([
                            'Password should have at least one uppercase character.'
                        ])
                if not any(char.islower() for char in password):
                        self._errors["lower"] = self.error_class([
                            'Password should have at least one lowercase character.'
                        ])
                if not any(char in specialChar for char in password):
                     self._errors["special"] = self.error_class([
                            'Password should have at least one special character.'
                        ])
      
        return self.cleaned_data
