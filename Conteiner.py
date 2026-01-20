import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ==========================================
# 1. VERİ YÜKLEME VE ÖN HAZIRLIK
# ==========================================
print("Veri yükleniyor...")
df = pd.read_csv('Smart_Bin.csv')

# Eksik Verileri (NaN) Temizleme
# Sayısal sütunlardaki boşlukları ortalama ile dolduruyoruz
numeric_cols = df.select_dtypes(include=['number']).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
print("Eksik veriler temizlendi.")

# ==========================================
# 2. GENİŞLETİLMİŞ KEŞİFSEL VERİ ANALİZİ (EDA)
# ==========================================
print("\nGrafikler hazırlanıyor...")
sns.set(style="whitegrid")

# Grafik 1: Hedef Değişken Dağılımı (Dengeli mi?)
plt.figure(figsize=(8, 5))
sns.countplot(x='Class', data=df, palette='viridis')
plt.title('Sınıf Dağılımı: Boşalt (Emptying) vs Boşaltma (Non Emptying)')
plt.show()

# Grafik 2: Doluluk Seviyesi Dağılımı (Histogram)
plt.figure(figsize=(10, 6))
sns.histplot(df['FL_B'], bins=30, kde=True, color='blue')
plt.title('Genel Doluluk Seviyesi Dağılımı (FL_B)')
plt.xlabel('Doluluk Oranı (%)')
plt.show()

# Grafik 3: Konteyner Tipine Göre Doluluk (Boxplot)
plt.figure(figsize=(14, 6))
sns.boxplot(x='Container Type', y='FL_B', data=df, palette='Set2')
plt.xticks(rotation=45)
plt.title('Hangi Konteyner Ne Kadar Doluyor?')
plt.show()

# Grafik 4: Atık Türüne Göre Doluluk (Boxplot)
plt.figure(figsize=(10, 6))
sns.boxplot(x='Recyclable fraction', y='FL_B', data=df, palette='Set3')
plt.title('Atık Türüne Göre Doluluk Analizi')
plt.show()

# Grafik 5: Korelasyon Matrisi (Isı Haritası)
plt.figure(figsize=(10, 8))
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Sensör Verileri Arasındaki İlişki (Korelasyon)')
plt.show()

# ==========================================
# 3. MODELLEME HAZIRLIĞI
# ==========================================
le = LabelEncoder()
df_model = df.copy()

# Kategorik verileri sayısal hale getirme (Label Encoding)
cat_cols = ['Container Type', 'Recyclable fraction', 'Class']
for col in cat_cols:
    df_model[col] = le.fit_transform(df_model[col].astype(str))

X = df_model.drop('Class', axis=1)
y = df_model['Class']

# Eğitim ve Test Seti Ayrımı (%80 Eğitim, %20 Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# KNN için Normalizasyon (Ölçekleme)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==========================================
# 4. MODELLERİN EĞİTİLMESİ VE KARŞILAŞTIRMA
# ==========================================
print("\nModeller eğitiliyor...")

# Model 1: Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
acc_rf = accuracy_score(y_test, rf.predict(X_test))

# Model 2: Gradient Boosting
gb = GradientBoostingClassifier(random_state=42)
gb.fit(X_train, y_train)
acc_gb = accuracy_score(y_test, gb.predict(X_test))

# Model 3: KNN (K-Nearest Neighbors) - Ölçeklenmiş veri ile
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)
acc_knn = accuracy_score(y_test, knn.predict(X_test_scaled))

# ==========================================
# 5. SONUÇ RAPORU
# ==========================================
print(f"\n🏆 --- MODEL KARŞILAŞTIRMA SONUÇLARI --- 🏆")
print(f"1. Random Forest Doğruluk Oranı : %{acc_rf*100:.2f}")
print(f"2. Gradient Boosting Doğruluk   : %{acc_gb*100:.2f}")
print(f"3. KNN (K-En Yakın Komşu)       : %{acc_knn*100:.2f}")

print("\n--- En İyi Modelin (Random Forest) Detaylı Raporu ---")
print(classification_report(y_test, rf.predict(X_test)))