import tkinter as tk
from tkinter import messagebox
import mysql.connector

class AddFriendForm:
    def __init__(self, master,user_id):
        self.master = master
        self.master.title("Dodaj znajomego")
        self.user_id = user_id
        # Rozmiar i położenie formularza
        self.master.geometry("600x300+400+200")

        # Tworzenie elementów interfejsu dla formularza dodawania znajomego
        self.lbl_title = tk.Label(self.master, text="Dodaj nowego znajomego", font=("Arial", 20))
        self.lbl_title.pack(pady=20)

        self.lbl_name = tk.Label(self.master, text="Nazwa użytkownika:")
        self.lbl_name.pack()

        self.entry_name = tk.Entry(self.master)
        self.entry_name.pack()

        self.btn_add_friend = tk.Button(self.master, text="Dodaj", command=self.add_friend)
        self.btn_add_friend.pack(pady=10)

    def find_friend_by_name(self, friend_name):
        # Połączenie z bazą danych
        conn = mysql.connector.connect(
            host='localhost', user='root', port='3306',
            password='', database='py_lg_rg_db'
        )

        # Utworzenie kursora
        c = conn.cursor()

        # Sprawdzenie, czy użytkownik istnieje w tabeli users
        select_user_query = "SELECT id FROM users WHERE BINARY username = %s"
        c.execute(select_user_query, (friend_name,))
        user_id = c.fetchone()

        if not user_id:
            # Użytkownik nie istnieje
            messagebox.showwarning('Błąd', f'Użytkownik o nazwie {friend_name} nie istnieje')
            c.close()
            conn.close()
            return None

        # Zapytanie SQL
        select_query = "SELECT id FROM `users` WHERE BINARY `username` = %s"
        c.execute(select_query, (friend_name,))
        friend_id = c.fetchone()

        # Zamknięcie kursora i połączenia
        c.close()
        conn.close()

        return friend_id[0] if friend_id else None

    def add_friend(self):
        friend_name = self.entry_name.get().strip()
        friend_id = self.find_friend_by_name(friend_name)
        user_id = self.user_id

        if friend_id is None:
            # Użytkownik nie istnieje, przerwanie dalszego wykonania metody
            return
        if friend_id == user_id:
            # Próba dodania samego siebie do znajomych
            messagebox.showwarning('Błąd', 'Nie możesz dodać samego siebie do znajomych')
            return

        conn = mysql.connector.connect(
            host='localhost', user='root', port='3306',
            password='', database='py_lg_rg_db'
        )
        c = conn.cursor()

        # Sprawdzenie, czy para ID użytkownika i ID znajomego już istnieje w tabeli friends
        select_query = "SELECT * FROM friends WHERE (user_id = %s AND friend_id = %s) OR (user_id = %s AND friend_id = %s)"
        c.execute(select_query, (user_id, friend_id, friend_id, user_id))
        existing_friendship = c.fetchone()
        print(existing_friendship)
        if existing_friendship:
            if existing_friendship[3]=='Odrzucony':
                if existing_friendship[1]==user_id:
                    # Znajomy odrzucił nasze zaproszenie, nie będziemy mu spamić
                    messagebox.showinfo('Błąd',f'Nie możesz zaprosić do znajomych użytkownika {friend_name}')
                elif existing_friendship[2]==user_id:
                    # Odrzuciliśmy zaproszenie kiedyś, ale teraz chcemy być jego znajomymi
                    messagebox.showinfo('Sukces', f'Dodano znajomego o nazwie {friend_name}')
                    delete_query = "DELETE FROM friends WHERE user_id = %s AND friend_id = %s"
                    values = (friend_id,user_id)
                    c.execute(delete_query, values)
                    conn.commit()

                    # Utworzenie nowego wiersza
                    insert_query = "INSERT INTO friends (user_id, friend_id, status) VALUES (%s, %s, %s)"
                    values = (user_id, friend_id, "Oczekujący")
                    c.execute(insert_query, values)
                    conn.commit()

            # Znaleziono istniejące zaproszenie lub przyjaźń
            else:
                messagebox.showinfo('Błąd', f'Już wysłałeś zaproszenie lub jesteś już znajomym użytkownika {friend_name}')
        else:
            # Nie znaleziono istniejącego zaproszenia ani przyjaźni
            messagebox.showinfo('Sukces', f'Dodano znajomego o nazwie {friend_name}')

            # Dodanie zaproszenia do bazy danych
            insert_query = "INSERT INTO friends (user_id, friend_id, status) VALUES (%s, %s, %s)"
            values = (user_id, friend_id, "Oczekujący")
            c.execute(insert_query, values)
            conn.commit()
            print("Dodano nowego znajomego z nazwą:", friend_name)

        # Zamknięcie kursora i połączenia z bazą danych
        c.close()
        conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    add_friend_form = AddFriendForm(root)
    root.mainloop()
