import secrets


def generate_pin() -> str:
    """
    產生一組六碼數字字串（不包含 0），範例：'483156'
    """
    digits = "123456789"  # 不含 0
    return "".join(secrets.choice(digits) for _ in range(6))
