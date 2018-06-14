from uuid import UUID


def is_uuid(string, version=4):
    try:
        UUID(string, version=version)
        return True
    except ValueError:
        return False
