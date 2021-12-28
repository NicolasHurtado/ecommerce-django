from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class CuentaAdministrador(BaseUserManager):
    def create_user(self, nombre, apellido, email, username, password=None):
        if not email:
            raise ValueError('El usuario debe tener un Email')
        
        if not username:
            raise ValueError('El usuario debe tener un username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            nombre = nombre,
            apellido = apellido,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, nombre, apellido, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            nombre = nombre,
            apellido = apellido,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user







class Cuenta(AbstractBaseUser):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    celular = models.CharField(max_length=50)

    # Campos atributos de django
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nombre', 'apellido']

    objects = CuentaAdministrador()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    
