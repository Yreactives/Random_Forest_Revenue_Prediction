from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import os
from datetime import datetime, timedelta
from meteostat import Point, Hourly, Daily
from functions import hash_file, is_same_file



def create_treeView():
    if not is_same_file(a.get(), previous_file_hash)[0]:
        submit()
    frame3 = tk.Frame(root)
    frame3.pack(fill=tk.BOTH, expand=1)

    tree = ttk.Treeview(frame3)

    tree["columns"] = list(summary.columns)
    tree["show"] = "headings"
    for col in summary.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

        # Add data to the Treeview
    for index, row in summary.iterrows():
        tree.insert("", "end", values=list(row))

        # Pack the Treeview widget
    tree.pack(fill=tk.BOTH, expand=1)
    buttonBack = tk.Button(frame3, text="Back", height=2, width=20 ,command=lambda: show_frame(frames['frame2']))
    buttonBack.pack(padx=10, pady=10)

    frames['frame3'] = frame3
def submit():
    global df
    global previous_file_hash
    global rf_regressor
    global summary
    global cuisine_list
    path = a.get()
    cuisine_list = ["Mie Kari Ayam Komplit",
                    "Mie Kari Sapi Komplit",
                    "Mie Kari Kari Polos",
                    "Mie Kari Tahu Telur",
                    "Mie Goreng Kari",
                    "Nasi Kari"]
    current_file_hash = hash_file(path)
    previous_file_hash = current_file_hash

    # weather start
    tomorrow = datetime.now() + timedelta(1)

    year = tomorrow.year

    month = tomorrow.month
    day = tomorrow.day


    start = datetime(year, month, day)
    end = datetime(year, month, day, 23, 59, 59)

    senimanmiekari = Point(-0.030952207938211476, 109.33624505209471, 70)

    data = Hourly(senimanmiekari, start, end)
    data = data.fetch()

    avg_temp = data['temp'].mean()
    max_temp = data['temp'].max()
    min_temp = data['temp'].min()
    prcp = data['prcp'].sum()

    summary = pd.DataFrame({
        'tavg': [avg_temp],
        'tmin': [min_temp],
        'tmax': [max_temp],
        'prcp': [prcp]
    })



    # weather end

    #train start
    pred_list = []
    for i in range(6):
        df = pd.read_excel(path, sheet_name=i)
        timestamps = pd.to_datetime(df['date'])
        today = datetime.now() - timedelta(1)
        start = datetime(timestamps[0].year, timestamps[0].month, timestamps[0].day)
        end = datetime(2024, 1, 1) + timedelta(len(df)-1)
        weather_data = Daily(senimanmiekari, start, end)
        weather_data = weather_data.fetch()
        weather_data = weather_data.iloc[:, 0:4]

        #X = df.drop("pendapatan", axis=1)
        #X = X.drop("date", axis=1)
        X = weather_data
        y = df["pendapatan"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, shuffle=True)

        rf_regressor = RandomForestRegressor(n_estimators=500, random_state=42)

        rf_regressor.fit(X_train, y_train)
        #train end

        y_pred = rf_regressor.predict(summary)
        pred_list.insert(len(pred_list), y_pred[0])

    tomorrow = datetime.now() + timedelta(1)

    summary = pd.DataFrame({
        'Date (dd-mm-yyyy)': [str(tomorrow.day) + " - "  + str(tomorrow.month) + " - " + str(tomorrow.year) for x in range(6)],

        'Cuisine': cuisine_list,

        'Prediction (Rp.)': pred_list
    })

    create_treeView()

    show_frame(frames['frame2'])

def browse():
    f_path = askopenfilename(initialdir="/",
    title="Select File", filetypes=(("Excel Files","*.xlsx*"),("All Files","*.*")))
    #entryFile.configure(text="File Opened: "+f_path)
    if f_path:
        a.set(f_path)
        with open("data.pkl", 'wb') as file:
            pickle.dump(f_path, file)

def show_frame(frame):
    frame.tkraise()

def show_line():
    for i in range(6):
        df = pd.read_excel(a.get(), sheet_name=i)
        plt.figure(num=i, figsize=(14, 6))
        plt.plot(df['date'], df['pendapatan'])
        plt.autoscale(True)

        plt.title(cuisine_list[i])
        plt.xlabel("Date")
        plt.ylabel("Value")
    plt.show()

def show_bar():
    for i in range(6):
        df = pd.read_excel(a.get(), sheet_name=i)
        plt.figure(num=i, figsize=(14, 6), dpi=100)

        plt.bar(df['date'], df['pendapatan'])

        plt.title(cuisine_list[i])
        plt.xlabel("Date")
        plt.ylabel("Value")
    plt.show()
def create_frame():
    frame1 = tk.Frame(root)
    frame1.place(relwidth=1, relheight=1)
    labelFile = tk.Label(frame1, text="File Name")
    labelFile.pack(padx=20, pady=20)
    entryFile = (tk.Entry(frame1, textvariable=a, width=300))
    entryFile.pack(padx=20, pady=20)
    buttonBrowse = tk.Button(frame1, text="Browse", command=browse)
    buttonBrowse.pack(padx=20, pady=20)
    buttonFile = tk.Button(frame1, text="Submit", command=submit)
    buttonFile.pack(padx=20, pady=20)

    frame2 = tk.Frame(root)
    frame2.place(relwidth=1, relheight=1)
    buttonLine = tk.Button(frame2, text="Show Line Chart", command=show_line, height=2)
    buttonLine.grid(row=0, column=0, padx=10, pady=10)
    buttonBar = tk.Button(frame2, text="Show Bar Chart", command=show_bar, height=2)
    buttonBar.grid(row=0, column=1, padx=10, pady=10)
    buttonPred = tk.Button(frame2, text="Show Prediction", command= lambda: show_frame(frames['frame3']),height = 2)
    buttonPred.grid(row=0, column=2, padx=10, pady = 10)
    buttonHome = tk.Button(frame2, text="Back", command=lambda: show_frame(frames['frame1']), height=2, width=20)
    buttonHome.grid(row = 1,  column=2, padx=10, pady=50)



    frames['frame1'] = frame1
    frames['frame2'] = frame2


root = tk.Tk()
root.geometry("400x400")
root.title("Revenue Predictor")
root.resizable(0, 0)
frames = {}

a = tk.StringVar()
a.set("dataset.xlsx")
if os.path.exists("data.pkl"):
    with open("data.pkl", 'rb') as file:

        pth = pickle.load(file)
        a.set(pth)

previous_file_hash = None

create_frame()
show_frame(frames['frame1'])
root.mainloop()

