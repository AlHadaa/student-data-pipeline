# مشروع هندسة بيانات الطلاب - ETL ودمج مصادر البيانات

## 1. نظرة عامة على المشروع

يهدف هذا المشروع إلى بناء خط أنابيب ETL ودمج بيانات الطلاب من عدة مصادر مختلفة، ثم التحقق من جودة البيانات وتنظيفها وتحويلها ودمجها وإنتاج Dataset نهائي منظم.

مصادر البيانات المستخدمة:

1. CSV
2. REST API
3. SQLite
4. MongoDB

الهدف الرئيسي هو تطبيق دورة معالجة بيانات منظمة وقابلة لإعادة الاستخدام.

### مراحل خط الأنابيب

```text
Extract
   ↓
Validate
   ↓
Clean
   ↓
Integrate
   ↓
Transform
   ↓
Final Validation
   ↓
Load
```

يتم حفظ السجلات الصحيحة في:

```text
data/processed/final_dataset.csv
```

ويتم حفظ السجلات المرفوضة في:

```text
data/rejected/rejected_records.csv
```

---

## 2. معمارية المشروع

```text
                 ┌──────────────┐
                 │     CSV      │
                 └──────┬───────┘
                        │
                 ┌──────▼───────┐
                 │   REST API   │
                 └──────┬───────┘
                        │
                 ┌──────▼───────┐
                 │    SQLite    │
                 └──────┬───────┘
                        │
                 ┌──────▼───────┐
                 │   MongoDB    │
                 └──────┬───────┘
                        │
                        ▼
                     Extract
                        │
                        ▼
                Clean & Validate
                        │
                        ▼
                    Integrate
                        │
                        ▼
                   Transform
                        │
                        ▼
                Final Validation
                    /       \
                   /         \
                  ▼           ▼
        final_dataset.csv   rejected_records.csv
```

المفتاح المشترك المستخدم لربط بيانات الطالب بين المصادر المختلفة هو:

```text
student_id
```

---

# 3. مصادر البيانات

## 3.1 ملف CSV

الموقع:

```text
data/raw/students.csv
```

يحتوي الملف على البيانات الأساسية للطلاب:

- `student_id`
- `student_name`
- `age`
- `major`
- `city`

---

## 3.2 REST API

المصدر الخارجي المستخدم:

```text
https://dummyjson.com/users?limit=100
```

يتم الاتصال بالـ API باستخدام مكتبة `requests` في Python.

يتم استخدام معرف المستخدم كـ `student_id` لربط بيانات الـ API ببيانات الطلاب.

يقوم جزء استخراج الـ API بتجهيز الحقول التالية لاستخدامها في عملية التكامل:

- `student_id`
- `gpa`
- `attendance`
- `status`

> الحقول الأكاديمية المطلوبة للمشروع يتم تجهيزها أثناء مرحلة استخراج بيانات الـ API، ولا ينبغي اعتبارها سجلات أكاديمية رسمية مقدمة من خدمة الـ API الخارجية.

---

## 3.3 قاعدة بيانات SQLite

قاعدة البيانات:

```text
database/students.db
```

وتحتوي على:

- `courses`
- `enrollments`

وتوفر معلومات إضافية مثل:

- `average_score`
- `courses_count`

ويتم ربط البيانات باستخدام:

```text
student_id
```

---

## 3.4 قاعدة بيانات MongoDB

اسم قاعدة البيانات:

```text
student_pipeline
```

اسم Collection:

```text
student_extra
```

توفر MongoDB معلومات إضافية مثل:

- `scholarship_status`
- `projects_count`

ويتم الربط باستخدام:

```text
student_id
```

---

# 4. مراحل ETL

## 4.1 Extract - الاستخراج

يتم استخراج البيانات من المصادر الأربعة:

- CSV
- REST API
- SQLite
- MongoDB

ولكل مصدر وحدة استخراج مستقلة داخل:

```text
app/sources/
```

يساعد هذا التصميم على فصل مسؤوليات المصادر وتسهيل اختبارها وتطويرها.

---

## 4.2 Validate - التحقق

يتم التحقق من جودة البيانات باستخدام مجموعة من القواعد.

القواعد الأساسية:

- يجب ألا يكون `student_id` فارغًا.
- العمر بين 16 و80.
- GPA بين 0 و4.
- الحضور بين 0 و100.
- الدرجة بين 0 و100.

