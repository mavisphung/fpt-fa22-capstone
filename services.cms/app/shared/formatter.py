
def format_response(success: bool = True, status: int = 200, message: str = None, data: dict = None):
    return {
        'success': success,
        'status': status,
        'message': message,
        'data': data if data else {}
    }