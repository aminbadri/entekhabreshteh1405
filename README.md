# راهنمای انتخاب رشته ۱۴۰۵ — داده‌محور

سامانه استاتیک برای تحلیل انتخاب رشته با دو خانواده منبع:
- راهنمای انتخاب رشته JobVision 1405
- داده‌های انتخاب رشته 1404 پروژه مرجع Sanjesh1404

## اصل کلیدی
هیچ داده ساختگی، تخمینی یا پرکننده در خروجی مجاز نیست.

## معماری انتشار
Vercel فقط پوشه `site/` را به‌صورت Static منتشر می‌کند.
استخراج و بازسازی داده در GitHub Actions انجام می‌شود.

```text
JobVision PDF (263 pages)
        ↓
download_sources.py
        ↓
extract_jobvision.py
        ↓
map_jobvision.py
        ↓
match_sanjesh_jobvision.py
        ↓
validate_data.py
        ↓
site/data/*.json
        ↓
Git commit
        ↓
Vercel auto-deploy
```

## اجرای محلی
```bash
python -m pip install -r requirements-data.txt
python scripts/build_data.py
python scripts/build_pipeline_report.py
python scripts/validate_data.py
python scripts/review_pdf.py
python -m http.server 8000 --directory site
```

## GitHub Actions
Workflow در:
`.github/workflows/data-pipeline.yml`

با `workflow_dispatch` می‌توان آن را دستی اجرا کرد؛ یک اجرای زمان‌بندی‌شده نیز برای بازسازی دوره‌ای تعریف شده است.

در هر اجرا:
1. PDF جاب‌ویژن و داده سنجش از URLهای ثبت‌شده دریافت می‌شوند.
2. هر 263 صفحه PDF استخراج می‌شود.
3. جدول‌ها و صفحاتی که سیگنال استخراج ضعیف دارند در `jobvision_review_queue.csv` ثبت می‌شوند.
4. تطبیق رشته/دانشگاه انجام می‌شود.
5. تطبیق‌های مبهم به‌عنوان `ambiguous` باقی می‌مانند و به‌صورت اجباری match نمی‌شوند.
6. خروجی معتبر در `site/data/` قرار می‌گیرد.
7. فایل‌های تولیدشده در صورت تغییر commit می‌شوند.
8. Vercel پس از push، سایت را دوباره Deploy می‌کند.

## کنترل بصری
Workflow علاوه بر فایل صف بررسی، contact sheet صفحات PDF را به‌صورت GitHub Actions Artifact منتشر می‌کند تا صفحات نیازمند کنترل انسانی قابل مشاهده باشند.

## Vercel
`vercel.json` عمداً بدون Build Command و Install Command است:

```json
{
  "outputDirectory": "site",
  "cleanUrls": true
}
```

بنابراین Vercel نباید `pip install` یا Python ETL اجرا کند.

## منابع
- JobVision: https://fileapi.jobvision.ir/public-files/reports/jobvision-education-field-selection-guide-1405.pdf
- Sanjesh1404: https://github.com/Hhhkarimi/sanjesh1404
