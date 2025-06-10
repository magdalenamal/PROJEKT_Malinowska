from tkinter import *
import tkintermapview
from tkinter import ttk

complexes = []
employees = []
clients = []


class Complex:
    def __init__(self, name, address, location, map_widget):
        self.name = name
        self.address = address
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(
            self.coordinates[0],
            self.coordinates[1],
            text=f'Kompleks: {self.name}',
            marker_color_circle="#1e90ff",  # Blue color
            marker_color_outside="#1e90ff"
        )

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        adres_url = f'https://pl.wikipedia.org/wiki/{self.location}'
        response = requests.get(adres_url)
        if response.status_code == 200:
            response_html = BeautifulSoup(requests.get(adres_url).text, 'html.parser')
            return [
                float(response_html.select('.latitude')[1].text.replace(',', '.')),
                float(response_html.select('.longitude')[1].text.replace(',', '.')),
            ]


class Employee:
    def __init__(self, name, surname, complex_name, position, map_widget):
        self.name = name
        self.surname = surname
        self.complex_name = complex_name
        self.position = position
        self.coordinates = self.get_complex_coordinates(complex_name)
        self.marker = map_widget.set_marker(
            self.coordinates[0],
            self.coordinates[1],
            text=f'Pracownik: {self.name} {self.surname}',
            marker_color_circle="#32CD32",  # Green color
            marker_color_outside="#32CD32"
        )

    def get_complex_coordinates(self, complex_name) -> list:
        for complex in complexes:
            if complex.name == complex_name:
                return complex.coordinates
        return [52.23, 21.00]  # Default Warsaw coordinates


class Client:
    def __init__(self, name, surname, location, sport, map_widget):
        self.name = name
        self.surname = surname
        self.location = location
        self.sport = sport
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(
            self.coordinates[0],
            self.coordinates[1],
            text=f'Klient: {self.name} {self.surname}',
            marker_color_circle="#FF4500",  # OrangeRed color
            marker_color_outside="#FF4500"
        )

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        adres_url = f'https://pl.wikipedia.org/wiki/{self.location}'
        response = requests.get(adres_url)
        if response.status_code == 200:
            response_html = BeautifulSoup(requests.get(adres_url).text, 'html.parser')
            return [
                float(response_html.select('.latitude')[1].text.replace(',', '.')),
                float(response_html.select('.longitude')[1].text.replace(',', '.')),
            ]


def add_item() -> None:
    category = combo_kategoria.get()

    if category == "Kompleksy sportowe":
        name = entry_nazwa.get()
        address = entry_adres.get()
        location = entry_lokalizacja.get()

        complex = Complex(name=name, address=address, location=location, map_widget=map_widget)
        complexes.append(complex)

        entry_nazwa.delete(0, END)
        entry_adres.delete(0, END)
        entry_lokalizacja.delete(0, END)

    elif category == "Pracownicy":
        name = entry_imie.get()
        surname = entry_nazwisko.get()
        complex_name = entry_kompleks.get()
        position = entry_stanowisko.get()

        employee = Employee(name=name, surname=surname, complex_name=complex_name,
                            position=position, map_widget=map_widget)
        employees.append(employee)

        entry_imie.delete(0, END)
        entry_nazwisko.delete(0, END)
        entry_kompleks.delete(0, END)
        entry_stanowisko.delete(0, END)

    elif category == "Klienci":
        name = entry_imie.get()
        surname = entry_nazwisko.get()
        location = entry_lokalizacja.get()
        sport = entry_sport.get()

        client = Client(name=name, surname=surname, location=location,
                        sport=sport, map_widget=map_widget)
        clients.append(client)

        entry_imie.delete(0, END)
        entry_nazwisko.delete(0, END)
        entry_lokalizacja.delete(0, END)
        entry_sport.delete(0, END)

    show_items()
    update_complex_combo()
    entry_imie.focus()


def show_items() -> None:
    category = combo_kategoria.get()
    listbox_lista_obiektow.delete(0, END)

    if category == "Kompleksy sportowe":
        for idx, complex in enumerate(complexes):
            listbox_lista_obiektow.insert(idx, f'{idx + 1}. {complex.name}')
    elif category == "Pracownicy":
        for idx, employee in enumerate(employees):
            listbox_lista_obiektow.insert(idx, f'{idx + 1}. {employee.name} {employee.surname}')
    elif category == "Klienci":
        for idx, client in enumerate(clients):
            listbox_lista_obiektow.insert(idx, f'{idx + 1}. {client.name} {client.surname}')


