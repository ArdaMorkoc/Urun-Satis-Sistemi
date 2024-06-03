import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from psycopg2 import Error
import os
import subprocess

# Global değişkenler
user_logged_in = False
logged_in_user_id = None
current_dir = os.path.dirname(os.path.abspath(__file__))
adminpanel_path = os.path.join(current_dir, "adminpanel.py")

# Database bağlantı fonksiyonu
def connect():
    try:
        return psycopg2.connect(
            user="postgres",
            password="12345",
            host="localhost",
            port="5432",
            database="urunsatissistemi"
        )
    except Error as e:
        print(e)

# Veritabanı sorgu yürütme fonksiyonu
def execute_query(query, fetch=False, values=None):
    connection = connect()
    cursor = connection.cursor()
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Sorgu çalıştırılırken hata oluştu:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

# Kullanıcı kayıt ve giriş fonksiyonları
def open_register_window(): # Kayıt penceresini açar ve kullanıcı bilgilerini alır
    register_window = tk.Toplevel(root)
    register_window.title("Kayıt Ol")
    
    label_username = tk.Label(register_window, text="Kullanıcı Adı:")
    label_username.grid(row=0, column=0, padx=5, pady=5)
    entry_username = tk.Entry(register_window)
    entry_username.grid(row=0, column=1, padx=5, pady=5)
    
    label_email = tk.Label(register_window, text="E-posta:")
    label_email.grid(row=1, column=0, padx=5, pady=5)
    entry_email = tk.Entry(register_window)
    entry_email.grid(row=1, column=1, padx=5, pady=5)
    
    label_password = tk.Label(register_window, text="Şifre:")
    label_password.grid(row=2, column=0, padx=5, pady=5)
    entry_password = tk.Entry(register_window, show="*")
    entry_password.grid(row=2, column=1, padx=5, pady=5)
    
    label_telefon = tk.Label(register_window, text="Telefon:")
    label_telefon.grid(row=3, column=0, padx=5, pady=5)
    entry_telefon = tk.Entry(register_window)
    entry_telefon.grid(row=3, column=1, padx=5, pady=5)
    
    button_register = tk.Button(register_window, text="Kayıt Ol", command=lambda: register_user(
        entry_username.get(), entry_email.get(), entry_password.get(), entry_telefon.get()))
    button_register.grid(row=4, column=1, padx=5, pady=5)

def register_user(username, email, password, telefon): # Yeni kullanıcıyı veritabanına kaydeder
    query = "INSERT INTO Musteriler (musteri_adi, email, musteri_sifre, telefon) VALUES (%s, %s, %s, %s)"
    execute_query(query, values=(username, email, password, telefon))
    messagebox.showinfo("Başarılı", "Kullanıcı başarıyla kaydedildi.")

def login(): # Kullanıcı girişini gerçekleştirir
    enable_menus()  # Giriş yapıldığında menüleri etkinleştir
    global user_logged_in, logged_in_user_id
    email = entry_email.get()
    password = entry_password.get()
    query = "SELECT musteri_id FROM Musteriler WHERE email = %s AND musteri_sifre = %s"
    result = execute_query(query, values=(email, password), fetch=True)
    if result:
        user_logged_in = True
        logged_in_user_id = result[0][0]
        messagebox.showinfo("Başarılı", "Giriş başarılı.")
        after_login_actions()
    else:
        messagebox.showerror("Hata", "Geçersiz e-posta veya şifre.")

def after_login_actions(): # Kullanıcı giriş yaptıktan sonra gerçekleştirilecek işlemleri yönetir
    global logged_in_user_id
    main_frame.destroy()
    donermarkt_frame.pack(padx=20, pady=20)

#Admin Paneli fonksiyonları (adminpanel.py dosyasını çalıştırır)
def open_admin_panel(): # Admin Paneli penceresini açıp çalıştıran Fonksiyon
    subprocess.Popen(["python", adminpanel_path])
    root.destroy()

# Ürün arama ve filtreleme işlemleri
def update_search_combobox(): # Arama kutusunu günceller
    query = "SELECT urun_adi FROM Urunler"
    products = execute_query(query, fetch=True)
    if products:
        product_names = [product[0] for product in products]
        search_combobox['values'] = product_names

