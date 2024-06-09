import pytest

def test_simple():
    mylist = [1,2,3,4,5]
    assert 1 in mylist
    
    
class Persona:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    
    def set_age(self,new_age:int):
        if type(new_age) == int:
            self.age = new_age
            return
        raise ValueError
    
    def __repr__(self) -> str:
        return f"Person {self.name,self.age}"
    

@pytest.fixture
def people():
    person = Persona('Ivan',30)
    return person

# Фикстура(функция people) результаты работы будут доступны в функции test_name   
def test_create_person(people):
    """Проверяем создание человека"""
    person = people
    assert person.name == "Ivan"
    assert person.age == 30
    
def test_set_age(people):
    assert people.age == 30
    people.set_age(50)
    assert people.age == 50