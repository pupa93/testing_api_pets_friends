from api import PetFriends
from settings import valid_email, valid_password, wrong_password, wrong_mail
import os
import pytest

class ArgumentsException (Exception):
    pass


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):

    status, result = pf.get_api_key(email, password)

    # checking result of req
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='Suslik',
                                     age='4', pet_photo='images/suslik.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/suslik.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


#  Здесь будут мои тесты

def test_add_photo_of_pet_meth(pet_photo='images/suslik.jpg'):
    # add new photo to existed pet
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    print(auth_key)

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("There is no my pets")


def test_get_api_key_with_empty_email(email='', password=valid_password):
    # запрос api ключа с пустым email возвращает статус 403
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result


def test_get_api_key_with_empty_password(email=valid_email, password=''):
    # запрос api ключа с пустым password возвращает статус 403
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result


def test_create_pet_simple_empty(name='', animal_type='', age=''):
    # проверяем что можно просто создать карточку питомца с пустыми данными
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_wrong_pass(mail=valid_email):
    # неверный пароль
    status, result = pf.get_api_key(mail, wrong_password)
    assert status == 403
    assert 'key' not in result


def test_add_new_pet_without_age(name='petucj', animal_type='Kokl', age='', pet_photo='images/suslik.jpg'):
    # пустое поле возраста
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200


def test_add_new_pet_without_animal_type(name='ezik', animal_type='', age='1', pet_photo='images/suslik.jpg'):
    # пустая порода
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200


def test_add_pet_with_four_digit_age_number(name='kopatych', animal_type='suslik', age='1234', pet_photo='images/suslik.jpg'):
    # больще трех знаков в переменной age
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert len(result['age']) >= 4


def test_add_pet_negative_age_number(name='Лыв', animal_type='ыгыдшл', age='-99', pet_photo='images/suslik.jpg'):
    # Добавление питомца с отрицательным числом в переменной age

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert age in result['age']


def test_add_new_pet_char_in_age(name='Фавр', animal_type='смирох', age='два', pet_photo='images/suslik.jpg'):
    # Отрицательный тест добавление питомца с string в age
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
#    assert result['age'] == age












