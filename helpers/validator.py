import re

def validate_create_request(request):
    email = request['email']
    password = request['password']

    if request['first_name'] == '' or request['last_name'] == '' or email == '' or password == '':
        return False

    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if len(password) < 8 or not re.search(regex, email):
        return False

    return True
