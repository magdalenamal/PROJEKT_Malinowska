import tkinter
from tkinter import *
import tkinter.ttk
from tkinter import messagebox
import tkintermapview
import requests
from bs4 import BeautifulSoup


def pobierz_wspolrzedne(miejscowosc):
    try:
        url = f'https://pl.wikipedia.org/wiki/{miejscowosc}'
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            lat = float(soup.select('.latitude')[1].text.replace(',', '.'))
            lon = float(soup.select('.longitude')[1].text.replace(',', '.'))
            return [lat, lon]
    except Exception as e:
        print(f"Błąd pobierania wspolrzednych dla {miejscowosc}: {e}")
    return [52.22977, 21.01178]


class KompleksSportowy:
    def __init__(self, nazwa, miejscowosc, mapa):
        self.nazwa = nazwa
        self.miejscowosc = miejscowosc
        self.wspolrzedne = pobierz_wspolrzedne(miejscowosc)
        self.marker = mapa.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"Kompleks: {self.nazwa}")
        self.pracownicy = []
        self.klienci = []

    def aktualizuj_marker(self, mapa):
        self.marker.delete()
        self.wspolrzedne = pobierz_wspolrzedne(self.miejscowosc)
        self.marker = mapa.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"Kompleks: {self.nazwa}")


class Osoba:
    def __init__(self, imie, nazwisko, miejscowosc, mapa, kompleks=None):
        self.imie = imie
        self.nazwisko = nazwisko
        self.miejscowosc = miejscowosc
        self.wspolrzedne = pobierz_wspolrzedne(miejscowosc)
        self.marker = mapa.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"{self.imie} {self.nazwisko}")
        self.kompleks = kompleks  # Do jakiego kompleksu należy (jeśli dotyczy)

    def aktualizuj_marker(self, mapa):
        self.marker.delete()
        self.wspolrzedne = pobierz_wspolrzedne(self.miejscowosc)
        self.marker = mapa.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"{self.imie} {self.nazwisko}")


class Pracownik(Osoba):
    pass


class Klient(Osoba):
    pass


lista_kompleksow = []
lista_pracownikow = []
lista_klientow = []



def wyczysc_formularz():
    entry_nazwa.delete(0, END)
    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_miejscowosc.delete(0, END)
    combo_kompleks.set('')


def pokaz_wszystkie_obiekty():
    listbox_obiekty.delete(0, END)
    typ = var_typ.get()
    if typ == "Kompleksy":
        for idx, k in enumerate(lista_kompleksow):
            listbox_obiekty.insert(END, f"{idx+1}. {k.nazwa} ({k.miejscowosc})")
    elif typ == "Pracownicy":
        for idx, p in enumerate(lista_pracownikow):
            listbox_obiekty.insert(END, f"{idx+1}. {p.imie} {p.nazwisko} ({p.miejscowosc}) - {p.kompleks.nazwa if p.kompleks else 'Brak'}")
    elif typ == "Klienci":
        for idx, c in enumerate(lista_klientow):
            listbox_obiekty.insert(END, f"{idx+1}. {c.imie} {c.nazwisko} ({c.miejscowosc}) - {c.kompleks.nazwa if c.kompleks else 'Brak'}")


def dodaj_obiekt():
    typ = var_typ.get()
    if typ == "Kompleksy":
        nazwa = entry_nazwa.get().strip()
        miejscowosc = entry_miejscowosc.get().strip()
        if not nazwa or not miejscowosc:
            messagebox.showwarning("Brak danych", "Podaj nazwę i miejscowość kompleksu!")
            return
        k = KompleksSportowy(nazwa, miejscowosc, mapa)
        lista_kompleksow.append(k)
        messagebox.showinfo("Dodano", f"Dodano kompleks: {nazwa}")
    elif typ == "Pracownicy":
        imie = entry_imie.get().strip()
        nazwisko = entry_nazwisko.get().strip()
        miejscowosc = entry_miejscowosc.get().strip()
        nazwa_kompleksu = combo_kompleks.get()
        if not imie or not nazwisko or not miejscowosc:
            messagebox.showwarning("Brak danych", "Podaj imię, nazwisko i miejscowość pracownika!")
            return
        kompleks = None
        for k in lista_kompleksow:
            if k.nazwa == nazwa_kompleksu:
                kompleks = k
                break
        p = Pracownik(imie, nazwisko, miejscowosc, mapa, kompleks)
        lista_pracownikow.append(p)
        if kompleks:
            kompleks.pracownicy.append(p)
        messagebox.showinfo("Dodano", f"Dodano pracownika: {imie} {nazwisko}")
    elif typ == "Klienci":
        imie = entry_imie.get().strip()
        nazwisko = entry_nazwisko.get().strip()
        miejscowosc = entry_miejscowosc.get().strip()
        nazwa_kompleksu = combo_kompleks.get()
        if not imie or not nazwisko or not miejscowosc:
            messagebox.showwarning("Brak danych", "Podaj imię, nazwisko i miejscowość klienta!")
            return
        kompleks = None
        for k in lista_kompleksow:
            if k.nazwa == nazwa_kompleksu:
                kompleks = k
                break
        c = Klient(imie, nazwisko, miejscowosc, mapa, kompleks)
        lista_klientow.append(c)
        if kompleks:
            kompleks.klienci.append(c)
        messagebox.showinfo("Dodano", f"Dodano klienta: {imie} {nazwisko}")
    wyczysc_formularz()
    pokaz_wszystkie_obiekty()


