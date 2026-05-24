# Akıllı Otopark ve Plaka Tanıma Projesi

Bu proje, otomata teorisi kapsamında geliştirilen akıllı otopark ve plaka tanıma sistemidir. Projede araç plakası, otopark doluluk durumu ve giriş uygunluğu gibi bilgiler alınarak sistemin durum geçişleri otomata mantığı ile modellenmiştir.

## Proje Amacı

Bu projenin amacı, sonlu otomata kavramını gerçek hayata yakın bir senaryo üzerinden uygulamalı olarak göstermektir. Akıllı otopark sistemi sayesinde araç girişleri kontrol edilmekte, plaka bilgisi değerlendirilmektedir ve otopark kapasitesine göre kabul veya ret kararı verilmektedir.

## Proje Konusu

Akıllı otopark sisteminde araçların otoparka giriş yapabilmesi için belirli kontrollerden geçmesi gerekir. Sistem, kullanıcıdan alınan plaka bilgisini ve otopark durumunu değerlendirerek aracın giriş yapıp yapamayacağına karar verir.

Bu süreçte her aşama bir durum olarak ele alınır ve girdilere göre durum geçişleri gerçekleştirilir.

## Sistem Mantığı

Sistem temel olarak şu adımlarla çalışır:

- Kullanıcıdan araç plakası alınır.
- Plaka formatı kontrol edilir.
- Otoparkta boş yer olup olmadığı kontrol edilir.
- Şartlar uygunsa araç kabul edilir.
- Plaka hatalıysa veya otopark doluysa araç reddedilir.
- Durum geçişleri arayüz üzerinde gösterilir.

## Otomata Durumları

Projede kullanılan temel durumlar şunlardır:

- Başlangıç durumu
- Plaka kontrol durumu
- Kapasite kontrol durumu
- Kabul durumu
- Ret durumu

## Proje Özellikleri

- Kullanıcıdan manuel veri alma
- Plaka kontrolü
- Otopark kapasite kontrolü
- Kabul ve ret durumlarını gösterme
- Durum geçişlerini izleme
- Görsel arayüz desteği
- Otomata mantığına uygun çalışma yapısı

## Kullanılan Teknolojiler

- Python
- Tkinter
- Otomata Teorisi
- Git
- GitHub

## Kurulum ve Çalıştırma

1. Projeyi bilgisayarınıza indirin.
2. Python kurulu olduğundan emin olun.
3. Proje klasörünü Visual Studio Code ile açın.
4. Terminal üzerinden aşağıdaki komutu çalıştırın:

```bash
python uygulama.py
```

## Proje Çıktısı

Program çalıştırıldığında kullanıcıdan alınan bilgilere göre sistemin hangi durumdan hangi duruma geçtiği gösterilir. Son aşamada araç için kabul veya ret sonucu ekrana yansıtılır.

## Geliştirici

**Yakup Çakmak**


