def normalize_access_right(access_right: str) -> str:
    """Normaliza nomes de direitos SMB e NTFS."""

    value = access_right.strip().lower()

    # O SMB retorna valores simples como:
    # Full, Change, Read
    smb_mapping = {
        "full": "FULL",
        "change": "MODIFY",
        "read": "READ",
    }

    if value in smb_mapping:
        return smb_mapping[value]

    # O NTFS pode retornar combinações como:
    # ReadAndExecute, Synchronize
    # Modify, Synchronize
    # FullControl
    parts = {
        part.strip()
        for part in value.split(",")
        if part.strip()
    }

    if "fullcontrol" in parts:
        return "FULL"

    if "modify" in parts:
        return "MODIFY"

    if "readandexecute" in parts:
        return "READ_EXECUTE"

    if "read" in parts:
        return "READ"

    if "write" in parts:
        return "WRITE"

    return value.upper()


def calculate_effective_access(
    smb_right: str,
    ntfs_right: str,
) -> str:
    """Calcula o menor nível de acesso entre SMB e NTFS."""

    smb = normalize_access_right(smb_right)
    ntfs = normalize_access_right(ntfs_right)

    access_levels = {
        "READ": 1,
        "READ_EXECUTE": 2,
        "WRITE": 2,
        "MODIFY": 3,
        "FULL": 4,
    }

    if smb not in access_levels:
        raise ValueError(
            f"Direito SMB não suportado: {smb_right}"
        )

    if ntfs not in access_levels:
        raise ValueError(
            f"Direito NTFS não suportado: {ntfs_right}"
        )

    return (
        smb
        if access_levels[smb] <= access_levels[ntfs]
        else ntfs
    )