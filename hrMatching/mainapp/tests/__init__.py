from datetime import date

# valid value for employee Date of Birth
twenty_years_ago = date.today().replace(year=date.today().year - 20)

employee_data = {
    "email": "test@example.com",
    "password1": "strongpassword123",
    "password2": "strongpassword123",
    "firstname": "Mo",
    "lastname": "Soleman",
    "dateOfBirth": twenty_years_ago,
    "gender": "MALE",
    "city": "Test City",
    "phone": "1234567890",
    "education": "",
    "experience": "",
    "awards": "",
    "hobbies": "",
    "skills": "Python, Django",
    "references": "",
    "other": "",
}

company_data = {
    "email": "test@example.com",
    "password1": "strongpassword123",
    "password2": "strongpassword123",
    "name": "Test Company",
    "city": "Test City",
    "phone": "123-456-7890",
}
