class DomainError(Exception):
    """Errores de negocio / dominio."""


class ValidationError(DomainError):
    pass


class ConflictError(DomainError):
    pass


class InfrastructureError(Exception):
    """Errores de infraestructura (DB caída, etc.)."""
