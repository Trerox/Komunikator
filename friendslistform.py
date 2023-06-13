import tkinter as tk
from tkinter import Scrollbar
import mysql.connector

class FriendListForm:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id

        # Tworzenie kontenera dla listy znajomych
        self.friends_canvas = tk.Canvas(self.master)
        self.friends_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tworzenie paska przewijania
        scrollbar = Scrollbar(self.master, command=self.friends_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Przypisanie paska przewijania do kontenera
        self.friends_canvas.config(yscrollcommand=scrollbar.set)
        self.friends_canvas.bind('<Configure>', lambda e: self.friends_canvas.configure(scrollregion=self.friends_canvas.bbox("all")))

        # Tworzenie ramki wewnątrz kontenera
        self.friends_container = tk.Frame(self.friends_canvas)

        # Tworzenie widżetu do przechowywania ramki
        self.friends_canvas.create_window((0, 0), window=self.friends_container, anchor="nw")

        # Wywołanie funkcji do wyświetlenia danych o znajomych
        self.show_friends_data(self.get_friends_data())


    def get_friends_data(self):
        # Połączenie z bazą danych
        conn = mysql.connector.connect(host='localhost', user='root', port='3306',
                                       password='', database='py_lg_rg_db')
        c = conn.cursor()

        query = """
            SELECT u1.id AS user_id, u1.username AS username_user,
                   u2.id AS friend_id, u2.username AS username_friend
            FROM friends f
            JOIN users u1 ON u1.id = f.user_id
            JOIN users u2 ON u2.id = f.friend_id
            WHERE (f.friend_id = %s AND f.status = 'Zaakceptowany')
                  OR (f.user_id = %s AND f.status = 'Zaakceptowany')
        """

        c.execute(query, (self.user_id, self.user_id))

        friends = c.fetchall()
        # Zamknięcie połączenia z bazą danych
        c.close()
        conn.close()
        return friends

    def show_friends_data(self, friends):
        for row in friends:
            user_id = row[0]
            username_user = row[1]
            friend_id = row[2]
            username_friend = row[3]

            if friend_id == self.user_id:
                username = username_user
                friend_text = f"ID: {user_id}, Nazwa użytkownika: {username}"
            else:
                username = username_friend
                friend_text = f"ID: {friend_id}, Nazwa użytkownika: {username}"

            # Tworzenie przycisku "Usuń"
            remove_button = tk.Button(self.friends_container, text="Usuń", command=lambda fid=friend_id: self.remove_friend(fid))
            remove_button.configure(command=lambda fid=friend_id: self.remove_friend(fid))
            friend_label = tk.Label(self.friends_container, text=friend_text)

            # Wyświetlanie znajomego i przycisku w siatce
            friend_label.grid(row=len(self.friends_container.winfo_children()), column=0, sticky="w")
            remove_button.grid(row=len(self.friends_container.winfo_children())-1, column=1, sticky="e", pady=5)


    def remove_friend(self, friend_id):
        # Połączenie z bazą danych
        conn = mysql.connector.connect(host='localhost', user='root', port='3306',
                                       password='', database='py_lg_rg_db')
        c = conn.cursor()

        # Usunięcie znajomego z bazy danych
        query = "DELETE FROM friends WHERE (user_id = %s AND friend_id = %s) OR (user_id = %s AND friend_id = %s)"
        c.execute(query, (self.user_id, friend_id, friend_id, self.user_id))

        # Zatwierdzenie zmian w bazie danych
        conn.commit()

        # Zamknięcie połączenia z bazą danych
        c.close()
        conn.close()

        # Odświeżenie listy znajomych
        self.refresh_friends_list()

    def refresh_friends_list(self):
        # Usunięcie poprzednich danych
        for widget in self.friends_container.winfo_children():
            widget.destroy()

        # Ponowne wyświetlenie danych o znajomych
        self.show_friends_data(self.get_friends_data())
