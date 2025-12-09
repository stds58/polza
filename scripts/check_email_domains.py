"""
1. Проверка email-доменов

Написать простой скрипт на Python, который:

• принимает список email-адресов;
• проверяет наличие MX-записей домена;
• выводит статус для каждого адреса:

– «домен валиден»;
– «домен отсутствует»;
– «MX-записи отсутствуют или некорректны».

Формат: один .py-файл + короткая инструкция по запуску.

python -m scripts.check_email_domains
"""
import asyncio
import aiodns
from typing import List
from pydantic import BaseModel, EmailStr, ValidationError, computed_field
from scripts.generate_emails import create_file


class SchemaEmailBase(BaseModel):
    email: EmailStr

    @computed_field
    @property
    def domain(self) -> str:
        return self.email.split('@')[1]


class SchemaResponse(BaseModel):
    email: str
    format_valid: bool = None
    mx_status: str = None


async def is_valid_mx(domain: str, resolver: aiodns.DNSResolver) -> bool:
    try:
        mx_records = await resolver.query(domain, "MX")
        if mx_records:
            return True
        return False
    except (aiodns.error.DNSError, Exception):
        return False


async def validate_single_email(email_str: str, resolver: aiodns.DNSResolver) -> SchemaResponse:
    response = SchemaResponse(email=email_str)
    try:
        obj = SchemaEmailBase(email=email_str)
        mx_records = await is_valid_mx(obj.domain, resolver)
        if mx_records:
            response.mx_status = "домен валиден"
            response.format_valid = True
        else:
            response.mx_status = "MX-записи отсутствуют или некорректны"
            response.format_valid = False
    except aiodns.error.DNSError:
        response.mx_status = "MX-записи отсутствуют или некорректны"
        response.format_valid = False
    except ValidationError as e:
        error_detail = e.errors()[0]
        error_msg = error_detail.get("msg", "").lower()
        if any(phrase in error_msg for phrase in ["must have an @-sign", "there must be something after the @-sign"]):
            response.mx_status = "домен отсутствует"
        else:
            response.mx_status = "MX-записи отсутствуют или некорректны"
        response.format_valid = False

    finally:
        return response


async def validate_email(emails: List[str]) -> List[SchemaResponse]:
    unique_emails = list(set(emails))
    resolver = aiodns.DNSResolver(nameservers=["8.8.8.8", "1.1.1.1"])
    tasks = [validate_single_email(email, resolver) for email in unique_emails]
    results = []

    for coro in asyncio.as_completed(tasks):
        result = await coro
        results.append(result)
        print(f"{result.email}: {result.mx_status}")

    return results
    

def get_emails(filename: str):
    try:
        create_file("emails_1000.txt")
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        emails = [line.strip() for line in lines if line.strip()]
        return emails
    except FileNotFoundError:
        return ("Файл %s не найден" % filename)


if __name__ == "__main__":
    emails = get_emails("emails_1000.txt")
    report = asyncio.run(validate_email(emails))