إذا فشل السجل في إحدى قواعد التحقق، يتم رفضه وتسجيل سبب الرفض.

---

## 4.3 Clean - التنظيف

تتعامل مرحلة التنظيف مع مشاكل جودة البيانات مثل:

- السجلات المكررة.
- القيم المفقودة.
- اختلاف تنسيق النصوص.
- القيم غير الصالحة.
- تحويل أنواع البيانات.

الهدف هو تجهيز البيانات قبل عملية الدمج.

---

## 4.4 Integrate - الدمج

يتم دمج البيانات القادمة من المصادر المختلفة باستخدام:

```text
student_id
```

وبذلك يمكن جمع معلومات الطالب الموجودة في:

```text
CSV + REST API + SQLite + MongoDB
```

في سجل طالب واحد.

---

## 4.5 Transform - التحويل

يتم إنشاء أعمدة مشتقة تساعد في تحليل البيانات.

### performance_level

يتم تحديد مستوى الأداء حسب الدرجة:

| الدرجة | المستوى |
|---:|---|
| >= 90 | Excellent |
| >= 80 | Very Good |
| >= 70 | Good |
| >= 60 | Acceptable |
| < 60 | At Risk |

### attendance_status

يتم تصنيف الحضور كالتالي:

| الحضور | الحالة |
|---:|---|
| >= 75 | Good |
| < 75 | Low |

---

## 4.6 Final Validation - التحقق النهائي

بعد الدمج والتحويل، يتم التحقق من البيانات النهائية مرة أخرى.

السجلات الصحيحة تحفظ في:

```text
data/processed/final_dataset.csv
```

والسجلات المرفوضة تحفظ في:

```text
data/rejected/rejected_records.csv
```

وبذلك لا تظهر السجلات المرفوضة داخل Dataset النهائي.

---

# 5. جودة البيانات

يطبق المشروع مجموعة من قواعد جودة البيانات.

### معرف الطالب

يجب أن يكون `student_id` موجودًا حتى يمكن ربط السجلات بين المصادر.

### العمر

النطاق المقبول:

```text
16 <= age <= 80
```

### GPA

النطاق المقبول:

```text
0 <= gpa <= 4
```

### الحضور

النطاق المقبول:

```text
0 <= attendance <= 100
```

### الدرجة

النطاق المقبول:

```text
0 <= score <= 100
```

### السجلات المكررة

يتم التعامل مع التكرارات باستخدام `student_id`.

### السجلات غير الصالحة

يتم فصل السجلات غير الصالحة عن البيانات النهائية وحفظها في:

```text
data/rejected/rejected_records.csv
```

مع تسجيل سبب الرفض.

---

# 6. التعامل مع القيم المفقودة

يستخدم المشروع قواعد بسيطة وواضحة للتعامل مع القيم المفقودة.

أمثلة:

- العمر المفقود يمكن معالجته باستخدام Median.
- متوسط الدرجات المفقود يعالج بالقيمة `0`.
- عدد المقررات المفقود يعالج بالقيمة `0`.

---

# 7. Dataset النهائي

يحتوي الملف النهائي على البيانات المدمجة، ومن أهم الحقول:

```text
student_id
student_name
age
major
city
gpa
attendance
status
average_score
courses_count
scholarship_status
projects_count
performance_level
attendance_status
```

الملف النهائي:

```text
data/processed/final_dataset.csv
```

---

# 8. هيكل المشروع

