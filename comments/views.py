from django.shortcuts import redirect, render, get_object_or_404

from users.models import UserRegistration
from posts.models import Posts
from .models import Comment

# Create your views here.
def comments_view(request):
    comments = Comment.objects.all()
    return render(request, 'posts_details.html', {'comments' : comments})

def create_comment(request):
    if request.method == "POST":
        comment_input = request.POST.get('comment_input', '')
        image = request.FILES.get('image_upload', None)
        gif = request.FILES.get('gif_upload', None)

        user_id = request.session.get('user_registration_id')
        user = get_object_or_404(UserRegistration, id=user_id)

        post_id = request.POST.get('post_id')
        post = get_object_or_404(Posts, id=post_id)

        Comment.objects.create(
            user=user,
            posts=post,
            comments=comment_input,
            image=image,
            gif=gif
        )

        return redirect('posts_detail', post_id=post.id)

    else:
        comments = Comment.objects.all()
        return render(request, 'posts_details.html', {'comments': comments})
