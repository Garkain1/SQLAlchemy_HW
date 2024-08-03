from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

engine = create_engine('sqlite:///:memory:')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    products = relationship("Product", back_populates="category")


Base.metadata.create_all(engine)

# Задача 1: Наполнение данными
category1 = Category(name="Электроника", description="Гаджеты и устройства.")
category2 = Category(name="Книги", description="Печатные книги и электронные книги.")
category3 = Category(name="Одежда", description="Одежда для мужчин и женщин.")
session.add_all([category1, category2, category3])
session.commit()

product1 = Product(name="Смартфон", price=299.99, in_stock=True, category=category1)
product2 = Product(name="Ноутбук", price=499.99, in_stock=True, category=category1)
product3 = Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=category2)
product4 = Product(name="Джинсы", price=40.50, in_stock=True, category=category3)
product5 = Product(name="Футболка", price=20.00, in_stock=True, category=category3)
session.add_all([product1, product2, product3, product4, product5])
session.commit()

# Задача 2: Чтение данных
categories = session.query(Category).all()
for category in categories:
    print(f"Категория: {category.name}, Описание: {category.description}")
    for product in category.products:
        print(f" - Продукт: {product.name}, Цена: {product.price}")

# Задача 3: Обновление данных
product_to_update = session.query(Product).filter_by(name="Смартфон").first()
if product_to_update:
    product_to_update.price = 349.99
    session.commit()

# Задача 4: Агрегация и группировка
category_counts = session.query(
    Category.name, func.count(Product.id)
).join(Product).group_by(Category.name).all()
for category_name, product_count in category_counts:
    print(f"Категория: {category_name}, Количество продуктов: {product_count}")

# Задача 5: Группировка с фильтрацией
filtered_category_counts = session.query(
    Category.name, func.count(Product.id)
).join(Product).group_by(Category.name).having(func.count(Product.id) > 1).all()
for category_name, product_count in filtered_category_counts:
    print(f"Категория: {category_name}, Количество продуктов: {product_count}")
