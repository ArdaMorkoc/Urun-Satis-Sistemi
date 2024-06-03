import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  
import psycopg2
from psycopg2 import Error

user_logged_in = False
logged_in_user_id = None

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

def execute_query(query, fetch=False):
    connection = connect()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        if fetch:
            result = cursor.fetchall()
            return result
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing query:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

def execute_query_params(query, values):
    connection = connect()
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount > 0:
            return cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing query:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()



def urunler_gorunumunu_listele():
    if not user_logged_in:
        messagebox.showerror("Hata", "Lütfen önce giriş yapın.")
        return
    
    for row in tree.get_children():
        tree.delete(row)

    query = "SELECT * FROM UrunlerGorunumu ORDER BY urun_id"
    result = execute_query(query, fetch=True)
    
    if result:
        sorted_result = sorted(result, key=lambda x: x[0])
        
        for row in sorted_result:
            tree.insert("", tk.END, values=row)
    else:
        messagebox.showerror("Hata", "Ürün görünümü bulunamadı.")

def urun_satinal(urun_id, miktar, kullanici_id):
    if not user_logged_in:
        messagebox.showerror("Hata", "Lütfen önce giriş yapın.")
        return
    
    query = "INSERT INTO Satislar (urun_id, miktar, kullanici_id) VALUES (%s, %s, %s)"
    execute_query_params(query, (urun_id, miktar, kullanici_id))
    messagebox.showinfo("Başarılı", "Ürün başarıyla satın alındı.")

def musteri_siparisleri_listele(kullanici_id):
    if not user_logged_in:
        messagebox.showerror("Hata", "Lütfen önce giriş yapın.")
        return
    
    query = "SELECT * FROM Satislar WHERE musteri_id = %s"
    result = execute_query_params(query, (kullanici_id,))
    if result:
        for row in result:
            print(row)  
    else:
        messagebox.showerror("Hata", "Sipariş bulunamadı.")

def kullanici_bilgilerini_guncelle(kullanici_id, yeni_adres, yeni_telefon):
    if not user_logged_in:
        messagebox.showerror("Hata", "Lütfen önce giriş yapın.")
        return
    
    query = "UPDATE Kullanicilar SET adres = %s, telefon = %s WHERE kullanici_id = %s"
    execute_query_params(query, (yeni_adres, yeni_telefon, kullanici_id))
    messagebox.showinfo("Başarılı", "Kullanıcı bilgileri başarıyla güncellendi.")



def show_successful_login_message():
    messagebox.showinfo("Başarılı", "Giriş başarılı.")

def enable_components():
    list_products_button.config(state="normal")

def login():
    kullanici_adi = entry_username.get()
    sifre = entry_password.get()

    query = "SELECT * FROM Kullanicilar WHERE kullanici_adi = %s AND sifre = %s"
    result = execute_query_params(query, (kullanici_adi, sifre))
    if result:
        show_successful_login_message()  
        enable_components()
        global user_logged_in
        user_logged_in = True
    else:
        messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre.")

root = tk.Tk()
root.title("Admin Paneli")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#E1E1E1", foreground="black", fieldbackground="#E1E1E1")
style.map("Treeview", background=[("selected", "#347083")])

