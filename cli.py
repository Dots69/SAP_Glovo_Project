import requests

BASE_URL = "http://localhost:5000"

def main():
    while True:
        print("\n=== Добре дошъл в GlovoApp ===")
        print("1. Вход")
        print("2. Регистрация")
        print("3. Изход")
        choice = input("Избери опция: ")

        if choice == "1":
            login()
        elif choice == "2":
            register()
        elif choice == "3":
            print("Довиждане!")
            break
        else:
            print("Невалиден избор. Опитай отново.")

def register():
    print("\n=== Регистрация ===")
    username = input("Потребителско име: ")
    password = input("Парола: ")
    role = input("Роля (customer/courier/admin): ").lower()

    if role not in ["customer", "courier", "admin"]:
        print("Невалидна роля.")
        return

    response = requests.post(f"{BASE_URL}/register", json={
        "username": username,
        "password": password,
        "role": role
    })

    if response.json().get("status") == "ok":
        print("Успешна регистрация!")
    else:
        print("Грешка при регистрация. Потребителското име може би вече съществува.")

def login():
    print("\n=== Вход ===")
    username = input("Потребителско име: ")
    password = input("Парола: ")

    response = requests.post(f"{BASE_URL}/login", json={
        "username": username,
        "password": password
    })

    data = response.json()
    if data.get("status") == "ok":
        user = data["user"]
        print(f"Успешен вход! Добре дошъл, {user['username']} ({user['role']})")
        if user["role"] == "customer":
            customer_menu(user)
        elif user["role"] == "courier":
            courier_menu(user)
        elif user["role"] == "admin":
            admin_menu(user)
    else:
        print("Грешно потребителско име или парола.")

def customer_menu(user):
    while True:
        print("\n=== Меню за Клиент ===")
        print("1. Виж ресторанти")
        print("2. Виж меню на ресторант")
        print("3. Направи поръчка")
        print("4. Изход")
        choice = input("Избери опция: ")

        if choice == "1":
            response = requests.get(f"{BASE_URL}/restaurants")
            restaurants = response.json()
            for r in restaurants:
                print(f"{r['id']}: {r['name']}")
        elif choice == "2":
            restaurant_id = input("Въведи ID на ресторант: ")
            response = requests.get(f"{BASE_URL}/menu/{restaurant_id}")
            menu_items = response.json()
            for item in menu_items:
                print(f"{item['id']}: {item['name']} - {item['price']} лв.")
        elif choice == "3":
            restaurant_id = input("ID на ресторант: ")
            item_id = input("ID на артикул: ")
            quantity = input("Количество: ")
            response = requests.post(f"{BASE_URL}/order", json={
                "customer_id": user["id"],
                "restaurant_id": int(restaurant_id),
                "item_id": int(item_id),
                "quantity": int(quantity)
            })
            print(response.json().get("message"))
        elif choice == "4":
            break
        else:
            print("Невалиден избор.")

def courier_menu(user):
    while True:
        print("\n=== Меню за Куриера ===")
        print("1. Виж чакащи поръчки")
        print("2. Завърши поръчка")
        print("3. Изход")
        choice = input("Избери опция: ")

        if choice == "1":
            response = requests.get(f"{BASE_URL}/courier/orders")
            orders = response.json()
            for o in orders:
                print(f"Поръчка {o['id']}: клиент {o['customer_id']}, ресторант {o['restaurant_id']}, артикул {o['item_id']}, количество {o['quantity']}")
        elif choice == "2":
            order_id = input("ID на поръчка: ")
            response = requests.post(f"{BASE_URL}/courier/complete", json={
                "order_id": int(order_id),
                "courier_id": user["id"]
            })
            if response.json().get("status") == "ok":
                print("Поръчката е завършена.")
            else:
                print("Грешка при завършване на поръчката.")
        elif choice == "3":
            break
        else:
            print("Невалиден избор.")

def admin_menu(user):
    while True:
        print("\n=== Меню за Администратор ===")
        print("1. Добави ресторант")
        print("2. Добави артикул в меню")
        print("3. Изход")
        choice = input("Избери опция: ")

        if choice == "1":
            name = input("Име на ресторанта: ")
            response = requests.post(f"{BASE_URL}/admin/restaurant", json={
                "name": name,
                "created_by": user["id"]
            })
            print("Ресторантът е добавен." if response.json().get("status") == "ok" else "Грешка.")
        elif choice == "2":
            name = input("Име на артикула: ")
            price = input("Цена: ")
            restaurant_id = input("ID на ресторант: ")
            response = requests.post(f"{BASE_URL}/admin/item", json={
                "name": name,
                "price": float(price),
                "restaurant_id": int(restaurant_id)
            })
            print("Артикулът е добавен." if response.json().get("status") == "ok" else "Грешка.")
        elif choice == "3":
            break
        else:
            print("Невалиден избор.")

if __name__ == "__main__":
    main()