def search_products(): # Ürünleri arar ve listeler
    keyword = search_combobox.get()
    sort_option = sort_combobox.get()  # Fiyat sıralama seçeneği
    price_range = None
    
    # Fiyat aralığı seçimi
    if price_from_entry.get() and price_to_entry.get():
        min_price = float(price_from_entry.get())
        max_price = float(price_to_entry.get())
        price_range = (min_price, max_price)
    
    # Ürünleri filtrele
    products = filter_products(keyword, sort_option, price_range)
    
    # Mevcut verileri temizle
    for row in tree.get_children():
        tree.delete(row)
    
    # Yeni verileri ekle
    for product in products:
        tree.insert("", "end", values=product)

def filter_products(keyword="", sort_option="default", price_range=None): # Ürünleri filtreler
    base_query = "SELECT urun_adi, birim_fiyat, stok_miktari, satis_sayisi FROM Urunler"
    parameters = []

    # Fiyat aralığı filtresi
    if price_range:
        min_price, max_price = price_range
        base_query += " WHERE birim_fiyat BETWEEN %s AND %s"
        parameters.extend([min_price, max_price])
        if keyword:
            base_query += " AND urun_adi ILIKE %s"
            parameters.append(f"%{keyword}%")
    else:
        if keyword:
            base_query += " WHERE urun_adi ILIKE %s"
            parameters.append(f"%{keyword}%")

    # Sıralama
    if sort_option == "Fiyat - Artan":
        base_query += " ORDER BY birim_fiyat ASC"
    elif sort_option == "Fiyat - Azalan":
        base_query += " ORDER BY birim_fiyat DESC"

    products = execute_query(base_query, fetch=True, values=parameters)
    return products

def purchase_product(product_name, user_id, quantity): # Ürün satın alımını gerçekleştirir
    product_info_query = "SELECT birim_fiyat, stok_miktari, satis_sayisi FROM Urunler WHERE urun_adi = %s"
    product_info = execute_query(product_info_query, fetch=True, values=(product_name,))
    if product_info:
        price, stock_quantity, sales_count = product_info[0]
        if stock_quantity > 0:
            if quantity <= stock_quantity:
                total_price = price * quantity
                if total_price > 0:
                    update_query = "UPDATE Urunler SET stok_miktari = stok_miktari - %s, satis_sayisi = satis_sayisi + %s WHERE urun_adi = %s"
                    execute_query(update_query, values=(quantity, quantity, product_name))
                    purchase_query = "INSERT INTO Satislar (urun_id, miktar, musteri_id, tarih) VALUES ((SELECT urun_id FROM Urunler WHERE urun_adi = %s), %s, %s, CURRENT_DATE)"
                    execute_query(purchase_query, values=(product_name, quantity, user_id))
                    messagebox.showinfo("Başarılı", f"{quantity} adet {product_name} satın alındı. Toplam tutar: {total_price} TL")
                else:
                    messagebox.showerror("Hata", "Toplam tutar sıfır veya negatif olamaz.")
            else:
                messagebox.showerror("Hata", "Yeterli stok bulunmamaktadır.")
        else:
            messagebox.showerror("Hata", f"{product_name} şu anda stokta bulunmamaktadır. Lütfen daha sonra tekrar deneyin.")
    else:
        messagebox.showerror("Hata", "Ürün bilgileri alınamadı.")

# Kullanıcı bilgilerini güncelleme işlemleri
def update_user_info(username, email, password, telefon): # Kullanıcı bilgilerini günceller
    global logged_in_user_id
    # Mevcut kullanıcı bilgilerini al
    current_info_query = "SELECT musteri_adi, email, musteri_sifre, telefon FROM Musteriler WHERE musteri_id = %s"
    current_info = execute_query(current_info_query, values=(logged_in_user_id,), fetch=True)
    if current_info:
        current_username, current_email, current_password, current_telefon = current_info[0]

        # Güncelleme değerlerini mevcut bilgilerle güncelle
        if not username:
            username = current_username
        if not email:
            email = current_email
        if not password:
            password = current_password
        if not telefon:
            telefon = current_telefon

        query = "UPDATE Musteriler SET musteri_adi = %s, email = %s, musteri_sifre = %s, telefon = %s WHERE musteri_id = %s"
        execute_query(query, values=(username, email, password, telefon, logged_in_user_id))
        messagebox.showinfo("Başarılı", "Kullanıcı bilgileri başarıyla güncellendi.")
    else:
        messagebox.showerror("Hata", "Kullanıcı bilgileri alınamadı.")