def remove_item():
    category = combo_kategoria.get()
    i = listbox_lista_obiektow.index(ACTIVE)

    if category == "Kompleksy sportowe":
        complexes[i].marker.delete()
        complexes.pop(i)
    elif category == "Pracownicy":
        employees[i].marker.delete()
        employees.pop(i)
    elif category == "Klienci":
        clients[i].marker.delete()
        clients.pop(i)

    show_items()


def edit_item():
    category = combo_kategoria.get()
    i = listbox_lista_obiektow.index(ACTIVE)

    if category == "Kompleksy sportowe":
        complex = complexes[i]
        entry_nazwa.insert(0, complex.name)
        entry_adres.insert(0, complex.address)
        entry_lokalizacja.insert(0, complex.location)

    elif category == "Pracownicy":
        employee = employees[i]
        entry_imie.insert(0, employee.name)
        entry_nazwisko.insert(0, employee.surname)
        entry_kompleks.insert(0, employee.complex_name)
        entry_stanowisko.insert(0, employee.position)

    elif category == "Klienci":
        client = clients[i]
        entry_imie.insert(0, client.name)
        entry_nazwisko.insert(0, client.surname)
        entry_lokalizacja.insert(0, client.location)
        entry_sport.insert(0, client.sport)

    button_dodaj_obiekt.config(text='Zapisz', command=lambda: update_item(i))


def update_item(i):
    category = combo_kategoria.get()

    if category == "Kompleksy sportowe":
        name = entry_nazwa.get()
        address = entry_adres.get()
        location = entry_lokalizacja.get()

        complexes[i].name = name
        complexes[i].address = address
        complexes[i].location = location

        complexes[i].coordinates = complexes[i].get_coordinates()
        complexes[i].marker.delete()
        complexes[i].marker = map_widget.set_marker(
            complexes[i].coordinates[0],
            complexes[i].coordinates[1],
            text=f'Kompleks: {complexes[i].name}',
            marker_color_circle="#1e90ff",
            marker_color_outside="#1e90ff"
        )

        entry_nazwa.delete(0, END)
        entry_adres.delete(0, END)
        entry_lokalizacja.delete(0, END)

    elif category == "Pracownicy":
        name = entry_imie.get()
        surname = entry_nazwisko.get()
        complex_name = entry_kompleks.get()
        position = entry_stanowisko.get()

        employees[i].name = name
        employees[i].surname = surname
        employees[i].complex_name = complex_name
        employees[i].position = position

        employees[i].coordinates = employees[i].get_complex_coordinates(complex_name)
        employees[i].marker.delete()
        employees[i].marker = map_widget.set_marker(
            employees[i].coordinates[0],
            employees[i].coordinates[1],
            text=f'Pracownik: {employees[i].name} {employees[i].surname}',
            marker_color_circle="#32CD32",
            marker_color_outside="#32CD32"
        )

        entry_imie.delete(0, END)
        entry_nazwisko.delete(0, END)
        entry_kompleks.delete(0, END)
        entry_stanowisko.delete(0, END)

    elif category == "Klienci":
        name = entry_imie.get()
        surname = entry_nazwisko.get()
        location = entry_lokalizacja.get()
        sport = entry_sport.get()

        clients[i].name = name
        clients[i].surname = surname
        clients[i].location = location
        clients[i].sport = sport

        clients[i].coordinates = clients[i].get_coordinates()
        clients[i].marker.delete()
        clients[i].marker = map_widget.set_marker(
            clients[i].coordinates[0],
            clients[i].coordinates[1],
            text=f'Klient: {clients[i].name} {clients[i].surname}',
            marker_color_circle="#FF4500",
            marker_color_outside="#FF4500"
        )

        entry_imie.delete(0, END)
        entry_nazwisko.delete(0, END)
        entry_lokalizacja.delete(0, END)
        entry_sport.delete(0, END)

    show_items()
    button_dodaj_obiekt.config(text='Dodaj', command=add_item)
    entry_imie.focus()


