from collections import Counter
from itertools import islice

from wfsa.collectors.file_metadata import get_file_metadata


SERVER = "lst-fs01"
PATH = r"E:\Shares\Financeiro"

LIMIT = 250_000


print("Iniciando teste de integridade...")
print(f"Limite: {LIMIT:,} arquivos")
print()

count = 0
total_size = 0
extensions = Counter()

target_name = (
    "2021-Termo de Autorização de Computador, "
    "Dispositivo móvel e Número de Celular”.pdf"
)

target_count = 0

for item in islice(
    get_file_metadata(SERVER, PATH),
    LIMIT,
):
    count += 1

    total_size += item.size

    extensions[item.extension.lower()] += 1

    if item.name == target_name:
        target_count += 1

        print(
            f"Arquivo especial encontrado: "
            f"{count:,} → {item.path}"
        )

print()
print("========================================")
print("RESULTADO")
print("========================================")
print(f"Arquivos processados : {count:,}")
print(f"Tamanho total        : {total_size:,} bytes")
print(f"Arquivos especiais   : {target_count}")
print()
print("Principais extensões:")

for extension, quantity in extensions.most_common(15):
    print(f"  {extension or '[sem extensão]'}: {quantity:,}")

print("========================================")