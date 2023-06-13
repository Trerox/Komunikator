import tkinter as tk
import mysql.connector

class MessageForm:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id
        self.friend_buttons = []  # Lista przechowująca przyciski znajomych
        self.selected_friend_id = None  # Zmienna przechowująca ID wybranego znajomego
        self.last_message_time = None  # Czas ostatniej odczytanej wiadomości

        self.master.title("Formularz wiadomości")
        self.master.geometry("800x400+300+200")

        self.left_frame = tk.Frame(self.master)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.right_frame = tk.Frame(self.master)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.txt_message = tk.Text(self.right_frame, height=10, width=50)
        self.txt_message.pack(side=tk.TOP, padx=10, pady=10)

        self.btn_send = tk.Button(self.right_frame, text="Wyślij", command=self.send_message, state=tk.DISABLED)
        self.btn_send.pack(side=tk.TOP, padx=10)

        self.txt_received_message = tk.Text(self.right_frame, height=10, width=50, state="disabled")
        self.txt_received_message.pack(side=tk.TOP, padx=10, pady=10)

        self.master.after(1000, self.read_messages)

        self.db_connection = mysql.connector.connect(
            host='localhost', user='root', port='3306',
            password='', database='py_lg_rg_db'
        )
        self.db_cursor = self.db_connection.cursor()

        self.refresh_friends_list()

    def open_message_history(self, friend_id):
        self.selected_friend_id = friend_id
        self.txt_received_message.config(state="normal")
        self.txt_received_message.delete("1.0", tk.END)  # Wyczyść pole z historią konwersacji
        self.txt_received_message.config(state="disabled")
        self.btn_send.config(state=tk.NORMAL)  # Włącz przycisk "Wyślij"

        # Aktualizuj czas ostatniej odczytanej wiadomości na bieżący czas
        self.last_message_time = None

        # Aktualizuj historię konwersacji dla wybranego znajomego
        self.read_messages()

    def send_message(self):
        message = self.txt_message.get("1.0", tk.END)

        insert_query = "INSERT INTO messages (sender_id, recipient_id, message_text) VALUES (%s, %s, %s)"
        values = (self.user_id, self.selected_friend_id, message)
        self.db_cursor.execute(insert_query, values)
        self.db_connection.commit()

        print("Wiadomość do:", self.selected_friend_id)
        print("Wiadomość:", message)

        # Wyczyść pole do wpisywania wiadomości po wysłaniu
        self.txt_message.delete("1.0", tk.END)

        # Aktualizuj czas ostatniej odczytanej wiadomości na bieżący czas
        self.last_message_time = None

        # Aktualizuj historię konwersacji dla wybranego znajomego
        self.read_messages()

    def receive_message(self, message):
        current_messages = self.txt_received_message.get("1.0", tk.END)
        if message not in current_messages:
            self.txt_received_message.config(state="normal")
            self.txt_received_message.insert(tk.END, message + "\n")
            self.txt_received_message.config(state="disabled")

    def read_messages(self):
        if self.selected_friend_id is not None:
            if self.last_message_time is None:
                query = "SELECT sender_id, message_text, sent_at FROM messages WHERE (sender_id = %s AND recipient_id = %s) OR (sender_id = %s AND recipient_id = %s)"
                values = (self.user_id, self.selected_friend_id, self.selected_friend_id, self.user_id)
            else:
                query = "SELECT sender_id, message_text, sent_at FROM messages WHERE ((sender_id = %s AND recipient_id = %s) OR (sender_id = %s AND recipient_id = %s)) AND sent_at > %s"
                values = (self.user_id, self.selected_friend_id, self.selected_friend_id, self.user_id, self.last_message_time)

            self.db_cursor.execute(query, values)
            messages = self.db_cursor.fetchall()
            for message in messages:
                sender_id, message_text, sent_at = message
                formatted_message = f"Wiadomość od {sender_id} ({sent_at}): {message_text}"
                self.receive_message(formatted_message)

            if messages:
                self.last_message_time = messages[-1][2]

        self.db_connection.commit()
        self.master.after(1000, self.read_messages)

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

        # Zamykanie połączenia z bazą danych
        c.close()
        conn.close()

        return friends

    def create_friend_button(self, friend_id, username):
        # Tworzenie przycisku dla danego znajomego
        print(friend_id)
        button = tk.Button(self.left_frame, text=username, command=lambda: self.open_message_history(friend_id))
        button.pack(side=tk.TOP, pady=5)
        self.friend_buttons.append(button)

    def refresh_friends_list(self):
        self.clear_friend_buttons()  # Wyczyść przyciski znajomych

        friends = self.get_friends_data()
        for row in friends:
            user_id = row[0]
            username_user = row[1]
            friend_id = row[2]
            username_friend = row[3]

            if friend_id == self.user_id:
                username = username_user
                self.create_friend_button(user_id, username)  # Tworzenie przycisku dla danego znajomego
            else:
                username = username_friend
                self.create_friend_button(friend_id, username)  # Tworzenie przycisku dla danego znajomego

    def clear_friend_buttons(self):
        for button in self.friend_buttons:
            button.pack_forget()
        self.friend_buttons = []


if __name__ == "__main__":
    root = tk.Tk()
    user_id = 1
    message_form = MessageForm(root, user_id)
    root.mainloop()
