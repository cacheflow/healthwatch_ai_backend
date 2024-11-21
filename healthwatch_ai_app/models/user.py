from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = [
      ('medical_staff', 'Medical Staff'),
      ('inmate', 'Inmate')
    ]
    created_at = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=100, blank=True, null=False)
    last_name = models.CharField(max_length=100, blank=True, null=False)
    password = models.CharField(max_length=128, verbose_name='password')
    updated_at = models.DateTimeField(default=timezone.now) 
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    groups = models.ManyToManyField(
        Group,
        related_name="user_groups", 
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    @classmethod
    def inmates(cls):
      return cls.objects.filter(role='inmate')
   
    @classmethod
    def medical_staff(cls):
      return cls.objects.filter(role='medical_staff')

    def is_medical_staff(self):
        return self.role == 'medical_staff'

    def is_inmate(self):
        return self.role == 'inmate'