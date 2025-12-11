Concert Booking System -- Python Tkinter GUI

A simple and interactive **Concert Ticket Booking Application** built
using **Python, Tkinter, CSV handling, and PIL for images**.\
Users can **sign up / log in**, choose from multiple concerts, view seat
availability, and book seats across different tiers (VIP / Gold /
Silver).

------------------------------------------------------------------------

Features

 User Login / Sign-up System

-   Accounts stored in `users.csv`
-   Duplicate username protection
-   Simple authentication

 Concert Selection

-   Multiple concerts with posters
-   VIP / Gold / Silver tiers
-   Different ticket pricing

 Tier-based Seat Booking

-   10 seats per tier (2×5 grid)
-   Colors:
    -   Red → booked\
    -   Grey → available\
    -   Green → selected

CSV Storage

-   `concert_bookings.csv` stores all bookings

 Booking Confirmation

-   Shows selected seats
-   Calculates total price
-   Saves to CSV

------------------------------------------------------------------------

 Project Structure

    ConcertBookingSystem/
    │
    ├── concertt.py
    ├── concert_bookings.csv
    ├── users.csv
    ├── hip.jpg
    ├── vijay.jpg
    ├── anirudh.jpg
    ├── str.jpg
    └── README.md

------------------------------------------------------------------------

How to Run

1️⃣ Install dependencies

    pip install pillow

2️⃣ Run the app

    python concertt.py

------------------------------------------------------------------------

Future Improvements

-   Payment simulation\
-   Cancel/modify bookings\
-   Better themes/UI\
-   Cloud database integration

------------------------------------------------------------------------

Credits

-   Developed by: **Krithik**
-   Built using **Python, Tkinter, PIL**
