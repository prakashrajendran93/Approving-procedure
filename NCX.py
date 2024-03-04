import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="prakash")


window = tk.Tk()
window.title("NCX")

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import uuid

smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'prakash.itec@gmail.com'
sender_password = 'luvlssfedrsjnrdo'
receiver_email = 'prakash.itec@gmail.com'

def Request():
    name = name_entry.get()
    department = department_entry.get()
    buyerpo = buyerpo_entry.get()
    mistake = mistake_entry.get()
    value = value_entry.get()

    if name != '' and department != '' and buyerpo != '' and mistake != '' and value != '':
        if name.isalpha() and department.isalpha() and value.isnumeric():
            #cursor = con.cursor()
            sql = "INSERT INTO data (name, department, buyerpo, mistake, value, status) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (name, department, buyerpo, mistake, value, 'Pending')
            cursor.execute(sql, values)
            con.commit()
            #cursor.close()
            messagebox.showinfo('Request', 'Request Raised Successfully')
            send_approval_email(name, department, buyerpo, mistake, value)
            print('Name:', name)
            print('Department:', department)
            print('Buyer PO:', buyerpo)
            print('Mistake:', mistake)
            print('Value:', value)
            name_entry.delete(0, 'end')
            department_entry.delete(0, 'end')
            buyerpo_entry.delete(0, 'end')
            mistake_entry.delete(0, 'end')
            value_entry.delete(0, 'end')
            name_entry.focus()
        else:
            messagebox.showerror('Value', 'Value should be in number only')
    else:
        messagebox.showerror('Data Missing', 'Some fields are empty')

def send_approval_email(name, department, buyerpo, mistake, value):
    subject = "Approval Needed for NCX Request"
    body = f"Name: {name}\nDepartment: {department}\nBuyer PO: {buyerpo}\nMistake: {mistake}\nValue: {value}\n\nPlease approve this request by clicking the following link: [Approval Link]"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
        smtp_connection.starttls()
        smtp_connection.login(sender_email, sender_password)
        smtp_connection.sendmail(sender_email, receiver_email, msg.as_string())
        smtp_connection.quit()
        print("Email notification sent.")
    except Exception as e:
        print(f"Failed to send email notification: {e}")

def approve():
    request_id = int(request_id_entry.get())
    sql = "UPDATE data SET status = %s WHERE id = %s"
    values = ("Approved", request_id)
    cursor.execute(sql, values)
    con.commit()
    messagebox.showinfo("approve", "Approved Successfully")
    print('Approved')
    request_id_entry.delete(0, 'end')

def reject():
    request_id = int(request_id_entry.get())
    sql = 'UPDATE data SET Status = %s WHERE id = %s'
    values = ('Rejected', request_id)
    cursor.execute(sql, values)
    con.commit()
    print('Rejected')
    request_id_entry.delete(0, 'end')

NCX_frame = ttk.LabelFrame(window, text="Request for NCX")
NCX_frame.pack(padx=10, pady=10)

name_label = ttk.Label(NCX_frame, text="Name:")
name_label.grid(row=1, column=0, padx=5, pady=5)
name_entry = ttk.Entry(NCX_frame)
name_entry.grid(row=1, column=1, padx=5, pady=5)

department_label = ttk.Label(NCX_frame, text="Department:")
department_label.grid(row=2, column=0, padx=5, pady=5)
department_entry = ttk.Entry(NCX_frame)
department_entry.grid(row=2, column=1, padx=5, pady=5)

buyerpo_label = ttk.Label(NCX_frame, text="Buyer PO:")
buyerpo_label.grid(row=3, column=0, padx=5, pady=5)
buyerpo_entry = ttk.Entry(NCX_frame)
buyerpo_entry.grid(row=3, column=1, padx=5, pady=5)

mistake_label = ttk.Label(NCX_frame, text="Type of Mistake:")
mistake_label.grid(row=4, column=0, padx=5, pady=5)
mistake_entry = ttk.Entry(NCX_frame)
mistake_entry.grid(row=4, column=1, padx=5, pady=5)

value_label = ttk.Label(NCX_frame, text="NCX Value:")
value_label.grid(row=5, column=0, padx=5, pady=5)
value_entry = ttk.Entry(NCX_frame)
value_entry.grid(row=5, column=1, padx=5, pady=5)



request_button = ttk.Button(NCX_frame, text="Request for Approve", command=Request)
request_button.grid(row=6, columnspan=2, padx=5, pady=5)

# Create the Approval/Rejection section
approval_frame = ttk.LabelFrame(window, text="Approval/Rejection")
approval_frame.pack(padx=10, pady=10)

request_id_label = ttk.Label(approval_frame, text="Request ID:")
request_id_label.grid(row=0, column=0, padx=5, pady=5)
request_id_entry = ttk.Entry(approval_frame)
request_id_entry.grid(row=0, column=1, padx=5, pady=5)

approve_button = ttk.Button(approval_frame, text="Approve", command=approve)
approve_button.grid(row=1, column=0, padx=5, pady=5)

reject_button = ttk.Button(approval_frame, text="Reject", command=reject)
reject_button.grid(row=1, column=1, padx=5, pady=5,)


cursor = con.cursor()

window.mainloop()
cursor.close()
con.close()

