from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    
    fk_user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    user_profile_image = models.ImageField(upload_to='user_images',null=True,blank=True) 
    user_cover_image = models.ImageField(upload_to='user_images',null=True,blank=True) 
    user_about = models.TextField(max_length=500)
    def __str__(self):
        return self.fk_user_id.username

class UserEducation(models.Model):

    fk_user_profile_id = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    education_title = models.CharField(null=False,max_length=20)
    education_details = models.TextField(null=False,max_length=200)
    from_date = models.DateField(null=False)
    to_date = models.DateField(null=True)
 
    def __str__(self):
        return f'{self.fk_user_profile_id.fk_user_id.username} education: {self.education_title}'

class UserExperience(models.Model):

    fk_user_profile_id = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='user_exp')
    job_position = models.CharField(null=False,max_length=20)
    company_name = models.CharField(null=False,max_length=20)
    experience_details = models.TextField(max_length=200)
    from_date = models.DateField(null=False)
    to_date = models.DateField(null=True)
    
    def __str__(self):
        return f'{self.fk_user_profile_id.fk_user_id.username} user_exp: {self.job_position}'

class NewFeed(models.Model):
    
    fk_user_profile_id = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to='new_feed')
    post_heading = models.CharField(max_length=100)
    post_details = models.TextField(max_length=500)
    github_link = models.TextField(max_length=500)
    status = models.CharField(choices=[('Not Started','Not Started'),
                                 ('In Progress','In Progress'),
                                 ('Completed','Completed')],
                                default='Not Started',
                                max_length=15
                                )

    def __str__(self):
        return f'{self.fk_user_profile_id.fk_user_id.username} has posted "{self.post_heading}" idea.'

class Contributor(models.Model):
    fk_user_profile_id = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    fk_new_feed_id = models.ForeignKey(NewFeed,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.fk_user_profile_id.fk_user_id.username} is \
            contributing on "{self.fk_new_feed_id.post_heading}"'

class Comment(models.Model):
    comment_by = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    fk_new_feed_id = models.ForeignKey(NewFeed,on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    def __str__(self):
        return f'comment by {self.comment_by.fk_user_id.username} on "{self.fk_new_feed_id.post_heading}"'

class UserStatistic(models.Model):
    fk_user_profile_id = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    project_completed = models.IntegerField()