def usun_obiekt():
    typ = var_typ.get()
    try:
        idx = listbox_obiekty.curselection()[0]
    except IndexError:
        messagebox.showwarning("Błąd", "Wybierz obiekt z listy do usunięcia!")
        return

    if typ == "Kompleksy":
        k = lista_kompleksow.pop(idx)
        k.marker.delete()
        for p in k.pracownicy:
            if p in lista_pracownikow:
                p.marker.delete()
                lista_pracownikow.remove(p)
        for c in k.klienci:
            if c in lista_klientow:
                c.marker.delete()
                lista_klientow.remove(c)
        messagebox.showinfo("Usunięto", f"Usunięto kompleks: {k.nazwa}")
    elif typ == "Pracownicy":
        p = lista_pracownikow.pop(idx)
        p.marker.delete()
        if p.kompleks and p in p.kompleks.pracownicy:
            p.kompleks.pracownicy.remove(p)
        messagebox.showinfo("Usunięto", f"Usunięto pracownika: {p.imie} {p.nazwisko}")
    elif typ == "Klienci":
        c = lista_klientow.pop(idx)
        c.marker.delete()
        if c.kompleks and c in c.kompleks.klienci:
            c.kompleks.klienci.remove(c)
        messagebox.showinfo("Usunięto", f"Usunięto klienta: {c.imie} {c.nazwisko}")

    wyczysc_formularz()
    pokaz_wszystkie_obiekty()


def edytuj_obiekt():
    typ = var_typ.get()
    try:
        idx = listbox_obiekty.curselection()[0]
    except IndexError:
        messagebox.showwarning("Błąd", "Wybierz obiekt z listy do edycji!")
        return

    if typ == "Kompleksy":
        k = lista_kompleksow[idx]
        entry_nazwa.delete(0, END)
        entry_nazwa.insert(0, k.nazwa)
        entry_miejscowosc.delete(0, END)
        entry_miejscowosc.insert(0, k.miejscowosc)
        entry_imie.delete(0, END)
        entry_nazwisko.delete(0, END)
        combo_kompleks.set('')
        button_dodaj.config(text="Zapisz", command=lambda: zapisz_edycje_kompleksu(idx))
    elif typ == "Pracownicy":
        p = lista_pracownikow[idx]
        entry_nazwa.delete(0, END)
        entry_nazwa.config(state=DISABLED)
        entry_imie.delete(0, END)
        entry_imie.insert(0, p.imie)
        entry_nazwisko.delete(0, END)
        entry_nazwisko.insert(0, p.nazwisko)
        entry_miejscowosc.delete(0, END)
        entry_miejscowosc.insert(0, p.miejscowosc)
        combo_kompleks.set(p.kompleks.nazwa if p.kompleks else '')
        button_dodaj.config(text="Zapisz", command=lambda: zapisz_edycje_pracownika(idx))
    elif typ == "Klienci":
        c = lista_klientow[idx]
        entry_nazwa.delete(0, END)
        entry_nazwa.config(state=DISABLED)
        entry_imie.delete(0, END)
        entry_imie.insert(0, c.imie)
        entry_nazwisko.delete(0, END)
        entry_nazwisko.insert(0, c.nazwisko)
        entry_miejscowosc.delete(0, END)
        entry_miejscowosc.insert(0, c.miejscowosc)
        combo_kompleks.set(c.kompleks.nazwa if c.kompleks else '')
        button_dodaj.config(text="Zapisz", command=lambda: zapisz_edycje_klienta(idx))


def zapisz_edycje_kompleksu(idx):
    k = lista_kompleksow[idx]
    nazwa = entry_nazwa.get().strip()
    miejscowosc = entry_miejscowosc.get().strip()
    if not nazwa or not miejscowosc:
        messagebox.showwarning("Brak danych", "Podaj nazwę i miejscowość kompleksu!")
        return
    k.nazwa = nazwa
    k.miejscowosc = miejscowosc
    k.aktualizuj_marker(mapa)
    button_dodaj.config(text="Dodaj", command=dodaj_obiekt)
    entry_nazwa.config(state=NORMAL)
    wyczysc_formularz()
    pokaz_wszystkie_obiekty()
    messagebox.showinfo("Zapisano", f"Zapisano zmiany kompleksu: {nazwa}")


