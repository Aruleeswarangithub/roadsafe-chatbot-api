import datetime
import random

user_preferences = {
    "default": ["fuel", "cafe"]
}

greetings_by_time = {
    "morning": [
        "Good morning! 😊 I’m Sandy, ready to help.",
        "Rise and shine! 😊 I’m Sandy, ready to help you today.",
        "Morning driver! How can I assist you on your journey?"
    ],
    "afternoon": [
        "Good afternoon! I'm Sandy. Need any help?",
        "Hey! I’m always ready to guide you through the journey.",
        "Hope you're having a great day! I'm Sandy. Where to next?"
    ],
    "evening": [
        "Good evening! I'm Sandy, your travel buddy.",
        "Evening driver! Wanna check rest stops nearby?",
        "Good evening! How can I help you wind down your drive?"
    ]
}

def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 12:
        time_period = "morning"
    elif hour < 17:
        time_period = "afternoon"
    else:
        time_period = "evening"
    return random.choice(greetings_by_time[time_period])
