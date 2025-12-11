import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import csv

# File to store booking data
filename = "concert_bookings.csv"
users_file = "users.csv"

# Initialize concert data
concerts = {
    "Vijay Antony": {"VIP": 3000, "Gold": 2000, "Silver": 1000, "image": "vijay.jpg"},
    "Hip Hop Tamizha": {"VIP": 2500, "Gold": 1800, "Silver": 900, "image": "hip.jpg"},
    "Anirudh": {"VIP": 2700, "Gold": 1900, "Silver": 800, "image": "anirudh.jpg"},
    "Yuvan X STR": {"VIP": 2000, "Gold": 1500, "Silver": 700, "image": "str.jpg"},
}

# Initialize CSV files
def initialize_csv():
    try:
        # Initialize bookings file
        with open(filename, mode="a+", newline="") as file:
            file.seek(0)
            if not file.read(1):  # File is empty
                writer = csv.writer(file)
                writer.writerow(["Concert", "User", "Tier", "Seats", "Total Price"])
        # Initialize users file
        with open(users_file, mode="a+", newline="") as file:
            file.seek(0)
            if not file.read(1):  # File is empty
                writer = csv.writer(file)
                writer.writerow(["Username", "Password"])
    except PermissionError:
        messagebox.showerror("Error", "Permission denied for file operations.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not initialize files: {e}")

# Load booked seats
def load_booked_seats():
    booked_seats = {concert: {"VIP": [], "Gold": [], "Silver": []} for concert in concerts}
    try:
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames != ["Concert", "User", "Tier", "Seats", "Total Price"]:
                raise ValueError("Invalid file format for bookings file.")
            for row in reader:
                if row["Concert"] in concerts:
                    tiers = row["Tier"].split(" / ")
                    seats = row["Seats"].split(", ")
                    for tier in tiers:
                        if tier in booked_seats[row["Concert"]]:
                            booked_seats[row["Concert"]][tier].extend(seats)
    except FileNotFoundError:
        # If file doesn't exist, initialize it
        initialize_csv()
    except ValueError as ve:
        messagebox.showerror("Error", f"File format error: {ve}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not load booked seats: {e}")
    return booked_seats

# Save booking
def save_booking(concert, user, tier, seats, total_price):
    try:
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([concert, user, tier, ", ".join(seats), f"${total_price:.2f}"])
    except Exception as e:
        messagebox.showerror("Error", f"Could not save booking: {e}")

# Save user
def save_user(username, password):
    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty!")
        return

    try:
        with open(users_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Username"] == username:
                    messagebox.showerror("Error", "Username already exists! Please choose another.")
                    return
    except FileNotFoundError:
        pass

    try:
        with open(users_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, password])
        messagebox.showinfo("Success", "Account created successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save user: {e}")

