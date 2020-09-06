from django.contrib.auth.models import User
from django.db import models

CHOICES = [('Male', 'Male'), ('Female', 'Female')]


# admin_user_name= admin
# admin_password = Admin@123

def increment_card_number():
    last_card_number = Patient.objects.all().order_by('id').last()
    if last_card_number:
        return 'CN-' + format(last_card_number.id + 1, '04d')
    else:
        return 'CN-' + format(1, '04d')


class Patient(models.Model):
    card_number = models.CharField(max_length=20, default=increment_card_number, editable=False)
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    middle = models.CharField(max_length=64)
    gender = models.CharField(max_length=20, choices=CHOICES, default=CHOICES[1])
    age = models.PositiveIntegerField()
    phone = models.IntegerField()
    address = models.CharField(max_length=64, default="")
    created_date = models.DateField(auto_now_add=True)
    appointment = models.DateField(blank=True)

    created_by = models.ForeignKey(User, default=None, on_delete=models.PROTECT,
                                   related_name="creator")
    updated_by = models.ForeignKey(User, default=None, on_delete=models.PROTECT,
                                   related_name="editor")

    def __str__(self):
        return f'{self.card_number} | {self.first} | {self.last} | {self.created_date}'

    class Meta:
        ordering = ['-id']
