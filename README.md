# Ürün Satış Sistemi

Bu proje, kullanıcıların ürünleri görüntüleyip satın alabileceği, kişisel bilgilerini güncelleyebileceği ve satın alma geçmişlerini inceleyebileceği bir Ürün Satış Sistemi'dir.

## Proje Amacı

Kullanıcılar, sisteme kullanıcı adı ve şifre ile kayıt olup, login ekranından giriş yaparlar. Filtreleme veya arama yaparak istedikleri ürünleri listelerler. İstedikleri ürünü satın alabilirler. Satılan ürünlerin satış sayıları ürün bilgisinde yer alır ve kullanıcı satın aldıktan sonra güncellenir. Kullanıcı, kendi ekranında satın aldığı ürünleri listeleyebilir. Ayrıca, kişisel bilgilerini (adres, telefon vb.) girip güncelleyebilir.

## Proje Özellikleri

1. **Kullanıcı Kaydı ve Girişi:**
   - Kullanıcılar, sisteme kayıt olabilirler. Kayıt olduktan sonra, giriş yaparak uygulamayı kullanabilirler.
   - Giriş yapılmadan önce, kullanıcıların kayıt olmaları gerekmektedir.

2. **Ürün Arama ve Filtreleme:**
   - Kullanıcılar, ürünleri isimleriyle arayabilir ve fiyat aralığına göre filtreleyebilirler.
   - Arama sonuçları, bir liste olarak gösterilir ve kullanıcılar istedikleri ürünleri seçebilirler.

3. **Ürün Satın Alma:**
   - Kullanıcılar, seçtikleri ürünleri sepete ekleyebilir ve istedikleri zaman satın alabilirler.
   - Sepetteki ürünlerin miktarları düzenlenebilir ve satın alınabilir.

4. **Kullanıcı Bilgilerini Güncelleme:**
   - Kullanıcılar, kişisel bilgilerini (kullanıcı adı, e-posta, şifre, telefon) güncelleyebilirler.

5. **Satın Alınan Ürünlerin Geçmişini Görüntüleme:**
   - Kullanıcılar, daha önce satın aldıkları ürünleri ve bu işlemlerin tarihlerini görüntüleyebilirler.

6. **Admin Paneli:**
   - Adminler, özel bir panele erişerek sistemdeki ürünleri ve kullanıcıları yönetebilirler.

## Kullanılan Teknolojiler

- **Python:** Uygulama, Python programlama dili kullanılarak geliştirilmiştir.
- **Tkinter:** Masaüstü arayüzü oluşturmak için Tkinter kütüphanesi kullanılmıştır.
- **Subprocess:** Python'da admin paneli çalıştırmak, yeni süreçler başlatmak ve sistem komutlarını çalıştırmak için kullanılmıştır.
- **PostgreSQL:** Veritabanı yönetimi için PostgreSQL kullanılmıştır. Psycopg2 kütüphanesi ile arayüze bağlanmıştır.

## Proje Geliştirme Süreci

1. **Analiz ve Tasarım:** Projenin gereksinimleri belirlenmiş ve tasarım aşamasına geçilmiştir.
2. **Veritabanı Oluşturma:** PostgreSQL veritabanı, önce OneCompiler üzerinden gerekli tablolar ve ilişkilerle oluşturulmuştur. Daha sonra PostgreSQL’e yüklenmiştir.
3. **Arayüz Geliştirme:** Tkinter kütüphanesi kullanılarak Python ile Visual Studio Code uygulaması aracılığıyla masaüstü arayüzü tasarlanmış ve geliştirilmiştir.
4. **Uygulama Mantığı:** Kullanıcı girişi, ürün arama, sepet işlemleri gibi temel işlevler Python kodlarıyla geliştirilmiştir.
5. **Test ve Geliştirme:** Uygulamanın tüm işlevleri test edilmiş ve hatalar giderilerek geliştirme süreci tamamlanmıştır.

## Proje Sonucu

Ürün Satış Sistemi, bir online teknoloji mağazasının temel işlevselliğini başarıyla simüle etmektedir. Kullanıcılar, uygulama aracılığıyla kolayca ürün arayabilir, sepete ekleyebilir ve satın alabilirler. Ayrıca, kullanıcılar kişisel bilgilerini güncelleyebilir ve satın alma geçmişlerini görüntüleyebilirler. Adminler ise özel bir panele erişerek sistemdeki ürünleri ve kullanıcıları yönetebilirler.

## İletişim

Herhangi bir sorunuz veya geri bildiriminiz varsa, lütfen benimle iletişime geçin:
- E-posta: [ardamorkoc@hotmail.com]
- GitHub: [https://github.com/ArdaMorkoc]
