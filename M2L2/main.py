# Полиморфизм
# Примеры
print('2'*3)
print(2*3)
print('2'+'2')
print(2+2)
print(len([1, 2, 3, 4]))
print(len('1, 2, 3, 4'))

class Person:
    def __init__(self, name, city):
        self.name = name
        self.city = city


    #a+b
    def __add__(self, other):
        return self.name + " and " + other.name
    #a-b
    def __sub__(self, other):
        return self.name + " and " + other.name
    #a*b
    def __mul__(self, other):
        return self.name + " and " + other.name
    #a/b
    def __truediv__(self, other):
        return self.name + " and " + other.name
        #a/b
    def __eq__(self, other):
        if self.city == other.city:
            return "MATCH"
        else:
            return
a = Person("Vasya", "Msk")
b = Person("Petya", "Nsk")

print(a==b)