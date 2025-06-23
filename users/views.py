from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from django.contrib import messages
from .models import UserRegistration, Profile
from django.contrib.auth.hashers import make_password
from posts.models import Posts
from comments.models import Comment, Notifications
from uuid import UUID
from datetime import timedelta

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


# Create your views here.
def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me')

        try:
            user = UserRegistration.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_registration_id'] = user.id

                if not remember_me:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(timedelta(days=7))
                return redirect('/')
            else:
                messages.error(request, 'Incorrect password')
        except UserRegistration.DoesNotExist:
            messages.error(request, 'Email not found')

        return redirect('login')
    else:
        return render(request, 'login.html')

def create_account_view(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if UserRegistration.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('create_account')
            else:
                user = UserRegistration.objects.create( firstname=firstname, lastname=lastname, email=email, password=make_password(password))
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Invalid Password....Make Sure Password Is Correct')
            return redirect('create_account')
            
    else:
        return render(request, 'create_account.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')

def landing_page_view(request):
    user_id = request.session.get('user_registration_id')
    posts = Posts.objects.select_related('user').order_by('-created_at')
    sort = request.GET.get('sort', 'all')

    for post in posts:
        post.comments_count = Comment.objects.filter(posts=post).count()
        post.likes_count = post.likes.count()
        
        if user_id:
            user = UserRegistration.objects.get(id=user_id)
            post.is_liked_by_user = post.likes.filter(id=user.id).exists()

        try:
            post.author_profile = Profile.objects.get(user=post.user)
        except Profile.DoesNotExist:
            post.author_profile = None


    
    if sort == 'popular':
        posts = sorted(posts, key=lambda p: p.likes_count, reverse=True)

    elif sort == 'hot':
        posts = sorted(posts, key=lambda p: p.comments_count, reverse=True)


    if user_id:
        user = UserRegistration.objects.get(id=user_id)

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None

        unread_count = Notifications.objects.filter(user=user_id, is_read=False).count()
        return render(request, 'landing_page.html', {
            'user': user,
            'profile' : profile,
            'posts': posts,
            'is_logged_in': True,
            'unread_notifications': unread_count,
            'sort': sort
    })
    elif user_id == None and not user_id:
        return redirect('login')
    else:
        return render(request, 'landing_page.html', {
            'posts': posts,
            'is_logged_in': False,
            'sort': sort
    })

    
def posts_details_view(request, post_id: UUID):
    user_id = request.session.get('user_registration_id')
    post_detail = get_object_or_404(Posts, id=post_id)
    comments = Comment.objects.select_related('user').filter(posts=post_detail).order_by('-created_at')
    comment_sort = request.GET.get('sort', 'all')

    post_detail.comments_count = Comment.objects.filter(posts=post_detail).count()
    post_detail.likes_count = post_detail.likes.count() 

    if user_id:
        user = UserRegistration.objects.get(id=user_id)
        post_detail.is_liked_by_user = post_detail.likes.filter(id=user.id).exists()

    try:
        post_detail.author_profile = Profile.objects.get(user=post_detail.user)
    except Profile.DoesNotExist:
        post_detail.author_profile = None

    for comment in comments:
        comment.like_count = comment.liked_by.count()
        comment.is_liked_by_user = comment.liked_by.filter(id=user.id).exists()

        if user_id:
            user = UserRegistration.objects.get(id=user_id)
            comment.is_liked_by_user = comment.liked_by.filter(id=user.id).exists()
            
        try:
            comment.author_profile = Profile.objects.get(user=comment.user)
        except Profile.DoesNotExist:
            comment.author_profile = None

    if comment_sort == 'popular':
        comments = sorted(comments, key=lambda c: c.like_count, reverse=True)

    elif comment_sort == 'hot':
        comments = sorted(comments, key=lambda c: c.like_count, reverse=True)


    if user_id:
        user = UserRegistration.objects.get(id=user_id)
        unread_count = Notifications.objects.filter(user=user_id, is_read=False).count()

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None
            
        context = {
            'user' : user,
            'profile': profile,
            'post_detail': post_detail,
            'comments': comments,
            'is_logged_in' : True,
            'unread_notifications': unread_count,
            'comment_sort': comment_sort
        }
        return render(request, 'posts_details.html', context)
    else:
        context = {
            'post_detail': post_detail,
            'comments': comments,
            'is_logged_in' : False
        }
        return render(request, 'posts_details.html', context)
    

    
def notification_view(request):
    user_id = request.session.get('user_registration_id')

    if user_id:
        user = UserRegistration.objects.get(id=user_id)

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None
        
        unread_notifications = Notifications.objects.filter(user=user_id).order_by('-created_at')
        
        for notification in unread_notifications:
            try:
                notification.author_profile = Profile.objects.get(user=notification.from_user)
            except Profile.DoesNotExist:
                notification.author_profile = None
        
        unread_count = Notifications.objects.filter(user=user, is_read=False).count()
        return render(request, 'notification.html', {
            'user': user,
            'profile' : profile,
            'is_logged_in': True,
            'notifications': unread_notifications,
            'unread_notifications': unread_count,
        })
    else:
        return render(request, 'notification.html', {
            'is_logged_in': False
        })
    

@require_POST
def mark_all_notifications_as_read(request):
    user_id = request.session.get('user_registration_id')
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    Notifications.objects.filter(user=user_id, is_read=False).update(is_read=True)    
    return JsonResponse({'success': True})

def read_notification(request, notification_id):
    user_id = request.session.get('user_registration_id')
    if not user_id:
        return redirect('login')

    try:
        notif = Notifications.objects.get(id=notification_id, user=user_id)
        notif.is_read = True
        notif.save()
        return redirect('posts_detail', post_id=notif.posts.id)
    except Notifications.DoesNotExist:
        return redirect('notification')
    
def profile_view(request, profile_id):
    current_user_id = request.session.get('user_registration_id')

    try:
        profile_user = UserRegistration.objects.get(id=profile_id)
    except UserRegistration.DoesNotExist:
        return redirect('landing_page')

    posts = Posts.objects.filter(user=profile_user).order_by('-created_at')

    for post in posts:
        post.comments_count = Comment.objects.filter(posts=post).count()
        post.likes_count = post.likes.count()

        if current_user_id:
            post.is_liked_by_user = post.likes.filter(id=current_user_id).exists()

        try:
            post.author_profile = Profile.objects.get(user=post.user)
        except Profile.DoesNotExist:
            post.author_profile = None
    try:
        viewed_profile = Profile.objects.get(user=profile_user)
    except Profile.DoesNotExist:
        viewed_profile = None

    if current_user_id:
        try:
            current_user = UserRegistration.objects.get(id=current_user_id)
        except UserRegistration.DoesNotExist:
            return redirect('login')

        try:
            current_user_profile = Profile.objects.get(user=current_user)
        except Profile.DoesNotExist:
            current_user_profile = None

        unread_count = Notifications.objects.filter(user=current_user_id, is_read=False).count()

        return render(request, 'profile.html', {
            'user': current_user,
            'profile_user': profile_user,
            'profile': current_user_profile,
            'viewed_profile': viewed_profile,
            'posts': posts,
            'is_logged_in': True,
            'unread_notifications': unread_count,
        })

    else:
        return render(request, 'profile.html', {
            'profile_user': profile_user,
            'viewed_profile': viewed_profile,
            'posts': posts,
            'is_logged_in': False
        })


def edit_profile_view(request):
    user_id = request.session.get('user_registration_id')

    if not user_id:
        return redirect('login')

    user = get_object_or_404(UserRegistration, id=user_id)
    posts = Posts.objects.filter(user=user).order_by('-created_at')

    for post in posts:
        post.comments_count = Comment.objects.filter(posts=post).count()
        post.likes_count = post.likes.count()
        
        if user_id:
            user = UserRegistration.objects.get(id=user_id)
            post.is_liked_by_user = post.likes.filter(id=user.id).exists()

        try:
            post.author_profile = Profile.objects.get(user=post.user)
        except Profile.DoesNotExist:
            post.author_profile = None

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        bio = request.POST.get('bio')
        profile_pic = request.FILES.get('image_upload', None)

        if bio:
            profile.bio = bio
        if profile_pic:
            profile.user_profile = profile_pic

        profile.save()
        return redirect('profile', profile_id=user_id)

    return render(request, 'edit_profile.html', {
        'user': user,
        'posts': posts,
        'profile': profile,
        'is_logged_in': True,
    })

def settings_view(request):
    user_id = request.session.get('user_registration_id')
    
    if user_id:
        user = UserRegistration.objects.get(id=user_id)

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None

        unread_count = Notifications.objects.filter(user=user_id, is_read=False).count()


        if request.method == "POST":
            form_type = request.POST.get("form_type")

            if form_type == 'firstname':
                user.firstname = request.POST.get('firstname')
                user.save()
            elif form_type == 'lastname':
                user.lastname = request.POST.get('lastname')
                user.save()
            elif form_type == 'email':
                user.email = request.POST.get('email')
                user.save()
                return redirect('login')
            elif form_type == 'bio' and profile:
                profile.bio = request.POST.get('bio')
                profile.save()
            elif form_type == 'delete_account':
                if profile:
                    profile.delete()
                user.delete()
                request.session.flush()
                return redirect('login')
                
            return redirect('settings')


        return render(request, 'settings.html', {
            'user': user,
            'profile': profile,
            'unread_notifications': unread_count,
            'is_logged_in': True
        })
    
    else:
        return render(request, 'settings.html', {
            'is_logged_in': False
        })
    
@csrf_exempt
def toggle_like(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        user_id = request.session.get("user_registration_id")

        if not user_id:
            return JsonResponse({'error': 'Not logged in'}, status=403)

        try:
            post = Posts.objects.get(id=post_id)
            user = UserRegistration.objects.get(id=user_id)

            if user in post.likes.all():
                post.likes.remove(user)
                liked = False
            else:
                post.likes.add(user)
                liked = True

            return JsonResponse({
                'liked': liked,
                'likes_count': post.total_likes()
            })

        except Posts.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
        

@csrf_exempt
@require_POST
def toggle_comment_like(request):
    user_id = request.session.get('user_registration_id')
    if not user_id:
        return JsonResponse({'error': 'User not logged in'}, status=401)

    comment_id = request.POST.get('comment_id')
    if not comment_id:
        return JsonResponse({'error': 'Missing comment ID'}, status=400)

    try:
        user = UserRegistration.objects.get(id=user_id)
        comment = Comment.objects.get(id=comment_id)
    except (UserRegistration.DoesNotExist, Comment.DoesNotExist):
        return JsonResponse({'error': 'Invalid user or comment'}, status=404)

    if user in comment.liked_by.all():
        comment.liked_by.remove(user)
        liked = False
    else:
        comment.liked_by.add(user)
        liked = True

    like_count = comment.liked_by.count()

    return JsonResponse({'liked': liked, 'like_count': like_count})

def popular_view(request):
    user_id = request.session.get('user_registration_id')
    posts = Posts.objects.select_related('user').order_by('-created_at')
    sort = request.GET.get('sort', 'popular')

    for post in posts:
        post.comments_count = Comment.objects.filter(posts=post).count()
        post.likes_count = post.likes.count()
        
        if user_id:
            user = UserRegistration.objects.get(id=user_id)
            post.is_liked_by_user = post.likes.filter(id=user.id).exists()

        try:
            post.author_profile = Profile.objects.get(user=post.user)
        except Profile.DoesNotExist:
            post.author_profile = None

    
    if sort == 'popular':
        posts = sorted(posts, key=lambda p: p.likes_count, reverse=True)

    elif sort == 'hot':
        posts = sorted(posts, key=lambda p: p.comments_count, reverse=True)

    if user_id:
        user = UserRegistration.objects.get(id=user_id)

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None

        unread_count = Notifications.objects.filter(user=user_id, is_read=False).count()
        return render(request, 'landing_page.html', {
            'user': user,
            'profile' : profile,
            'posts': posts,
            'is_logged_in': True,
            'unread_notifications': unread_count,
            'sort': sort
    })
    else:
        return render(request, 'landing_page.html', {
            'posts': posts,
            'is_logged_in': False,
            'sort': sort
    })


def hot_view(request):
    user_id = request.session.get('user_registration_id')
    posts = Posts.objects.select_related('user').order_by('-created_at')
    sort = request.GET.get('sort', 'hot')

    for post in posts:
        post.comments_count = Comment.objects.filter(posts=post).count()
        post.likes_count = post.likes.count()
        
        if user_id:
            user = UserRegistration.objects.get(id=user_id)
            post.is_liked_by_user = post.likes.filter(id=user.id).exists()

        try:
            post.author_profile = Profile.objects.get(user=post.user)
        except Profile.DoesNotExist:
            post.author_profile = None

    
    if sort == 'popular':
        posts = sorted(posts, key=lambda p: p.likes_count, reverse=True)

    elif sort == 'hot':
        posts = sorted(posts, key=lambda p: p.comments_count, reverse=True)

    if user_id:
        user = UserRegistration.objects.get(id=user_id)

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None

        unread_count = Notifications.objects.filter(user=user_id, is_read=False).count()
        return render(request, 'landing_page.html', {
            'user': user,
            'profile' : profile,
            'posts': posts,
            'is_logged_in': True,
            'unread_notifications': unread_count,
            'sort': sort
    })
    else:
        return render(request, 'landing_page.html', {
            'posts': posts,
            'is_logged_in': False,
            'sort': sort
    })


def about_us_view(request):
    user_id = request.session.get('user_registration_id')

    if user_id:
        user = UserRegistration.objects.get(id=user_id)

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None

        unread_count = Notifications.objects.filter(user=user_id, is_read=False).count()

        return render(request, 'about_us.html', {
            'user': user,
            'profile': profile,
            'is_logged_in': True,
            'unread_notifications': unread_count
        })
    else:
        return render(request, 'about_us.html', {
            'is_logged_in': False,
        })