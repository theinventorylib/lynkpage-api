from lynkpage.users.models import ClientToken


def validate_client_token(client_token) -> bool:
    try:
        token = ClientToken.objects.get(token=client_token)
        if token:
            return True
    except ClientToken.DoesNotExist:
        return False
