import tkinter as tk
from tkinter import messagebox as msgbox

import mysql.connector


class NotificationsForm:
    def __init__(self, master, user_id):
        self.master = master
        self.master.title("Powiadomienia")
        self.user_id = user_id

        # Rozmiar i położenie formularza
        self.master.geometry("400x300+400+200")

        # Tworzenie elementów interfejsu dla formularza powiadomień
        self.lbl_title = tk.Label(self.master, text="Powiadomienia", font=("Arial", 20))
        self.lbl_title.pack(pady=20)

        self.frame_notifications = tk.Frame(self.master)
        self.frame_notifications.pack()

        self.notifications = []  # Lista przechowująca informacje o powiadomieniach

        self.check_friend_requests()

    def check_friend_requests(self):
        # Sprawdzanie czy istnieją zaproszenia do znajomych
        conn = mysql.connector.connect(host='localhost', user='root', port='3306',
                                       password='', database='py_lg_rg_db')
        c = conn.cursor()

        select_query = "SELECT * FROM friends WHERE friend_id = %s AND status = 'Oczekujący'"
        c.execute(select_query, (self.user_id,))
        friend_requests = c.fetchall()

        if len(friend_requests) > 0:
            for request in friend_requests:
                self.show_friend_request(request)

        c.close()
        conn.close()

    def accept_invitation(self, friend_id, notification_id):
        conn = mysql.connector.connect(host='localhost', user='root', port='3306',
                                       password='', database='py_lg_rg_db')
        c = conn.cursor()

        update_query = "UPDATE friends SET status = 'Zaakceptowany' WHERE id = %s"
        c.execute(update_query, (notification_id,))
        conn.commit()

        c.close()
        conn.close()

        msgbox.showinfo("Sukces", f"Akceptowano zaproszenie od użytkownika o ID {friend_id}")
        self.update_notifications_list()

    def decline_invitation(self, friend_id, notification_id):
        conn = mysql.connector.connect(host='localhost', user='root', port='3306',
                                       password='', database='py_lg_rg_db')
        c = conn.cursor()

        update_query = "UPDATE friends SET status = 'Odrzucony' WHERE id = %s"
        c.execute(update_query, (notification_id,))
        conn.commit()

        c.close()
        conn.close()

        msgbox.showinfo("Sukces", f"Odrzucono zaproszenie od użytkownika o ID {friend_id}")
        self.update_notifications_list()

    def update_notifications_list(self):
        # Czyszczenie listy powiadomień i aktualizacja
        for widget in self.frame_notifications.winfo_children():
            widget.destroy()

        self.check_friend_requests()

    def show_friend_request(self, request):
        # Wyświetlanie powiadomienia o zaproszeniu do znajomych
        print(request)
        friend_id = request[1]  # ID osoby zapraszającej do znajomych
        notification_id = request[0]  # ID powiadomienia

        frame = tk.Frame(self.frame_notifications)
        frame.pack(pady=10)

        message = f"Użytkownik o ID {friend_id} zaprosił Cię do znajomych."
        lbl_message = tk.Label(frame, text=message)
        lbl_message.pack(side=tk.LEFT)

        btn_accept = tk.Button(frame, text="Akceptuj",
                               command=lambda f=friend_id, n=notification_id: self.accept_invitation(f, n))
        btn_accept.pack(side=tk.LEFT, padx=5)

        btn_decline = tk.Button(frame, text="Odrzuć",
                                command=lambda f=friend_id, n=notification_id: self.decline_invitation(f, n))
        btn_decline.pack(side=tk.LEFT, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    user_id = 123  # Podaj swoje ID użytkownika
    notifications_form = NotificationsForm(root, user_id)
    root.mainloop()
