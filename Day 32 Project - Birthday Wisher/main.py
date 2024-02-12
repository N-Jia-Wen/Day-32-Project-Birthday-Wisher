##################### Extra Hard Starting Project ######################
import tkinter
from tkinter import messagebox
import pandas
import datetime as dt
import smtplib
import random
# 1. Update the birthdays.csv

PLACEHOLDER_NAME = "[NAME]"
my_email = "example123@gmail.com"
my_password = "placeholder password"
current_time = dt.datetime.now()


def save_birthday():
    ok_to_save = messagebox.askokcancel(title="Are you sure?", message=f"You are about to save the following details:\n"
                                                          f"Name: {name_entry.get()}\n"
                                                          f"Email: {email_entry.get()}\n"
                                                          f"Birthday: {day_spinbox.get()}/"
                                                          f"{month_spinbox.get()}/"
                                                          f"{year_spinbox.get()}\n")
    if ok_to_save is True:

        new_birthday_dict = {
            "name": [name_entry.get()],
            "email": [email_entry.get()],
            "year": [year_spinbox.get()],
            "month": [month_spinbox.get()],
            "day": [day_spinbox.get()]
        }
        new_birthday_dataframe = pandas.DataFrame(new_birthday_dict)
        try:
            # Simply checks if birthdays.csv exists:
            with open("birthdays.csv", mode="r") as _:
                pass
        except FileNotFoundError:
            new_birthday_dataframe.to_csv("birthdays.csv", mode="a", index=False, header=True,
                                      index_label=["name", "email", "year", "month", "day"])
        else:
            new_birthday_dataframe.to_csv("birthdays.csv", mode="a", index=False, header=False)
        # This section is to prevent additional headers from being added after the csv file is created.

        finally:
            tkinter_widgets = [name_entry, email_entry, year_spinbox, month_spinbox, day_spinbox]
            for widget in tkinter_widgets:
                widget.delete(0, tkinter.END)

            year_spinbox.insert(s="1960", index=tkinter.END)
            month_spinbox.insert(s="1", index=tkinter.END)
            day_spinbox.insert(s="1", index=tkinter.END)


window = tkinter.Tk()
window.title("Birthday Logger")
window.config(padx=20, pady=20, bg="white")

canvas = tkinter.Canvas(width=500, height=400, bg="white", highlightthickness=0)
cake_img = tkinter.PhotoImage(file="pink_birthday_cake.png")
canvas.create_image(250, 200, image=cake_img)
canvas.grid(row=0, column=0, columnspan=3)

title_label = tkinter.Label(text="Birthday Wisher!", font=("Courier", 30, "normal"), bg="white")
title_label.place(x=60, y=0)

info_label = tkinter.Label(text="Enter the details of the person whose birthday you want to save:",
                           font=("Ariel", 12, "normal"), bg="white")
info_label.place(x=0, y=370)

name_label = tkinter.Label(text="Name:", font=("Ariel", 16, "normal"), bg="white")
name_label.grid(row=1, column=0)
name_entry = tkinter.Entry(width=60)
name_entry.grid(row=1, column=1, columnspan=2)

email_label = tkinter.Label(text="Email:", font=("Ariel", 16, "normal"), bg="white")
email_label.grid(row=2, column=0)
email_entry = tkinter.Entry(width=60)
email_entry.grid(row=2, column=1, columnspan=2)

year_label = tkinter.Label(text="Year:", font=("Ariel", 16, "normal"), bg="white")
year_label.grid(row=3, column=0)
year_spinbox = tkinter.Spinbox(from_=1960, to=current_time.year)
year_spinbox.grid(row=4, column=0)

month_label = tkinter.Label(text="Month:", font=("Ariel", 16, "normal"), bg="white")
month_label.grid(row=3, column=1)
month_spinbox = tkinter.Spinbox(from_=1, to=12)
month_spinbox.grid(row=4, column=1)

day_label = tkinter.Label(text="Day:", font=("Ariel", 16, "normal"), bg="white")
day_label.grid(row=3, column=2)
day_spinbox = tkinter.Spinbox(from_=1, to=31)
day_spinbox.grid(row=4, column=2)

confirm_button = tkinter.Button(text="Confirm", command=save_birthday, font=("Ariel", 16, "normal"))
confirm_button.grid(row=5, column=0, columnspan=2)


# 2. Check if today matches a birthday in the birthdays.csv
def check_birthday():
    try:
        birthdays = pandas.read_csv("birthdays.csv")
    except FileNotFoundError:
        messagebox.showinfo(title="No Birthdays Found", message="You have not saved anyone's birthdays yet.")
    else:
        birthday_list = birthdays.to_dict(orient="records")
        for details in birthday_list:

            if details.get("month") == current_time.month and details.get("day") == current_time.day:

                # 3. If step 2 is true, pick a random letter from letter templates
                # and replace the [NAME] with the person's actual name from birthdays.csv

                with open(file=f"./letter_templates/letter_{random.randint(1, 3)}.txt") as chosen_letter:
                    name = details.get("name").title()
                    letter_contents = chosen_letter.read()
                    personalised_letter = letter_contents.replace(PLACEHOLDER_NAME, name)

                    # 4. Send the letter generated in step 3 to that person's email address.
                    with smtplib.SMTP("smtp.gmail.com") as connection:
                        connection.starttls()
                        connection.login(user=my_email, password= my_password)
                        try:
                            connection.sendmail(from_addr=my_email, to_addrs=details.get("email"),
                                                msg=f"Subject:Happy Birthday!\n\n{personalised_letter}")

                        # The former error is when password of sender's email account is incorrect,
                        # The latter error is when recipient's email address is invalid.
                        except smtplib.SMTPAuthenticationError:
                            messagebox.showinfo(title="Invalid Credentials",
                                                message="Sorry, the email(s) could not be sent."
                                                        "Maybe check your login credentials?")
                        except smtplib.SMTPRecipientsRefused:
                            messagebox.showinfo(title="Invalid Address",
                                                message=f"Sorry, we could not send the email to {name} "
                                                        f"as they have an invalid email address saved.")

                        else:
                            messagebox.showinfo(title="Email sent!", message=f"Your email has been sent to {name}!")


check_button = tkinter.Button(text="Wish Birthday", command=check_birthday, font=("Ariel", 16, "normal"))
check_button.place(x=250, y=500)

window.mainloop()
