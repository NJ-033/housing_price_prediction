import customtkinter as ctk
import tkinter.messagebox as messagebox
from tkinter import ttk
from src.database import initialize_database, authenticate_user, save_prediction, get_user_predictions, delete_prediction
from src.model import predict_price

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Filipino Housing Price Predictor")
        self.geometry("900x600")
        
        # Initialize DB
        if not initialize_database():
            messagebox.showerror("Database Error", "Could not connect to MySQL database. Please check your XAMPP/MySQL server.")
            
        self.current_user = None
        self.show_login_frame()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login_frame(self):
        self.clear_window()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.login_frame = ctk.CTkFrame(self, width=400, height=400, corner_radius=15)
        self.login_frame.grid(row=0, column=0, padx=20, pady=20)
        self.login_frame.grid_propagate(False)

        # Centering inside login frame
        self.login_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.login_frame.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(self.login_frame, text="Welcome Back", font=ctk.CTkFont(size=24, weight="bold"))
        label.grid(row=0, column=0, pady=(40, 10))

        sub_label = ctk.CTkLabel(self.login_frame, text="Login to your account", font=ctk.CTkFont(size=14))
        sub_label.grid(row=1, column=0, pady=(0, 20))

        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username", width=250)
        self.username_entry.grid(row=2, column=0, pady=10)

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*", width=250)
        self.password_entry.grid(row=3, column=0, pady=10)

        login_btn = ctk.CTkButton(self.login_frame, text="Login", command=self.login, width=250)
        login_btn.grid(row=4, column=0, pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password")
            return
            
        user = authenticate_user(username, password)
        if user:
            self.current_user = user
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def show_dashboard(self):
        self.clear_window()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        logo_label = ctk.CTkLabel(self.sidebar_frame, text="HousingPredict", font=ctk.CTkFont(size=20, weight="bold"))
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        predict_btn = ctk.CTkButton(self.sidebar_frame, text="Predict Price", command=self.show_predict_frame)
        predict_btn.grid(row=1, column=0, padx=20, pady=10)
        
        history_btn = ctk.CTkButton(self.sidebar_frame, text="My History", command=self.show_history_frame)
        history_btn.grid(row=2, column=0, padx=20, pady=10)
        
        logout_btn = ctk.CTkButton(self.sidebar_frame, text="Logout", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.show_login_frame)
        logout_btn.grid(row=5, column=0, padx=20, pady=20)
        
        # Main content area
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.show_predict_frame()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def validate_int(self, P):
        if P == "": return True
        return P.isdigit()

    def validate_float(self, P):
        if P == "" or P == ".": return True
        try:
            float(P)
            return True
        except ValueError:
            return False

    def on_input_change(self, *args):
        if hasattr(self, 'save_btn'):
            self.save_btn.configure(state="disabled")


    def show_predict_frame(self):
        self.clear_main_frame()
        
        title = ctk.CTkLabel(self.main_frame, text="Predict Housing Price", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(20, 30), sticky="w", padx=30)
        
        # Input Form
        labels = ["Bedrooms", "Bathrooms", "Floor Area (sqm)", "Land Size (sqm)", "Subdivision", "Build Year"]
        self.entries = {}
        
        subdivisions = ['Ayala Alabang', 'Forbes Park', 'Dasmarinas Village', 'Bel-Air', 'BF Homes', 'Loyola Grand Villas']
        
        vcmd_int = (self.register(self.validate_int), '%P')
        vcmd_float = (self.register(self.validate_float), '%P')
        
        for i, label_text in enumerate(labels):
            lbl = ctk.CTkLabel(self.main_frame, text=label_text)
            lbl.grid(row=i+1, column=0, padx=(30, 10), pady=10, sticky="e")
            
            if label_text == "Subdivision":
                entry = ctk.CTkOptionMenu(self.main_frame, values=subdivisions, width=200, command=self.on_input_change)
            else:
                is_float = label_text in ["Floor Area (sqm)", "Land Size (sqm)"]
                vcmd = vcmd_float if is_float else vcmd_int
                entry = ctk.CTkEntry(self.main_frame, width=200, validate="key", validatecommand=vcmd)
                entry.bind("<KeyRelease>", self.on_input_change)
            entry.grid(row=i+1, column=1, padx=(0, 30), pady=10, sticky="w")
            self.entries[label_text] = entry
            
        predict_action_btn = ctk.CTkButton(self.main_frame, text="Predict", command=self.perform_prediction, width=200)
        predict_action_btn.grid(row=7, column=0, columnspan=2, pady=30)
        
        self.result_label = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=20, weight="bold"), text_color="green")
        self.result_label.grid(row=8, column=0, columnspan=2, pady=10)
        
        self.save_btn = ctk.CTkButton(self.main_frame, text="Save Prediction", command=self.save_current_prediction, state="disabled")
        self.save_btn.grid(row=9, column=0, columnspan=2, pady=10)

    def perform_prediction(self):
        try:
            features = {
                'bedrooms': int(self.entries["Bedrooms"].get()),
                'bathrooms': int(self.entries["Bathrooms"].get()),
                'floor_area': float(self.entries["Floor Area (sqm)"].get()),
                'land_size': float(self.entries["Land Size (sqm)"].get()),
                'subdivision': self.entries["Subdivision"].get(),
                'build_year': int(self.entries["Build Year"].get())
            }
            
            # Show a small loading state
            self.result_label.configure(text="Predicting...", text_color="orange")
            self.update()
            
            price = predict_price(features)
            
            self.current_prediction_features = features
            self.current_predicted_price = price
            
            self.result_label.configure(text=f"Estimated Price: ₱ {price:,.2f}", text_color="#2FA572")
            self.save_btn.configure(state="normal")
            
        except ValueError:
            self.save_btn.configure(state="disabled")
            messagebox.showerror("Input Error", "Please ensure all numeric fields are correctly filled.")
        except Exception as e:
            self.save_btn.configure(state="disabled")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_current_prediction(self):
        if not hasattr(self, 'current_predicted_price'):
            return
            
        f = self.current_prediction_features
        success = save_prediction(
            self.current_user['id'],
            f['bedrooms'], f['bathrooms'], f['floor_area'], f['land_size'], f['subdivision'], f['build_year'],
            self.current_predicted_price
        )
        
        if success:
            messagebox.showinfo("Success", "Prediction saved successfully!")
            self.save_btn.configure(state="disabled")
        else:
            messagebox.showerror("Database Error", "Failed to save prediction. Ensure MySQL is running.")

    def show_history_frame(self):
        self.clear_main_frame()
        
        title = ctk.CTkLabel(self.main_frame, text="Prediction History", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, pady=(20, 20), sticky="w", padx=30)
        
        # We use a standard tkinter Treeview for the table as customtkinter doesn't have a table widget yet
        columns = ("id", "date", "subdivision", "area", "price")
        
        tree_frame = ctk.CTkFrame(self.main_frame)
        tree_frame.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("subdivision", text="Subdivision")
        self.tree.heading("area", text="Floor Area")
        self.tree.heading("price", text="Predicted Price")
        
        self.tree.column("id", width=50)
        self.tree.column("date", width=150)
        self.tree.column("subdivision", width=150)
        self.tree.column("area", width=100)
        self.tree.column("price", width=150)
        
        self.tree.pack(fill="both", expand=True)
        
        self.load_history()
        
        delete_btn = ctk.CTkButton(self.main_frame, text="Delete Selected", command=self.delete_selected_record, fg_color="#C8504B", hover_color="#8E3533")
        delete_btn.grid(row=2, column=0, pady=20)

    def load_history(self):
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        records = get_user_predictions(self.current_user['id'])
        for r in records:
            # Handle SQLite returning string for created_at
            created_at = r['created_at']
            if hasattr(created_at, 'strftime'):
                created_at_str = created_at.strftime("%Y-%m-%d %H:%M")
            else:
                created_at_str = str(created_at)[:16] # Just get the YYYY-MM-DD HH:MM part
                
            self.tree.insert("", "end", values=(
                r['id'], 
                created_at_str, 
                r['subdivision'], 
                f"{r['floor_area']} sqm", 
                f"₱ {r['predicted_price']:,.2f}"
            ))

    def delete_selected_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return
            
        record_id = self.tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
            if delete_prediction(record_id):
                self.load_history()
            else:
                messagebox.showerror("Error", "Failed to delete record.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
