from tkinter import *
import customtkinter as ctk
import selenium_driver
from PIL import Image, ImageTk
import concurrent.futures
import time
import webbrowser
import sprouts

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


def raise_frame(frame_require):
    frame_require.tkraise()


def on_closing():
    selenium_driver.driver.quit()
    selenium_driver.driver2.quit()
    selenium_driver.driver3.quit()
    root.destroy()


def show_loading():
    raise_frame(frame_loading)
    root.update()


def back_button():
    product_name_e.delete(0, END)
    company_name_e.delete(0, END)
    keywords_e.delete(0, END)
    raise_frame(frame_entry)
    root.update()



def get_next_page():
    print("Submit button clicked")
    start = time.time()
    if product_name_e.get():
        frame_product = ctk.CTkFrame(root)
        ctk.CTkButton(frame_product, text="", image=img_back, command=back_button, width=50, height=50,
                      corner_radius=25).place(
            x=20, y=20, anchor=NW)
        frame_product.grid(row=0, column=0, sticky='news')
        show_loading()
        product_name = product_name_e.get()
        company_name = company_name_e.get()
        keywords = keywords_e.get()
        # product_name = "whole wheat bread"
        # company_name = "nature's own"
        # keywords = "whole wheat bread"
        necessary_words = tuple(keywords.split()) + tuple(company_name.split())
        with concurrent.futures.ThreadPoolExecutor() as executor:
            t4 = executor.submit(sprouts.get_from_sprouts, product=company_name + " " + product_name,
                                 keywords=necessary_words)
            t1 = executor.submit(selenium_driver.get_from_amazon, product=company_name + " " + product_name,
                                 keywords=necessary_words)
            t2 = executor.submit(selenium_driver.get_from_target, product=company_name + " " + product_name,
                                 keywords=necessary_words)
            t3 = executor.submit(selenium_driver.get_from_wholefoods, product=company_name + " " + product_name,
                                 brand=tuple(company_name.split()), keywords=tuple(keywords.split()))

            amazon_result = t1.result()
            target_result = t2.result()
            wholefoods_result = t3.result()
            sprouts_result = t4.result()

        lowest_price = ["", 10000000, "", "", '']
        col = 0
        for k, va in amazon_result.items():
            if col == 2:
                break
            frame_result = ctk.CTkFrame(frame_product, cursor="hand2")
            frame_result.bind('<Button-1>', lambda x: webbrowser.open_new(va[1]))

            img_product = Image.open(va[2])
            img_product = img_product.resize((int(((
                                                           root.winfo_height() - 100) / 4 - 50) / img_product.height * img_product.width),
                                              int((root.winfo_height() - 100) / 4 - 50)), Image.ANTIALIAS)
            if col == 0:
                product_image = ImageTk.PhotoImage(img_product)
                root.product_image = product_image
                canvas_result = ctk.CTkCanvas(frame_result, width=img_product.width, height=img_product.height)
                canvas_result.create_image((0, 0), image=product_image, anchor=NW)
            else:
                result_image = ImageTk.PhotoImage(img_product)
                root.result_image = result_image
                canvas_result = ctk.CTkCanvas(frame_result, width=img_product.width, height=img_product.height)
                canvas_result.create_image((0, 0), image=result_image, anchor=NW)
            canvas_result.grid(column=0, row=0, sticky='n', columnspan=2)
            canvas_result.bind('<Button-1>', lambda x: webbrowser.open_new(va[1]))

            price = ctk.CTkLabel(frame_result, text="$" + str(va[0]))
            if len(va) == 4:
                ctk.CTkLabel(frame_result, text=va[3]).grid(row=1, column=1, sticky="ne")
                price.grid(row=1, column=0, sticky="nw")
            else:
                price.grid(row=1, column=0, sticky="n")
            price.bind('<Button-1>', lambda x: webbrowser.open_new(va[1]))
            try:
                name = ctk.CTkLabel(frame_result, text=k[:31] + '\n' + k[31:])
            except ValueError:
                name = ctk.CTkLabel(frame_result, text=k)
            name.grid(row=2, column=0, sticky="n", columnspan=2)
            name.bind('<Button-1>', lambda x: webbrowser.open_new(va[1]))
            frame_result.grid(row=3, column=col, padx=5, pady=5)
            col += 1
            if va[0] < lowest_price[1]:
                lowest_price[0] = k
                lowest_price[1] = va[0]
                lowest_price[2] = va[1]
                lowest_price[3] = "amazon"
                lowest_price[4] = img_product

        amazon_label = ctk.CTkLabel(frame_product, text="Amazon", text_font=("Roboto Medium", -16))
        if col == 0:
            amazon_label.grid(row=2, column=0, columnspan=1)
        else:
            amazon_label.grid(row=2, column=0, columnspan=col)
        if not amazon_result:
            frame_result = ctk.CTkFrame(frame_product)
            ctk.CTkLabel(frame_result, text="Sorry, no item available").grid(row=0, column=0)
            frame_result.grid(row=3, column=0, padx=5, pady=5)

        col_t = 0
        for k, vt in target_result.items():
            if col_t == 2: break
            frame_result = ctk.CTkFrame(frame_product, cursor="hand2")
            frame_result.bind('<Button-1>', lambda x: webbrowser.open_new(vt[1]))

            img_product = Image.open(vt[2])
            img_product = img_product.resize((int(((
                                                           root.winfo_height() - 100) / 4 - 50) / img_product.height * img_product.width),
                                              int((root.winfo_height() - 100) / 4 - 50)), Image.ANTIALIAS)
            if col_t:
                product = ImageTk.PhotoImage(img_product)
                root.product = product
                canvas_result = ctk.CTkCanvas(frame_result, width=img_product.width, height=img_product.height)
                canvas_result.create_image((0, 0), image=product, anchor=NW)
            else:
                tar_product = ImageTk.PhotoImage(img_product)
                root.tar_product = tar_product
                canvas_result = ctk.CTkCanvas(frame_result, width=img_product.width, height=img_product.height)
                canvas_result.create_image((0, 0), image=tar_product, anchor=NW)
            canvas_result.grid(column=0, row=0, sticky='n', columnspan=2)
            canvas_result.bind('<Button-1>', lambda x: webbrowser.open_new(vt[1]))

            price = ctk.CTkLabel(frame_result, text="$" + str(vt[0]))
            price.grid(row=1, column=0, sticky="nw")
            price.bind('<Button-1>', lambda x: webbrowser.open_new(vt[1]))
            if len(vt) == 4:
                ctk.CTkLabel(frame_result, text=vt[3]).grid(row=1, column=1, sticky="ne")
                price.grid(row=1, column=0, sticky="nw")
            else:
                price.grid(row=1, column=0, sticky="n")
            try:
                name = ctk.CTkLabel(frame_result, text=k[:31] + '\n' + k[31:])
            except ValueError:
                name = ctk.CTkLabel(frame_result, text=k)
            name.grid(row=2, column=0, sticky="n", columnspan=2)
            name.bind('<Button-1>', lambda x: webbrowser.open_new(vt[1]))
            frame_result.grid(row=5, column=col_t, padx=5, pady=5)
            col_t += 1
            if vt[0] < lowest_price[1]:
                lowest_price[0] = k
                lowest_price[1] = vt[0]
                lowest_price[2] = vt[1]
                lowest_price[3] = "target"
                lowest_price[4] = img_product
        target_label = ctk.CTkLabel(frame_product, text="Target", text_font=("Roboto Medium", -16))
        if col_t == 0:
            target_label.grid(row=4, column=0, columnspan=1)
        else:
            target_label.grid(row=4, column=0, columnspan=col_t)
        if not target_result:
            frame_result = ctk.CTkFrame(frame_product)
            ctk.CTkLabel(frame_result, text="Sorry, no item available").grid(row=0, column=0)
            frame_result.grid(row=5, column=0, padx=5, pady=5)

        no = 0
        for k, v in wholefoods_result.items():
            if no == 2:
                break
            frame_result = ctk.CTkFrame(frame_product, cursor="hand2")
            frame_result.bind('<Button-1>', lambda x: webbrowser.open_new(v[1]))
            img_product = Image.open(v[2])
            img_product = img_product.resize((int(((
                                                           root.winfo_height() - 100) / 4 - 50) / img_product.height * img_product.width),
                                              int((root.winfo_height() - 100) / 4 - 50)), Image.ANTIALIAS)
            if no == 0:
                product_img = ImageTk.PhotoImage(img_product)
                root.product_img = product_img
                canvas_result = ctk.CTkCanvas(frame_result, width=img_product.width, height=img_product.height)
                canvas_result.create_image((0, 0), image=product_img, anchor=NW)
            else:
                whole_img = ImageTk.PhotoImage(img_product)
                root.whole_img = whole_img
                canvas_result = ctk.CTkCanvas(frame_result, width=img_product.width, height=img_product.height)
                canvas_result.create_image((0, 0), image=whole_img, anchor=NW)
            no += 1
            canvas_result.grid(column=0, row=0, sticky='n')
            canvas_result.bind('<Button-1>', lambda x: webbrowser.open_new(v[1]))

            price = ctk.CTkLabel(frame_result, text=v[0])
            price.grid(row=1, column=0, sticky="n")
            price.bind('<Button-1>', lambda x: webbrowser.open_new(v[1]))
            try:
                name = ctk.CTkLabel(frame_result, text=k[:31] + '\n' + k[31:])
            except ValueError:
                name = ctk.CTkLabel(frame_result, text=k)
            name.grid(row=2, column=0, sticky="n")
            name.bind('<Button-1>', lambda x: webbrowser.open_new(v[1]))

            if col >= 2:
                frame_result.grid(row=3, column=col, padx=(40, 5), pady=5)
            else:
                frame_result.grid(row=3, column=col, padx=(300, 5), pady=5)

            col += 1
            if float(v[0].replace("$", "").replace("/lb", "").replace("¢", "")) < lowest_price[1]:
                lowest_price[0] = k
                lowest_price[1] = float(v[0].replace("$", "").replace("/lb", "").replace("¢", ""))
                lowest_price[2] = v[1]
                lowest_price[3] = "whole foods"
                lowest_price[4] = img_product

        wholefoods_label = ctk.CTkLabel(frame_product, text="Whole Foods Market", text_font=("Roboto Medium", -16))
        if len(amazon_result) >= 2:
            wholefoods_label.grid(row=2, column=2, padx=(40, 5))
        else:
            wholefoods_label.grid(row=2, column=1, padx=(300, 5))
        if not wholefoods_result:
            frame_result = ctk.CTkFrame(frame_product)
            ctk.CTkLabel(frame_result, text="Sorry, no item available", text_font=("Roboto Medium", -16)).grid(row=0, column=0)
            if col >= 2:
                frame_result.grid(row=3, column=col, padx=(40, 5), pady=5)
            else:
                frame_result.grid(row=3, column=col, padx=(300, 5), pady=5)

        for k, vs in sprouts_result.items():
            frame_result = ctk.CTkFrame(frame_product, cursor="hand2")
            frame_result.bind('<Button-1>', lambda x: webbrowser.open_new(vs[1]))
            img_product = Image.open(vs[2])
            img_product = img_product.resize((int(((
                                                           root.winfo_height() - 100) / 4 - 50) / img_product.height * img_product.width),
                                              int((root.winfo_height() - 100) / 4 - 50)), Image.ANTIALIAS)
            sprouts_img = ImageTk.PhotoImage(img_product)
            root.sprouts_img = sprouts_img
            canvas_result = ctk.CTkCanvas(frame_result, width=img_product.width, height=img_product.height)
            canvas_result.create_image((0, 0), image=sprouts_img, anchor=NW)
            canvas_result.grid(column=0, row=0, sticky='n')
            canvas_result.bind('<Button-1>', lambda x: webbrowser.open_new(vs[1]))

            price = ctk.CTkLabel(frame_result, text="$" + str(vs[0]))
            price.grid(row=0, column=0, sticky="n")
            price.bind('<Button-1>', lambda x: webbrowser.open_new(vs[1]))
            try:
                name = ctk.CTkLabel(frame_result, text=k[:31]+'\n'+k[31:])
            except ValueError:
                name = ctk.CTkLabel(frame_result, text=k)
            name.grid(row=1, column=0, sticky="n")
            name.bind('<Button-1>', lambda x: webbrowser.open_new(vs[1]))

            if col_t >= 2:
                frame_result.grid(row=5, column=col_t, padx=(40, 5), pady=5)
            elif col - no >= 2:
                frame_result.grid(row=5, column=col - no, padx=(40, 5), pady=5)
            else:
                frame_result.grid(row=5, column=col_t, padx=(300, 5), pady=5)
            col_t += 1
            if vs[0] < lowest_price[1]:
                lowest_price[0] = k
                lowest_price[1] = vs[0]
                lowest_price[2] = vs[1]
                lowest_price[3] = "sprouts"
                lowest_price[4] = img_product
        sprouts_label = ctk.CTkLabel(frame_product, text="Sprouts", text_font=("Roboto Medium", -16))
        if col_t >= 2:
            sprouts_label.grid(row=4, column=col_t, padx=(40, 5), pady=5)
        elif col - no >= 2:
            sprouts_label.grid(row=4, column=col - no, padx=(40, 5), pady=5)
        else:
            sprouts_label.grid(row=4, column=col_t, padx=(300, 5), pady=5)
        if not sprouts_result:
            frame_result = ctk.CTkFrame(frame_product)
            ctk.CTkLabel(frame_result, text="Sorry, no item available", text_font=("Roboto Medium", -16)).grid(row=0,
                                                                                                               column=0)
            if col_t >= 2:
                frame_result.grid(row=5, column=col_t, padx=(40, 5), pady=5)
            elif col - no >= 2:
                frame_result.grid(row=5, column=col - no, padx=(300, 5), pady=5)
            else:
                frame_result.grid(row=5, column=col_t, padx=(300, 5), pady=5)

        def lowest_price_frame(lowest_price):
            ctk.CTkLabel(frame_product, text=f"Lowest price - {lowest_price[3].title()}",
                         text_font=("Roboto Medium", -16)).grid(row=0, column=0, columnspan=4)
            frame_low_price = ctk.CTkFrame(frame_product, cursor="hand2")
            frame_low_price.bind('<Button-1>', lambda x: webbrowser.open_new(lowest_price[2]))
            low_img = ImageTk.PhotoImage(lowest_price[4])
            root.low_img = low_img
            canvas_result = ctk.CTkCanvas(frame_low_price, width=lowest_price[4].width, height=lowest_price[4].height)
            canvas_result.create_image((0, 0), image=low_img, anchor=NW)
            canvas_result.update()
            canvas_result.grid(column=0, row=0, sticky='n')
            canvas_result.bind('<Button-1>', lambda x: webbrowser.open_new(lowest_price[2]))

            ctk.CTkButton(frame_low_price, text="", image=img_cross, command=calculate, width=50
                          , height=50, corner_radius=25).place(relx=0.94, rely=0.1, anchor=NE)
            price = ctk.CTkLabel(frame_low_price, text="$" + str(lowest_price[1]))
            price.grid(row=1, column=0, sticky="n")
            price.bind('<Button-1>', lambda x: webbrowser.open_new(lowest_price[2]))
            title = ctk.CTkLabel(frame_low_price, text=lowest_price[0])
            title.grid(row=2, column=0, sticky="n")
            title.bind('<Button-1>', lambda x: webbrowser.open_new(lowest_price[2]))
            frame_low_price.grid(row=1, column=0, pady=5, columnspan=4)
            frame_product.update()
            return frame_low_price

        crossed_list = []

        def calculate():
            crossed_list.append(lowest_price[0])
            lowest_price2 = ["", 10000000, "", "", '']
            num = 0
            for key, value in amazon_result.items():
                if num == 2: break
                num += 1
                img_product2 = Image.open(value[2])
                img_product2 = img_product2.resize((int(((
                                                               root.winfo_height() - 100) / 4 - 50) / img_product2.height * img_product2.width),
                                                  int((root.winfo_height() - 100) / 4 - 50)), Image.ANTIALIAS)
                if value[0] < lowest_price2[1] and key not in crossed_list:
                    lowest_price2[0] = key
                    lowest_price2[1] = value[0]
                    lowest_price2[2] = value[1]
                    lowest_price2[3] = "amazon"
                    lowest_price2[4] = img_product2
            num = 0
            for key, value in target_result.items():
                if num == 2: break
                num += 1
                img_product2 = Image.open(value[2])
                img_product2 = img_product2.resize((int(((
                                                                 root.winfo_height() - 100) / 4 - 50) / img_product2.height * img_product2.width),
                                                    int((root.winfo_height() - 100) / 4 - 50)), Image.ANTIALIAS)
                if value[0] < lowest_price2[1] and key not in crossed_list:
                    lowest_price2[0] = key
                    lowest_price2[1] = value[0]
                    lowest_price2[2] = value[1]
                    lowest_price2[3] = "target"
                    lowest_price2[4] = img_product2
            num = 0
            for key, value in wholefoods_result.items():
                if num == 2: break
                num += 1
                img_product2 = Image.open(value[2])
                img_product2 = img_product2.resize((int(((
                                                                 root.winfo_height() - 100) / 4 - 50) / img_product2.height * img_product2.width),
                                                    int((root.winfo_height() - 100) / 4 - 50)), Image.ANTIALIAS)
                if float(v[0].replace("$", "").replace("/lb", "").replace("¢", "")) < lowest_price2[1] and key not in crossed_list:
                    lowest_price2[0] = key
                    lowest_price2[1] = float(v[0].replace("$", "").replace("/lb", "").replace("¢", ""))
                    lowest_price2[2] = value[1]
                    lowest_price2[3] = "whole foods"
                    lowest_price2[4] = img_product2

            for key, value in sprouts_result.items():
                if num == 2: break
                num += 1
                img_product2 = Image.open(value[2])
                img_product2 = img_product2.resize((int(((
                                                                 root.winfo_height() - 100) / 4 - 50) / img_product2.height * img_product2.width),
                                                    int((root.winfo_height() - 100) / 4 - 50)), Image.ANTIALIAS)
                if value[0] < lowest_price2[1] and key not in crossed_list:
                    lowest_price2[0] = key
                    lowest_price2[1] = value[0]
                    lowest_price2[2] = value[1]
                    lowest_price2[3] = "sprouts"
                    lowest_price2[4] = img_product2
            low_price_frame.destroy()
            lowest_price_frame(lowest_price2)

        low_price_frame = lowest_price_frame(lowest_price)

        raise_frame(frame_product)
        root.update_idletasks()
        print(time.time() - start)
        print("amazon:", amazon_result)
        print("target:", target_result)
        print("wholefoods:", wholefoods_result)
        # print("sprouts:", sprouts_result)


