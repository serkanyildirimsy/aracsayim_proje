# Gişe Veri Analizi Projesi

Bu proje, kullanıcıların gişe verilerini filtreleyip analiz edebileceği bir Flask tabanlı web uygulamasıdır. Uygulama, yerel bir SQLite veritabanından gişe verilerini alır ve kullanıcıların bölge, gişe, araç sınıfı ve tarih aralığına göre filtreleme yapmalarına olanak tanır.

[![Python](https://img.shields.io/badge/Python-3.12-orange.svg?style=flat-square)]


## Özellikler

- **Bölge ve Gişe Seçimi**: Kullanıcılar bir bölge seçebilir ve o bölgedeki mevcut gişeler dinamik olarak yüklenir.

- **Araç Sınıfı Filtreleme**: Kullanıcılar analiz etmek istedikleri araç sınıf(lar)ını seçebilirler.

- **Tarih Filtreleme**: Kullanıcılar başlangıç ve bitiş tarihine göre verileri filtreleyebilirler.

- **Gerçek Zamanlı Veri Analizi**: Kullanıcıların seçtiği kriterlere göre, belirtilen tarih aralığında seçilen araç sınıf(lar)ının toplam araç sayısını hesaplar.

- **Sıfırlama Fonksiyonu**: Kullanıcılar tüm seçimlerini sıfırlayarak yeni bir arama yapabilirler.


## Kullanılan Teknolojiler

- **Flask**: Python ile yazılmış hafif bir web uygulama çerçevesi.

- **SQLite**: Gişe verilerini depolamak için kullanılan, sunucusuz, yapılandırma gerektirmeyen SQL veritabanı.

- **Pandas**: Veri işleme ve analizinde kullanılan güçlü bir Python kütüphanesi.

- **HTML/CSS**: Kullanıcı arayüzü ve sonuçların görüntülenmesi için kullanılır.


## Kurulum

1. Depoyu klonlayın:

   ```bash

   git clone https://github.com/serkanyildirimsy/aracsayim_proje.git

   cd aracsayim_proje

   ```


2. Gereksinimleri yükleyin:

   ```bash

   pip install flask pandas

   ```


3. `gise_verileri.db` veritabanı dosyasının proje dizininde bulunduğundan emin olun.


4. Uygulamayı çalıştırın:

   ```bash

   python app.py

   ```

5. Tarayıcınızda [http://127.0.0.1:5000/](http://127.0.0.1:5000/) adresine giderek uygulamayı kullanmaya başlayabilirsiniz.


## Nasıl Çalışır?

- `load_data()` fonksiyonu, SQLite veritabanından gişe verilerini Pandas DataFrame'e yükler.

- `gise_verileri` tablosundaki tüm verileri okur ve `TARİH` sütununu datetime formatına dönüştürür.


Uygulama kullanıcıya şu seçenekleri sunar:


- **Bölge**: Gişeleri bölgeye göre filtreler.

- **Gişe**: Bölge seçildikten sonra o bölgedeki gişeler görüntülenir.

- **Araç Sınıfları**: 1. sınıf, 2. sınıf gibi araç sınıfları arasından seçim yapılır.

- **Tarih Aralığı**: Verileri analiz etmek için başlangıç ve bitiş tarihi belirlenir.


POST isteği, kullanıcının seçtiği verileri alır ve filtreler. Eğer tüm kriterler geçerliyse, belirtilen araç sınıfları için toplam araç sayısını hesaplar.


Sıfırlama fonksiyonu, kullanıcıların tüm alanları sıfırlayarak yeni bir arama yapmalarını sağlar.


## Veri Yapısı

Proje, `gise_verileri` veritabanı tablosunda şu sütunların bulunduğunu varsayar:


- **BÖLGE MÜDÜRLÜĞÜ**: Gişenin bulunduğu bölge.

- **GİŞE ADI**: Gişe adı.

- **TARİH**: Veri giriş tarihi.

- **1.SINIF ile 6.SINIF**: Araç sınıflarının sayıları (1. sınıf, 2. sınıf, vb.).
  
