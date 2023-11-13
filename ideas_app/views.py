from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .models import UserEducation
from .models import UserExperience
from .models import NewFeed
from .models import Contributor
from .models import Comment
from django.db.models import Q
import urllib.parse
from notification.models import Notification
from datetime import datetime
from .serializers import idea_app_insert_comment_serializer
from .serializers import idea_app_change_status_serializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


@login_required(login_url="login")
def home(request):
    auth_user_row = request.user
    user_profile_row = UserProfile.objects.get(fk_user_id=auth_user_row.id)
    user_projects_rows = NewFeed.objects.filter(fk_user_profile_id=user_profile_row.id)
    new_feeds_list = []
    new_feeds = NewFeed.objects.all()
    for feed in new_feeds:
        usr_exp = UserExperience.objects.filter(fk_user_profile_id = feed.fk_user_profile_id.id).order_by('to_date')[0]
        project_contributors = Contributor.objects.filter(fk_new_feed_id = feed.id)
        user_sent_notifications = Notification.objects.filter(notification_from_id=user_profile_row.id)
        comments = Comment.objects.filter(fk_new_feed_id=feed.id)
        new_feeds_list.append((feed,usr_exp,project_contributors,user_sent_notifications,comments))
    
    user_projects_4_rows = user_projects_rows[:5]
    ideas_posted = len(user_projects_rows)
    num_of_user_worked_with_auth_user = 0
    
    for user_projects in user_projects_rows:
        user_worked_with_auth_user = Contributor.objects.filter(fk_new_feed_id=user_projects.id)
        num_of_user_worked_with_auth_user +=len(user_worked_with_auth_user)
    return render(
        request,"home.html",
        {'username':auth_user_row.username.capitalize(),
        'user_profile_row':user_profile_row,
        'user_projects_4_rows':user_projects_4_rows,
        'new_feeds_list':new_feeds_list,
        'ideas_posted':ideas_posted,
        'num_of_user_worked_with_auth_user':num_of_user_worked_with_auth_user,
        }
        )


@login_required(login_url="login")
def profile(request,username):
        auth_username = username
        auth_user_row = User.objects.get(username = auth_username)
        user_profile_row = UserProfile.objects.get(fk_user_id=auth_user_row.id)
        user_education_rows = UserEducation.objects.filter(fk_user_profile_id=user_profile_row.id)
        user_experience_rows = UserExperience.objects.filter(fk_user_profile_id=user_profile_row.id).order_by('-to_date')
        user_projects_rows = NewFeed.objects.filter(fk_user_profile_id=user_profile_row.id)
        user_projects_4_rows = user_projects_rows[:5]
        ideas_posted = len(user_projects_rows)
        num_of_user_worked_with_auth_user = 0
        for user_projects in user_projects_rows:
            user_worked_with_auth_user = Contributor.objects.filter(fk_new_feed_id=user_projects.id)
            num_of_user_worked_with_auth_user +=len(user_worked_with_auth_user)
            
        return render(
            request,"profile.html",
            {'username':auth_username.capitalize(),
            'user_profile_row':user_profile_row,
            'user_education_rows':user_education_rows,
            'user_experience_rows':user_experience_rows,
            'user_projects_4_rows':user_projects_4_rows,
            'ideas_posted':ideas_posted,
            'num_of_user_worked_with_auth_user':num_of_user_worked_with_auth_user,
            }
            )

