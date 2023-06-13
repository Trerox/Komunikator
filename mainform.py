import tkinter as tk
import messageform
import addfriendform
import notificationsform
import friendslistform


class mainform:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id

        # ----------- CENTER FORM ------------- #
        w = 1000  # Zmniejszono szerokość okna
        h = 500  # Zmniejszono wysokość okna
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws - w) / 2
        y = (hs - h) / 2
        self.master.title("Menu główne")
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))

        # ----------- MENU ------------- #

        # Przycisk "Napisz wiadomość"
        self.btn_create_conversation = tk.Button(self.master, text="Utwórz konwersację", command=self.open_message_form,
                                                 width=20, height=2)
        self.btn_create_conversation.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

        # Przycisk "Dodaj znajomego"
        self.btn_add_friend = tk.Button(self.master, text="Dodaj znajomego", command=self.open_add_friend_form,
                                        width=20, height=2)
        self.btn_add_friend.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

        # Przycisk "Powiadomienia"
        self.btn_notifications = tk.Button(self.master, text="Powiadomienia", command=self.show_notifications,
                                           width=20, height=2)
        self.btn_notifications.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

        # Przycisk "Lista znajomych"
        self.btn_friends_list = tk.Button(self.master, text="Lista znajomych", command=self.open_friends_list,
                                          width=20, height=2)
        self.btn_friends_list.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

        # ------------------------------ #

    def open_message_form(self):
        message_form = tk.Toplevel(self.master)
        message_form.title("Konwersacja")
        message_form.geometry("800x400+300+200")

        # Tworzenie instancji klasy MessageForm w nowym oknie
        message_form_instance = messageform.MessageForm(message_form,self.user_id)

    def open_add_friend_form(self):
        add_friend_form = tk.Toplevel(self.master)
        add_friend_form.title("Dodaj znajomego")
        add_friend_form.geometry("600x300+400+200")

        # Tworzenie instancji klasy AddFriendForm w nowym oknie
        add_friend_form_instance = addfriendform.AddFriendForm(add_friend_form, self.user_id)

    def show_notifications(self):
        notifications_window = tk.Toplevel(self.master)
        notifications_window.title("Powiadomienia")
        notifications_window.geometry("400x300+400+200")

        # Tworzenie instancji klasy NotificationsForm w nowym oknie
        notifications_form_instance = notificationsform.NotificationsForm(notifications_window, self.user_id)

    def open_friends_list(self):
        friends_list_window = tk.Toplevel(self.master)
        friends_list_window.title("Lista znajomych")
        friends_list_window.geometry("400x300+400+200")

        # Tworzenie instancji klasy FriendListForm w nowym oknie
        friends_list_form_instance = friendslistform.FriendListForm(friends_list_window, self.user_id)


if __name__ == "__main__":
    root = tk.Tk()
    main_form = mainform(root)
    root.mainloop()
