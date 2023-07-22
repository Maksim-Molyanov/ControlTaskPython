import datetime
import json

class Note:
    def __init__(self, id, title, body, time=datetime.datetime.now()):
        self._id = id
        self._title = title
        self._body = body
        self._time = time

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def body(self):
        return self._body

    @property
    def time(self):
        return self._time

    @title.setter
    def title(self, title):
        self._title = title

    @body.setter
    def body(self, body):
        self._body = body

    def __str__(self):
        return f"ID:{self._id}, Дата:{self._time.day}.{self._time.month}.{self._time.year} {self._time.hour}:{self._time.minute}, Заголовок:{self._title}"


class NoteStorage:
    def __init__(self):
        self.notes = []

    def create_note(self, title, body):
        id = len(self.notes)
        self.notes.append(Note(id, title, body))

    def view_notes(self):
        if not self.notes:
            print("Нет заметок")
        else:
            print("Список заметок:")
            for note in self.notes:
                print(note)

    def edit_note(self, id, title, body):
        if self.check_id(id):
            self.notes[id].title = title
            self.notes[id].body = body

    def check_id(self, id):
        for note in self.notes:
            if id == note._id:
                return True
        return False

    def delete(self, id):
        self.notes.pop(id)

    def find_date(self, date):
        result = ""
        for note in self.notes:
            if date == note.time.strftime("%d.%m.%Y"):
                result += str(note) + "\n"
        if result == "":
            return "Заметок с введеной датой отсутствуют."
        return result


class NoteEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Note):
            return {"id": obj.id, "title": obj.title, "body": obj.body, "time": obj.time.strftime("%d.%m.%Y %H:%M")}
        return super().default(obj)


class NoteDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.dict_to_note, *args, **kwargs)

    def dict_to_note(self, dict):
        if "id" in dict and "title" in dict and "body" in dict and "time" in dict:
            return Note(dict["id"], dict["title"], dict["body"],
                        datetime.datetime.strptime(dict["time"], "%d.%m.%Y %H:%M"))
        return dict


note_storage = NoteStorage()

while True:
    print("\nМеню:")
    print("1. Создать заметку.")
    print("2. Посмотреть все заметки.")
    print("3. Редактировать заметку.")
    print("4. Удалить заметку.")
    print("5. Найти заметку и показать.")
    print("L. Загрузить файл с заметками.")
    print("S. Сохранить файл с заметками.")
    print("0. Выйти.")

    choice = input("Введите номер операции: ")
    if choice == "1":
        title = input("Введите название заметки: ")
        text = input("Введите тело заметки: ")
        note_storage.create_note(title, text)
        print("Заметка создана.")

    elif choice == "2":
        note_storage.view_notes()

    elif choice == "3":
        id = int(input("Введите id заметки: "))
        if not note_storage.check_id(id):
            print("Заметки с таким id не существует.")
        else:
            title = input("Введите новое название заметки: ")
            text = input("Введите новое тело заметки: ")
            note_storage.edit_note(id, title, text)
        print("Заметка отредактирована.")

    elif choice == "4":
        id = int(input("Введите id заметки: "))
        if not note_storage.check_id(id):
            print("Заметки с таким id не существует.")
        else:
            note_storage.delete(id)
        print("Заметка удалена.")

    elif choice == "5":
        date = input("Введите дату в формате 00.00.0000: ")
        print(note_storage.find_date(date))

    elif choice == "S":
        json_data = json.dumps(note_storage.notes, cls=NoteEncoder)
        file_name = input("Введите название файла: ")
        with open(file_name + ".json", "w") as json_file:
            json_file.write(json_data)

    elif choice == "L":
        file_name = input("Введите название файла: ") + ".json"
        with open(file_name, "r") as json_file:
            json_data = json_file.read()
        note_storage.notes = json.loads(json_data, cls=NoteDecoder)

    elif choice == "0":
        break
    else:
        print("Некорректный ввод, повторите попытку.")