@login_required(login_url="login")
def edit_profile(request):
    user_profile_row = UserProfile.objects.get(fk_user_id=request.user.id)
    user_education = UserEducation.objects.filter(fk_user_profile_id=request.user.id)
    user_experience = UserExperience.objects.filter(fk_user_profile_id=request.user.id)
    if request.method == 'POST':
        # edit personal info
        user_profile_image = request.FILES.get('user_profile_image','')
        user_cover_image = request.FILES.get('user_cover_image','')
        print('user_cover_image:',user_cover_image)
        user_about = request.POST['user_about']
        if user_profile_image == '':
            user_profile_image = user_profile_row.user_profile_image
        if user_cover_image == '':
            user_cover_image = user_profile_row.user_cover_image
        
        user_profile_row.user_profile_image = user_profile_image
        user_profile_row.user_cover_image = user_cover_image
        user_profile_row.user_about = user_about
        user_profile_row.save()

        # add new education
        new_education_title = request.POST['new_education_title']
        if new_education_title:
            new_education_details = request.POST['new_education_details']
            new_edu_from_date = datetime.strptime(request.POST['new_edu_from_date'],'%Y-%m-%d')
            new_edu_to_date = datetime.strptime(request.POST['new_edu_to_date'],'%Y-%m-%d')

            new_user_edu = UserEducation(fk_user_profile_id=user_profile_row,education_title=new_education_title,
                                        education_details=new_education_details,
                                        from_date=new_edu_from_date,to_date=new_edu_to_date)
            new_user_edu.save()
        
        # edit old education

        for education in user_education:
            old_education_title = request.POST[f'education_title_{education.id}']
            old_education_details = request.POST[f'education_details_{education.id}']
            old_edu_from_date = request.POST[f'edu_from_date_{education.id}']
            old_edu_to_date = request.POST[f'edu_to_date_{education.id}']
            education.education_title = old_education_title
            education.education_details = old_education_details
            education.from_date = datetime.strptime(old_edu_from_date,'%Y-%m-%d')
            education.to_date = datetime.strptime(old_edu_to_date,'%Y-%m-%d')
            education.save()

        # add new job
        new_exp_job_position = request.POST['new_exp_job_position']
        if new_exp_job_position:
            new_exp_company_name = request.POST['new_exp_company_name']
            new_experience_details = request.POST['new_experience_details']
            new_exp_from_date = datetime.strptime(request.POST['new_exp_from_date'],'%Y-%m-%d')
            new_exp_to_date = datetime.strptime(request.POST['new_exp_to_date'],'%Y-%m-%d')

            new_user_exp = UserExperience(fk_user_profile_id=request.user.id,job_position=new_exp_job_position,
                        company_name=new_exp_company_name,experience_details=new_experience_details,
                        from_date=new_exp_from_date,to_date=new_exp_to_date)

            new_user_exp.save()

        # edit old experience 
        for experience in user_experience:
            old_job_position = ''
            old_company_name = ''
            old_experience_details = ''
            old_exp_from_date = ''
            old_exp_to_date = ''

            old_job_position = request.POST[f'job_position_{experience.id}']
            old_company_name = request.POST[f'company_name_{experience.id}']
            old_experience_details = request.POST[f'experience_details_{experience.id}']
            old_exp_from_date = request.POST[f'exp_from_date_{experience.id}']
            old_exp_to_date = request.POST[f'exp_to_date_{experience.id}']
            
            experience.job_position = old_job_position
            experience.company_name = old_company_name
            experience.experience_details = old_experience_details
            experience.from_date = datetime.strptime(old_exp_from_date,'%Y-%m-%d')
            experience.to_date = datetime.strptime(old_exp_to_date,'%Y-%m-%d')
            experience.save()

    return render(request,'edit_profile.html',
                {'user_profile_row':user_profile_row,
                'user_education':user_education,
                'user_experience':user_experience})


@login_required(login_url="login")
def ideas(request,username):
    user = User.objects.get(username = username)
    user_profile_row = UserProfile.objects.get(fk_user_id=user.id)
    user = User.objects.get(username = username)
    auth_user_projects = NewFeed.objects.filter(fk_user_profile_id = user.id)
    auth_user_projects_list = []
    for feed in auth_user_projects:
        # usr_exp = UserExperience.objects.filter(fk_user_profile_id = feed.fk_user_profile_id.id).order_by('to_date')[0]
        project_contributors = Contributor.objects.filter(fk_new_feed_id = feed.id)
        auth_user_projects_list.append((feed,project_contributors))
    return render(request,'ideas.html',
                    {"auth_user_projects_list":auth_user_projects_list,
                    'user_profile_row':user_profile_row
                    })


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            print('invalid password or username')
            messages.info(request, 'Invalid Password Or User Name')
            return redirect('login')
    else:
        return render(request, "login.html")


def logout_form(request):
    logout(request)
    return redirect('login')