# Authenticate user
def authenticate_user(username, password):
    try:
        with open(users_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Username"] == username and row["Password"] == password:
                    return True
    except FileNotFoundError:
        messagebox.showerror("Error", "User database not found!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not authenticate user: {e}")
    return False

# Tiered Seating Page
def open_seat_selection(username, concert):
    booked_seats = load_booked_seats()  # Reload booked seats for fresh updates
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"{concert} - Seat Selection", font=("Helvetica", 16)).pack(pady=10)
    tk.Label(root, text="Stage Location: Performer will perform at the bottom of the seating layout.", font=("Helvetica", 12), fg="blue").pack()

    tiers = ["VIP", "Gold", "Silver"]
    tier_frames = {}
    selected_seats = {tier: [] for tier in tiers}

    def toggle_seat(tier, seat):
        if seat in selected_seats[tier]:
            selected_seats[tier].remove(seat)
            tier_frames[tier][seat].config(bg="lightgray")
        elif len(selected_seats[tier]) < 10:  # Limit seats to 10 per tier
            selected_seats[tier].append(seat)
            tier_frames[tier][seat].config(bg="green")
        else:
            messagebox.showwarning("Limit Reached", "You can only select up to 10 seats per tier.")

    for tier in tiers:
        tk.Label(root, text=f"{tier} Section - Price: ₹{concerts[concert][tier]} per seat", font=("Helvetica", 14)).pack(pady=5)
        tier_frame = tk.Frame(root)
        tier_frame.pack(pady=5)
        tier_frames[tier] = {}

        rows, cols = 2, 5  # 10 seats per tier (2 rows, 5 columns)
        seats = [f"{tier[0]}{r}{c}" for r in range(1, rows + 1) for c in range(1, cols + 1)]
        booked = booked_seats[concert][tier]

        for i, seat in enumerate(seats):
            row, col = divmod(i, cols)
            color = "red" if seat in booked else "lightgray"  # Booked seats are red
            btn = tk.Button(
                tier_frame, text=seat, width=5, height=2, bg=color,
                state="disabled" if seat in booked else "normal",  # Disable booked seats
                command=lambda t=tier, s=seat: toggle_seat(t, s)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            tier_frames[tier][seat] = btn

    def confirm_booking():
        total_price = 0
        all_selected_seats = []
        for tier in tiers:
            seats = selected_seats[tier]
            if seats:
                price = concerts[concert][tier]
                total_price += price * len(seats)
                all_selected_seats.extend(seats)

        if not all_selected_seats:
            messagebox.showwarning("Error", "No seats selected!")
            return

        save_booking(concert, username, " / ".join(tiers), all_selected_seats, total_price)
        messagebox.showinfo("Success", f"Booking confirmed!\nSeats: {', '.join(all_selected_seats)}\nTotal Price: ₹{total_price}")
        open_concert_selection(username)
     #performer
    stage_label = tk.Label(root, text="Stage", font=("Helvetica", 14), bg="yellow", width=10, height=2)
    stage_label.pack(pady=10)

    tk.Button(root, text="Confirm Booking", command=confirm_booking, width=15, bg="green", fg="white").pack(pady=10)
    tk.Button(root, text="Back", command=lambda: open_concert_selection(username), width=10, bg="red", fg="white").pack(pady=5)
   
# Concert Selection
def open_concert_selection(username):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"Welcome {username}!", font=("Helvetica", 18, "bold")).pack(pady=10)
    tk.Label(root, text="Select a Concert", font=("Helvetica", 16)).pack(pady=10)

    concert_frame = tk.Frame(root)
    concert_frame.pack()

    for i, (concert_name, concert_data) in enumerate(concerts.items()):
        try:
            img = Image.open(concert_data["image"])
            img = img.resize((120, 180))
            img = ImageTk.PhotoImage(img)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Image file for {concert_name} not found!")
            continue

        btn = tk.Button(
            concert_frame,
            image=img,
            command=lambda c=concert_name: open_seat_selection(username, c)
        )
        btn.image = img
        btn.grid(row=0, column=i, padx=10)
        tk.Label(concert_frame, text=concert_name, font=("Helvetica", 12)).grid(row=1, column=i)

# Login or Sign Up
def show_login_signup_page():
    for widget in root.winfo_children():
        widget.destroy()

    def attempt_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if authenticate_user(username, password):
            open_concert_selection(username)
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def attempt_signup():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        save_user(username, password)

    tk.Label(root, text="Login / Sign Up", font=("Helvetica", 18, "bold")).pack(pady=10)
    tk.Label(root, text="Username", font=("Helvetica", 14)).pack()
    username_entry = tk.Entry(root, font=("Helvetica", 14))
    username_entry.pack(pady=5)

    tk.Label(root, text="Password", font=("Helvetica", 14)).pack()
    password_entry = tk.Entry(root, font=("Helvetica", 14), show="*")
    password_entry.pack(pady=5)

    tk.Button(root, text="Login", command=attempt_login, font=("Helvetica", 14), bg="green", fg="white").pack(pady=5)
    tk.Button(root, text="Sign Up", command=attempt_signup, font=("Helvetica", 14), bg="blue", fg="white").pack(pady=5)

# Initialize the app
initialize_csv()
root = tk.Tk()
root.geometry("900x800")
root.title("Concert Booking System")
show_login_signup_page()
root.mainloop()
