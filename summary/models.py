from django.db import models

# Create your models here.


class Upload_Pdf(models.Model):
    title=models.CharField(max_length=100,default=None)
    file=models.FileField(upload_to='pdf/')
    
    
    def __str__(self):
        return f'{self.title}'