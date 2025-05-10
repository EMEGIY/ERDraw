from faker import Faker
from faker.providers import BaseProvider
import random
from data import book_title, cs_fields


class additional_attributes(BaseProvider):
    def annual_salary(self):
        return random.randint(30,200) * 1000
    def age(self, min=1, max=110):
        return random.randint(min, max)
    def book_title(self):
        return random.choice(book_title)
    def number_of_pages(self):
        return random.randint(10, 500)
    def cs_field(self):
        return random.choice(cs_fields)
    def german_date(self, year_min=1980, year_max=2024,):
        return f"{random.randint(1,31)}-{random.randint(1,12)}-{random.randint(year_min, year_max)}"

def get(region=["de_DE"]):
    generator = Faker(region)
    generator.add_provider(additional_attributes)
    return generator

if __name__ == '__main__':
    gen = get()
    print(gen.date())