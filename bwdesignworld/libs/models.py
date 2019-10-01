from django.db import models

# Create your models here.
class Contactus(models.Model):
    contact_id = models.AutoField(db_column='contact_Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=100)
    email_id = models.CharField(db_column='email_Id', max_length=100)  # Field name made lowercase.
    purpose = models.CharField(max_length=50)
    comment = models.TextField()
    contact_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'contactus'

class SearchIndexingTbl(models.Model):
    id = models.AutoField(primary_key=True)  # Field name made lowercase.
    tbl_name = models.CharField(max_length=100)
    last_inserted_index_id = models.IntegerField()
    updated_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'search_indexing_tbl'