root = ctk.CTk()
root.title("Price Comparison extension")
root.state("zoomed")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
frame_entry = ctk.CTkFrame(root)
frame_loading = ctk.CTkFrame(root)
canvas_loading = ctk.CTkCanvas(frame_loading, height=root.winfo_height(), width=root.winfo_width())
canvas_loading.place(x=0, y=0)
loading_image = ImageTk.PhotoImage(Image.open(r"loading_image.jpg"))
canvas_loading.create_image(0, 0, image=loading_image, anchor=NW)

canvas = ctk.CTkCanvas(frame_entry, height=400, width=root.winfo_width())
canvas.pack(side="top")
img = ImageTk.PhotoImage(Image.open(r"download.jpg"))
text = ImageTk.PhotoImage(Image.open(r"C:\Users\roopa\Downloads\image (1).png").resize((1200, 270)), Image.ANTIALIAS)
canvas.create_image(0, 0, anchor=NW, image=img)
canvas.create_image(1920 / 2, 200, anchor=CENTER, image=text)
img_back = ImageTk.PhotoImage(Image.open(r"back_button-removebg-preview.png").resize((50, 50)), Image.ANTIALIAS)
root.img_back = img_back
img_cross = ImageTk.PhotoImage(Image.open(r"cross_button-removebg-preview.png").resize((50, 50)), Image.ANTIALIAS)
root.img_cross = img_cross
for frame in (frame_entry, frame_loading):
    frame.grid(row=0, column=0, sticky='news')

