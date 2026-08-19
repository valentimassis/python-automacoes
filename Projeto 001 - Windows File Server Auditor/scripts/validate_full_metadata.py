from wfsa.collectors.file_metadata import get_file_metadata


SERVER = "lst-fs01"
PATH = r"E:\Shares\Financeiro"


print("Iniciando validação completa...")
print()

count = 0
total_size = 0

for item in get_file_metadata(SERVER, PATH):
    count += 1
    total_size += item.size

    if count % 50_000 == 0:
        print(
            f"Processados: {count:,} | "
            f"Tamanho: {total_size:,} bytes"
        )

print()
print("========================================")
print("VALIDAÇÃO COMPLETA")
print("========================================")
print(f"Arquivos processados: {count:,}")
print(f"Tamanho total: {total_size:,} bytes")
print("Nenhum erro de transporte/parsing.")
print("========================================")