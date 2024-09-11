# Self Driving Car

***Proje hala geliştiriliyor.***

# Gereksinimler

weboots == R2023b

opencv==4.10.0.84

scipy==1.14.1

---
# 10 Eylül 2024 (Eklemeler ve Güncellemeler)

## main.py Ana Kod (Güncellemeler)

Main koduna, trafik tabelalarını ve işaretlerini tespit etmek için YOLOv4 ile eğitilmiş bir model entegre edilmiştir. Bu modelin veri seti, TTVS veri seti içindeki verilerden alınmıştır, ancak model tam olarak eğitilmediği için doğruluk oranı yüksek değildir. Ayrıca, dönüş işlemlerini gerçekleştirmek için `dönüş.py` kodu eklenmiştir. Bu kod, aracın sola, sağa ve ileri doğru dönüşlerini başarılı bir şekilde, ancak tam olarak stabil olmayan bir şekilde yapabilmesini sağlar.

### Genel Yapı

1. **Mesafe Kontrolü (`is_close`)**

   YOLOv4 ile görselden nesne tespiti yaparken aynı nesneyi birden fazla kez tespit etmesini engellemek için bu fonksiyon eklenmiştir. Bu fonksiyon, tespit edilen iki nesnenin merkezlerini karşılaştırarak, aralarındaki mesafe belirli bir değerin altında olduğunda aynı nesne olarak değerlendirilmesini sağlar.

2. **Trafik İşareti Tespiti ve Filtreleme (`get_detected_labels_with_area_filter`)**

   YOLOv4 modeli, ikinci kameradan gelen görüntüler ile belirli bir süre (kodda 2 saniyede bir olarak ayarlandı) içinde nesne tespiti yapar. Bu süre sınırı, kaynakların sürekli olarak kullanılmasını önlemek içindir. Model, TTVS veri setinden alınan 3000 görsel üzerinde eğitilmiştir, ancak eğitim tam olarak tamamlanmadığı için doğruluk oranı yüksek değildir. Tabela tespiti dönüş algoritması için kullanıldığından, tespit edilen nesnelerin bir alan ölçeği eklenmiştir; bu sayede küçük alanlı nesneler dönüş algoritması tarafından dikkate alınmaz.

### dönüş.py Dönüş Algoritması (Ekleme)

Aracın trafik işaretlerine göre yönlendirilmesi için PID kontrol algoritması kullanılmıştır. PID algoritmasının kullanımı, dönüşlerin daha düzgün ve genel yapının daha stabil olmasını sağlamaktadır. Tabela tespiti gerçekleştiğinde `dönüş.py` modülündeki `start()` fonksiyonu çalışır. Bu fonksiyon, ilk olarak tespit edilen tabelaya göre yapılması gereken eylemi belirler. Şimdilik sağa, sola ve ileri gitme eylemleri eklenmiştir. Daha sonra, araç belirli bir süre düz gider ve ardından işarete göre düz, sola veya sağa dönüş başlar. Hedef direksiyon açısı belirlenir ve PID algoritması aracın direksiyon açısını hesaplayarak ayarlar. Dönüş tamamlandığında, direksiyon açısı sıfırlanır. Sol veya sağ dönüşlerde, dönüş sonrası şerit tekrar tespit edilebilmesi için araç belirli bir süre boyunca düz gitmeye devam eder. Kod, aracın şerit tespit ve takibine devam etmesiyle sonlanır.




---

# 4 Eylül 2024 (eklemeler ve güncellemeler)

---
## main.py Ana kod. (Ekleme)

`main.py` dosyası, Webots simülasyon ortamında bir aracı şeritler üzerinde yönlendirmek için kullanılan ana kontrol kodunu içerir. Kod, araç kameralardan aldığı görüntülerle şeritleri tespit eder ve PID kontrol algoritmasını kullanarak aracın yönünü ayarlar.

### 1. Kameraların Tanımlanması

İki kamera kullanılır:

