from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NONUM_REGEX = re.compile(r'^([^0-9]*)$')
UPNUM_REGEX = re.compile(r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])')

# Create your models here.
class UserManager(models.Manager):
    def UserRegisterValidator(self,data,session):
        errors = {}
        if len(data['email']) < 1:
            errors['regemail'] = "Please enter Email."
        elif not EMAIL_REGEX.match(data['email']):
            errors['regemail'] = "Invalid Email Address!"
        elif User.objects.filter(email=data['email']):
            errors['regemail'] = "Account already exists."
        if len(data['first_name']) < 2:
            errors['first_name'] = "Please enter valid First Name."
        elif not NONUM_REGEX.match(data['first_name']):
            errors['first_name'] = "You cannot have number(s) in your name."
        if len(data['last_name']) < 2:
            errors['last_name'] = "Please enter valid Last Name."
        elif not NONUM_REGEX.match(data['last_name']):
            errors['last_name'] = "You cannot have number(s) in your name."
        if len(data['password']) < 1:
            errors['regpassword'] = "Please enter Password."
        elif len(data['password']) < 8:
            errors['regpassword'] = "Password must be 8 characters or longer."
        elif not UPNUM_REGEX.match(data['password']):
            errors['regpassword'] = "Password needs to have 1 uppercase letter, 1 lowercase and 1 number."
        elif len(data['confirm_password']) < 1:
            errors['confirmpassword'] = "Please confirm password."
        elif data['password'] != data['confirm_password']:
            errors['confirmpassword'] = "Password does not match confirmation! Please confirm password again."

        if not errors:
            password_hash = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            User.objects.create(first_name=data['first_name'], last_name=data['last_name'],
                                email=data['email'], password=password_hash, session=session)

        return errors

    def UserLoginValidator(self,data,session):
        errors = {}
        if len(data['email']) < 1:
            errors['loginemail'] = "Please enter Email."
        elif not EMAIL_REGEX.match(data['email']):
            errors['loginemail'] = "Invalid Email Address."
        elif not User.objects.filter(email=data['email']):
            errors['loginemail'] = "Please register to log in."
        if len(data['password']) < 1:
            errors['loginpassword'] = "Please enter Password."

        if not errors:
            this_user = User.objects.filter(email=data['email'])[0]
            if not bcrypt.checkpw(data['password'].encode(), this_user.password.encode()):
                errors['loginemail'] = "Invalid Email or Password."
            else:
                this_user.session = session
                this_user.save()

        return errors

    def UserSessionValidator(self,session):
        if session=="":
            return False
        else:
            this_user = User.objects.filter(session=session)
            if this_user:
                return True
            else:
                return False

    def UserLogout(self,session):
        this_user = User.objects.filter(session=session)[0]
        this_user.session = ""
        this_user.save()
        return True

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=60)
    session = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    def __repr__(self):
        return "<User: {}|{} {}>".format(self.id, self.first_name, self.last_name)