def open_update_user_window(): # Kullanıcı bilgilerini güncelleme penceresini açar
    update_user_window = tk.Toplevel(root)
    update_user_window.title("Kullanıcı Bilgilerini Güncelle")

    # Mevcut kullanıcı bilgilerini al
    query = "SELECT musteri_adi, email, musteri_sifre, telefon FROM Musteriler WHERE musteri_id = %s"
    user_info = execute_query(query, values=(logged_in_user_id,), fetch=True)
    if user_info:
        current_username, current_email, _, current_telefon = user_info[0]

        # Kullanıcı adı güncelleme
        label_username = tk.Label(update_user_window, text="Kullanıcı Adı:")
        label_username.grid(row=0, column=0, padx=5, pady=5)
        entry_username = tk.Entry(update_user_window)
        entry_username.grid(row=0, column=1, padx=5, pady=5)
        entry_username.insert(0, current_username)  # Mevcut kullanıcı adını varsayılan olarak görüntüle

        # E-posta güncelleme
        label_email = tk.Label(update_user_window, text="E-posta:")
        label_email.grid(row=1, column=0, padx=5, pady=5)
        entry_email = tk.Entry(update_user_window)
        entry_email.grid(row=1, column=1, padx=5, pady=5)
        entry_email.insert(0, current_email)  # Mevcut e-postayı varsayılan olarak görüntüle

        # Şifre güncelleme
        label_password = tk.Label(update_user_window, text="Şifre:")
        label_password.grid(row=2, column=0, padx=5, pady=5)
        entry_password = tk.Entry(update_user_window, show="*")
        entry_password.grid(row=2, column=1, padx=5, pady=5)

        # Telefon güncelleme
        label_telefon = tk.Label(update_user_window, text="Telefon:")
        label_telefon.grid(row=3, column=0, padx=5, pady=5)
        entry_telefon = tk.Entry(update_user_window)
        entry_telefon.grid(row=3, column=1, padx=5, pady=5)
        entry_telefon.insert(0, current_telefon)  # Mevcut telefon numarasını varsayılan olarak görüntüle

        # Güncelleme işlevi
        def update_user_info_safe():
            if entry_password.get():
                update_user_info(entry_username.get(), entry_email.get(), entry_password.get(), entry_telefon.get())
            else:
                messagebox.showerror("Hata", "Şifre girmeden diğer bilgileri güncelleyemezsiniz.")
        button_update = tk.Button(update_user_window, text="Güncelle", command=update_user_info_safe)
        button_update.grid(row=4, column=1, padx=5, pady=5)
    else:
        messagebox.showerror("Hata", "Kullanıcı bilgileri alınamadı.")

# Satın alınan ürünleri görüntüleme işlemleri
def display_purchased_items():
    purchased_items_window = tk.Toplevel(root)
    purchased_items_window.title("Satın Alınan Ürünler")

    label_heading = tk.Label(purchased_items_window, text="Satın Alınan Ürünler", font=("Helvetica", 16, "bold"))
    label_heading.pack(pady=10)

    frame = tk.Frame(purchased_items_window)
    frame.pack(padx=20, pady=20)

    tree = ttk.Treeview(frame, columns=("Ürün Adı", "Miktar", "Toplam Tutar", "Satın Alma Tarihi"), show="headings")
    tree.heading("Ürün Adı", text="Ürün Adı")
    tree.heading("Miktar", text="Miktar")
    tree.heading("Toplam Tutar", text="Toplam Tutar")
    tree.heading("Satın Alma Tarihi", text="Satın Alma Tarihi")
    tree.pack(fill="both", expand=True)

    query = "SELECT U.urun_adi, S.miktar, U.birim_fiyat * S.miktar AS toplam_tutar, S.tarih FROM Satislar AS S  JOIN Urunler AS U ON S.urun_id = U.urun_id  WHERE musteri_id = %s ORDER BY S.tarih"
    purchased_items = execute_query(query, values=(logged_in_user_id,), fetch=True)
    if purchased_items:
        for item in purchased_items:
            # Satın alma tarihini düzgün formata dönüştür
            item_with_date = list(item)
            item_with_date[3] = item_with_date[3].strftime("%m/%d/%Y")
            tree.insert("", "end", values=item_with_date)
    else:
        tree.insert("", "end", values=("Henüz hiçbir ürün satın alınmamış.", "", "", ""))

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

def after_login_actions():
    global logged_in_user_id
    main_frame.destroy()
    donermarkt_frame.pack(padx=20, pady=20)



