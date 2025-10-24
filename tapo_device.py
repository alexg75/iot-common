from tapo import ApiClient
def get_client():
    client = ApiClient(tapo_username="alexgrimaldi@gmail.com", tapo_password="**********")
    return client