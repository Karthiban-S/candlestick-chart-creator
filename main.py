from tkinter import *
from tkinter import messagebox
import pandas as pd
import plotly.graph_objects as go

def df_creator():
    file = FilePath_entry.get()
    try:
        df = pd.read_csv(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="File Path or File Name Not Found")

    return df, file


def reformat_csv_date():


    df, file = df_creator()
    # Suppose the column with dates is called 'date'
    # Convert to datetime format
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, format='mixed')
    # Reformat to desired format, e.g. DD-MM-YYYY
    df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')

    # Save back to CSV
    df.to_csv(file, index=False)

    messagebox.showinfo(title="Success", message="Reformated the Date in CSV. Check once again before proceeding")


def create_chart():

    # Load the CSV file
    df, file = df_creator()

    # Drop rows with missing values
    df.dropna(inplace=True)

    df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True)

    # Sort by Date
    # df.sort_values('Date', inplace=True)
    start_year = int(StartYear_entry.get())
    end_year = int(EndYear_entry.get())

    filtered_df = df.query(f'Date > {start_year} and Date < {end_year+1}')
    print(filtered_df)
    print(100 * "-")
    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=filtered_df['Date'],
        open=filtered_df['Open'],
        high=filtered_df['High'],
        low=filtered_df['Low'],
        close=filtered_df['Close']
    )])

    fig.update_layout(
        title="SPX Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )
    fig.show()



THEME_COLOR = "#375362"
BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("Candle Chart Creator")
window.config(padx=40, pady=40)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100,100, image=logo_img)
canvas.grid(row=0, column=1, padx=10, pady=10)

#Labels
FilePath_label = Label(text="File Path:")
FilePath_label.grid(row=1, column=0)
StartYear_label = Label(text="Starting Year:")
StartYear_label.grid(row=2, column=0)
EndYear_label = Label(text="Ending Year")
EndYear_label.grid(row=3, column=0)

#Entries
FilePath_entry = Entry(width=32)
FilePath_entry.grid(row=1, column=1)
FilePath_entry.focus()
StartYear_entry = Entry(width=32)
StartYear_entry.grid(row=2, column=1)
EndYear_entry = Entry(width=32)
EndYear_entry.grid(row=3, column=1)


# Buttons
reformat_button = Button(text="Reformat CSV", command=reformat_csv_date, width=15, bg='BLUE', fg="WHITE")
reformat_button.grid(row=1, column=2)
CreateChart_button = Button(text="Create Chart", width=36, command=create_chart, bg=BACKGROUND_COLOR, fg=THEME_COLOR)
CreateChart_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10)


window.mainloop()