#Sepet İşlemleri
def add_to_cart():
    selected_item = tree.item(tree.selection())["values"]
    if selected_item:
        product_name = selected_item[0]
        if product_name in sepet:
            sepet[product_name] += 1
        else:
            sepet[product_name] = 1
        messagebox.showinfo("Başarılı", f"{product_name} sepete eklendi.")
    else:
        messagebox.showerror("Hata", "Lütfen bir ürün seçin.")

sepet = {}
def display_cart():
    cart_window = tk.Toplevel(root)
    cart_window.title("Sepet")

    label_heading = tk.Label(cart_window, text="Sepet", font=("Helvetica", 16, "bold"))
    label_heading.pack(pady=10)

    frame = tk.Frame(cart_window)
    frame.pack(padx=20, pady=20)

    global tree_cart
    tree_cart = ttk.Treeview(frame, columns=("Ürün Adı", "Miktar"), show="headings")
    tree_cart.heading("Ürün Adı", text="Ürün Adı")
    tree_cart.heading("Miktar", text="Miktar")
    tree_cart.pack(fill="both", expand=True)

    for product, quantity in sepet.items():
        tree_cart.insert("", "end", values=(product, quantity))

    def remove_from_cart():
        selected_item = tree_cart.item(tree_cart.selection())["values"]
        if selected_item:
            product_name = selected_item[0]
            if product_name in sepet:
                sepet[product_name] -= 1
                if sepet[product_name] == 0:
                    del sepet[product_name]
                messagebox.showinfo("Başarılı", f"{product_name} sepetten çıkarıldı.")
                display_cart()
            else:
                messagebox.showerror("Hata", "Bu ürün sepetinizde bulunmamaktadır.")
        else:
            messagebox.showerror("Hata", "Lütfen bir ürün seçin.")

    button_remove_from_cart = tk.Button(cart_window, text="Sepetten Çıkar", command=remove_from_cart)
    button_remove_from_cart.pack(padx=20, pady=5)


def purchase_cart():
    for product, quantity in sepet.items():
        purchase_product(product, logged_in_user_id, quantity)
    messagebox.showinfo("Başarılı", "Sepet başarıyla satın alındı.")
    sepet.clear()

# GUI setup
root = tk.Tk()
root.title("Dönermarkt - Teknolojinin Adresi")


main_frame = tk.Frame(root)
main_frame.pack(padx=20, pady=20)

# Ana Pencere, giriş ekranı penceresi
label_title = tk.Label(main_frame, text="DONERMARKT", font=("Goudy Stout", 16, "bold"))
label_title.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

label_email = tk.Label(main_frame, text="E-posta:")
label_email.grid(row=1, column=0, padx=5, pady=5)
entry_email = tk.Entry(main_frame)
entry_email.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

label_password = tk.Label(main_frame, text="Şifre:")
label_password.grid(row=2, column=0, padx=5, pady=5)
entry_password = tk.Entry(main_frame, show="*")
entry_password.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

button_login = tk.Button(main_frame, text="Giriş Yap", command=login)
button_login.grid(row=3, column=1, padx=5, pady=5)

button_register = tk.Button(main_frame, text="Kayıt Ol", command=open_register_window)
button_register.grid(row=3, column=2, padx=5, pady=5)


donermarkt_frame = tk.Frame(root)

# Donermarkt başlığı ekleyelim
label_title = tk.Label(donermarkt_frame, text="DONERMARKT", font=("Goudy Stout", 24, "bold"))
label_title.pack(pady=20)

search_frame = tk.LabelFrame(donermarkt_frame, text="Ürün Arama ve Filtreleme")
search_frame.pack(fill="both", expand="yes", padx=20, pady=20)

label_search = tk.Label(search_frame, text="Ürün Arama:")
label_search.grid(row=0, column=0, padx=5, pady=5)
search_combobox = ttk.Combobox(search_frame, width=30)
search_combobox.grid(row=0, column=1, padx=5, pady=5)
update_search_combobox()

label_sort = tk.Label(search_frame, text="Fiyat Sıralama:")
label_sort.grid(row=0, column=2, padx=5, pady=5)
sort_combobox = ttk.Combobox(search_frame, width=20, values=["Varsayılan", "Fiyat - Artan", "Fiyat - Azalan"])
sort_combobox.grid(row=0, column=3, padx=5, pady=5)
sort_combobox.current(0)

