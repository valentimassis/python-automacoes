from datetime import datetime

from wfsa.collectors.file_metadata import get_file_metadata
from wfsa.analyzers.file_metadata import analyze_old_files


files = get_file_metadata(
    "lst-fs01",
    r"E:\Shares\Financeiro",
)

findings = analyze_old_files(
    files,
    datetime(2026, 8, 18),
)

count = 0

for finding in findings:
    count += 1

print(f"Total de findings: {count}")
