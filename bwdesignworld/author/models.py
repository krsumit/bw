from django.db import models

# Create your models here.

class Author(models.Model):
    author_id = models.IntegerField(primary_key=True)
    author_name = models.CharField(max_length=255)
    author_photo = models.CharField(max_length=255)
    author_bio = models.TextField()
    author_type = models.IntegerField()
    column_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'author'

    def author_name_for_url(self):
        return self.author_name.strip().replace(' ', '-')

    def author_id_for_url(self):
        return self.author_id

    def get_absolute_url(self):
        author_label_val = AuthorType.objects.filter(author_type_id=self.author_type).first()
        author_label = author_label_val.label.strip().replace(' ', '-')
        author_name_for_url = self.author_name.strip().replace(' ', '-')
        return '/author/'+str(author_label)+'/'+str(author_name_for_url)+'-'+str(self.author_id)


class AuthorType(models.Model):
    author_type_id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=255)
    valid = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'author_type'

    def author_type_for_url(self):
        return self.label.strip().replace(' ', '-')