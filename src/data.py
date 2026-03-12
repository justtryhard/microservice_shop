from src.models.user import User
from src.models.product import Product
from src.models.order import Order

# Продукты
p1 = Product(name='bread', price=2.5, quantity=2)
p2 = Product(name='curd', price=3.0, quantity=1)
p3 = Product(name='milk', price=1.8, quantity=3)
p4 = Product(name='eggs', price=0.2, quantity=12)
p5 = Product(name='cheese', price=4.5, quantity=1)
p6 = Product(name='butter', price=2.2, quantity=2)
p7 = Product(name='chicken', price=6.0, quantity=1)
p8 = Product(name='rice', price=1.5, quantity=2)
p9 = Product(name='vegetables', price=3.5, quantity=1)
p10 = Product(name='pasta', price=1.7, quantity=2)
p11 = Product(name='tomato sauce', price=2.3, quantity=1)
p12 = Product(name='beef', price=8.0, quantity=1)
p13 = Product(name='potatoes', price=1.2, quantity=5)
p14 = Product(name='fish', price=7.5, quantity=1)
p15 = Product(name='apples', price=2.0, quantity=4)

products = {
    1: p1, 2: p2, 3: p3, 4: p4, 5: p5,
    6: p6, 7: p7, 8: p8, 9: p9, 10: p10,
    11: p11, 12: p12, 13: p13, 14: p14, 15: p15
}

# Пользователи
u1 = User(name="Thomas", email="thomas@example.com")
u2 = User(name="Alice", email="alice@example.com")
u3 = User(name="John", email="john@example.com")
u4 = User(name="Emma", email="emma@example.com")
u5 = User(name="Michael", email="michael@example.com")
u6 = User(name="Sophia", email="sophia@example.com")
u7 = User(name="Daniel", email="daniel@example.com")
u8 = User(name="Olivia", email="olivia@example.com")
u9 = User(name="James", email="james@example.com")
u10 = User(name="Isabella", email="isabella@example.com")

users = {
    1: u1, 2: u2, 3: u3, 4: u4, 5: u5,
    6: u6, 7: u7, 8: u8, 9: u9, 10: u10
}

# Заказы
o1 = Order(user=u1, products=[p1, p2, p3])
o2 = Order(user=u2, products=[p4, p5, p6])
o3 = Order(user=u3, products=[p7, p8, p9])
o4 = Order(user=u4, products=[p10, p11, p5])
o5 = Order(user=u5, products=[p2, p4])
o6 = Order(user=u6, products=[p3, p15, p12])
o7 = Order(user=u7, products=[p14, p8])
o8 = Order(user=u8, products=[p4, p1, p15])
o9 = Order(user=u9, products=[p6, p2])
o10 = Order(user=u10, products=[p9, p10, p13])

orders = {1: o1, 2: o2, 3: o3, 4: o4, 5: o5, 6: o6, 7: o7, 8: o8, 9: o9, 10: o10}