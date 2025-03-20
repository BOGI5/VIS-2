from agent import get_completion_with_retries
import json

if __name__ == "__main__":
    with open("instructions.txt", "r", encoding="utf8") as file:
        instructions = file.read()


        # Read client data
    with open("info.json", "r", encoding="utf-8") as file:
        client_data = json.load(file)

    # Format client data into a text representation
    client_info = f"""
    Информация за клиента:
    - Име: {client_data['firstName']} {client_data['lastName']}
    - Телефон: {client_data['phone']}
    - Дължима сума: {client_data['amount']} лв.
    - Срок на кредита: {client_data['creditExpire']}
    - Семейно положение: {client_data['familyStatus']}
    - Доход: {client_data['income']} лв.
    - ЕГН: {client_data['egn']}
    - Адрес: {client_data['address']}
    - Възраст: {client_data['age']}
    - Работа: {client_data['job']}
    """

    # Build the system prompt with client information
    system_prompt = instructions + "\n\n" + client_info

    result = get_completion_with_retries("Здрасти", system_prompt)

    print(result["content"])

    result = get_completion_with_retries("Да, имам", system_prompt)

    print(result["content"])

    result = get_completion_with_retries("Да, проиграх си парите на комар", system_prompt)

    print(result["content"])