def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2 :
        # and validating_password(password1)
            # if password1 == password2 and len(password1)>=2:

            if User.objects.filter(username=username).exists():

                messages.error(request, 'Username Already Registered')
                return redirect('signup')

            elif User.objects.filter(email=email).exists():

                messages.info(request, 'Email Exist')
                return redirect('signup')

            else:
                user = User.objects.create_user(
                    username=username, first_name=username, password=password1, email=email)
                user.save()
                messages.success(request, 'User Registered')
                return redirect('login')

        else:
            messages.warning(request,'Password Miss match') 
        #     messages.warning(request, 
        #                      """Password requirement:
        #                         Length > 8,
        #                         Upper case letters,
        #                         Special characters,
        #                         And
        #                         Numbers""")
            return redirect('signup')
    else:
        return render(request, "signup.html")

@login_required(login_url="login")
def search_idea(request):
    projects = []
    user_profile_row = UserProfile.objects.get(fk_user_id=request.user.id)
    if request.method == 'POST':
        project_topic = request.POST['search']
        project_ideas = NewFeed.objects.filter(post_heading__icontains=project_topic)
        for project_idea in project_ideas:
            project_contributors = Contributor.objects.filter(fk_new_feed_id = project_idea.id)
            projects.append((project_idea,project_contributors))
    if projects == []:
        projects.append(({'post_heading':'No Match'},''))

    return render(request,'search_idea.html',
                    {'projects':projects,
                    'user_profile_row':user_profile_row})

@login_required(login_url="login")    
def specific_idea(request,idea_name):
    projects = []
    idea_name = urllib.parse.unquote(idea_name)
    project_idea = NewFeed.objects.get(post_heading=idea_name)
    project_contributors = Contributor.objects.filter(fk_new_feed_id = project_idea.id)
    projects.append((project_idea,project_contributors))
    return render(request,'specific_idea.html',{'projects':projects})

@login_required(login_url="login")
def post_idea(request):
    auth_user = UserProfile.objects.get(fk_user_id=request.user.id)
    heading = request.POST.get('heading','')
    description = request.POST.get('description','')
    fileUpload = request.FILES.get('fileUpload','')
    github_link = request.POST.get('github_link','')
    if '' == heading:
        messages.warning(request,'Heading should not be empty')
    elif '' == description:
        messages.warning(request,'Description should not be empty')
    elif  '.png' not in str(fileUpload) and '.jpg' not in str(fileUpload) and '.jpeg' not in str(fileUpload):
        messages.warning(request, "File should be '.png' or '.jpg' or '.jpeg'.")
    else:
        if NewFeed.objects.filter(Q(post_heading=heading)|Q(post_details=description)).exists():
            messages.warning(request,'This idea is already exists.')
        else:
            new_project = NewFeed.objects.create(post_image=fileUpload,post_heading=heading,
                                post_details=description,github_link=github_link,fk_user_profile_id=auth_user)
            new_project.save()
            messages.info(request,'Idea posted successfully.')
    return redirect('home')

@api_view(['POST'])
def insert_comment(request):
    if request.user.is_authenticated:
        comment = request.data['comment']
        comment_by_id = request.data['comment_by_id']
        new_feed_id = request.data['new_feed_id']
        comment = {
            'comment':comment,
            'comment_by':comment_by_id,
            'fk_new_feed_id':new_feed_id
        }
        msg_srlzr = idea_app_insert_comment_serializer(data=comment)
        if msg_srlzr.is_valid():
            msg_srlzr.save()
            return Response({"msg":"comment is saved"})
        else:
            return Response({'msg':msg_srlzr.errors})
    else:
        return Response({'msg':'unauthenticated request'},403)
@api_view(['PUT'])
def update_status(request):
    if request.user.is_authenticated:
        updated_status = request.data['status']
        id = request.data['id']
        project = NewFeed.objects.get(id=id)
        status_data = {
            "status":updated_status
        }
        print(status_data)
        status_serializer = idea_app_change_status_serializer(project,data=status_data)
        if status_serializer.is_valid():
            status_serializer.save()
            return Response({"msg":"project status is changed"})
        else:
            return Response({'msg':status_serializer.errors})

    else:
        return Response({'msg':'unauthenticated request'},403)