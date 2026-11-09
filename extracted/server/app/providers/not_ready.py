def not_installed(kind: str):
    raise NotImplementedError(
        f"{kind} model worker is not installed yet. The API route is reserved, "
        "but no generation will be claimed until a real local model runtime is configured."
    )
