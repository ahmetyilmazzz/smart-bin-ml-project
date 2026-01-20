# Smart Bin Projesi - Doluluk Tahmini ve Sınıflandırma

Bu projede akıllı çöp konteynerlerinden gelen sensör verilerini kullanarak konteynerlerin boşaltılıp boşaltılmayacağını tahmin etmeye çalıştım.

---

## Sertifikalar

### Makine Öğrenmesi Sertifikası

![Makine Öğrenmesi Sertifika](images/makine_ogrenmesi_sertifika.png)

### Python Sertifikası

![Python Sertifika](images/python_sertifika.png)

---

---

## Proje Amacı

Amacım akıllı atık yönetiminde verimliliği artırmak için konteynerlerin ne kadar dolduğuna bakmak ve boşaltma kararlarını optimize etmek.

Yapmak istediklerim:
- Hangi konteyner tipi hangi atıkta daha hızlı doluyor bulmak
- Sensör verilerini kullanarak boşaltma kararı tahmin etmek
- Farklı modelleri deneyip hangisi daha iyi görmek

---

## Veri Seti

Smart_Bin.csv dosyasını kullanıyorum. İçinde 4638 tane kayıt ve 10 tane sütun var.

### Değişkenler ne anlama geliyor?

- Class: Boşaltılıp boşatılmadığı (Emptying / Non-Emptying) - Tahmin etmeye çalıştığım şey
- FL_B: Alt sensörden gelen doluluk oranı
- FL_A: Üst sensörden gelen doluluk oranı
- VS: Hacim sensörü verisi
- FL_B_3, FL_A_3: 3 saat önceki doluluk verileri
- FL_B_12, FL_A_12: 12 saat önceki doluluk verileri
- Container Type: Çöp kutusunun tipi (Cubic, Diamond, Accordion gibi)
- Recyclable fraction: Atık türü (Mixed, Recyclable, Non Recyclable)

---

## Pivot Tablo Analizi

Hangi konteyner tipi hangi atık türünde daha hızlı doluyor bulmak için pivot tablo yaptım.

Neden pivot tablo yaptım?
- FL_A ve FL_B arasındaki farka bakınca doluluk artışını görebiliyorum
- Bu farkı hesaplayıp konteyner ve atık türüne göre gruplayınca hangi kombinasyonun daha hızlı dolduğunu anlayabiliyorum
- Bu sayede en hızlı dolan çöp kutusu + atık türünü bulabiliyorum

### 1. FL_B (Alt Sensör) Ortalamaları

![FL_B Pivot](images/pivot_fl_b.png)

### 2. FL_A (Üst Sensör) Ortalamaları

![FL_A Pivot](images/pivot_fl_a.png)

### 3. Doluluk Artışı (FL_B - FL_A)

![Delta Pivot](images/pivot_delta.png)

---

## Veri Ön İşleme

Veride birkaç tane eksik Container Type değeri vardı, onları en çok tekrar eden değer (mod) ile doldurdum.

Kategorik değişkenleri sayıya çevirmek için LabelEncoder kullandım. Çünkü makine öğrenmesi modelleri sayıları anlıyor, yazıları anlamıyor.

- Container Type → Container_Enc
- Recyclable fraction → Recyclable_Enc
- Class → y (bu bizim tahmin etmeye çalıştığımız şey)

Veriyi de %75 eğitim, %25 test olarak ikiye böldüm.

EN HIZLI DOLAN KOMBINASYON: Fiberglass Igloo-b + Recyclable

---

## Kullanılan Modeller

3 farklı model denedim:

1. Random Forest
2. Gradient Boosting
3. Logistic Regression

Her birini eğitip test ettim.

### Random Forest Sonuçları

![Random Forest Sonuç](images/random_forest_sonuclar.png)

### Gradient Boosting Sonuçları

![Gradient Boosting Sonuç](images/gradient_boosting_sonuclar.png)

### Logistic Regression Sonuçları

![Logistic Regression Sonuç](images/logistic_regression_sonuclar.png)


---

## Kod Çalışınca Oluşan Görseller

### Pivot Heatmap

Kod çalıştırılınca otomatik olarak bu heatmap oluşturuluyor:

![Pivot Heatmap](images/pivot_heatmap.png)

Bu grafikte renk ne kadar koyuysa o kombinasyon o kadar hızlı doluyor demek.

### Confusion Matrix

En iyi model için confusion matrix çiziliyor:

![Confusion Matrix](images/confusion_matrix.png)

Bu grafik modelin hangi sınıfları ne kadar doğru tahmin ettiğini gösteriyor.

---

## smart_bin_classification.py Kod Açıklaması

Önce csv dosyasını okudum, veri setinin boyutunu ve class dağılımına baktım.

Sonra FL_B'den FL_A'yı çıkararak doluluk artışını hesapladım. Bu değeri kullanarak 3 tane pivot tablo oluşturdum - biri FL_B ortalamaları, biri FL_A ortalamaları, biri de doluluk artışı ortalamaları için. Kod en hızlı dolan kombinasyonu otomatik buldu, ben de bunu heatmap olarak çizip images klasörüne kaydettim.

Veri ön işleme kısmında eksik olan Container Type değerlerini mod ile doldurdum. Kategorik verileri sayıya çevirmek için LabelEncoder kullandım çünkü modeller sayıları anlıyor. Container Type, Recyclable fraction ve Class sütunlarını sayıya çevirdim.

Model kısmında 3 farklı model denedim: Random Forest, Gradient Boosting ve Logistic Regression. Her birini eğitip Accuracy, F1-Score ve Confusion Matrix değerlerine baktım. En iyi sonucu veren model için de confusion matrix grafiğini çizdim.


Kod çalışınca pivot tablolarını ekrana yazacak, heatmap'i oluşturacak, confusion matrix'i çizecek ve en iyi modeli gösterecek.

---

## Sonuç

Bu projede Smart Bin veri seti üzerinde pivot tablo analizi yaptım ve sınıflandırma modelleri denedim. Random Forest en iyi sonucu verdi. Pivot tablo sayesinde hangi konteyner tipinin hangi atık türünde daha hızlı dolduğunu buldum.
