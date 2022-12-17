from tkinter import *
import selenium_driver
from PIL import Image, ImageTk
import concurrent.futures


def raise_frame(frame_require):
    frame_require.tkraise()


def get_next_page():
    raise_frame(frame_product)
    submit_button["state"] = "disabled"
    if product_name_e.get():
        product_name = product_name_e.get()
        company_name = company_name_e.get()
        necessary_words = keywords_e.get()
        necessary_words = tuple(necessary_words.split()) + tuple(company_name.split())

        with concurrent.futures.ThreadPoolExecutor() as executor:
            t1 = executor.submit(selenium_driver.get_from_amazon, product=company_name + " " + product_name,
                                 keywords=necessary_words)
            t2 = executor.submit(selenium_driver.get_from_target, product=company_name + " " + product_name,
                                 keywords=necessary_words)
            t3 = executor.submit(selenium_driver.get_from_costco, product=company_name + " " + product_name,
                                 keywords=necessary_words)
            t4 = executor.submit(selenium_driver.get_from_sprouts, product=company_name + " " + product_name,
                                 keywords=necessary_words)
            amazon_result = t1.result()
            target_result = t2.result()
            costco_result = t3.result()
            sprouts_result = t4.result()

        print("amazon:", amazon_result)
        print("target:", target_result)
        print("costco:", costco_result)
        print("sprouts:", sprouts_result)

        selenium_driver.driver.quit()
        selenium_driver.driver2.quit()
        selenium_driver.driver3.quit()
        selenium_driver.driver4.quit()


root = Tk()
root.title("Price Comparison extension")
root.state("zoomed")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
frame_product = Frame(root)
frame_entry = Frame(root)
canvas = Canvas(frame_entry, height=400, width=root.winfo_width())
canvas.pack(side="top")
img = ImageTk.PhotoImage(Image.open(r"download.jpg"))
text = ImageTk.PhotoImage(Image.open(r"C:\Users\roopa\Downloads\image (1).png").resize((1200, 270)))
canvas.create_image(0, 0, anchor=NW, image=img)
canvas.create_image(1920 / 2, 200, anchor=CENTER, image=text)
# Add image file
Label(frame_product, text="Lowest price", font=("Roboto Medium", -16)).grid(row=0, column=0)
Label(frame_product, text="Amazon", font=("Roboto Medium", -16)).grid(row=2, column=0)
Label(frame_product, text="Target", font=("Roboto Medium", -16)).grid(row=4, column=0)
Label(frame_product, text="Costco", font=("Roboto Medium", -16)).grid(row=6, column=0)
Label(frame_product, text="Sprouts", font=("Roboto Medium", -16)).grid(row=8, column=0)

for frame in (frame_entry, frame_product):
    frame.grid(row=0, column=0, sticky='news')

Label(frame_entry, text='What is the product\'s name', font=("Roboto Medium", -16)).place(relx=0.35,
                                                                                                      rely=0.5,
                                                                                                      anchor="s")
product_name_e = Entry(frame_entry, width=300, font=("Roboto Medium", -16))
product_name_e.place(relx=0.52, rely=0.5, anchor="sw")

Label(frame_entry, text='Enter the name of the company', font=("Roboto Medium", -16)).place(relx=0.35,
                                                                                                        rely=0.6,
                                                                                                        anchor="center")
company_name_e = Entry(frame_entry, width=300, font=("Roboto Medium", -16))
company_name_e.place(relx=0.52, rely=0.6, anchor="w")

Label(frame_entry, text='Enter the words that are required in the product title\n They should be less specific',
             font=("Roboto Medium", -16)).place(relx=0.35, rely=0.7, anchor="n")
keywords_e = Entry(frame_entry, width=300, font=("Roboto Medium", -16))
keywords_e.place(relx=0.52, rely=0.7, anchor="nw")

submit_button = Button(frame_entry, text="Submit", font=("Roboto Medium", -16),
                              command=get_next_page)
submit_button.place(relx=0.52, rely=0.83, anchor="center")
raise_frame(frame_entry)
root.mainloop()
