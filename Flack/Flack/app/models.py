#from django.utils.encoding import python_2_unicode_compatible
import os
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage
fsimage = FileSystemStorage(location='media/photos')
fspdf= FileSystemStorage(location='upload/pdf')
fsfile=FileSystemStorage(location='upload/file')
#UploadImage
#FileSystemStorage

from .forms import forms
from django.db import models

"""
Definition of models.
"""


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = ModelWithFileField(file_field=request.FILES['file'])
            instance.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

class UploadPDF(models.Model):
    filename=models.CharField(max_length=100)
    pdf = models.FileField(upload_to=fspdf)
    def __str__(self):
        return self.filename
class UploadImage(models.Model):
    filename=models.CharField(max_length=100)
    upload_file = models.FileField(upload_to=fsfile)
    Image = models.ImageField(storage=fsimage)
    UploadPDF=models.FileField(upload_to=fspdf)
    def __str__(self):
        return self.filename

class Domain(models.Model):
    domainname = models.CharField(max_length=30, default='DEFAULT', unique=False)
    fullurlname = models.CharField(max_length=65, default='DEFAULT', unique=False)
    upload_file = models.FileField(upload_to=fsfile)
    Image = models.ImageField(storage=fsimage)
    UploadPDF=models.FileField(upload_to=fspdf)
    def __str__(self):
        return f"{self.id} - Domain: {self.domainname} DNS: {self.fullurlname}"
class DomainChannel(models.Model):
    domainchannelname = models.CharField(max_length=30, default='DEFAULT')
    fullurlname = models.CharField(max_length=65, default='DEFAULT')
    domain= models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="domainchannels")
    upload_file = models.FileField(upload_to=fsfile)
    Image = models.ImageField(storage=fsimage)
    UploadPDF=models.FileField(upload_to=fspdf)
    def __str__(self):
        return f"{self.id} - Channel: {self.domainchannelname} DNS: {self.fullurlname}"
class DomainChannelSetting(models.Model):
    LAYOUTS=(('DEFAULT','Default'), ('VERTICAL','Vertical'),('HORIZONTAL','Horizontal'))
    THEMES=(
            ('DEFAULT','Default'),
            ('green','Forest'),
            ('orange','Fruity'),
            ('springgreen','Limey'),
            ('blue','Cold'),
            ('red','Hot'),
            ('yellow','Sunny'),
            ('spaceinvaders','Space Invaders Game'),
            ('pacman','PacMan Game'),
            ('chess','MultiUser Chess Game'),
            ('adventure','MultiUser Adventure Game'),
            ('TI','TI Games'))
    theme=models.CharField(max_length=30,choices=THEMES, default='DEFAULT')
    layout=models.CharField(max_length=30,choices=LAYOUTS, default='DEFAULT')
    upload_file = models.FileField(upload_to=fsfile)
    Image = models.ImageField(storage=fsimage)
    UploadPDF=models.FileField(upload_to=fspdf)
    domainchannel= models.ForeignKey(DomainChannel, on_delete=models.CASCADE, related_name="domainchannelsettings")
    def __str__(self):
        return f"{self.id} - Theme:{self.theme} Layout: {self.layout}"

    class UserSetting(models.Model):
        YES_NO=( ('Y','Yes'),
                 ('y','Yes'),
                 ('N','No'),
                 ('n','No'))
        LAYOUTS=(('DEFAULT','Default'),('VERTICAL','Vertical'),('HORIZONTAL','Horizontal'))
        THEMES=(
            ('DEFAULT','Default'),
            ('green','Forest'),
            ('orange','Fruity'),
            ('springgreen','Limey'),
            ('blue','Cold'),
            ('red','Hot'),
            ('yellow','Sunny'),
            ('spaceinvaders','Space Invaders Game'),
            ('pacman','PacMan Game'),
            ('chess','MultiUser Chess Game'),
            ('adventure','MultiUser Adventure Game'),
            ('TI','TI Games'))
        upload_file = models.FileField(upload_to=fsfile)
        Image = models.ImageField(storage=fsimage)
        UploadPDF=models.FileField(upload_to=fspdf)
        theme1=models.CharField(max_length=30,choices=THEMES, default='DEFAULT')
        layout1=models.CharField(max_length=30,choices=LAYOUTS,default='DEFAULT')
        theme2=models.CharField(max_length=30,choices=THEMES, default='DEFAULT')
        layout2=models.CharField(max_length=30,choices=LAYOUTS,default='DEFAULT')
        usermonitor =  models.CharField(max_length=2,choices=YES_NO,default='N')
        useradmin =  models.CharField(max_length=2,choices=YES_NO,default='N')
        gameadmin =  models.CharField(max_length=2,choices=YES_NO,default='N')
        domainrestriction =  models.CharField(max_length=2,choices=YES_NO,default='N')
        domainchannelrestriction =  models.CharField(max_length=2,choices=YES_NO,default='N')
        messagerestriction =  models.CharField(max_length=2,choices=YES_NO,default='N')
        agerestriction =  models.CharField(max_length=2,choices=YES_NO,default='N')
        flagged =  models.CharField(max_length=2,choices=YES_NO,default='N')
        user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="usersettings")
        domainchannels = models.ManyToManyField(DomainChannel, blank=True, related_name="manytomanydomainchannelusers")
