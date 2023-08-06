from hashlib import md5


def get_avatar_url(email: str, default="mp") -> str:
    email_hash = md5(email.strip().lower().encode("utf-8")).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?d={default}"
