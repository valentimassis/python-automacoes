def normalize_access_right(access_right: str) -> str:
    """Normaliza nomes de direitos SMB e NTFS para uma representação comum."""

    value = access_right.strip().lower()

    mapping = {
        "full": "FULL",
        "fullcontrol": "FULL",
        "modify": "MODIFY",
        "read": "READ",
        "write": "WRITE",
        "readandexecute": "READ_EXECUTE",
    }

    return mapping.get(value, value.upper())


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
        raise ValueError(f"Direito SMB não suportado: {smb_right}")

    if ntfs not in access_levels:
        raise ValueError(f"Direito NTFS não suportado: {ntfs_right}")

    return smb if access_levels[smb] <= access_levels[ntfs] else ntfs
