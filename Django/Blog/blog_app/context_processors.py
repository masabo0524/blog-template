from .models import Topics
from django.core.cache import cache

def topic_list(request):
    topic_list = cache.get('topics')

    if not topic_list:
        topic_list = Topics.objects.all()
        cache.set('topics', topic_list, 60 * 1)
    
    return {
        'topics': topic_list,
    }
