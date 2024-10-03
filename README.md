# Self Driving Car

***Proje geliştirilmeye devam ediyor.***

# Gereksinimler

weboots == R2023b

opencv==4.10.0.84

scipy==1.14.1

[YoloV4 dosyaları](https://drive.google.com/drive/folders/12GEDLy-Ujzgo5AEnpvfesSiQYkwWzi02?usp=sharing)

---

# 3 Ekim 2024 (Eklemeler ve Güncellemeler)

## Eklenenler

### Durak algoritamsı:

Teknofest'teki görevlerden biri, otonom aracın durak tabelasını gördüğünde durak cebine girip belirli bir süre beklemesi ve ardından yola devam etmesidir. Bu görevi gerçekleştirmek için birkaç farklı algoritma geliştirdim.

İlk olarak, park algoritmasında kullandığım şerit tespit algoritması ile durak cebinin şeritlerinin orta noktasını bulup aracı bu noktaya yönlendirmeyi planladım. Ancak bu yöntem tam olarak istediğim stabiliteyi sağlayamadı. Bazen şerit tespiti kayboluyor veya şeritlerin kaymasından dolayı araç ani dönüşler yapıyordu, bu da görevin başarısız olmasına yol açıyordu.

Daha sonra, kameranın en solundaki şeridi sürekli takip eden bir algoritma denedim, ancak bu da istediğim başarıyı getirmedi. Sonunda geliştirdiğim üçüncü algoritma ile istediğim başarıyı elde ettim. Bu algoritma, durak tabelası tespit edildiğinde direksiyon açısını sabit tutarak aracın düz bir şekilde ilerlemesini sağlıyor. Araç ilerlerken, şerit tespiti için kullanılan kameradan gelen veriler ile mavi alan araması yapılıyor.

Mavi alan araması için görüntü işleme teknikleri kullanılıyor. Önce, `inRange` fonksiyonu ile mavi alan maskelemesi yapılıyor. Ardından, `findContours` ile maskede beyaz noktaların koordinatları bulunuyor. Bu koordinatlar, mavi alanın yerini gösteriyor. Araç, mavi alanı bulana kadar düz bir şekilde ilerliyor ve alan bulunduğunda, bu alanın orta noktası alınıyor.

Bu orta noktanın x koordinatı, pozisyon değerini hesaplamak için kullanılıyor. Formül şu şekilde:

```python
pos = (540 - center_x) * 0.00513888888
```

Bu formül, kameranın orta noktası ile tespit edilen mavi alanın x koordinatının farkını ve webots simülasyonunda piksel uzunluğunun metreye oranını kullanarak hesaplanıyor. Bu pos değeri, PID algoritmasına veriliyor ve çıkan sonuç direksiyon açısı olarak kullanılıyor.


Aracın durak cebinde olduğunu belirlemek için şu formülü kullanıyorum:

```python
np.sum(mask == 255) / (img.shape[0] * img.shape[1])
```

Bu formül, maskede 255 değeri ile gösterilen beyaz piksellerin ekran oranını hesaplıyor. Eğer bu oran 0.56’dan büyükse, araç durak cebinin içinde kabul ediliyor. Araç 10 saniye boyunca durduktan sonra, önceden belirlenmiş bir hareket planı ile durak cebinden çıkıp yola devam ediyor.

Bu yöntem, görevde istenen stabiliteyi sağlamada başarılı oldu.

## Güncellemeler.

Main.py dosyasındaki durak algoritmasını sağlamak için bazı güncellemeler yapıldı. 

Öncelikle durak tabelası tespit edilip kontrol edilir ve eğer tabela bir durak tabelasıysa, durak algoritması devreye girer ve şerit tespit için kullanılan kamera göreslleri durak algoritmasına aktarılıyor. Durak algoritmasından gelen veriler PID algoritmasına gönderilir ve çıkan değer direksiyon açısı olarak ayarlanır. Ardından, aracın durak cebinin içinde olup olmadığı kontrol edilir. Eğer araç cebin içindeyse, 10 saniye boyunca bekler. Bekleme süresi dolduğunda, önceden belirlenmiş hareketler ile araç cebin dışına çıkar. Son olarak, durak algoritması devre dışı bırakılır ve araç yoluna devam eder.

https://github.com/user-attachments/assets/3796ba41-0a23-4283-8fb9-9ec3148ce33c

---
# 17 Eylül 2024 (Eklemeler ve Güncellemeler)

## Eklenenler

### Şerit değiştirme algoritması:


Engel çıkması veya gerekli durumlarda aracın karşı şeride geçebilmesi gerekmektedir. Bu şerit değişimini sağlamak için kamera kullanılmıştır. Genellikle engel tespiti gibi durumlarda LIDAR tercih edilse de, özellikle Tesla gibi otonom sürüş özelliklerine sahip elektrikli araç satan büyük firmalar, maliyetleri düşürmek için LIDAR sensörlerini çıkarmakta ve genel olarak kamera ve mesafe sensörleri kullanmaktadır. Bu projede de benzer bir yaklaşım izleyerek, LIDAR sensörü eklemenin mantıklı olmadığını düşündüm. Bunun yerine, kameradan gelen verileri YOLOv4 ile eğittiğim modele vererek engel tespitini gerçekleştirmeyi planlıyorum.

Şerit değiştirme, kameradan gelen görsel verilerle algılanacak. Şerit değiştirmenin gerektiği durumlarda, örneğin videoda girilmez tabelasının tespit edilmesiyle bu işlem başlatılacak. Tespit edilen nesnenin kameranın hangi yönünde olduğuna bağlı olarak şerit değiştirme işlemi yapılacak. Örneğin, engel kameranın solundaysa araç sağa, sağındaysa sola geçecek(Şerit tespiti kısmında, şerit koordinatları alınarak, şerit bilgilerine göre sağ veya sol şerit belirlemesi de yapılabilir.). Bu geçiş işlemi sırasında, aracın önce direksiyonu sabit bir açıyla belli bir süre döndürülüp, ardından tam tersi açıya geçilerek şerit değiştirilmiş olacak. Bu işlem tamamlandıktan sonra, aracın şerit tespit ve takip sistemi devreye girecek ve yeni şeritte aracı ortalayacak. Şerit takip, başka bir işlem gerektiğinde devre dışı kalana kadar devam edecek.



https://github.com/user-attachments/assets/a90081f1-d1e7-478b-adcc-0c72c80e530e

---
### Park algoritması:

Park etme aşamasında, araç park tabelasını görene kadar "kör ilerleyiş" olarak adlandırılan, önceden tanımlanmış bir sürüş gerçekleştirecektir. Bu süreçte, YOLOv4 ile eğitilmiş modele sürekli olarak kamera görüntüleri aktarılacak ve model park tabelasını tespit etmeye çalışacaktır. Park tabelası tespit edildiğinde, sistemin kararlılığını korumak adına birden fazla tabela tespit edilme olasılığı göz önünde bulundurulacaktır. Bu durumda, kamera merkezine en yakın olan tabela ve park alanı esas alınacaktır. Ardından HoughLinesP ile geliştirilen şerit tespit algoritması devreye girecektir.

Bu noktada ana şerit tespit algoritması kullanılmayacaktır. Bunun nedeni, ana algoritmanın histogram yöntemini kullanarak görüntüdeki en yoğun piksel bölgelerini şerit olarak algılamasıdır. Bu yöntem, park alanlarındaki istenilen şeritleri doğru şekilde algılayamayabilir. Çünkü park alanında birden fazla şerit bulunur ve sadece "park edilebilir" tabelasının olduğu şeritler algılanmalı ve takip edilmelidir. Bu nedenle, park alanlarındaki şeritler için HoughLinesP kullanılarak özel bir şerit tespit algoritması geliştirilmiştir.

Geliştirilen şerit tespit algoritması, park tabelasının x koordinatına en yakın sol ve sağ şeritleri belirler. Tabelanın hemen solunda ve sağında yer alan bu iki şerit, aracın park edebileceği alanı tanımlar. Algoritma, bu iki şeridin orta noktasını hesaplayarak aracı bu bölgeye yönlendirir. Hesaplama orta nokta bu formülle verilir: 

(((line_center / (cam_width / 2)) - 1) * -1) 

Bu forlüm sonucunda elde edilen değer, PID kontrol sistemine iletilir ve aracın direksiyon açısı buna göre ayarlanır.

 Sistem şu an tam olarak stabil olmasa da, ilerleyen zamanlarda yapılacak iyileştirmelerle daha kararlı ve güvenilir hale getirilmesi planlanmaktadır.


https://github.com/user-attachments/assets/98a1f074-7a3d-4bde-9d32-81b64f40e523

---

### Kırmızı ışıkta durma

Yolo modelini eğitmek için kullanılan veri setinde trafik ışık görselleri eklendi, bu sayede aracın kırmızı ışıkta durması salanacak. Kameradan gelen görselde, kırmızı işık tespit edilirse araç belli bir süre boyunca hızını kesecek ve süre bitince eski hızı ile ilerlemeye devam edecek. 

https://github.com/user-attachments/assets/328c157a-2127-43dd-b30e-6ebad8208eec

---

## Geliştirmeler.

10 Eylül'de eklenen YOLOv4 modeli, yeterince iyi eğitilmediği için yanlış tespitler yapıyordu ve bu durum, sistemin stabilitesini ve güvenilirliğini olumsuz etkiliyordu. Bu aşamada, elimdeki görsellerle modeli eğitmeye devam ettim. Her ne kadar model hala istediğim doğruluk seviyesine ulaşmamış olsa da, önceki duruma kıyasla çok daha doğru ve hassas tespitler yapıyor. Bu da sistemin güvenilirliğini ve stabilitesini artırıyor.

---
# 10 Eylül 2024 (Eklemeler ve Güncellemeler)

## main.py Ana Kod (Güncellemeler)

Main koduna, trafik tabelalarını ve işaretlerini tespit etmek için YOLOv4 ile eğitilmiş bir model entegre edilmiştir. Bu modelin veri seti, [TTVS veri seti](https://github.com/ituracingdriverless/TTVS) içindeki verilerden alınmıştır, ancak model tam olarak eğitilmediği için doğruluk oranı yüksek değildir. Ayrıca, dönüş işlemlerini gerçekleştirmek için `dönüş.py` kodu eklenmiştir. Bu kod, aracın sola, sağa ve ileri doğru dönüşlerini başarılı bir şekilde, ancak tam olarak stabil olmayan bir şekilde yapabilmesini sağlar.

[YoloV4 dosyaları](https://drive.google.com/drive/folders/12GEDLy-Ujzgo5AEnpvfesSiQYkwWzi02?usp=sharing)

### Genel Yapı

1. **Mesafe Kontrolü (`is_close`)**

   YOLOv4 ile görselden nesne tespiti yaparken aynı nesneyi birden fazla kez tespit etmesini engellemek için bu fonksiyon eklenmiştir. Bu fonksiyon, tespit edilen iki nesnenin merkezlerini karşılaştırarak, aralarındaki mesafe belirli bir değerin altında olduğunda aynı nesne olarak değerlendirilmesini sağlar.

2. **Trafik İşareti Tespiti ve Filtreleme (`get_detected_labels_with_area_filter`)**

   YOLOv4 modeli, ikinci kameradan gelen görüntüler ile belirli bir süre (kodda 2 saniyede bir olarak ayarlandı) içinde nesne tespiti yapar. Bu süre sınırı, kaynakların sürekli olarak kullanılmasını önlemek içindir. Model, TTVS veri setinden alınan 3000 görsel üzerinde eğitilmiştir, ancak eğitim tam olarak tamamlanmadığı için doğruluk oranı yüksek değildir. Tabela tespiti dönüş algoritması için kullanıldığından, tespit edilen nesnelerin bir alan ölçeği eklenmiştir; bu sayede küçük alanlı nesneler dönüş algoritması tarafından dikkate alınmaz.

### dönüş.py Dönüş Algoritması (Ekleme)

Aracın trafik işaretlerine göre yönlendirilmesi için PID kontrol algoritması kullanılmıştır. PID algoritmasının kullanımı, dönüşlerin daha düzgün ve genel yapının daha stabil olmasını sağlamaktadır. Tabela tespiti gerçekleştiğinde `dönüş.py` modülündeki `start()` fonksiyonu çalışır. Bu fonksiyon, ilk olarak tespit edilen tabelaya göre yapılması gereken eylemi belirler. Şimdilik sağa, sola ve ileri gitme eylemleri eklenmiştir. Daha sonra, araç belirli bir süre düz gider ve ardından işarete göre düz, sola veya sağa dönüş başlar. Hedef direksiyon açısı belirlenir ve PID algoritması aracın direksiyon açısını hesaplayarak ayarlar. Dönüş tamamlandığında, direksiyon açısı sıfırlanır. Sol veya sağ dönüşlerde, dönüş sonrası şerit tekrar tespit edilebilmesi için araç belirli bir süre boyunca düz gitmeye devam eder. Kod, aracın şerit tespit ve takibine devam etmesiyle sonlanır.

> [!NOTE]
> Kullanılan YOLOv4 modelinin eğitiminin tamamlanmamış olması nedeniyle doğruluğun düşük olması ve dönüş algoritmasının hala istenilen stabiliteye ulaşamaması sebebiyle yapı tam olarak stabil değil.
>

---

https://github.com/user-attachments/assets/30a03da8-7f35-4071-8cfa-f2636c6b6632

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
