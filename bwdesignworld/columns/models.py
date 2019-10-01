from django.db import models

# Create your models here.

class Columns(models.Model):
    column_id = models.AutoField(primary_key=True)
    column_name = models.CharField(max_length=255)
    column_summary = models.TextField()
    column_description = models.TextField()

    class Meta:
        managed = False
        db_table = 'columns'

    def column_nameed_for_url(self):
        return self.column_name.strip().replace(' ', '-')
