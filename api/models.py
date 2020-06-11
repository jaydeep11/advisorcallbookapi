from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Create and return a `User` with an email, and password.
        """
        if not email:
            raise ValueError('Users Must Have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name= name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,name, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, name,password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )
    name = models.CharField(max_length=100 ,default="Name")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

class Advisor(models.Model):
    advisor_name = models.CharField(max_length=255,default="name")
    advisor_photo_url = models.ImageField(upload_to='pictures/%Y/%m/%d/',max_length=255,null=True)

    def __str__(self):
        return self.advisor_name

class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    advisor=models.ForeignKey(Advisor,on_delete=models.CASCADE)
    time=models.DateTimeField()

    def __str__(self):
        return self.user.name +" "+self.advisor.advisor_name+" "+str(self.time)