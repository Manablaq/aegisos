# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from dataclasses import dataclass
import hashlib, json, typing
from genlayer import *

@allow_storage
@dataclass
class AuthorityAttestation:
    authority: Address
    role: u8
    evidence_record_id: str
    evidence_record_version: str
    immutable_source_ref: str
    evidence_payload_hash: str
    source_content_hash: str
    published_at: u64
    expires_at: u64
    generation: u32
    present: bool

@allow_storage
@dataclass
class AgreementRecord:
    creator: Address
    counterparty: Address
    policy_hash: str
    authority_set_hash: str
    primary_authority: Address
    corroborating_authority: Address
    max_evidence_age_seconds: u32
    evidence_record_id: str
    evidence_set_hash: str
    challenge_hash: str
    decision_digest: str
    state: u8
    generation: u32
    decision_nonce: u64
    challenge_window_seconds: u32
    challenge_deadline: u64
    recovery_deadline: u64
    evidence_expires_at: u64
    outcome_code: u8
    consequence_code: u8
    beneficiary: Address
    principal_amount: u256
    entitlement_amount: u256
    accepted: bool
    challenged: bool
    decision_recorded: bool

class AegisPureDigestHelper(gl.Contract):

    def __init__(self):
        pass

    def _h(self, v: str) -> str:
        return hashlib.sha256(v.encode('utf-8')).hexdigest()

    def _u(self, p: AuthorityAttestation, c: AuthorityAttestation) -> str:
        return f'AEGISOS_EVIDENCE_PAIR_V2|{p.evidence_record_id!s}|{p.evidence_record_version!s}|{c.evidence_record_id!s}|{c.evidence_record_version!s}'

    def _m(self, agreement_id: str, generation: int, p: AuthorityAttestation, c: AuthorityAttestation) -> str:
        return f'AEGISOS_AUTHENTICATED_EVIDENCE_SET_V2|agreement={agreement_id!s}|generation={generation!s}|primary_authority={p.authority.as_hex!s}|primary_record={p.evidence_record_id!s}|primary_version={p.evidence_record_version!s}|primary_source={p.immutable_source_ref!s}|primary_payload_hash={p.evidence_payload_hash!s}|primary_source_hash={p.source_content_hash!s}|primary_published_at={int(p.published_at)!s}|primary_expires_at={int(p.expires_at)!s}|corroborator_authority={c.authority.as_hex!s}|corroborator_record={c.evidence_record_id!s}|corroborator_version={c.evidence_record_version!s}|corroborator_source={c.immutable_source_ref!s}|corroborator_payload_hash={c.evidence_payload_hash!s}|corroborator_source_hash={c.source_content_hash!s}|corroborator_published_at={int(c.published_at)!s}|corroborator_expires_at={int(c.expires_at)!s}'

    def _g(self, agreement_id: str, r: AgreementRecord, o: int, co: int, b: Address, am: int, nn: int) -> str:
        pl = json.dumps({'agreement_id': agreement_id, 'policy_hash': r.policy_hash, 'authority_set_hash': r.authority_set_hash, 'evidence_record_id': r.evidence_record_id, 'evidence_set_hash': r.evidence_set_hash, 'evidence_expires_at': int(r.evidence_expires_at), 'challenge_hash': r.challenge_hash, 'challenge_deadline': int(r.challenge_deadline), 'recovery_deadline': int(r.recovery_deadline), 'principal_amount': int(r.principal_amount), 'generation': int(r.generation), 'outcome_code': o, 'consequence_code': co, 'beneficiary': b.as_hex, 'entitlement_amount': am, 'decision_nonce': nn}, sort_keys=True, separators=(',', ':'))
        return self._h(pl)

    def _a(self, x: typing.Any) -> AuthorityAttestation:
        if isinstance(x, AuthorityAttestation):
            return x
        return AuthorityAttestation(**typing.cast(dict[str, typing.Any], x))

    def _r(self, x: typing.Any) -> AgreementRecord:
        if isinstance(x, AgreementRecord):
            return x
        return AgreementRecord(**typing.cast(dict[str, typing.Any], x))

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def e(self, a: str, n: int, p: AuthorityAttestation, c: AuthorityAttestation) -> str:
        p = self._a(p)
        c = self._a(c)
        return self._h(self._u(p, c)) + self._h(self._m(a, n, p, c))

    @gl.public.view  # pyright: ignore[reportUnknownMemberType]
    def g(self, a: str, r: AgreementRecord, o: int, c: int, b: Address, m: int, n: int) -> str:
        r = self._r(r)
        return self._g(a, r, o, c, b, m, n)