label_price_range = tk.Label(search_frame, text="Fiyat Aralığı:")
label_price_range.grid(row=1, column=0, padx=5, pady=5)
price_from_entry = tk.Entry(search_frame, width=10)
price_from_entry.grid(row=1, column=1, padx=5, pady=5)
label_to = tk.Label(search_frame, text=" - ")
label_to.grid(row=1, column=2, padx=5, pady=5)
price_to_entry = tk.Entry(search_frame, width=10)
price_to_entry.grid(row=1, column=3, padx=5, pady=5)

button_search = tk.Button(search_frame, text="Ara", command=search_products)
button_search.grid(row=1, column=4, padx=5, pady=5)

tree_frame = tk.LabelFrame(donermarkt_frame, text="Ürün Listesi")
tree_frame.pack(fill="both", expand="yes", padx=20, pady=20)

tree = ttk.Treeview(tree_frame, columns=("Ürün Adı", "Fiyat", "Stok Miktarı", "Satış Sayısı"), show="headings")
tree.heading("Ürün Adı", text="Ürün Adı")
tree.heading("Fiyat", text="Fiyat")
tree.heading("Stok Miktarı", text="Stok Miktarı")
tree.heading("Satış Sayısı", text="Satış Sayısı")
tree.pack(fill="both", expand="yes")

label_quantity = tk.Label(donermarkt_frame, text="Adet:")
label_quantity.pack(side="left", padx=20, pady=5)

entry_quantity = tk.Entry(donermarkt_frame)
entry_quantity.pack(side="left", padx=5, pady=5)

button_purchase = tk.Button(donermarkt_frame, text="Satın Al", command=lambda: purchase_product(
    tree.item(tree.selection())["values"][0], logged_in_user_id, int(entry_quantity.get())))
button_purchase.pack(side="left", padx=20, pady=20)

button_add_to_cart = tk.Button(donermarkt_frame, text="Sepete Ekle", command=add_to_cart)
button_add_to_cart.pack(side="right", padx=20, pady=5)

button_display_cart = tk.Button(donermarkt_frame, text="Sepeti Görüntüle", command=display_cart)
button_display_cart.pack(side="right", padx=20, pady=5)

button_purchase_cart = tk.Button(donermarkt_frame, text="Sepeti Satın Al", command=purchase_cart)
button_purchase_cart.pack(side="right", padx=20, pady=5)


# //ESTETİK DÜZENLEMELER
# Kök pencere arka plan rengini değiştirme
root.config(bg="#f0f0f0")

# Butonların arka plan rengini ve yazı rengini değiştirme, kenarları yuvarlama ve gölge ekleme
button_login.config(bg="#007bff", fg="white", borderwidth=0, padx=10, pady=5, relief="raised", font=("Helvetica", 10, "bold"))
button_register.config(bg="#28a745", fg="white", borderwidth=0, padx=10, pady=5, relief="raised", font=("Helvetica", 10, "bold"))
button_search.config(bg="#17a2b8", fg="white", borderwidth=0, padx=10, pady=5, relief="raised", font=("Helvetica", 10, "bold"))
button_purchase.config(bg="#dc3545", fg="white", borderwidth=0, padx=10, pady=5, relief="raised", font=("Helvetica", 10, "bold"))
button_add_to_cart.config(bg="#ffc107", fg="black", borderwidth=0, padx=10, pady=5, relief="raised", font=("Helvetica", 10, "bold"))
button_display_cart.config(bg="#17a2b8", fg="white", borderwidth=0, padx=10, pady=5, relief="raised", font=("Helvetica", 10, "bold"))
button_purchase_cart.config(bg="#28a745", fg="white", borderwidth=0, padx=10, pady=5, relief="raised", font=("Helvetica", 10, "bold"))



def enable_menus(): # giriş yaptıktan sonra kullanılabilir olacak menü butonları
    file_menu.entryconfig("Bilgileri Güncelle", state="normal")
    file_menu.entryconfig("Satın Alınan Ürünleri Göster", state="normal")

#Menü Oluşturma
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Ayarlar Ve Özellikler", menu=file_menu)
file_menu.add_command(label="Admin Paneli", command=open_admin_panel)
file_menu.add_command(label="Bilgileri Güncelle", command=open_update_user_window, state="disabled")
file_menu.add_command(label="Satın Alınan Ürünleri Göster", command=display_purchased_items, state="disabled")

root.mainloop()
