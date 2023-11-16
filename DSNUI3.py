import tkinter as tk
import json

class User:
    def __init__(self, username):
        self.username = username
        self.posts = []
        self.friends = []

    def create_post(self, content):
        self.posts.append(content)
        print(f"Post created by {self.username}.")

    def add_friend(self, friend):
        self.friends.append(friend)
        print(f"{self.username} and {friend} are now friends.")

class Network:
    def __init__(self):
        self.users = {}
        self.load_user_data()

    def create_user(self, username):
        if username not in self.users:
            self.users[username] = User(username)
            print(f"User {username} created.")
            self.save_user_data()  # Save user data after creating a user
            return True
        else:
            print("Username already exists.")
            return False

    def login_user(self, username):
        if username in self.users:
            print(f"User {username} logged in.")
            return True
        else:
            print("User does not exist.")
            return False

    def make_post(self, username, content):
        if username in self.users:
            user = self.users[username]
            user.create_post(content)
            self.save_user_data()  # Save user data after making a post
        else:
            print("User not found.")

    def add_friendship(self, username, friend):
        if username in self.users and friend in self.users:
            user = self.users[username]
            friend_user = self.users[friend]
            user.add_friend(friend)
            friend_user.add_friend(username)
            self.save_user_data()  # Save user data after adding friendship
        else:
            print("User(s) not found.")

    def save_user_data(self):
        with open("user_data.json", "w") as file:
            user_data = {username: {"posts": user.posts, "friends": user.friends} for username, user in self.users.items()}
            json.dump(user_data, file)

    def load_user_data(self):
        try:
            with open("user_data.json", "r") as file:
                user_data = json.load(file)
                for username, data in user_data.items():
                    new_user = User(username)
                    new_user.posts = data["posts"]
                    new_user.friends = data["friends"]
                    self.users[username] = new_user
        except FileNotFoundError:
            # File does not exist, continue with an empty user database
            pass

class LoginWindow:
    def __init__(self, master, network, account_window):
        self.master = master
        self.master.title("Login")
        self.master.configure(bg="black")  # Set background color to black

        self.network = network
        self.account_window = account_window

        self.label_username = tk.Label(master, text="Enter Username:", font=("Arial", 16), bg="black", fg="white")
        self.entry_username = tk.Entry(master, font=("Arial", 16))
        self.button_login = tk.Button(master, text="Login", command=self.login, bg="light green", fg="black", font=("Arial", 16))
        self.button_signup = tk.Button(master, text="Sign Up", command=self.signup, bg="sky blue", fg="black", font=("Arial", 16))

        self.label_username.grid(row=0, column=0, padx=10, pady=10)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)
        self.button_login.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.button_signup.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.button_exit = tk.Button(master, text="Exit", command=self.exit_app, bg="red", fg="black", font=("Arial", 16))
        self.button_exit.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def exit_app(self):
        self.master.destroy()

    def login(self):
        username = self.entry_username.get()
        if self.network.login_user(username):
            self.account_window.set_current_user(username)
            self.account_window.show_window()

    def signup(self):
        username = self.entry_username.get()
        if self.network.create_user(username):
            self.account_window.set_current_user(username)
            self.account_window.show_window()

class AccountWindow:
    def __init__(self, master, network):
        self.master = master
        self.master.title("Account")
        self.master.configure(bg="black")  # Set background color to black

        self.network = network
        self.current_user = None

        self.label_username = tk.Label(master, text="", font=("Arial", 16), bg="black", fg="white")
        self.entry_content = tk.Entry(master, font=("Arial", 16))
        self.entry_friend = tk.Entry(master, font=("Arial", 16))
        self.button_make_post = tk.Button(master, text="Make Post", command=self.make_post, bg="light green", fg="black", font=("Arial", 16))
        self.button_add_friendship = tk.Button(master, text="Add Friendship", command=self.add_friendship, bg="orange", fg="black", font=("Arial", 16))
        self.button_display_friends_info = tk.Button(master, text="Display Friends Info", command=self.display_friends_info, bg="light blue", fg="black", font=("Arial", 16))
        self.button_display_posts_info = tk.Button(master, text="Display Posts Info", command=self.display_posts_info, bg="light yellow", fg="black", font=("Arial", 16))
        self.button_exit = tk.Button(master, text="Exit", command=self.exit_windows, bg="red", fg="black", font=("Arial", 16))

        self.label_username.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.entry_content.grid(row=1, column=0, padx=10, pady=10)
        self.entry_friend.grid(row=1, column=1, padx=10, pady=10)
        self.button_make_post.grid(row=2, column=0, padx=10, pady=10)
        self.button_add_friendship.grid(row=2, column=1, padx=10, pady=10)
        self.button_display_friends_info.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.button_display_posts_info.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.button_exit.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def set_current_user(self, username):
        self.current_user = username
        self.label_username.config(text=f"Logged in as: {username}")

    def make_post(self):
        content = self.entry_content.get()
        if self.current_user:
            self.network.make_post(self.current_user, content)

    def add_friendship(self):
        friend = self.entry_friend.get()
        if self.current_user:
            self.network.add_friendship(self.current_user, friend)

    def display_friends_info(self):
        if self.current_user:
            user = self.network.users[self.current_user]
            friend_info_window = tk.Toplevel(self.master)
            friend_info_window.title("Friends Information")
            friend_info_window.configure(bg="black")

            info_label = tk.Label(friend_info_window, text=f"Friends of {self.current_user}: {', '.join(user.friends)}", fg="white", bg="black", font=("Arial", 16))
            info_label.pack(padx=20, pady=10)

    def display_posts_info(self):
        if self.current_user:
            user = self.network.users[self.current_user]
            posts_info_window = tk.Toplevel(self.master)
            posts_info_window.title("Posts Information")
            posts_info_window.configure(bg="black")

            info_label = tk.Label(posts_info_window, text=f"Posts by {self.current_user}: {', '.join(user.posts)}", fg="white", bg="black", font=("Arial", 16))
            info_label.pack(padx=20, pady=10)

    def exit_windows(self):
        self.master.destroy()

    def show_window(self):
        self.master.deiconify()

# Main code block
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="black")
    network = Network()
    account_window = AccountWindow(tk.Toplevel(root), network)
    login = LoginWindow(root, network, account_window)
    root.mainloop()
