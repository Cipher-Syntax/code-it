from django.shortcuts import render, redirect, get_object_or_404
from .models import Posts
from users.models import UserRegistration, Profile
from comments.models import Comment
from comments.models import Notifications
from django.contrib import messages
from uuid import UUID

# Create your views here.
def create_posts_view(request):
    user_id = request.session.get('user_registration_id')

    if user_id:
        user = UserRegistration.objects.get(id=user_id)

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None

        unread_count = Notifications.objects.filter(user=user_id, is_read=False).count()

        if request.method == "POST":
            title = request.POST.get('title', '')
            image = request.FILES.get('image_upload', None)
            description = request.POST.get('description', '')

            create = Posts.objects.create(user=user, title=title, image=image, caption=description)
            create.save()

            if create:
                messages.success(request, 'Post created successfully')
            else:
                messages.error(request, 'Failed to create posts')
                
            return redirect('create_posts')
        
            
        return render(request, 'create_posts.html', {
            'user': user,
            'profile' : profile,
            'is_logged_in': True,
            'unread_notification': unread_count
        })
    else:
        return render(request, 'create_posts.html', {
            'is_logged_in': False
    })
    
def edit_posts_view(request, posts_id: UUID):
    user_id = request.session.get('user_registration_id')
    edit_posts = get_object_or_404(Posts, id=posts_id)

    try:
        edit_posts.author_profile = Profile.objects.get(user=edit_posts.user)
    except Profile.DoesNotExist:
        edit_posts.author_profile = None

    if user_id:
        user = UserRegistration.objects.get(id=user_id)
        unread_count = Notifications.objects.filter(user=user_id, is_read=False).count()

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None

        
        if request.method == 'POST':
            edit_title = request.POST.get('edit_title', '')
            edit_caption = request.POST.get('edit_caption', '')

            if edit_title:
                edit_posts.title = edit_title

            if edit_caption:
                edit_posts.caption = edit_caption

            edit_posts.save()
            return redirect('edit_posts', posts_id=edit_posts.id)


        context = {
            'user': user,
            'profile': profile,
            'edit_posts': edit_posts,
            'is_logged_in': True,
            'unread_notifications': unread_count
        }

        return render(request, 'edit_posts..html', context)
    
    else:
        context = {
            'post_detail': edit_posts,
            'is_logged_in' : False
        }
        return render(request, 'edit_posts..html', context)
    
def delete_post_view(request, post_id: UUID):
    user_id = request.session.get('user_registration_id')
    post = get_object_or_404(Posts, id=post_id)

    if not user_id:
        return redirect('login')

    post.delete()
    messages.success(request, 'Post deleted successfully.')
    return redirect('edit_profile')
    
def search_view(request):
    user_id = request.session.get('user_registration_id')
    search = request.POST.get('search_bar', '')
    results = []

    if user_id:
        user = UserRegistration.objects.get(id=user_id)

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None

        unread_count = Notifications.objects.filter(user=user_id, is_read=False).count()

        if search:
            results = Posts.objects.filter(title__icontains=search).select_related('user').order_by('-created_at')
        else:
            results = Posts.objects.select_related('user').order_by('-created_at')

        for post in results:
            post.comments_count = Comment.objects.filter(posts=post).count()
            post.likes_count = post.likes.count()
            post.is_liked_by_user = post.likes.filter(id=user.id).exists()

            try:
                post.author_profile = Profile.objects.get(user=post.user)
            except Profile.DoesNotExist:
                post.author_profile = None

        return render(request, 'landing_page.html', {
            'user': user,
            'profile': profile,
            'is_logged_in': True,
            'unread_notifications': unread_count,
            'search': search,
            'results': results,
            'posts': [] if search else results 
        })

    else:
        return render(request, 'landing_page.html', {
            'is_logged_in': False
        })


