from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    mdp = models.CharField(max_length=255)

    def __str__(self):
        return "user nom:{} prenom:{}".format(self.name, self.prenom)

class Topic(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return "nom topic : {}".format(self.nom)

class Messages(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return "contenu message : {}".format(self.message)
