from rest_framework.pagination import CursorPagination

class Pagination(CursorPagination):
    page_size = 2 
    cursor_query_param = 'id_val'
    ordering = '-id'