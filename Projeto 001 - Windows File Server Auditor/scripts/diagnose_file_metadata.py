from itertools import islice

from wfsa.collectors.file_metadata import get_file_metadata


SERVER = "lst-fs01"
PATH = r"E:\Shares\Financeiro"


print("Iniciando teste...")
print()

count = 0

for item in islice(
    get_file_metadata(SERVER, PATH),
    100,
):
    count += 1

    print(f"[{count}]")
    print(f"Name: {item.name}")
    print(f"Path: {item.path}")
    print(f"Extension: {item.extension}")
    print(f"Size: {item.size}")
    print(f"Creation: {item.creation_time}")
    print(f"Last Write: {item.last_write_time}")
    print(f"Last Access: {item.last_access_time}")
    print()

print("================================")
print(f"Arquivos processados: {count}")
print("================================")