#        domains= models.ManyToManyField(Domain, on_delete=models.CASCADE, related_name="manytomanydomainusers")
        domains= models.ManyToManyField(Domain, related_name="manytomanydomainusers")
    def __str__(self):
        return f"{self.id} - Theme1:{self.theme1} Theme2: {self.theme2} Layout1: {self.layout1} Layout2: {self.layout2}"
  
    class UserMessage(models.Model):
        MESSAGE_CODES=(
                   ('DEFAULT','Default Message'),
                   ('GENERALMSG','General Message'),
                   ('ATTACHMENTMSG','Attachments Message'),
                   ('RESPONSEMSG','Response Message'),
                   ('HAPPYFACEMSG','HAPPY FACE Message'),
                   ('SADFACEMSG','SAD FACE Message'),
                   ('IMOGIMSG','IMOGI Message'),
                   ('HTMLMSG','HTML Message'),
                   ('PDFMSG','PDF Message'),
                   ('IMAGEMSG','IMAGE Message'),
                   ('FLAGMSG','FLAG Message'),
                   ('CREATEGAMEPACMAN','Create A PACMAN Game'),
                   ('ASSIGNGAMEPACMAN','Assign User to a PACMAN Game'),
                   ('STARTGAMEPACMAN','Start PACMAN Game'),
                   ('RESTARTGAMEPACMAN','ReStart PACMAN Game'),
                   ('STOPGAMEPACMAN','Stop PACMAN Game'),
                   ('UPDATEGAMEPACMAN','Update PACMAN Game'),
                   ('DELETEGAMEPACMAN','Delete PACMAN Game'),
                   ('CREATEGAMECHESS','Create A CHESS Game'),
                   ('ASSIGNGAMECHESS','Assign User to a CHESS Game'),
                   ('STARTGAMECHESS','Start CHESS Game'),
                   ('RESTARTGAMECHESS','ReStart CHESS Game'),
                   ('STOPGAMECHESS','Stop CHESS Game'),
                   ('UPDATEGAMECHESS','Update CHESS Game'),
                   ('DELETEGAMECHESS','Delete CHESS Game'),
                   ('CREATEGAMESPACEINVADERS','Create A TI99 SPACE INVADERS Game'),
                   ('ASSIGNGAMESPACEINVADERS','Assign User to a TI99 SPACE INVADERS Game'),
                   ('STARTGAMESPACEINVADERS','Start TI99 SPACE INVADERS Game'),
                   ('RESTARTGAMESPACEINVADERS','ReStart TI99 SPACE INVADERS Game'),
                   ('STOPGAMESPACEINVADERS','Stop TI99 SPACE INVADERS Game'),
                   ('UPDATEGAMESPACEINVADERS','Update TI99 SPACE INVADERS Game'),
                   ('DELETEGAMESPACEINVADERS','Delete TI99 SPACE INVADERS Game'),
                   ('CREATETASK','Create A Task'),
                   ('ASSIGNTASK','Assign User to a Task'),
                   ('UPDATETASK','Update Task'),
                   ('DELETETASK','Delete Task'),
                   ('NEWPROJECT','Create A Project'),
                   ('ASSIGNPROJECT','Assign A Project'),
                   ('UPDATEPROJECT','Update A Project'),
                   ('DELTEPROJECT','Delete A Project'),
                   ('PRIVATEMSG','Private Message'),
                   ('ALLINTHISDOMAINCHANNELMSG','All in this Domain Channel Message'),
                   ('ALLINTHISDOMAINMSG','All in this Domain Message'),
                   ('ALLDOMAINSMSG','All Domains Message'))
        created = models.DateTimeField(auto_now_add=True)
        upload_file = models.FileField(upload_to=fsfile)
        Image = models.ImageField(storage=fsimage)
        UploadPDF=models.FileField(upload_to=fspdf)
        code = models.CharField(max_length=30,choices=MESSAGE_CODES,default='DEFAULT')
        note = models.CharField(max_length=200, default='no entry')
        senttodomain= models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="senttodomainmessages")
        senttodomainchannel= models.ForeignKey(DomainChannel, on_delete=models.CASCADE, related_name="senttodomainchannelmessages")
        senttouser= models.ForeignKey(User, on_delete=models.CASCADE, related_name="senttomessages")
        user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="usermessages")
    def __str__(self):
        return f"{'id': {self.id}, 'created': {created}, 'upload_file': {upload_file}, 'Image': {Image}, 'UploadPDF': {UploadPDF},'code': {self.code},'note': {self.note}}"
