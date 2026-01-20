import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


#  Veri Yükleme 

print("Veri yükleniyor...")
df = pd.read_csv('Smart_Bin.csv')

# Eksik Verileri (NaN) Temizleme
# Sayısal sütunlardaki boşlukları ortalama ile dolduruyoruz
numeric_cols = df.select_dtypes(include=['number']).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
print("Eksik veriler temizlendi.")


#  Veri Analizi 


sns.set(style="whitegrid")
# Pivot Table dönüşümü atık tipine göre doluluk oranlarını analiz etmek için
pivot_table = df.pivot_table(index='Container Type', 
                             columns='Recyclable fraction', 
                             values='FL_B', 
                             aggfunc='mean')

# Atık Türüne ve Konteyner Tipine Göre Doluluk Isı Haritası
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap="YlOrRd", linewidths=.5)
plt.title('Konteyner Tipi ve Atık Türüne Göre Doluluk Analizi')
plt.show()

#  Hedef Değişken Dağılımı 
plt.figure(figsize=(8, 5))
sns.countplot(x='Class', data=df, palette='viridis')
plt.title('Sınıf Dağılımı: Boşalt (Emptying) vs Boşaltma (Non Emptying)')
plt.show()

# Doluluk Seviyesi Dağılımı 
plt.figure(figsize=(10, 6))
sns.histplot(df['FL_B'], bins=30, kde=True, color='blue')
plt.title('Genel Doluluk Seviyesi Dağılımı (FL_B)')
plt.xlabel('Doluluk Oranı (%)')
plt.show()

#  Konteyner Tipine Göre Doluluk 
plt.figure(figsize=(14, 6))
sns.boxplot(x='Container Type', y='FL_B', data=df, palette='Set2')
plt.xticks(rotation=45)
plt.title('Hangi Konteyner Ne Kadar Doluyor?')
plt.show()

# Atık Türüne Göre Doluluk 
plt.figure(figsize=(10, 6))
sns.boxplot(x='Recyclable fraction', y='FL_B', data=df, palette='Set3')
plt.title('Atık Türüne Göre Doluluk Analizi')
plt.show()

#  Korelasyon Matrisi 
plt.figure(figsize=(10, 8))
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Sensör Verileri Arasındaki İlişki (Korelasyon)')
plt.show()


le = LabelEncoder()
df_model = df.copy()

# Kategrorik koloları encode etme
cat_cols = ['Container Type', 'Recyclable fraction', 'Class']
for col in cat_cols:
    df_model[col] = le.fit_transform(df_model[col].astype(str))

X = df_model.drop('Class', axis=1)
y = df_model['Class']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# KNN için Normalizasyon
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
acc_rf = accuracy_score(y_test, rf.predict(X_test))

# Gradient Boosting
gb = GradientBoostingClassifier(random_state=42)
gb.fit(X_train, y_train)
acc_gb = accuracy_score(y_test, gb.predict(X_test))

#  KNN 
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)
acc_knn = accuracy_score(y_test, knn.predict(X_test_scaled))

#  SONUÇ RAPORU
print(f"\n --- MODEL KARŞILAŞTIRMA SONUÇLARI --- ")
print(f"1. Random Forest Doğruluk Oranı : %{acc_rf*100:.2f}")
print(f"2. Gradient Boosting Doğruluk   : %{acc_gb*100:.2f}")
print(f"3. KNN (K-En Yakın Komşu)       : %{acc_knn*100:.2f}")