def zapisz_edycje_pracownika(idx):
    p = lista_pracownikow[idx]
    imie = entry_imie.get().strip()
    nazwisko = entry_nazwisko.get().strip()
    miejscowosc = entry_miejscowosc.get().strip()
    nazwa_kompleksu = combo_kompleks.get()
    if not imie or not nazwisko or not miejscowosc:
        messagebox.showwarning("Brak danych", "Podaj imię, nazwisko i miejscowość pracownika!")
        return
    p.imie = imie
    p.nazwisko = nazwisko
    p.miejscowosc = miejscowosc
    if p.kompleks and p in p.kompleks.pracownicy:
        p.kompleks.pracownicy.remove(p)
    nowy_kompleks = None
    for k in lista_kompleksow:
        if k.nazwa == nazwa_kompleksu:
            nowy_kompleks = k
            break
    p.kompleks = nowy_kompleks
    if nowy_kompleks:
        nowy_kompleks.pracownicy.append(p)
    p.aktualizuj_marker(mapa)
    button_dodaj.config(text="Dodaj", command=dodaj_obiekt)
    entry_nazwa.config(state=NORMAL)
    wyczysc_formularz()
    pokaz_wszystkie_obiekty()
    messagebox.showinfo("Zapisano", f"Zapisano zmiany pracownika: {imie} {nazwisko}")


def zapisz_edycje_klienta(idx):
    c = lista_klientow[idx]
    imie = entry_imie.get().strip()
    nazwisko = entry_nazwisko.get().strip()
    miejscowosc = entry_miejscowosc.get().strip()
    nazwa_kompleksu = combo_kompleks.get()
    if not imie or not nazwisko or not miejscowosc:
        messagebox.showwarning("Brak danych", "Podaj imię, nazwisko i miejscowość klienta!")
        return
    c.imie = imie
    c.nazwisko = nazwisko
    c.miejscowosc = miejscowosc
    if c.kompleks and c in c.kompleks.klienci:
        c.kompleks.klienci.remove(c)
    nowy_kompleks = None
    for k in lista_kompleksow:
        if k.nazwa == nazwa_kompleksu:
            nowy_kompleks = k
            break
    c.kompleks = nowy_kompleks
    if nowy_kompleks:
        nowy_kompleks.klienci.append(c)
    c.aktualizuj_marker(mapa)
    button_dodaj.config(text="Dodaj", command=dodaj_obiekt)
    entry_nazwa.config(state=NORMAL)
    wyczysc_formularz()
    pokaz_wszystkie_obiekty()
    messagebox.showinfo("Zapisano", f"Zapisano zmiany klienta: {imie} {nazwisko}")


def pokaz_szczegoly():
    typ = var_typ.get()
    try:
        idx = listbox_obiekty.curselection()[0]
    except IndexError:
        messagebox.showwarning("Błąd", "Wybierz obiekt z listy!")
        return

    if typ == "Kompleksy":
        k = lista_kompleksow[idx]
        label_szczegoly.config(text=f"Nazwa: {k.nazwa}\nMiejscowość: {k.miejscowosc}\n"
                                    f"Pracownicy: {len(k.pracownicy)}\nKlienci: {len(k.klienci)}")
        mapa.set_position(k.wspolrzedne[0], k.wspolrzedne[1])
        mapa.set_zoom(13)
    elif typ == "Pracownicy":
        p = lista_pracownikow[idx]
        label_szczegoly.config(text=f"Imię: {p.imie}\nNazwisko: {p.nazwisko}\nMiejscowość: {p.miejscowosc}\n"
                                    f"Kompleks: {p.kompleks.nazwa if p.kompleks else 'Brak'}")
        mapa.set_position(p.wspolrzedne[0], p.wspolrzedne[1])
        mapa.set_zoom(15)
    elif typ == "Klienci":
        c = lista_klientow[idx]
        label_szczegoly.config(text=f"Imię: {c.imie}\nNazwisko: {c.nazwisko}\nMiejscowość: {c.miejscowosc}\n"
                                    f"Kompleks: {c.kompleks.nazwa if c.kompleks else 'Brak'}")
        mapa.set_position(c.wspolrzedne[0], c.wspolrzedne[1])
        mapa.set_zoom(15)