- **Birinci Kamera**: Yol şeritlerini tespit etmek için kullanılır. Bu kamera, yolun önünü görüntüleyerek şeritlerin doğru bir şekilde takip edilmesini sağlar.
- **İkinci Kamera**: Trafik işaretlerini algılamak için kullanılır. Bu kamera, trafik işaretlerinin tanımlanmasını ve işaretlere göre aracın yönlendirilmesini sağlar.

### 2. Görüntü İşleme

- **Görüntülerin Alınması ve Kaydedilmesi**: Kameralardan alınan görüntüler `cv2` (OpenCV) kullanılarak işlenir ve kaydedilir. Bu görüntüler, şerit tespiti ve trafik işareti algılama işlemleri için kullanılır.

### 3. Şerit Tespiti

- **Şerit Tespiti Fonksiyonu**: `line.py` dosyasından içe aktarılan `main()` fonksiyonu, birincil kameradan alınan görüntüde yol şeritlerini tespit eder. Bu fonksiyon, yolun şeritlerini doğru bir şekilde takip edebilmek için gerekli veriyi sağlar.

### 4. PID Kontrol Algoritması

- **PID Kontrol**: `pid_controller()` fonksiyonu, şerit tespitinden gelen verileri kullanarak aracın direksiyon açısını hesaplar. Bu algoritma, şerit sapmasını en aza indirgemek ve aracın şerit ortasında kalmasını sağlamak için kullanılır. PID (Proportional-Integral-Derivative) algoritması, hatayı, integralini ve türevini değerlendirerek doğru direksiyon açısını belirler.

### 5. Çalışma Döngüsü

- **Ana Döngü**: Araç sürekli olarak aşağıdaki işlemleri gerçekleştirir:
  - Kameradan görüntü alır.
  - Görüntüleri işleyerek şerit tespiti yapar.
  - PID kontrol algoritmasını uygular ve aracın direksiyon açısını ayarlar.
    
Bu yapı, aracın yol şeritlerini doğru bir şekilde takip etmesini ve uygun şekilde yönlendirilmesini sağlar. Kod, Webots simülasyon ortamında gerçek zamanlı olarak çalışacak şekilde tasarlanmıştır.

---

# line.py (Şerit Tespit Algoritması) (Ekleme)

Bu algoritma, görüntü işleme teknikleri kullanarak yol üzerindeki şeritleri tespit etmeyi amaçlar. Yolun alt yarısındaki şerit pikselleri analiz edilerek, sol ve sağ şeritler bulunur ve bu piksellere polinom eğriler uydurularak şerit çizgilerinin eğriliği ve aracın konumu hesaplanır.

## Algoritmanın Adımları

### 1. Görüntü İşleme:
Giriş görüntüsü gri tonlamaya çevrilir ve ardından görüntüdeki gürültüleri azaltmak için genişletme ve erozyon işlemleri uygulanır. Bu sayede, şerit çizgileri daha net bir şekilde ortaya çıkarılır.

### 2. Histogram Analizi:
Görüntünün alt yarısında, şerit çizgilerini tespit etmek için piksel yoğunlukları analiz edilir. Histogram verileri, sol ve sağ şeritlerin başlangıç noktalarını belirlemek için kullanılır.

### 3. Kayan Pencere Yöntemi:
Algoritma, şerit piksellerini tespit etmek için dikey olarak kayan pencereler kullanır. Bu pencerelerle sol ve sağ şeritlerdeki pikseller taranır ve bu piksellerin koordinatları kaydedilir.

### 4. Polinom Uydurma:
Tespit edilen şerit piksellerine ikinci derece bir polinom eğrisi uydurulur. Bu eğri, şerit çizgilerinin geometrik yapısını anlamak ve izlemek için kullanılır.

### 5. Eğrilik Hesaplama:
Uydurulan polinom eğrilerine dayanarak, şeritlerin eğrilik yarıçapı hesaplanır. Ayrıca, aracın şerit ortasına göre pozisyonu belirlenir ve aracın yol üzerindeki hizası hakkında bilgi sağlanır.

Bu algoritma, gerçek zamanlı olarak şerit takibi ve araç hizalama sistemlerinde kullanılabilir.

---

https://github.com/user-attachments/assets/c2809628-b58f-4afc-876c-97b30633844d

---
