import generator

def get():
    gen = generator.get()

    return {
        "name": gen.name,
        "first name": gen.first_name,
        "last name": gen.last_name,
        "prefix": gen.prefix,
        "suffix": gen.suffix,
        "address": gen.address,
        "street adress": gen.street_address,
        "book title": gen.book_title,
        "cs_field": gen.cs_field,
        "annual_salary": gen.annual_salary,
        "date": gen.date,
        "pages": gen.number_of_pages,
        "id": gen.uuid4,
        "salary": gen.annual_salary
    }