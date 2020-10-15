from django.db import models
import re
import bcrypt

# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def validator(self,postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid Email Address'
        email_check = self.filter(email=postData['email'])
        if email_check:
            errors['email'] = "Email already in use"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData['password2']:
            errors['password'] = 'Passwords do not match'
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, postData):
        pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = pw,
        )
  


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Message(models.Model):
    message = models.CharField(max_length=255) 
    user = models.ForeignKey(User, related_name="user_has_messages",on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment = models.CharField(max_length=255)
    message = models.ForeignKey(Message, related_name="message_has_comments",on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_has_comments",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)






    