tk.Label(root, text="Kullanıcı Adı:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Şifre:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5)
entry_username = tk.Entry(root, font=("Helvetica", 12))
entry_password = tk.Entry(root, show="*", font=("Helvetica", 12))

entry_username.grid(row=0, column=1, padx=10, pady=5)
entry_password.grid(row=1, column=1, padx=10, pady=5)

login_button = tk.Button(root, text="Giriş Yap", font=("Helvetica", 12), command=login)
login_button.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

list_products_button = tk.Button(root, text="Ürünleri Listele", state="disabled", font=("Helvetica", 12), command=urunler_gorunumunu_listele)
list_products_button.grid(row=3, column=1, columnspan=2, padx=10, pady=5)

tree = ttk.Treeview(root, columns=("ID", "Ürün Adı", "Birim Fiyat", "Stok Miktarı"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Ürün Adı", text="Ürün Adı")
tree.heading("Birim Fiyat", text="Birim Fiyat")
tree.heading("Stok Miktarı", text="Stok Miktarı")
tree.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

tk.Label(root, text="İşlem Tipi:", font=("Helvetica", 12)).grid(row=5, column=0, padx=10, pady=5)
tk.Label(root, text="Ürün ID:", font=("Helvetica", 12)).grid(row=6, column=0, padx=10, pady=5)
tk.Label(root, text="Yeni Ürün Adı:", font=("Helvetica", 12)).grid(row=7, column=0, padx=10, pady=5)
tk.Label(root, text="Yeni Birim Fiyatı:", font=("Helvetica", 12)).grid(row=8, column=0, padx=10, pady=5)
tk.Label(root, text="Yeni Stok Miktarı:", font=("Helvetica", 12)).grid(row=9, column=0, padx=10, pady=5)

operation_type_options = ["insert", "update", "delete"]
selected_operation_type = tk.StringVar(root)
selected_operation_type.set(operation_type_options[0])
operation_type_menu = ttk.Combobox(root, textvariable=selected_operation_type, values=operation_type_options).grid(row=5, column=1, padx=10, pady=5)

entry_product_id = tk.Entry(root, font=("Helvetica", 12))
entry_new_product_name = tk.Entry(root, font=("Helvetica", 12))
entry_new_unit_price = tk.Entry(root, font=("Helvetica", 12))
entry_new_stock_amount = tk.Entry(root, font=("Helvetica", 12))

entry_product_id.grid(row=6, column=1, padx=10, pady=5)
entry_new_product_name.grid(row=7, column=1, padx=10, pady=5)
entry_new_unit_price.grid(row=8, column=1, padx=10, pady=5)
entry_new_stock_amount.grid(row=9, column=1, padx=10, pady=5)

def perform_operation():
    if not user_logged_in:
        messagebox.showerror("Hata", "Lütfen önce giriş yapın.")
        return

    operation_type = selected_operation_type.get()
    product_id = entry_product_id.get()
    new_product_name = entry_new_product_name.get()
    new_unit_price = entry_new_unit_price.get()
    new_stock_amount = entry_new_stock_amount.get()

    old_product_info_query = "SELECT urun_adi, birim_fiyat, stok_miktari FROM Urunler WHERE urun_id = %s"
    old_product_info = execute_query_params(old_product_info_query, (product_id,))

    if old_product_info:
        old_product_info = old_product_info[0]  
        
        if not new_product_name:
            new_product_name = old_product_info[0]
        if not new_unit_price:
            new_unit_price = old_product_info[1]
        if not new_stock_amount:
            new_stock_amount = old_product_info[2]

        if operation_type == "insert":
            query = "INSERT INTO Urunler (urun_adi, birim_fiyat, stok_miktari) VALUES (%s, %s, %s)"
            execute_query_params(query, (new_product_name, new_unit_price, new_stock_amount))
            messagebox.showinfo("Başarılı", "Ürün başarıyla eklendi.")
        elif operation_type == "update":
            query = "UPDATE Urunler SET urun_adi = %s, birim_fiyat = %s, stok_miktari = %s WHERE urun_id = %s"
            execute_query_params(query, (new_product_name, new_unit_price, new_stock_amount, product_id))
            messagebox.showinfo("Başarılı", "Ürün bilgileri başarıyla güncellendi. Ürünleri Listele butonuna tekrar basarak kayıtları görebilirsiniz.")
        elif operation_type == "delete":
            delete_product_query = "DELETE FROM Urunler WHERE urun_id = %s"
            execute_query_params(delete_product_query, (product_id,))
            
            delete_order_details_query = "DELETE FROM SiparisDetaylari WHERE urun_id = %s"
            execute_query_params(delete_order_details_query, (product_id,))
            
            messagebox.showinfo("Başarılı", "Ürün başarıyla silindi. Ürünleri Listele butonuna tekrar basarak kayıtları görebilirsiniz.")
        else:
            messagebox.showerror("Hata", "Geçersiz işlem tipi.")
    else:
        messagebox.showerror("Hata", "Belirtilen ID'ye sahip bir ürün bulunamadı.")

perform_operation_button = tk.Button(root, text="İşlemi Gerçekleştir", font=("Helvetica", 12), command=perform_operation)
perform_operation_button.grid(row=10, column=1, columnspan=2, padx=10, pady=5)

def execute_query_params_fetchall(query, values):
    connection = connect()
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        result = cursor.fetchall()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing query:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

def urun_adi_ile_listele():
    if not user_logged_in:
        messagebox.showerror("Hata", "Lütfen önce giriş yapın.")
        return
    
    arama_terimi = entry_search.get()
    print("Arama Terimi:", arama_terimi)  

    for row in tree.get_children():
        tree.delete(row)

    query = "SELECT urun_id, urun_adi, birim_fiyat, stok_miktari FROM Urunler WHERE urun_adi ILIKE %s ORDER BY urun_id"
    result = execute_query_params_fetchall(query,('%' + arama_terimi + '%',))
    
    if result:
        sorted_result = sorted(result, key=lambda x: x[0])
        
        for row in sorted_result:
            tree.insert("", tk.END, values=row)
    else:
        messagebox.showerror("Hata", "Ürün bulunamadı.")

search_button = tk.Button(root, text="Ürün Adına Göre Ara", font=("Helvetica", 12), command=urun_adi_ile_listele)
search_button.grid(row=12, column=1, columnspan=2, padx=10, pady=5)

entry_search = tk.Entry(root, font=("Helvetica", 12))
entry_search.grid(row=12, column=0, padx=10, pady=5)

def musterileri_listele():
    if not user_logged_in:
        messagebox.showerror("Hata", "Lütfen önce giriş yapın.")
        return
    
    for row in tree.get_children():
        tree.delete(row)

    query = "SELECT * FROM Musteriler ORDER BY musteri_id"
    result = execute_query(query, fetch=True)
    
    if result:
        sorted_result = sorted(result, key=lambda x: x[0])
        
        for row in sorted_result:
            tree.insert("", tk.END, values=row)
    else:
        messagebox.showerror("Hata", "Ürün görünümü bulunamadı.")

search_button = tk.Button(root, text="Müşterileri Listele", font=("Helvetica", 12), command=musterileri_listele)
search_button.grid(row=13, column=0, columnspan=2, padx=10, pady=5)



def update_user_info(user_id, new_username, new_email, new_phone, new_password):
    if not user_logged_in:
        messagebox.showerror("Hata", "Lütfen önce giriş yapın.")
        return

    if not new_username and not new_email and not new_phone and not new_password:
        messagebox.showerror("Hata", "Lütfen en az bir alanı doldurun.")
        return

    query = "UPDATE Kullanicilar SET "
    data = []
    if new_username:
        query += "kullanici_adi = %s, "
        data.append(new_username)
    if new_email:
        query += "email = %s, "
        data.append(new_email)
    if new_phone:
        query += "telefon = %s, "
        data.append(new_phone)
    if new_password:
        query += "sifre = %s, "
        data.append(new_password)
    query = query[:-2]
    query += " WHERE kullanici_id = %s"
    data.append(user_id)
    
    execute_query_params(query, data)
    messagebox.showinfo("Başarılı", "Kullanıcı bilgileri başarıyla güncellendi.")

def open_user_update_operations_window():
    if not user_logged_in:
        messagebox.showerror("Hata", "Lütfen önce giriş yapın.")
        return
    
    other_operations_window = tk.Toplevel(root)
    other_operations_window.title("Kullanıcı Bilgilerini Güncelleme")
    
    # Kullanıcılar tablosunu listeleme
    query = "SELECT * FROM Kullanicilar"
    user_data = execute_query(query, fetch=True)

    # Kullanıcılar tablosu Treeview
    user_tree = ttk.Treeview(other_operations_window, columns=("ID", "Kullanıcı Adı", "Şifre", "E-posta", "Telefon"), show="headings")
    user_tree.heading("ID", text="ID")
    user_tree.heading("Kullanıcı Adı", text="Kullanıcı Adı")
    user_tree.heading("Şifre", text="Şifre")
    user_tree.heading("E-posta", text="E-posta")
    user_tree.heading("Telefon", text="Telefon")
    user_tree.grid(row=0, column=0, padx=10, pady=5, columnspan=2)

    if user_data:
        for row in user_data:
            user_tree.insert("", tk.END, values=row)

    tk.Label(other_operations_window, text="Kullanıcı Bilgilerini Güncelleme", font=("Helvetica", 12)).grid(row=1, column=0, columnspan=2, pady=5)
    tk.Label(other_operations_window, text="ID:", font=("Helvetica", 10)).grid(row=2, column=0, padx=5, pady=5)
    entry_user_id = tk.Entry(other_operations_window, font=("Helvetica", 10))
    entry_user_id.grid(row=2, column=1, padx=5, pady=5)
    tk.Label(other_operations_window, text="Yeni Kullanıcı Adı:", font=("Helvetica", 10)).grid(row=3, column=0, padx=5, pady=5)
    entry_new_username = tk.Entry(other_operations_window, font=("Helvetica", 10))
    entry_new_username.grid(row=3, column=1, padx=5, pady=5)
    tk.Label(other_operations_window, text="Yeni E-posta:", font=("Helvetica", 10)).grid(row=4, column=0, padx=5, pady=5)
    entry_new_email = tk.Entry(other_operations_window, font=("Helvetica", 10))
    entry_new_email.grid(row=4, column=1, padx=5, pady=5)
    tk.Label(other_operations_window, text="Yeni Telefon Numarası:", font=("Helvetica", 10)).grid(row=5, column=0, padx=5, pady=5)
    entry_new_phone = tk.Entry(other_operations_window, font=("Helvetica", 10))
    entry_new_phone.grid(row=5, column=1, padx=5, pady=5)
    tk.Label(other_operations_window, text="Yeni Şifre:", font=("Helvetica", 10)).grid(row=6, column=0, padx=5, pady=5)
    entry_new_password = tk.Entry(other_operations_window, font=("Helvetica", 10))
    entry_new_password.grid(row=6, column=1, padx=5, pady=5)
    update_info_button = tk.Button(other_operations_window, text="Bilgileri Güncelle", font=("Helvetica", 10), command=lambda: update_user_info(entry_user_id.get(), entry_new_username.get(), entry_new_email.get(), entry_new_phone.get(), entry_new_password.get()))
    update_info_button.grid(row=7, column=0, columnspan=2, pady=5)




# Kullanıcı Bilgilerini Güncelle butonu
other_operations_button = tk.Button(root, text="Kullanıcı Bilgilerini Güncelle", font=("Helvetica", 12), command=open_user_update_operations_window)
other_operations_button.grid(row=14, column=1, columnspan=2, padx=10, pady=5)

def update_order_info(order_id, new_order_date, new_total_amount):
    if not user_logged_in:
        messagebox.showerror("Hata", "Lütfen önce giriş yapın.")
        return

    if not new_order_date and not new_total_amount:
        messagebox.showerror("Hata", "Lütfen en az bir alanı doldurun.")
        return

    query = "UPDATE Siparisler AS s SET "
    data = []
    if new_order_date:
        query += "siparis_tarihi = %s, "
        data.append(new_order_date)
    if new_total_amount:
        query += "toplam_tutar = %s, "
        data.append(new_total_amount)
    query = query[:-2]  
    query += " FROM Musteriler AS m WHERE s.musteri_id = m.musteri_id AND s.siparis_id = %s"
    data.append(order_id)
    
    execute_query_params(query, data)
    messagebox.showinfo("Başarılı", "Sipariş bilgileri başarıyla güncellendi.")

def open_order_update_operations_window():
    if not user_logged_in:
        messagebox.showerror("Hata", "Lütfen önce giriş yapın.")
        return
    
    order_operations_window = tk.Toplevel(root)
    order_operations_window.title("Sipariş Bilgilerini Güncelleme")
    
    # Siparişler tablosunu listeleme
    query = "SELECT s.siparis_id, m.musteri_adi, s.siparis_tarihi, s.toplam_tutar FROM Siparisler AS s JOIN Musteriler AS m ON s.musteri_id = m.musteri_id ORDER BY s.siparis_id"
    order_data = execute_query(query, fetch=True)

    # Sipariş tablosu Treeview
    order_tree = ttk.Treeview(order_operations_window, columns=("ID", "Müşteri Adı", "Sipariş Tarihi", "Toplam Tutar"), show="headings")
    order_tree.heading("ID", text="ID")
    order_tree.heading("Müşteri Adı", text="Müşteri Adı")
    order_tree.heading("Sipariş Tarihi", text="Sipariş Tarihi")
    order_tree.heading("Toplam Tutar", text="Toplam Tutar")
    order_tree.grid(row=0, column=0, padx=10, pady=5, columnspan=2)

    if order_data:
        for row in order_data:
            order_tree.insert("", tk.END, values=row)

    tk.Label(order_operations_window, text="Sipariş Bilgilerini Güncelleme", font=("Helvetica", 12)).grid(row=1, column=0, columnspan=2, pady=5)
    tk.Label(order_operations_window, text="ID:", font=("Helvetica", 10)).grid(row=2, column=0, padx=5, pady=5)
    entry_order_id = tk.Entry(order_operations_window, font=("Helvetica", 10))
    entry_order_id.grid(row=2, column=1, padx=5, pady=5)
    tk.Label(order_operations_window, text="Yeni Sipariş Tarihi (YYYY-AA-GG):", font=("Helvetica", 10)).grid(row=3, column=0, padx=5, pady=5)
    entry_new_order_date = tk.Entry(order_operations_window, font=("Helvetica", 10))
    entry_new_order_date.grid(row=3, column=1, padx=5, pady=5)
    tk.Label(order_operations_window, text="Yeni Toplam Tutar:", font=("Helvetica", 10)).grid(row=4, column=0, padx=5, pady=5)
    entry_new_total_amount = tk.Entry(order_operations_window, font=("Helvetica", 10))
    entry_new_total_amount.grid(row=4, column=1, padx=5, pady=5)
    update_order_button = tk.Button(order_operations_window, text="Siparişi Güncelle", font=("Helvetica", 10), command=lambda: update_order_info(entry_order_id.get(), entry_new_order_date.get(), entry_new_total_amount.get()))
    update_order_button.grid(row=5, column=0, columnspan=2, pady=5)


# Sipariş Bilgilerini Güncelle butonu
order_operations_button = tk.Button(root, text="Sipariş Bilgilerini Güncelle", font=("Helvetica", 12), command=open_order_update_operations_window)
order_operations_button.grid(row=15, column=1, columnspan=2, padx=10, pady=5)

def urun_satinal(urun_id, miktar, musteri_id):
    if not user_logged_in:
        messagebox.showerror("Hata", "Lütfen önce giriş yapın.")
        return

    # Ürün stoğunu kontrol et
    query = "SELECT stok_miktari FROM Urunler WHERE urun_id = %s"
    result = execute_query_params(query, (urun_id,))
    
    if not result:
        messagebox.showerror("Hata", "Ürün bulunamadı.")
        return
    
    stok_miktari = result[0][0]
    if stok_miktari < int(miktar):
        messagebox.showerror("Hata", "Stokta yeterli ürün yok.")
        return

    # Satışı kaydet
    query = "INSERT INTO Satislar (urun_id, miktar, musteri_id) VALUES (%s, %s, %s)"
    execute_query_params(query, (urun_id, miktar, musteri_id))
    
    # Stok miktarını güncelle
    yeni_stok_miktari = stok_miktari - int(miktar)
    query = "UPDATE Urunler SET stok_miktari = %s WHERE urun_id = %s"
    execute_query_params(query, (yeni_stok_miktari, urun_id))
    
    messagebox.showinfo("Başarılı", "Ürün başarıyla satın alındı ve stoktan düşüldü.")

def open_product_purchase_window():
    if not user_logged_in:
        messagebox.showerror("Hata", "Lütfen önce giriş yapın.")
        return
    
    product_purchase_window = tk.Toplevel(root)
    product_purchase_window.title("Ürün Satın Alma")

    tk.Label(product_purchase_window, text="Ürün Satın Alma", font=("Helvetica", 12)).grid(row=0, column=0, columnspan=2, pady=5)
    tk.Label(product_purchase_window, text="Ürün ID:", font=("Helvetica", 10)).grid(row=1, column=0, padx=5, pady=5)
    entry_product_id = tk.Entry(product_purchase_window, font=("Helvetica", 10))
    entry_product_id.grid(row=1, column=1, padx=5, pady=5)
    tk.Label(product_purchase_window, text="Miktar:", font=("Helvetica", 10)).grid(row=2, column=0, padx=5, pady=5)
    entry_quantity = tk.Entry(product_purchase_window, font=("Helvetica", 10))
    entry_quantity.grid(row=2, column=1, padx=5, pady=5)
    tk.Label(product_purchase_window, text="Müşteri ID:", font=("Helvetica", 10)).grid(row=3, column=0, padx=5, pady=5)
    entry_customer_id = tk.Entry(product_purchase_window, font=("Helvetica", 10))
    entry_customer_id.grid(row=3, column=1, padx=5, pady=5)

    purchase_button = tk.Button(product_purchase_window, text="Satın Al", font=("Helvetica", 10), command=lambda: urun_satinal(entry_product_id.get(), entry_quantity.get(), entry_customer_id.get()))
    purchase_button.grid(row=4, column=0, columnspan=2, pady=5)

# Satış Yap butonu
order_operations_button = tk.Button(root, text="Satış Yap", font=("Helvetica", 12), command=open_product_purchase_window)
order_operations_button.grid(row=14, column=0, columnspan=2, padx=10, pady=5)


root.mainloop()