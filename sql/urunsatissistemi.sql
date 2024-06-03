-- Ürünler Tablosu
CREATE TABLE Urunler (
    urun_id SERIAL PRIMARY KEY,
    urun_adi VARCHAR(100) NOT NULL,
    birim_fiyat NUMERIC(10,2) NOT NULL CHECK (birim_fiyat >= 0),
    stok_miktari INTEGER NOT NULL CHECK (stok_miktari >= 0),
    satis_sayisi INTEGER NOT NULL DEFAULT 0
);

-- Müşteriler tablosu
CREATE TABLE Musteriler (
    musteri_id SERIAL PRIMARY KEY,
    musteri_adi VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    musteri_sifre VARCHAR(100) NOT NULL,
    telefon VARCHAR(15)
);


-- Siparişler tablosu
CREATE TABLE Siparisler (
    siparis_id SERIAL PRIMARY KEY,
    musteri_id INTEGER REFERENCES Musteriler(musteri_id),
    siparis_tarihi DATE DEFAULT CURRENT_DATE,
    toplam_tutar NUMERIC(10,2) NOT NULL CHECK (toplam_tutar >= 0)
);

-- Sipariş Detayları tablosu
CREATE TABLE SiparisDetaylari (
    siparis_detay_id SERIAL PRIMARY KEY,
    siparis_id INTEGER REFERENCES Siparisler(siparis_id) ON DELETE CASCADE,
    urun_id INTEGER REFERENCES Urunler(urun_id),
    miktar INTEGER NOT NULL CHECK (miktar > 0),
    ara_toplam NUMERIC(10,2) NOT NULL CHECK (ara_toplam >= 0)
);

-- Kullanıcılar tablosu
CREATE TABLE Kullanicilar (
    kullanici_id SERIAL PRIMARY KEY,
    kullanici_adi VARCHAR(100) NOT NULL,
    sifre VARCHAR(100) NOT NULL,
    adres VARCHAR(200),
    telefon VARCHAR(15)
);

-- Satışlar tablosu
CREATE TABLE Satislar (
    satis_id SERIAL PRIMARY KEY,
    urun_id INTEGER REFERENCES Urunler(urun_id),
    miktar INTEGER NOT NULL CHECK (miktar > 0),
    kullanici_id INTEGER REFERENCES Kullanicilar(kullanici_id),
    tarih DATE DEFAULT CURRENT_DATE
);

-- Ürünler Tablosu veri ekleme
INSERT INTO Urunler (urun_adi, birim_fiyat, stok_miktari, satis_sayisi) VALUES
    ('Laptop', 25000.00, 50, 0),
    ('Akıllı Telefon', 15000.00, 100, 0),
    ('Kulaklık', 500.00, 200, 0),
    ('Fare', 500.00, 150, 0),
    ('Klavye', 900.00, 120, 0),
    ('Monitor', 2000.00, 80, 0),
    ('Yazıcı', 1500.00, 30, 0),
    ('Tablet', 4000.00, 70, 0),
    ('Hard Disk', 3000.00, 90, 0),
    ('Hoparlör', 800.00, 120, 0);

-- Müşteriler tablosu veri ekleme
INSERT INTO Musteriler (musteri_adi, email, musteri_sifre, telefon) VALUES
    ('Arda Anıl Morkoç', 'ornek@hotmail.com', '1234', '+905056666666'),
    ('Acun Ilıcalı', 'acunilicali@gmail.com', '1234', '+905012345678'),
    ('Walter White', 'walterwhite@hotmail.com', '1234', '+905021234567'),
    ('Michael Scofield', 'michael.scofield@hotmail.com', '1234', '+905031234567'),
    ('Thomas Shelby', 'shelby.thomas@outlook.com', '1234', '+905041234567'),
    ('Willy Wonka', 'willy.wonka@yahoo.com', '1234', '+905051234567'),
    ('Sherlock Holmes', 'sherlockholmes@yahoo.com', '1234', '+905061234567'),
    ('Rick Sanchez', 'sanchez.rick@hotmail.com', '1234', '+905071234567');

-- Siparişler tablosu veri ekleme
INSERT INTO Siparisler (musteri_id, siparis_tarihi, toplam_tutar) VALUES
    (1, '2024-03-01', 2000.00),
    (2, '2024-03-02', 40000.00),
    (3, '2024-03-03', 5500.00),
    (4, '2024-03-04', 1500.00),
    (5, '2024-03-05', 1400.00),
    (6, '2024-03-06', 2200.00),
    (7, '2024-03-07', 800.00),
    (8, '2024-03-08', 3800.00),
    (9, '2024-03-09', 7000.00),
    (10, '2024-03-10', 3000.00);

-- Sipariş Detayları tablosu veri ekleme
INSERT INTO SiparisDetaylari (siparis_id, urun_id, miktar, ara_toplam) VALUES
    (1, 1, 2, 2400.00),
    (2, 2, 1, 800.00),
    (3, 3, 3, 150.00),
    (4, 4, 5, 100.00),
    (5, 5, 2, 60.00),
    (6, 6, 1, 200.00),
    (7, 7, 2, 300.00),
    (8, 8, 4, 600.00),
    (9, 9, 1, 100.00),
    (10, 10, 3, 240.00);
    

-- Kullanicilar Tablosu veri ekleme
INSERT INTO Kullanicilar (kullanici_adi, sifre, adres, telefon) VALUES
    ('admin', 'admin123', 'Admin Adresi', '+905051234567');

-- View ile tanımlanmış
CREATE VIEW UrunlerGorunumu AS
SELECT urun_id, urun_adi, birim_fiyat, stok_miktari
FROM Urunler;

--Satislar ve Musteri Tablosu Bağlantısı
ALTER TABLE Satislar
ADD COLUMN musteri_id INTEGER REFERENCES Musteriler(musteri_id);