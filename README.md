#  Akıllı Çöp Konteyneri: Atık Yönetimi Analizi ve Tahminlemesi


##  Proje Hakkında
Bu proje, atık yönetimi operasyonlarını optimize etmek amacıyla akıllı çöp konteynerlerinden gelen IoT sensör verilerini analiz eder. Konteynerlerin doluluk oranlarını (`FL_B`), atık türlerini ve fiziksel yapılarını inceleyerek operasyonel içgörüler sunar ve bir konteynerin boşaltılması gerekip gerekmediğini tahminleyen bir Makine Öğrenmesi modeli geliştirir.

---

##  Veri Seti Açıklaması
Veri seti, akıllı çöp kutularından alınan aşağıdaki öznitelikleri içerir:

Kolonlar:

**Class:** Boşaltma durumu (Emptying / Non-Emptying) — Hedef Değişken (y)
**FL_B:** Güncel doluluk oranı (B Sensörü)
**FL_A:** Güncel doluluk oranı (A Sensörü)
**VS:** Hacimsel sensör verisi
**FL_B_3:** 3 saat önceki doluluk verisi
**FL_B_12:** 12 saat önceki doluluk verisi
**Container Type:** Konteynerin yapısal tipi (Cubic, Diamond, vb.)
**Recyclable fraction:** Atık türü (Mixed, Recyclable, vb.).
---

## Veri Analizi
###  Pivot Analizi: Pivot Dönüşümü 
 Bu analiz, hangi konteyner tipinin hangi atık türüyle ne kadar sürede/seviyede dolduğunu ortaya koyar.Hedef değişkenimiz olan konteynerin boşaltılmalı/boşaltılmamalı 
 olayını mantığını anlamak ve hangi tür konteynerlerin hangi tür atıklarla daha çabuk dolma riskinin bulunduğunu anlamak için çok önemlidir.

**Metodoloji:**
- **Satırlar:** Konteyner Tipi (Örn: Diamond, Cubic, Accordion)
- **Sütunlar:** Atık Türü (Mixed, Recyclable, Non-Recyclable)
- **Değerler:** Boşaltma Öncesi Ortalama Doluluk Seviyesi (`FL_B`)


Veri setini derinlemesine anlamak için genişletilmiş grafiksel analizler yapılmıştır:

**Sınıf Dağılımı:** "Boşalt" (Emptying) ve "Boşaltma" (Non-Emptying) etiketlerinin veri setindeki dengesi incelendi.
**Doluluk Histogramı:** `FL_B` değişkeninin dağılımı incelenerek genel doluluk eşikleri belirlendi.
**Kutu Grafikleri :**
  * *Konteyner Bazlı:* Her bir konteyner tasarımının doluluk varyansı ve aykırı değerleri tespit edildi.
  * *Atık Türü Bazlı:* Farklı atık yoğunluklarının sensör verilerine etkisi görselleştirildi.
**Korelasyon Matrisi:** Sensör okumaları (FL_B, FL_A) ve batarya/voltaj durumları arasındaki ilişkiler haritalandırıldı.

---
## Ön İşleme Adımları:
* **Eksik Veri:** Sayısal boşluklar ortalama değer ile dolduruldu.
* **Encoding:** Kategorik veriler Label Encoding ile sayısallaştırıldı.
* **Normalizasyon(Scaling):** Özellikle **KNN** algoritması için veriler `StandardScaler` ile normalize edildi.
---
##  Model Karşılaştırması ve Sonuçlar
Konteynerin boşaltılma durumunu tahmin etmek için 3 farklı Makine Öğrenmesi algoritması eğitilmiş ve kıyaslanmıştır.


###  Performans Liderlik Tablosu

| Sıra | Model | Doğruluk (Accuracy) | Notlar |
|------|-------|---------------------|--------|
| 1 | **Random Forest** | **%96.01** | En iyi performansı gösterdi. Gürültülü verilerde ve karmaşık ilişkilerde çok başarılı. |
| 2 | Gradient Boosting | %91.70 | Güçlü bir model ancak Random Forest'a göre hafif bir aşırı öğrenme (overfitting) eğilimi var. |
| 3 | KNN (K-En Yakın Komşu) | %90.41 | İyi bir taban (baseline) skoru verdi, ancak yüksek başarı için veri normalizasyonu şart. |

---
## Grafikler



##  Kurulum ve Çalıştırma
1.  **Repoyu klonlayın:**
    ```bash
    git clone [https://github.com/kullaniciadiniz/akilli-cop-analizi.git](https://github.com/kullaniciadiniz/akilli-cop-analizi.git)
    ```
2.  **Gerekli kütüphaneleri yükleyin:**
    ```bash
    pip install pandas numpy seaborn matplotlib scikit-learn
    ```
3.  **Analizi çalıştırın:**
    `Conteiner.py` dosyasını VS Code üzerinde açıp çalıştırın.

---