```text
student_data_pipeline/
│
├── app/
│   ├── sources/
│   │   ├── csv_source.py
│   │   ├── api_source.py
│   │   ├── database_source.py
│   │   └── mongo_source.py
│   │
│   ├── transformation/
│   │   ├── cleaner.py
│   │   ├── integration.py
│   │   └── transformer.py
│   │
│   ├── validation/
│   │   └── quality.py
│   │
│   ├── output/
│   │   └── csv_writer.py
│   │
│   └── utils/
│       └── logger.py
│
├── data/
│   ├── raw/
│   │   └── students.csv
│   ├── processed/
│   │   └── final_dataset.csv
│   └── rejected/
│       └── rejected_records.csv
│
├── database/
│   ├── create_sqlite.py
│   └── seed_mongo.py
│
├── tests/
│   └── test_pipeline.py
│
├── logs/
│   └── pipeline.log
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 9. التقنيات المستخدمة

- Python
- Pandas
- Requests
- SQLite
- MongoDB
- PyMongo
- Pytest

---

# 10. التثبيت

تثبيت المكتبات المطلوبة:

```bash
pip install -r requirements.txt
```

يفضل استخدام Python Virtual Environment.

---

# 11. تجهيز قواعد البيانات

## SQLite

إنشاء وتجهيز قاعدة بيانات SQLite:

```bash
python database/create_sqlite.py
```

## MongoDB

يجب التأكد من تشغيل MongoDB محليًا، ثم تشغيل:

```bash
python database/seed_mongo.py
```

---

# 12. تشغيل Pipeline

لتشغيل خط الأنابيب بالكامل:

```bash
python main.py
```

مثال على التشغيل الناجح:

```text
Pipeline completed successfully.
Valid records: 6
Rejected records: 2
Output: data/processed/final_dataset.csv
Rejected: data/rejected/rejected_records.csv
```

---

# 13. الاختبارات

لتشغيل الاختبارات:

```bash
pytest
```

تغطي الاختبارات عمليات مهمة مثل:

- تحميل CSV.
- الاتصال بالـ API.
- استخراج بيانات SQLite.
- التعامل مع التكرارات.
- التعامل مع القيم المفقودة.
- رفض البيانات غير الصالحة.
- دمج المصادر.
- إنشاء ملف CSV النهائي.

---

# 14. Logging

يتم تسجيل معلومات تشغيل الـ Pipeline في:

```text
logs/pipeline.log
```

يساعد ملف السجل في متابعة التنفيذ وتشخيص المشكلات.

يتم استثناء ملفات السجل من Git باستخدام `.gitignore`.

---

# 15. لماذا نستخدم Data Pipeline؟

يساعد Data Pipeline على توفير طريقة منظمة وقابلة لإعادة الاستخدام من أجل:

- جمع البيانات من مصادر متعددة.
- التحقق من جودة البيانات.
- تنظيف البيانات غير المتناسقة.
- دمج البيانات المرتبطة.
- تحويل البيانات إلى معلومات مفيدة.
- إنتاج Dataset نهائي موحد.

كما أن فصل مراحل الاستخراج والتحويل والتحقق والإخراج يجعل المشروع أسهل في الاختبار والصيانة.

---

# 16. Raw و Processed

## Raw Data

تمثل البيانات الأصلية قبل تنفيذ عمليات المعالجة الرئيسية.

مثال:

```text
data/raw/students.csv
```

## Processed Data

تمثل البيانات بعد التنظيف والتحقق والدمج والتحويل.

مثال:

```text
data/processed/final_dataset.csv
```

---

# 17. السجلات المرفوضة

السجلات التي تفشل في قواعد التحقق لا تدخل إلى Dataset النهائي.

بدلًا من ذلك يتم حفظها في:

```text
data/rejected/rejected_records.csv
```

ويحتوي الملف على معرف الطالب وسبب الرفض.

يساعد ذلك في تتبع السجلات غير الصالحة ومعرفة سبب استبعادها.

---

# 18. التطوير المستقبلي

يمكن تطوير المشروع مستقبلًا من خلال:

- إضافة REST APIs أخرى.
- دعم MySQL أو PostgreSQL.
- معالجة البيانات الكبيرة باستخدام Batch Processing.
- جدولة تشغيل الـ Pipeline.
- استخدام أدوات Workflow Orchestration مثل Apache Airflow.
- إضافة قواعد أكثر لفحص جودة البيانات.
- توسيع اختبارات Unit وIntegration.

---

# 19. الخلاصة

يوضح هذا المشروع كيفية بناء ETL وData Integration Pipeline باستخدام عدة مصادر للبيانات.

يقوم المشروع باستخراج البيانات من CSV وREST API وSQLite وMongoDB، ثم يتحقق من صحتها وينظفها ويدمجها باستخدام `student_id`، وينشئ الحقول المشتقة، ويجري التحقق النهائي، ثم ينتج Dataset نهائيًا منظمًا.

تم تقسيم المشروع إلى وحدات مستقلة للاستخراج والتحويل والتحقق والإخراج، مما يجعله أسهل في الفهم والاختبار والتطوير.