def show_item_details() -> None:
    category = combo_kategoria.get()
    i = listbox_lista_obiektow.index(ACTIVE)

    if category == "Kompleksy sportowe":
        complex = complexes[i]
        label_szczegoly_obiektu_nazwa_wartosc.config(text=complex.name)
        label_szczegoly_obiektu_adres_wartosc.config(text=complex.address)
        label_szczegoly_obiektu_lokalizacja_wartosc.config(text=complex.location)

        # Clear other fields
        label_szczegoly_obiektu_imie_wartosc.config(text="")
        label_szczegoly_obiektu_nazwisko_wartosc.config(text="")
        label_szczegoly_obiektu_kompleks_wartosc.config(text="")
        label_szczegoly_obiektu_stanowisko_wartosc.config(text="")
        label_szczegoly_obiektu_sport_wartosc.config(text="")

        map_widget.set_zoom(15)
        map_widget.set_position(complex.coordinates[0], complex.coordinates[1])

    elif category == "Pracownicy":
        employee = employees[i]
        label_szczegoly_obiektu_imie_wartosc.config(text=employee.name)
        label_szczegoly_obiektu_nazwisko_wartosc.config(text=employee.surname)
        label_szczegoly_obiektu_kompleks_wartosc.config(text=employee.complex_name)
        label_szczegoly_obiektu_stanowisko_wartosc.config(text=employee.position)

        # Clear other fields
        label_szczegoly_obiektu_nazwa_wartosc.config(text="")
        label_szczegoly_obiektu_adres_wartosc.config(text="")
        label_szczegoly_obiektu_lokalizacja_wartosc.config(text="")
        label_szczegoly_obiektu_sport_wartosc.config(text="")

        map_widget.set_zoom(15)
        map_widget.set_position(employee.coordinates[0], employee.coordinates[1])

    elif category == "Klienci":
        client = clients[i]
        label_szczegoly_obiektu_imie_wartosc.config(text=client.name)
        label_szczegoly_obiektu_nazwisko_wartosc.config(text=client.surname)
        label_szczegoly_obiektu_lokalizacja_wartosc.config(text=client.location)
        label_szczegoly_obiektu_sport_wartosc.config(text=client.sport)

        # Clear other fields
        label_szczegoly_obiektu_nazwa_wartosc.config(text="")
        label_szczegoly_obiektu_adres_wartosc.config(text="")
        label_szczegoly_obiektu_kompleks_wartosc.config(text="")
        label_szczegoly_obiektu_stanowisko_wartosc.config(text="")

        map_widget.set_zoom(15)
        map_widget.set_position(client.coordinates[0], client.coordinates[1])


def update_form_fields(event=None):
    category = combo_kategoria.get()

    # Hide all fields first
    label_nazwa.grid_remove()
    entry_nazwa.grid_remove()
    label_adres.grid_remove()
    entry_adres.grid_remove()
    label_imie.grid_remove()
    entry_imie.grid_remove()
    label_nazwisko.grid_remove()
    entry_nazwisko.grid_remove()
    label_kompleks.grid_remove()
    entry_kompleks.grid_remove()
    label_stanowisko.grid_remove()
    entry_stanowisko.grid_remove()
    label_lokalizacja.grid_remove()
    entry_lokalizacja.grid_remove()
    label_sport.grid_remove()
    entry_sport.grid_remove()

    # Show appropriate fields
    if category == "Kompleksy sportowe":
        label_nazwa.grid()
        entry_nazwa.grid()
        label_adres.grid()
        entry_adres.grid()
        label_lokalizacja.grid()
        entry_lokalizacja.grid()

    elif category == "Pracownicy":
        label_imie.grid()
        entry_imie.grid()
        label_nazwisko.grid()
        entry_nazwisko.grid()
        label_kompleks.grid()
        entry_kompleks.grid()
        label_stanowisko.grid()
        entry_stanowisko.grid()

    elif category == "Klienci":
        label_imie.grid()
        entry_imie.grid()
        label_nazwisko.grid()
        entry_nazwisko.grid()
        label_lokalizacja.grid()
        entry_lokalizacja.grid()
        label_sport.grid()
        entry_sport.grid()

    show_items()