def odswiez_mape():
    mapa.delete_all_marker()
    typ = var_typ.get()
    if typ == "Kompleksy":
        for k in lista_kompleksow:
            k.marker = mapa.set_marker(k.wspolrzedne[0], k.wspolrzedne[1], text=f"Kompleks: {k.nazwa}")
    elif typ == "Pracownicy":
        for p in lista_pracownikow:
            p.marker = mapa.set_marker(p.wspolrzedne[0], p.wspolrzedne[1], text=f"Pracownik: {p.imie} {p.nazwisko}")
    elif typ == "Klienci":
        for c in lista_klientow:
            c.marker = mapa.set_marker(c.wspolrzedne[0], c.wspolrzedne[1], text=f"Klient: {c.imie} {c.nazwisko}")


def aktualizuj_combo_kompleks():
    combo_kompleks['values'] = [k.nazwa for k in lista_kompleksow]


def zmien_typ(event=None):
    typ = var_typ.get()
    if typ == "Kompleksy":
        entry_nazwa.config(state=NORMAL)
        entry_imie.config(state=DISABLED)
        entry_nazwisko.config(state=DISABLED)
        combo_kompleks.config(state=DISABLED)
    else:
        entry_nazwa.delete(0, END)
        entry_nazwa.config(state=DISABLED)
        entry_imie.config(state=NORMAL)
        entry_nazwisko.config(state=NORMAL)
        combo_kompleks.config(state=NORMAL)

    wyczysc_formularz()
    pokaz_wszystkie_obiekty()
    aktualizuj_combo_kompleks()
    odswiez_mape()
    label_szczegoly.config(text="")



root = Tk()
root.title("Zarządzanie kompleksami sportowymi i rezerwacjami")
root.geometry("900x600")

# Lewa ramka - lista i szczegóły
frame_lewy = Frame(root)
frame_lewy.pack(side=LEFT, fill=BOTH, expand=False, padx=10, pady=10)

Label(frame_lewy, text="Typ obiektu:").pack(anchor=W)
var_typ = StringVar()
var_typ.set("Kompleksy")
combo_typ = OptionMenu(frame_lewy, var_typ, "Kompleksy", "Pracownicy", "Klienci", command=zmien_typ)
combo_typ.pack(anchor=W, fill=X)

listbox_obiekty = Listbox(frame_lewy, height=20)
listbox_obiekty.pack(fill=BOTH, expand=True)
listbox_obiekty.bind('<<ListboxSelect>>', lambda e: pokaz_szczegoly())

label_szczegoly = Label(frame_lewy, text="", justify=LEFT)
label_szczegoly.pack(fill=X, pady=5)

button_edytuj = Button(frame_lewy, text="Edytuj", command=edytuj_obiekt)
button_edytuj.pack(fill=X)

button_usun = Button(frame_lewy, text="Usuń", command=usun_obiekt)
button_usun.pack(fill=X, pady=5)

# Prawa ramka - formularz i mapa
frame_prawy = Frame(root)
frame_prawy.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

# Formularz
frame_form = Frame(frame_prawy)
frame_form.pack(fill=X, pady=5)

Label(frame_form, text="Nazwa (kompleks):").grid(row=0, column=0, sticky=W)
entry_nazwa = Entry(frame_form)
entry_nazwa.grid(row=0, column=1, sticky=EW)

Label(frame_form, text="Imię:").grid(row=1, column=0, sticky=W)
entry_imie = Entry(frame_form)
entry_imie.grid(row=1, column=1, sticky=EW)

Label(frame_form, text="Nazwisko:").grid(row=2, column=0, sticky=W)
entry_nazwisko = Entry(frame_form)
entry_nazwisko.grid(row=2, column=1, sticky=EW)

Label(frame_form, text="Miejscowość:").grid(row=3, column=0, sticky=W)
entry_miejscowosc = Entry(frame_form)
entry_miejscowosc.grid(row=3, column=1, sticky=EW)

Label(frame_form, text="Kompleks (dla prac./klientów):").grid(row=4, column=0, sticky=W)
combo_kompleks = tkinter.ttk.Combobox(frame_form, state="readonly")
combo_kompleks.grid(row=4, column=1, sticky=EW)

frame_form.columnconfigure(1, weight=1)

button_dodaj = Button(frame_prawy, text="Dodaj", command=dodaj_obiekt)
button_dodaj.pack(fill=X, pady=5)

button_odswiez_mape = Button(frame_prawy, text="Odśwież mapę", command=odswiez_mape)
button_odswiez_mape.pack(fill=X)

# Mapa
frame_mapa = Frame(frame_prawy)
frame_mapa.pack(fill=BOTH, expand=True)

mapa = tkintermapview.TkinterMapView(frame_mapa, width=600, height=400, corner_radius=0)
mapa.pack(fill=BOTH, expand=True)
mapa.set_position(52.22977, 21.01178)
mapa.set_zoom(6)

zmien_typ()

root.mainloop()
