import names
import random_address
import random
from flaskapiRequest.configurations import fileReader
from flaskapiRequest.configurations.fileReader import load_files, update_json_file


def get_first_name():
    _name = names.get_first_name()
    return _name


def get_random_address():
    _address = random_address.real_random_address()
    return _address


def get_age(min_age: int, max_age: int):
    _age = random.randint(min_age, max_age)
    return _age


def get_gender():
    random_index = random.randint(0, 1)
    if random_index == 1:
        return 'Female'
    else:
        return 'Male'


def employee_params(index=0):
    data = fileReader.load_files('payload')
    _employee_name = data[index]['name']
    _employee_id = data[index]['id']
    params = {
        "name": _employee_name,
        "id": _employee_id
    }
    return params


def get_employee_details_from_payload():
    data = fileReader.load_files('payload')
    _employee_name = data[0]['name']
    _employee_id = data[0]['id']
    _employee_age = data[0]['age']
    _employee_address = data[0]['address']
    _employee_gender = data[0]['gender']
    details = {
        "id": _employee_id,
        "name": _employee_name,
        "age": _employee_age,
        "address": _employee_address,
        "gender": _employee_gender
    }
    return details


def configure_update_employee_payload(min_age, max_age, index=0):
    """get employee id and name to update"""
    _data = load_files('payload')
    _employee_id = _data[index]['id']
    _employee_name = _data[index]['name']
    """update employee details"""
    _random_address = get_random_address()
    _employee_address = _random_address['address1']
    _employee_age = get_age(min_age, max_age)
    _gender = get_gender()
    fileReader.update_json_file(_file_name='update_payload', _id=_employee_id, _name=_employee_name,
                                _address=_employee_address, _age=_employee_age, _gender=_gender)

    data = fileReader.load_files('update_payload')
    return data


def configure_create_employee_payload(min_age, max_age, employee_id=1, index=0):
    """getting and incrementing employee id"""
    _data = load_files('payload')
    _employee_id = _data[index]['id']
    _new_employee_id = _employee_id + employee_id
    """generating random name"""
    _new_employee_name = get_first_name()
    """generating random address"""
    _new_random_address = get_random_address()
    _new_employee_address = _new_random_address['address1']
    """generating random age"""
    _new_employee_age = get_age(min_age, max_age)

    _data = update_json_file('payload', _id=_new_employee_id, _name=_new_employee_name,
                             _address=_new_employee_address, _gender='Male', _age=_new_employee_age)
    return _data
