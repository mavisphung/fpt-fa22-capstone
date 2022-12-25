import asyncio
from django.utils.decorators import sync_and_async_middleware
from django.middleware.common import CommonMiddleware

@sync_and_async_middleware
def authentication_middleware(get_response):
    # One-time configuration and initialization goes here.
    if asyncio.iscoroutinefunction(get_response):
        async def middleware(request):
            # Do something here!
            print('----- authentication_middleware invoked -----')
            response = await get_response(request)
            return response

    else:
        def middleware(request):
            # Do something here!
            print('----- authentication_middleware invoked -----')
            response = get_response(request)
            return response

    return middleware