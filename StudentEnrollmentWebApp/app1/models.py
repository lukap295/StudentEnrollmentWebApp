from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class User(AbstractUser):
    ROLES = (('admin', 'administrator'), ('prof', 'profesor'), ('stu', 'student'))
    STATUS = (('izv', 'izvanredni student'), ('red', 'redovni student'))
    status = models.CharField(max_length=20, choices=STATUS, default='none') 
    role = models.CharField(max_length=20, choices=ROLES, default='stu')
    enrolled_subjects = models.ManyToManyField('Predmeti', through='Enrollment', related_name='enrolled_students')

    def save(self, *args, **kwargs):
        # If role is 'prof' or 'admin', set status to 'None'
        if self.role in ['prof', 'admin']:
            self.status = 'None'
        super().save(*args, **kwargs)

class Predmeti(models.Model):
    IZBORNI = (('da', 'da'), ('ne', 'ne'))
    Ime = models.CharField(max_length=50)
    Kod = models.CharField(max_length=50)
    Program = models.CharField(max_length=50)
    ECTS = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    izborni = models.CharField(max_length=50, choices=IZBORNI)
    nositelj = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s' % (self.IZBORNI, self.Ime, self.Kod, self.Program, self.ECTS, self.sem_red, self.sem_izv, self.izborni, self.nositelj)


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('pass', 'Passed'),
        ('fail', 'Failed'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.subject.name} - Status: {self.get_status_display()}"
#Kad minjan model onda python manage.py makemigrations i onda python manage.py migrate