def update_complex_combo():
    entry_kompleks['values'] = [complex.name for complex in complexes]


def clear_map():
    map_widget.delete_all_marker()


def generate_complexes_map():
    clear_map()
    for complex in complexes:
        complex.marker = map_widget.set_marker(
            complex.coordinates[0],
            complex.coordinates[1],
            text=f'Kompleks: {complex.name}',
            marker_color_circle="#1e90ff",
            marker_color_outside="#1e90ff"
        )
    if complexes:
        map_widget.set_position(complexes[0].coordinates[0], complexes[0].coordinates[1])
        map_widget.set_zoom(10)


def generate_employees_map():
    clear_map()
    for employee in employees:
        employee.marker = map_widget.set_marker(
            employee.coordinates[0],
            employee.coordinates[1],
            text=f'Pracownik: {employee.name} {employee.surname}',
            marker_color_circle="#32CD32",
            marker_color_outside="#32CD32"
        )
    if employees:
        map_widget.set_position(employees[0].coordinates[0], employees[0].coordinates[1])
        map_widget.set_zoom(10)


def generate_clients_map():
    clear_map()
    for client in clients:
        client.marker = map_widget.set_marker(
            client.coordinates[0],
            client.coordinates[1],
            text=f'Klient: {client.name} {client.surname}',
            marker_color_circle="#FF4500",
            marker_color_outside="#FF4500"
        )
    if clients:
        map_widget.set_position(clients[0].coordinates[0], clients[0].coordinates[1])
        map_widget.set_zoom(10)


def generate_employees_for_complex_map():
    clear_map()
    complex_name = combo_wybrany_kompleks.get()
    found = False

    for employee in employees:
        if employee.complex_name == complex_name:
            employee.marker = map_widget.set_marker(
                employee.coordinates[0],
                employee.coordinates[1],
                text=f'Pracownik: {employee.name} {employee.surname}',
                marker_color_circle="#32CD32",
                marker_color_outside="#32CD32"
            )
            if not found:
                map_widget.set_position(employee.coordinates[0], employee.coordinates[1])
                map_widget.set_zoom(15)
                found = True

    # Add complex marker
    for complex in complexes:
        if complex.name == complex_name:
            complex.marker = map_widget.set_marker(
                complex.coordinates[0],
                complex.coordinates[1],
                text=f'Kompleks: {complex.name}',
                marker_color_circle="#1e90ff",
                marker_color_outside="#1e90ff"
            )
            if not found:
                map_widget.set_position(complex.coordinates[0], complex.coordinates[1])
                map_widget.set_zoom(15)
                found = True


def generate_clients_for_complex_map():
    clear_map()
    complex_name = combo_wybrany_kompleks.get()
    complex_coords = None

    # Find complex coordinates
    for complex in complexes:
        if complex.name == complex_name:
            complex_coords = complex.coordinates
            complex.marker = map_widget.set_marker(
                complex.coordinates[0],
                complex.coordinates[1],
                text=f'Kompleks: {complex.name}',
                marker_color_circle="#1e90ff",
                marker_color_outside="#1e90ff"
            )
            map_widget.set_position(complex.coordinates[0], complex.coordinates[1])
            map_widget.set_zoom(15)
            break

    # Add clients who visited this complex
    if complex_coords:
        for client in clients:
            # Simple approximation - show clients within 0.5 degree (~55 km)
            if (abs(client.coordinates[0] - complex_coords[0]) < 0.5 and
                    abs(client.coordinates[1] - complex_coords[1]) < 0.5):
                client.marker = map_widget.set_marker(
                    client.coordinates[0],
                    client.coordinates[1],
                    text=f'Klient: {client.name} {client.surname}',
                    marker_color_circle="#FF4500",
                    marker_color_outside="#FF4500"
                )


root = Tk()
root.geometry("1200x800")
root.title("System zarządzania kompleksami sportowymi")

# Create frames
ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa = Frame(root)
ramka_kontrolna = Frame(root)

# Grid layout
ramka_kontrolna.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
ramka_lista_obiektow.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
ramka_formularz.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
ramka_szczegoly_obiektow.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
ramka_mapa.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

# Configure row and column weights
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Control frame
label_kategoria = Label(ramka_kontrolna, text="Kategoria:")
label_kategoria.grid(row=0, column=0, padx=5, pady=5)

