from application.salary import calculate_salary
from application.db.people import get_employees
from datetime import datetime


def main():
    current_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    print(f"Текущая дата и время: {current_date}")
    print("-" * 40)

    calculate_salary()
    get_employees()


if __name__ == '__main__':
    main()