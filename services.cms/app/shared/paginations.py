from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.paginator import Paginator
from myapp.settings import PAGE_SIZE
from shared.response_messages import ResponseMessage

class CustomPageNumberPagination(PageNumberPagination):
    page_size = PAGE_SIZE or 10
    page_query_param = 'page'
    
def get_paginated_data(
    success: bool = False, 
    status: int = 200, 
    message: str = None,
    totalItems: int = 0,
    nextPage: int = None,
    previousPage: int = None,
    currentPage: int = 0,
    totalPages: int = 0,
    limit: int = 10,
    data = None
):
    return {
        'success': success,
        'status': status,
        'message': message,
        'totalItems': totalItems,
        'nextPage': nextPage,
        'previousPage': previousPage,
        'currentPage': currentPage,
        'totalPages': totalPages,
        'limit': limit,
        'data': data if isinstance(data, dict) or isinstance(data, list) else []
    }
def get_paginated_response(ret_list, page_number: int, limit: int, serializer_class = None):
    paginator = Paginator(ret_list, limit) # new one Paginator instance
    page = paginator.get_page(page_number) # get page
    if serializer_class:
        serializer = serializer_class(page, many = True) # serialize page
    response = get_paginated_data(
        success = True,
        status = 200,
        message = ResponseMessage.GET_DATA_SUCCEEDED,
        limit = paginator.per_page,
        totalItems = paginator.count,
        totalPages = paginator.num_pages,
        currentPage = page_number,
        nextPage = page_number + 1 if page.has_next() else None,
        previousPage = page_number - 1 if page.has_previous() else None,
        data = serializer.data if serializer_class else page.object_list
    )
    return Response(response, response.get('status'))