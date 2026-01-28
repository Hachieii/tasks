import requests

def check_success(response):
    return "Congratulations, you solved the lab!" in response