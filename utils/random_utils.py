import random
import requests


def get_random_fact():
    """Получение случайного факта"""
    try:
        url = 'https://uselessfacts.jsph.pl/random.json?language=en'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['text']
        else:
            return "Could not fetch a fact right now."
    except Exception as e:
        print(f"Error fetching fact: {str(e)}")
        return "Error fetching fact."


def get_random_joke():
    """Получение случайной шутки"""
    try:
        url = 'https://official-joke-api.appspot.com/random_joke'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return f"{data['setup']} - {data['punchline']}"
        else:
            return "Could not fetch a joke right now."
    except Exception as e:
        print(f"Error fetching joke: {str(e)}")
        return "Error fetching joke."


def get_random_photo():
    """Получение случайного фото"""
    return f'https://picsum.photos/200/300?random={random.randint(1, 1000)}'


def get_random_motivation():
    """Получение случайной мотивационной цитаты"""
    try:
        url = 'https://zenquotes.io/api/random'
        response = requests.get(url)
        if response.status_code == 200:
            quotes = response.json()
            random_quote = random.choice(quotes)
            return random_quote['q']
        else:
            return "Could not fetch motivation right now."
    except Exception as e:
        print(f"Error fetching motivation: {str(e)}")
        return f"Error fetching motivation: {str(e)}"
