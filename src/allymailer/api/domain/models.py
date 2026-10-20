"""Models of the Domain section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, model_of, to_enum

from allymailer.common import VerificationRecordStatus

__all__ = ["DkimStatus", "DomainGetDnsRecordsRequest", "DomainGetDnsRecordsResponse", "DomainValidateVerificationRecordRequest", "DomainValidateVerificationRecordResponse", "DomainValidateDkimRequest", "DomainValidateDkimResponse", "DomainListRequest", "DomainListResponse", "DomainListResponseDomainsItem", "DomainListResponseDomainsItemVerificationRecord", "DomainListResponseDomainsItemDkim", "DomainGetSandboxDomainResponse", "DomainDeleteRequest", "DomainDeleteResponse"]


class DkimStatus(str, Enum):
    """Лише домени зі статусом DKIM-запису "active" можуть використовуватися для надсилання листів."""

    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass
class DomainGetDnsRecordsRequest:
    """DomainGetDnsRecordsRequest"""

    domain: str
    """Домен, для якого потрібно отримати інформацію про DNS-записи."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainGetDnsRecordsRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            domain=data.get("domain"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "domain": self.domain,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainGetDnsRecordsResponse:
    """DomainGetDnsRecordsResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    domain: Optional[str] = None
    """Домен, для якого потрібно отримати інформацію про DNS-записи."""

    verification_record: Optional[str] = None
    """Запис, який потрібно внести "як є" для підтвердження володіння цим доменом."""

    dkim: Optional[str] = None
    """DKIM-підпис для домену. У цьому полі повертається лише ключ. Щоб TXT-запис був коректним, перед
    ключем потрібно додати "v=DKIM1; k=rsa; p=".
    """

    dmarc: Optional[str] = None
    """Значення CNAME-запису для хоста "_dmarc" домену."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainGetDnsRecordsResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            domain=data.get("domain"),
            verification_record=data.get("verification-record"),
            dkim=data.get("dkim"),
            dmarc=data.get("dmarc"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "domain": self.domain,
            "verification-record": self.verification_record,
            "dkim": self.dkim,
            "dmarc": self.dmarc,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainValidateVerificationRecordRequest:
    """DomainValidateVerificationRecordRequest"""

    domain: str
    """Домен, для якого перевіряється запис про володіння."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainValidateVerificationRecordRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            domain=data.get("domain"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "domain": self.domain,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainValidateVerificationRecordResponse:
    """DomainValidateVerificationRecordResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    message: Optional[str] = None
    """Налагоджувальне повідомлення про хід перевірки."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainValidateVerificationRecordResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            message=data.get("message"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "message": self.message,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainValidateDkimRequest:
    """DomainValidateDkimRequest"""

    domain: str
    """Домен, для якого перевіряється DKIM-запис."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainValidateDkimRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            domain=data.get("domain"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "domain": self.domain,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainValidateDkimResponse:
    """DomainValidateDkimResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    message: Optional[str] = None
    """Налагоджувальне повідомлення про хід перевірки."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainValidateDkimResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            message=data.get("message"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "message": self.message,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainListRequest:
    """DomainListRequest"""

    domain: Optional[str] = None
    """Опціональне ім'я домену, якщо вам потрібно отримати статуси лише за одним доменом."""

    limit: Optional[int] = None
    """Максимальна кількість доменів, що повертаються. За замовчуванням 50.
    За замовчуванням: `50`.
    """

    offset: Optional[int] = None
    """Індекс першого домену зі списку, що повертається, рахуючи з нуля.
    За замовчуванням: `0`.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainListRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            domain=data.get("domain"),
            limit=data.get("limit"),
            offset=data.get("offset"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "domain": self.domain,
            "limit": self.limit,
            "offset": self.offset,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainListResponse:
    """DomainListResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    domains: Optional[List[DomainListResponseDomainsItem]] = None
    """Масив об'єктів, що описують домени."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainListResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            domains=list_of(data.get("domains"), lambda item0: model_of(DomainListResponseDomainsItem, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "domains": [item0.to_dict() for item0 in self.domains] if self.domains is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainListResponseDomainsItem:
    """DomainListResponseDomainsItem"""

    domain: Optional[str] = None
    """Ім'я домену."""

    verification_record: Optional[DomainListResponseDomainsItemVerificationRecord] = None
    """Об'єкт, що описує запис перевірки володіння та її статус."""

    dkim: Optional[DomainListResponseDomainsItemDkim] = None
    """Об'єкт, що описує DKIM-запис та її статус."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainListResponseDomainsItem:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            domain=data.get("domain"),
            verification_record=model_of(DomainListResponseDomainsItemVerificationRecord, data.get("verification-record")),
            dkim=model_of(DomainListResponseDomainsItemDkim, data.get("dkim")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "domain": self.domain,
            "verification-record": self.verification_record.to_dict() if self.verification_record is not None else None,
            "dkim": self.dkim.to_dict() if self.dkim is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainListResponseDomainsItemVerificationRecord:
    """Об'єкт, що описує запис перевірки володіння та її статус."""

    value: Optional[str] = None
    """Запис, який потрібно внести "як є" для підтвердження володіння цим доменом."""

    status: Optional[VerificationRecordStatus] = None
    """Лише домени зі статусом "confirmed" запису про володіння доменом можуть використовуватися для
    надсилання листів.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainListResponseDomainsItemVerificationRecord:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            value=data.get("value"),
            status=to_enum(VerificationRecordStatus, data.get("status")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "value": self.value,
            "status": self.status,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainListResponseDomainsItemDkim:
    """Об'єкт, що описує DKIM-запис та її статус."""

    key: Optional[str] = None
    """DKIM-підпис для домену. У цьому полі повертається лише ключ. Щоб DNS-запис був коректним, перед
    ключем потрібно додати "k=rsa, p=" (див.
    [domain/get-dns-records](https://docs.allymailer.com.ua/ua/web-api-ref#domain-get-dns-records)).
    """

    status: Optional[DkimStatus] = None
    """Лише домени зі статусом DKIM-запису "active" можуть використовуватися для надсилання листів."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainListResponseDomainsItemDkim:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            key=data.get("key"),
            status=to_enum(DkimStatus, data.get("status")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "key": self.key,
            "status": self.status,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainGetSandboxDomainResponse:
    """DomainGetSandboxDomainResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    domain: Optional[str] = None
    """Ім'я sandbox-домену."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainGetSandboxDomainResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            domain=data.get("domain"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "domain": self.domain,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainDeleteRequest:
    """DomainDeleteRequest"""

    domain: str
    """Ім'я домену, який потрібно видалити."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainDeleteRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            domain=data.get("domain"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "domain": self.domain,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainDeleteResponse:
    """DomainDeleteResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    message: Optional[str] = None
    """Домен видалено"""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainDeleteResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            message=data.get("message"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "message": self.message,
        }
        return {k: v for k, v in result.items() if v is not None}