# ctk.CTkLabel(frame_entry, text='Price Comparison tool', text_font=("Roboto Medium", 64)).place(relx=0.5, rely=0.25,
#                                                                     anchor="center")
ctk.CTkLabel(frame_entry, text='What is the product\'s name', text_font=("Roboto Medium", -16)).place(relx=0.35,
                                                                                                      rely=0.5,
                                                                                                      anchor="s")
product_name_e = ctk.CTkEntry(frame_entry, width=300, corner_radius=6, text_font=("Roboto Medium", -16))
product_name_e.place(relx=0.52, rely=0.5, anchor="sw")

ctk.CTkLabel(frame_entry, text='Enter the name of the company', text_font=("Roboto Medium", -16)).place(relx=0.35,
                                                                                                        rely=0.6,
                                                                                                        anchor="center")
company_name_e = ctk.CTkEntry(frame_entry, width=300, corner_radius=6, text_font=("Roboto Medium", -16))
company_name_e.place(relx=0.52, rely=0.6, anchor="w")

ctk.CTkLabel(frame_entry, text='Enter the words that are required in the product title\n They should be less specific',
             text_font=("Roboto Medium", -16)).place(relx=0.35, rely=0.7, anchor="n")
keywords_e = ctk.CTkEntry(frame_entry, width=300, corner_radius=6, text_font=("Roboto Medium", -16))
keywords_e.place(relx=0.52, rely=0.7, anchor="nw")

submit_button = ctk.CTkButton(frame_entry, text="Submit", corner_radius=6, text_font=("Roboto Medium", -16),
                              command=get_next_page)
submit_button.place(relx=0.52, rely=0.83, anchor="center")
raise_frame(frame_entry)
# root.protocol("W,M_DELETE_WINDOW", on_closing)
root.mainloop()
