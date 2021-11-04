from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from events.models import Event
from articles.models import Article

SEACH_TYPE_MAPPING = {
    'event': Event,
    'events': Event,
    'article': Article,
    'articles': Article
}

# Create your views here.
@permission_required('events.view_event')
def search_view(request):
    query = request.GET.get('q')
    search_type = request.GET.get('type')
    Klass = Event
    if search_type in SEACH_TYPE_MAPPING.keys():
        Klass = SEACH_TYPE_MAPPING[search_type]
    qs = Klass.objects.search(query=query)
    context = {
        "queryset": qs
    }
    template = "search/results-view.html"
    if request.htmx:
        context['queryset'] = qs[:5]
        template = "search/partials/results.html"
        return render(request, template, context)
    return render(request, template, context) 