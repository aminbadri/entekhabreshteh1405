from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def run(script):
    print(f"\n=== RUN {script} ===", flush=True)
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / script)])

if __name__ == "__main__":
    run("download_sources.py")
    run("extract_jobvision.py")
    run("map_jobvision.py")
    run("match_sanjesh_jobvision.py")
