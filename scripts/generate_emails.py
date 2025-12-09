import random
import string

# Список популярных и реально существующих доменов
REAL_DOMAINS = [
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "yandex.ru",
    "mail.ru", "protonmail.com", "icloud.com", "aol.com", "gmx.com",
    "ukr.net", "inbox.ru", "list.ru", "bk.ru", "live.com",
    "example.com", "test.org",
]

# Список "липовых" TLD и корней — заведомо несуществующих
FAKE_TLDS = ["zz", "xx", "yy", "fake", "invalid", "testtld", "nop", "xyz123", "local", "internal", ""]
FAKE_PREFIXES = ["fake", "nonexistent", "bogus", "dummy", "trash", "tempmail", "spam", "bad", "wrong", "error"]

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_emails(total=1000, real_ratio=0.6):
    emails = []
    real_count = int(total * real_ratio)
    fake_count = total - real_count

    # Генерация валидных email
    for _ in range(real_count):
        local = random_string(random.randint(5, 12))
        domain = random.choice(REAL_DOMAINS)
        emails.append(f"{local}@{domain}")

    # Генерация липовых email
    for _ in range(fake_count):
        local = random_string(random.randint(5, 12))
        prefix = random.choice(FAKE_PREFIXES)
        tld = random.choice(FAKE_TLDS)
        domain = f"{prefix}{random.randint(1, 9999)}.{tld}"
        emails.append(f"{local}@{domain}")

    for _ in range(fake_count):
        local = random_string(random.randint(5, 12))
        emails.append(f"{local}")

    return emails


def create_file(filename: str):
    emails = generate_emails(1000)
    with open(filename, "w", encoding="utf-8") as f:
        for email in emails:
            f.write(email + "\n")


if __name__ == "__main__":
    create_file("emails_1000.txt")
    print("Сгенерировано 1000 email-адресов → emails_1000.txt")
