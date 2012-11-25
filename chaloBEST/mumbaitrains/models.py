from django.contrib.gis.db import models


LINE_CHOICES = (
    ('Western', 'Western'),
    ('Central', 'Central'),
    ('Harbour', 'Harbour'),
)

class Train(models.Model):
    number = models.CharField(max_length=128)
    line = models.CharField(max_length=128, choices=LINE_CHOICES, db_index=True)    
    stations = models.ManyToManyField("Station", through='TrainStation')

    def __unicode__(self):
        return self.number

class Station(models.Model):
    name = models.CharField(max_length=128)
    point = models.PointField(null=True, blank=True)
#   line = models.CharField(choices=LINE_CHOICES, db_index=True)

    def __unicode__(self):
        return self.name

class TrainStation(models.Model):
    train = models.ForeignKey(Train)
    station = models.ForeignKey(Station)
    serial = models.IntegerField()
    time = models.TimeField()        

# Create your models here.
