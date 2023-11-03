import mysql.connector
import tkinter as tk

class TaxiServiceDatabase:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Создание таблиц в базе данных
        create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255)
            )
        """
        create_rides_table = """
            CREATE TABLE IF NOT EXISTS rides (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                pickup_location VARCHAR(255),
                dropoff_location VARCHAR(255),
                fare DECIMAL(10, 2),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """
        
        self.cursor.execute(create_users_table)
        self.cursor.execute(create_rides_table)
        self.conn.commit()
    
    def insert_user(self, name, email):
        # Вставка нового пользователя в таблицу "users"
        insert_user_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        self.cursor.execute(insert_user_query, (name, email))
        self.conn.commit()
    
    def insert_ride(self, user_id, pickup_location, dropoff_location, fare):
        # Вставка новой поездки в таблицу "rides"
        insert_ride_query = "INSERT INTO rides (user_id, pickup_location, dropoff_location, fare) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(insert_ride_query, (user_id, pickup_location, dropoff_location, fare))
        self.conn.commit()
    
    def close(self):
        self.cursor.close()
        self.conn.close()

class TaxiServiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Taxi Service App")

        self.db = TaxiServiceDatabase(host='your_host', user='your_user', password='your_password', database='your_database')

        self.create_user_entry()
        self.create_ride_entry()
    
    def create_user_entry(self):
        user_frame = tk.Frame(self.root)
        user_frame.pack()

        tk.Label(user_frame, text="Name:").grid(row=0, column=0)
        tk.Label(user_frame, text="Email:").grid(row=1, column=0)

        self.name_entry = tk.Entry(user_frame)
        self.email_entry = tk.Entry(user_frame)

        self.name_entry.grid(row=0, column=1)
        self.email_entry.grid(row=1, column=1)

        insert_user_button = tk.Button(user_frame, text="Insert User", command=self.insert_user)
        insert_user_button.grid(row=2, columnspan=2)
    
    def create_ride_entry(self):
        ride_frame = tk.Frame(self.root)
        ride_frame.pack()

        tk.Label(ride_frame, text="User ID:").grid(row=0, column=0)
        tk.Label(ride_frame, text="Pickup Location:").grid(row=1, column=0)
        tk.Label(ride_frame, text="Dropoff Location:").grid(row=2, column=0)
        tk.Label(ride_frame, text="Fare:").grid(row=3, column=0)

        self.user_id_entry = tk.Entry(ride_frame)
        self.pickup_entry = tk.Entry(ride_frame)
        self.dropoff_entry = tk.Entry(ride_frame)
        self.fare_entry = tk.Entry(ride_frame)

        self.user_id_entry.grid(row=0, column=1)
        self.pickup_entry.grid(row=1, column=1)
        self.dropoff_entry.grid(row=2, column=1)
        self.fare_entry.grid(row=3, column=1)

        insert_ride_button = tk.Button(ride_frame, text="Insert Ride", command=self.insert_ride)
        insert_ride_button.grid(row=4, columnspan=2)
    
    def insert_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()

        if name and email:
            self.db.insert_user(name, email)
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
    
    def insert_ride(self):
        user_id = self.user_id_entry.get()
        pickup_location = self.pickup_entry.get()
        dropoff_location = self.dropoff_entry.get()
        fare = self.fare_entry.get()

        if user_id and pickup_location and dropoff_location and fare:
            self.db.insert_ride(int(user_id), pickup_location, dropoff_location, float(fare))
            self.user_id_entry.delete(0, tk.END)
            self.pickup_entry.delete(0, tk.END)
            self.dropoff_entry.delete(0, tk.END)
            self.fare_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaxiServiceApp(root)
    root.mainloop()
