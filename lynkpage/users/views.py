from lynkpage.users.models import ClientToken


def validate_client_token(client_token):
    try:
        token = ClientToken.objects.get(token=client_token)
        if token:
            return True
        else:
            return False
    except ClientToken.DoesNotExist:
        return False