kategorie = ["Kompleksy sportowe", "Pracownicy", "Klienci"]
combo_kategoria = ttk.Combobox(ramka_kontrolna, values=kategorie, state="readonly")
combo_kategoria.current(0)
combo_kategoria.grid(row=0, column=1, padx=5, pady=5)
combo_kategoria.bind("<<ComboboxSelected>>", update_form_fields)

# Map buttons
button_kompleksy = Button(ramka_kontrolna, text="Mapa kompleksów", command=generate_complexes_map)
button_kompleksy.grid(row=0, column=2, padx=5, pady=5)

button_pracownicy = Button(ramka_kontrolna, text="Mapa pracowników", command=generate_employees_map)
button_pracownicy.grid(row=0, column=3, padx=5, pady=5)

button_klienci = Button(ramka_kontrolna, text="Mapa klientów", command=generate_clients_map)
button_klienci.grid(row=0, column=4, padx=5, pady=5)

label_wybrany_kompleks = Label(ramka_kontrolna, text="Wybierz kompleks:")
label_wybrany_kompleks.grid(row=0, column=5, padx=5, pady=5)

combo_wybrany_kompleks = ttk.Combobox(ramka_kontrolna, state="readonly")
combo_wybrany_kompleks.grid(row=0, column=6, padx=5, pady=5)

button_pracownicy_kompleks = Button(ramka_kontrolna, text="Pracownicy kompleksu",
                                    command=generate_employees_for_complex_map)
button_pracownicy_kompleks.grid(row=0, column=7, padx=5, pady=5)

button_klienci_kompleks = Button(ramka_kontrolna, text="Klienci kompleksu",
                                 command=generate_clients_for_complex_map)
button_klienci_kompleks.grid(row=0, column=8, padx=5, pady=5)

# Object list frame
label_lista_obiektow = Label(ramka_lista_obiektow, text="Lista obiektów:")
label_lista_obiektow.grid(row=0, column=0, sticky="w")

listbox_lista_obiektow = Listbox(ramka_lista_obiektow, width=50, height=15)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3, sticky="nsew")

button_pokaz_szczegoly = Button(ramka_lista_obiektow, text="Pokaż szczegóły", command=show_item_details)
button_pokaz_szczegoly.grid(row=2, column=0, pady=5)

button_usun_obiekt = Button(ramka_lista_obiektow, text="Usuń", command=remove_item)
button_usun_obiekt.grid(row=2, column=1, pady=5)

button_edytuj_obiekt = Button(ramka_lista_obiektow, text="Edytuj", command=edit_item)
button_edytuj_obiekt.grid(row=2, column=2, pady=5)

# Form frame
label_formularz = Label(ramka_formularz, text="Formularz:")
label_formularz.grid(row=0, column=0, sticky="w")

# Fields for complexes
label_nazwa = Label(ramka_formularz, text="Nazwa kompleksu:")
label_nazwa.grid(row=1, column=0, sticky="w")
entry_nazwa = Entry(ramka_formularz, width=30)
entry_nazwa.grid(row=1, column=1)

label_adres = Label(ramka_formularz, text="Adres:")
label_adres.grid(row=2, column=0, sticky="w")
entry_adres = Entry(ramka_formularz, width=30)
entry_adres.grid(row=2, column=1)

label_lokalizacja = Label(ramka_formularz, text="Lokalizacja (Wikipedia):")
label_lokalizacja.grid(row=3, column=0, sticky="w")
entry_lokalizacja = Entry(ramka_formularz, width=30)
entry_lokalizacja.grid(row=3, column=1)

# Fields for employees
label_imie = Label(ramka_formularz, text="Imię:")
label_imie.grid(row=1, column=0, sticky="w")
entry_imie = Entry(ramka_formularz, width=30)
entry_imie.grid(row=1, column=1)

label_nazwisko = Label(ramka_formularz, text="Nazwisko:")
label_nazwisko.grid(row=2, column=0, sticky="w")
entry_nazwisko = Entry(ramka_formularz, width=30)
entry_nazwisko.grid(row=2, column=1)

label_kompleks = Label(ramka_formularz, text="Kompleks:")
label_kompleks.grid(row=3, column=0, sticky="w")
entry_kompleks = ttk.Combobox(ramka_formularz, width=28)
entry_kompleks.grid(row=3, column=1)

