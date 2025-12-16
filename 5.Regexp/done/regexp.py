import re
import csv
from pprint import pprint

with open("phonebook_raw.csv", encoding="cp1251") as f:
    rows = csv.reader(f, delimiter=";")
    contacts_list = list(rows)

print("Исходные данные после чтения с правильным разделителем:")
pprint(contacts_list)
print("\n" + "=" * 80 + "\n")


def process_name(record):
    full_name = ' '.join(record[:3])

    name_parts = full_name.split()

    while len(record) < 7:
        record.append('')

    if len(name_parts) >= 1:
        record[0] = name_parts[0]

    if len(name_parts) >= 2:
        record[1] = name_parts[1]

    if len(name_parts) >= 3:
        record[2] = name_parts[2]
    else:
        record[2] = ''

    return record


def format_phone(phone):
    if not phone:
        return ''

    phone = str(phone).strip()

    extension = ''
    if 'доб' in phone.lower():
        ext_match = re.search(r'доб\.?\s*(\d+)', phone, re.IGNORECASE)
        if ext_match:
            extension = ext_match.group(1)а
        phone = re.sub(r'доб\.?\s*\d+', '', phone, flags=re.IGNORECASE)

    digits = re.sub(r'[^\d+]', '', phone)

    # Если номер начинается с 8, меняем на 7
    if digits.startswith('8'):
        digits = '7' + digits[1:]

    if digits.startswith('+7'):
        digits = digits[1:]

    if digits.startswith('7') and len(digits) == 11:
        formatted = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:]}"
        if extension:
            formatted += f' доб.{extension}'

        return formatted
          
    if len(digits) == 10:
        formatted = f"+7({digits[0:3]}){digits[3:6]}-{digits[6:8]}-{digits[8:10]}"
        if extension:
            formatted += f' доб.{extension}'
        return formatted

    return phone


for i in range(1, len(contacts_list)):
    while len(contacts_list[i]) < 7:
        contacts_list[i].append('')

    contacts_list[i] = process_name(contacts_list[i])

    contacts_list[i][5] = format_phone(contacts_list[i][5])

print("Данные после обработки ФИО и телефонов:")
pprint(contacts_list)
print("\n" + "=" * 80 + "\n")

merged_dict = {}

for contact in contacts_list:
    if contact[0] == 'lastname':
        header = contact
        continue

    key = (contact[0], contact[1])

    if key not in merged_dict:
        merged_dict[key] = contact.copy()
    else:
        existing = merged_dict[key]

        for j in range(2, 7):  # Всего 7 полей
            if j < len(contact):
                if not existing[j] and contact[j]:
                    existing[j] = contact[j]

final_contacts_list = [header]

for key in sorted(merged_dict.keys()):
    final_contacts_list.append(merged_dict[key])

print("Финальный список после объединения дубликатов:")
pprint(final_contacts_list)
print("\n" + "=" * 80 + "\n")

# TODO 2: сохраните получившиеся данные в другой файл
with open("phonebook.csv", "w", encoding="cp1251", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts_list)

print(f"Всего уникальных записей: {len(final_contacts_list) - 1}")
print("Данные сохранены в файл phonebook.csv")
