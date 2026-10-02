from pathlib import Path
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/raw"

SOURCES = {
    "jobvision.pdf": "https://fileapi.jobvision.ir/public-files/reports/jobvision-education-field-selection-guide-1405.pdf",
    "sanjesh_records.ndjson.gz": "https://raw.githubusercontent.com/Hhhkarimi/sanjesh1404/main/site/data/records.ndjson.gz",
    "sanjesh_summary.json": "https://raw.githubusercontent.com/Hhhkarimi/sanjesh1404/main/site/data/summary.json",
    "sanjesh_capacity.csv.gz": "https://raw.githubusercontent.com/Hhhkarimi/sanjesh1404/main/site/data/sanjesh_1404_all_degrees_capacity_detailed.csv.gz",
}

session = requests.Session()
retry = Retry(
    total=4,
    connect=4,
    read=4,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)
session.mount("https://", HTTPAdapter(max_retries=retry))
session.headers.update({"User-Agent": "entekhabreshte1405-data-pipeline/1.0"})

for name, url in SOURCES.items():
    target = OUT / ("jobvision/" + name if name == "jobvision.pdf" else "sanjesh/" + name)
    target.parent.mkdir(parents=True, exist_ok=True)
    print("GET", url)
    with session.get(url, timeout=(30, 300), stream=True) as r:
        r.raise_for_status()
        with target.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
    print("WROTE", target, target.stat().st_size, "bytes")
