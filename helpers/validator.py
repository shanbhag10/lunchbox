def validate_create_request(request):
    email = request['email']
    password = request['password']

    if request['first_name'] == '' or request['last_name'] == '' or email == '' or password == '':
        return False

    if len(password) < 8 or '@' not in email:
        return False

    return True
