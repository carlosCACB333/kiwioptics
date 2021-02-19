from django.db.models.query import QuerySet
from django.db.models import Q

def django_admin_keyword_search(model, keywords, search_fields):
    all_queries = None

    for keyword in keywords.split(' '):  
        keyword_query = None

        for field in search_fields:
            each_query = Q(**{field+'__icontains':keyword})

            if not keyword_query:
                keyword_query = each_query
            else:
                keyword_query = keyword_query | each_query

        if not all_queries:
            all_queries = keyword_query
        else:
            all_queries = all_queries & keyword_query

    result_set = model.objects.filter(all_queries).distinct()

    return result_set