import prompt

HELP_MESSAGE = """***
<command> exit — выйти из программы
<command> help — справочная информация
***"""


def welcome():
    print(HELP_MESSAGE)
    while True:
        command = prompt.string("Введите команду: ").strip().lower()

        if command == "exit":
            break
        elif command == "help":
            print(HELP_MESSAGE)
        else:
            print(f"Неизвестная команда: {command}. Введите 'help' для справки.")
