def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'username': user.username,
        'uuid': user.uuid,
        'nickname': user.nickname,
        'permission': user.permission_set
    }
