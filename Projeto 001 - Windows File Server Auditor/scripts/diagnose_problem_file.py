from wfsa.collectors.file_metadata import get_file_metadata


SERVER = "lst-fs01"
PATH = r"E:\Shares\Financeiro"


print("Procurando arquivos relacionados...")
print()

count = 0
found = 0

for item in get_file_metadata(SERVER, PATH):
    count += 1

    if "2021-Termo" in item.name or "Celular" in item.name:
        found += 1

        print("========================================")
        print(f"Registro: {count}")
        print(f"Name: {item.name}")
        print(f"Name repr: {item.name!r}")
        print(f"Path: {item.path}")
        print(f"Path repr: {item.path!r}")
        print(f"Tamanho: {item.size}")
        print("========================================")
        print()

        if found >= 10:
            break

print()
print(f"Registros percorridos: {count}")
print(f"Arquivos relacionados encontrados: {found}")