label_stanowisko = Label(ramka_formularz, text="Stanowisko:")
label_stanowisko.grid(row=4, column=0, sticky="w")
entry_stanowisko = Entry(ramka_formularz, width=30)
entry_stanowisko.grid(row=4, column=1)

# Fields for clients
label_sport = Label(ramka_formularz, text="Ulubiony sport:")
label_sport.grid(row=4, column=0, sticky="w")
entry_sport = Entry(ramka_formularz, width=30)
entry_sport.grid(row=4, column=1)

button_dodaj_obiekt = Button(ramka_formularz, text="Dodaj", command=add_item)
button_dodaj_obiekt.grid(row=5, column=0, columnspan=2, pady=10)

# Hide all fields initially
update_form_fields()

# Details frame
label_szczegoly = Label(ramka_szczegoly_obiektow, text="Szczegóły obiektu:")
label_szczegoly.grid(row=0, column=0, sticky="w")

# Labels for complexes
label_szczegoly_obiektu_nazwa = Label(ramka_szczegoly_obiektow, text="Nazwa:")
label_szczegoly_obiektu_nazwa.grid(row=1, column=0, sticky="w")
label_szczegoly_obiektu_nazwa_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_szczegoly_obiektu_nazwa_wartosc.grid(row=1, column=1, sticky="w")

label_szczegoly_obiektu_adres = Label(ramka_szczegoly_obiektow, text="Adres:")
label_szczegoly_obiektu_adres.grid(row=1, column=2, sticky="w")
label_szczegoly_obiektu_adres_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_szczegoly_obiektu_adres_wartosc.grid(row=1, column=3, sticky="w")

label_szczegoly_obiektu_lokalizacja = Label(ramka_szczegoly_obiektow, text="Lokalizacja:")
label_szczegoly_obiektu_lokalizacja.grid(row=1, column=4, sticky="w")
label_szczegoly_obiektu_lokalizacja_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_szczegoly_obiektu_lokalizacja_wartosc.grid(row=1, column=5, sticky="w")

# Labels for employees
label_szczegoly_obiektu_imie = Label(ramka_szczegoly_obiektow, text="Imię:")
label_szczegoly_obiektu_imie.grid(row=2, column=0, sticky="w")
label_szczegoly_obiektu_imie_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_szczegoly_obiektu_imie_wartosc.grid(row=2, column=1, sticky="w")

label_szczegoly_obiektu_nazwisko = Label(ramka_szczegoly_obiektow, text="Nazwisko:")
label_szczegoly_obiektu_nazwisko.grid(row=2, column=2, sticky="w")
label_szczegoly_obiektu_nazwisko_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_szczegoly_obiektu_nazwisko_wartosc.grid(row=2, column=3, sticky="w")

label_szczegoly_obiektu_kompleks = Label(ramka_szczegoly_obiektow, text="Kompleks:")
label_szczegoly_obiektu_kompleks.grid(row=2, column=4, sticky="w")
label_szczegoly_obiektu_kompleks_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_szczegoly_obiektu_kompleks_wartosc.grid(row=2, column=5, sticky="w")

label_szczegoly_obiektu_stanowisko = Label(ramka_szczegoly_obiektow, text="Stanowisko:")
label_szczegoly_obiektu_stanowisko.grid(row=2, column=6, sticky="w")
label_szczegoly_obiektu_stanowisko_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_szczegoly_obiektu_stanowisko_wartosc.grid(row=2, column=7, sticky="w")

# Labels for clients
label_szczegoly_obiektu_sport = Label(ramka_szczegoly_obiektow, text="Ulubiony sport:")
label_szczegoly_obiektu_sport.grid(row=3, column=0, sticky="w")
label_szczegoly_obiektu_sport_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_szczegoly_obiektu_sport_wartosc.grid(row=3, column=1, sticky="w")

# Map frame
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1100, height=400, corner_radius=0)
map_widget.grid(row=0, column=0, sticky="nsew")
map_widget.set_position(52.23, 21.00)  # Warsaw coordinates
map_widget.set_zoom(6)

# Initial update
update_form_fields()
update_complex_combo()

root.mainloop()