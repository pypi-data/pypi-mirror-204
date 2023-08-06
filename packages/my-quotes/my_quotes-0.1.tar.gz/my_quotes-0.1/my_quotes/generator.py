import random

QUOTES = [    "The best way to predict the future is to invent it.",    "The only way to do great work is to love what you do.",    "Simplicity is the ultimate sophistication.",    "Success is not final, failure is not fatal: it is the courage to continue that counts.",    "Innovation distinguishes between a leader and a follower.",    "Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work.",    "The only source of knowledge is experience.",    "Quality is not an act, it is a habit.",    "The function of good software is to make the complex appear to be simple."]

def generate_quote():
    return random.choice(QUOTES)
