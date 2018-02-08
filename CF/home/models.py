from django.db import models

class Comments( models.Model ) :
    video_name = models.CharField( max_length = 20 )
    video_id = models.CharField( max_length = 20 )
    all_comments = models.DecimalField( max_digits = 5, decimal_places = 0)
    machine_num = models.DecimalField( max_digits = 5, decimal_places = 0)
    time = models.CharField(max_length=30)
    click = models.DecimalField( max_digits = 5, decimal_places = 0)
    def __str__(self) :
        return self.video_name