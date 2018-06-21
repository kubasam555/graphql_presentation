from django.db import models


# Create your models here.


class Author(models.Model):
    MALE_TYPE = 'male'
    FEMALE_TYPE = 'female'
    GENDER_TYPES = (
        (MALE_TYPE, 'Male'),
        (FEMALE_TYPE, 'Female'),
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.CharField(max_length=1023, null=True, blank=True)
    gender = models.CharField(choices=GENDER_TYPES, default=FEMALE_TYPE,
                              max_length=31)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1023, null=True, blank=True)
    author = models.ForeignKey(Author, null=True, blank=True,
                               on_delete=models.SET_NULL, related_name='books')

    def __str__(self):
        return self.title
