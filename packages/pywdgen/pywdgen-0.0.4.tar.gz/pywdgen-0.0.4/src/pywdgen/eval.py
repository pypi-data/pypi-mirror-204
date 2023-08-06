import re


def password_strength(password: str) -> int:
    score = 0

    # Longueur
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1

    # Complexité
    if re.search("[a-z]", password) and re.search("[A-Z]", password):
        score += 1
    if re.search("[0-9]", password):
        score += 1
    if re.search("[@#$%^&+=]", password):
        score += 1
    if re.search("[^a-zA-Z0-9@#$%^&+=]", password):
        score += 1

    # Variation
    if len(set(password)) >= 10:
        score += 1
    if len(set(password)) >= 15:
        score += 1
    if len(set(password)) >= 20:
        score += 1

    return score
