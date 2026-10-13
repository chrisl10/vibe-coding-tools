#!/usr/bin/env python3
"""Read-only structural validation of an app-primer-zero JSON wave handoff."""

import argparse
import json
import re
import sys
from pathlib import Path


LIMITATIONS = [
    "Structural validation does not execute a wave or authorize any action.",
    "Approval fields are assertions supplied by the author; human evidence is not verified.",
    "SHA syntax is checked; commit existence and repository identity are not verified.",
    "Capacity verification is author-supplied; harness concurrency is not inspected.",
    "Review ordering is structural; independent reviewers, review success and candidate identity are not verified.",
    "Path prefixes are lexical ownership declarations; symlinks and actual files are not inspected.",
    "No credentials, external APIs, dependencies or application runtime are inspected.",
]
ROLES = {"coordinator", "implementation", "security", "quality"}


def positive_int(value):
    return type(value) is int and value > 0


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def canonical_path(value):
    if not nonempty(value) or value != value.strip():
        return False
    if "\\" in value or re.search(r"[\x00-\x1f\x7f*?\[\]{}:]", value):
        return False
    parts = value.split("/")
    return all(part not in {"", ".", ".."} for part in parts)


def overlaps(left, right):
    return left == right or left.startswith(right + "/") or right.startswith(left + "/")


def validate(data):
    """Return a JSON-serializable report, without modifying data or the filesystem."""
    errors, warnings = [], []

    def fail(where, message):
        errors.append({"path": where, "message": message})

    if not isinstance(data, dict):
        fail("$", "Expected an object.")
        return report(errors, warnings)
    if not nonempty(data.get("project")):
        fail("project", "Expected a nonempty project name.")
    if not isinstance(data.get("base_sha"), str) or not re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", data.get("base_sha", "")):
        fail("base_sha", "Expected a full 40- or 64-character hexadecimal Git object ID.")
    if "example" in data and type(data["example"]) is not bool:
        fail("example", "Expected a boolean.")
    if data.get("example") is True:
        warnings.append("Illustrative example: repository identity and decisions must be replaced before execution.")

    capacity = data.get("capacity")
    if not isinstance(capacity, dict):
        fail("capacity", "Expected an object.")
        capacity = {}
    for key in set(capacity) - {"limit", "coordinator_slots", "reviewer_slots", "verified", "mode"}:
        fail("capacity." + key, "Unknown capacity field; hidden reservations or workers are unsupported.")
    if not positive_int(capacity.get("limit")):
        fail("capacity.limit", "Expected a positive integer; booleans are not integers.")
    mode = capacity.get("mode", "parallel")
    if mode not in ("parallel", "serial-preparation"):
        fail("capacity.mode", "Expected parallel or serial-preparation.")
    if type(capacity.get("coordinator_slots")) is not int or capacity.get("coordinator_slots") != 1:
        fail("capacity.coordinator_slots", "Expected exactly 1 logical integrator slot.")
    if not positive_int(capacity.get("reviewer_slots")):
        fail("capacity.reviewer_slots", "Expected a positive simultaneous reviewer limit.")
    if mode == "serial-preparation" and capacity.get("limit") != 1:
        fail("capacity.limit", "Serial preparation requires a limit of exactly 1.")
    overhead = 0 if mode == "serial-preparation" else 1
    if mode == "serial-preparation":
        warnings.append("Serial preparation does not establish independent review or implementation readiness.")
    if "verified" in capacity and type(capacity["verified"]) is not bool:
        fail("capacity.verified", "Expected a boolean.")
    if capacity.get("verified") is not True:
        warnings.append("Harness capacity remains unverified; ready implementation waves are refused.")

    def records(key):
        values = data.get(key)
        if not isinstance(values, list):
            fail(key, "Expected an array.")
            return {}
        found = {}
        for index, item in enumerate(values):
            where = "%s[%s]" % (key, index)
            if not isinstance(item, dict):
                fail(where, "Expected an object.")
                continue
            identity = item.get("id")
            if not nonempty(identity) or identity != identity.strip():
                fail(where + ".id", "Expected a nonempty ID without outer whitespace.")
                continue
            if identity in found:
                fail(where + ".id", "Duplicate ID: " + identity)
                continue
            found[identity] = item
        return found

    contracts, shards, waves = records("contracts"), records("shards"), records("waves")
    if len(waves) > 64:
        fail("waves", "At most 64 waves are supported; split a larger plan into handoffs.")
        return report(errors, warnings)
    for identity, contract in contracts.items():
        where = "contracts." + identity
        if not positive_int(contract.get("revision")):
            fail(where + ".revision", "Expected a positive integer; booleans are not revisions.")
        if contract.get("status") not in ("Draft", "Accepted"):
            fail(where + ".status", "Expected Draft or Accepted.")
        for field in ("approved_by", "approval_evidence"):
            if field not in contract or (contract[field] is not None and not nonempty(contract[field])):
                fail(where + "." + field, "Expected null or a nonempty string.")
        if contract.get("status") == "Accepted" and not all(nonempty(contract.get(field)) for field in ("approved_by", "approval_evidence")):
            warnings.append("Accepted contract %s lacks approval attribution or evidence." % identity)

    safe_paths = {}
    role_counts = {role: 0 for role in ROLES}
    for identity, shard in shards.items():
        where = "shards." + identity
        role = shard.get("role")
        if not isinstance(role, str) or role not in ROLES:
            fail(where + ".role", "Unknown shard role.")
        else:
            role_counts[role] += 1
        paths = shard.get("owned_paths")
        if not isinstance(paths, list) or not all(canonical_path(path) for path in paths):
            fail(where + ".owned_paths", "Expected canonical relative POSIX prefixes; no traversal, absolute paths, globs or trailing slashes.")
            safe_paths[identity] = []
        else:
            safe_paths[identity] = paths
            if len(set(paths)) != len(paths):
                fail(where + ".owned_paths", "Duplicate ownership prefix.")
        if role == "implementation" and paths == []:
            fail(where + ".owned_paths", "Implementation shards require explicit ownership.")
        if role in ("coordinator", "security", "quality") and paths != []:
            fail(where + ".owned_paths", "Coordinators and reviewers must not own product source paths.")
        if "exclude_paths" in shard:
            fail(where + ".exclude_paths", "Exclusion leases are unsupported; declare disjoint owned prefixes.")
        if any(field in shard for field in ("nested_workers", "nested_slots", "reserved_slots")):
            fail(where, "Flatten nested workers and reservations into explicit active shards.")
    for role in ("coordinator", "security", "quality"):
        if role_counts[role] != 1:
            fail("shards", "Declare exactly one %s shard." % role)

    deps, active = {}, {}
    if not waves:
        fail("waves", "Declare at least one wave.")
    for identity, wave in waves.items():
        where = "waves." + identity
        for field in ("implementation", "ready"):
            if type(wave.get(field)) is not bool:
                fail(where + "." + field, "Expected a boolean.")
        for field, known in (("depends_on", waves), ("active_shards", shards)):
            refs = wave.get(field)
            if not isinstance(refs, list) or not all(nonempty(ref) for ref in refs):
                fail(where + "." + field, "Expected an array of IDs.")
                refs = []
            elif len(set(refs)) != len(refs):
                fail(where + "." + field, "Duplicate reference.")
            for ref in refs:
                if ref not in known:
                    fail(where + "." + field, "Unknown reference: " + ref)
            if field == "depends_on":
                deps[identity] = [ref for ref in refs if ref in known]
            else:
                active[identity] = [ref for ref in refs if ref in known]
        impl = [sid for sid in active[identity] if shards[sid].get("role") == "implementation"]
        # One logical integrator is counted once; idle reviewer ceilings are not workers.
        workers = [sid for sid in active[identity] if shards[sid].get("role") != "coordinator"]
        slot_count = max(1, len(workers) + overhead)
        if positive_int(capacity.get("limit")) and slot_count > capacity["limit"]:
            fail(where + ".active_shards", "%s active slots including coordinator overhead exceed limit %s." % (slot_count, capacity["limit"]))
        if wave.get("implementation") is False and impl:
            fail(where + ".active_shards", "A nonimplementation wave cannot activate implementation shards.")
        if wave.get("implementation") is True and not impl:
            fail(where + ".active_shards", "An implementation wave needs an implementation shard.")
        pins = wave.get("contract_pins")
        if not isinstance(pins, list):
            fail(where + ".contract_pins", "Expected an array.")
            pins = []
        if wave.get("implementation") is True and not pins:
            fail(where + ".contract_pins", "Implementation waves must pin their contracts.")
        pinned = set()
        for index, pin in enumerate(pins):
            pwhere = "%s.contract_pins[%s]" % (where, index)
            if not isinstance(pin, dict) or not nonempty(pin.get("id")):
                fail(pwhere, "Expected an object with a contract ID and revision.")
                continue
            cid = pin["id"]
            if cid in pinned:
                fail(pwhere, "Duplicate contract pin: " + cid)
            pinned.add(cid)
            if not positive_int(pin.get("revision")):
                fail(pwhere + ".revision", "Expected a positive integer; booleans are not revisions.")
            contract = contracts.get(cid)
            if contract is None:
                fail(pwhere + ".id", "Unknown contract: " + cid)
                continue
            if pin.get("revision") != contract.get("revision"):
                fail(pwhere + ".revision", "Pin must match the exact declared contract revision.")
            if wave.get("ready") is True and wave.get("implementation") is True:
                if contract.get("status") != "Accepted" or not all(nonempty(contract.get(field)) for field in ("approved_by", "approval_evidence")):
                    fail(pwhere, "Ready implementation requires an Accepted contract with attribution and approval evidence.")
        if wave.get("ready") is True:
            for dependency in deps[identity]:
                if waves[dependency].get("ready") is not True:
                    fail(where + ".depends_on", "Ready wave depends on a wave that is not ready: " + dependency)
            if wave.get("implementation") is True and capacity.get("verified") is not True:
                fail(where + ".ready", "Implementation readiness requires declared verified capacity.")
            if wave.get("implementation") is True and data.get("example") is True:
                fail(where + ".ready", "Illustrative examples cannot declare implementation ready.")
            if wave.get("implementation") is True and mode == "serial-preparation":
                fail(where + ".ready", "Serial preparation cannot declare implementation ready; independent reviews and runtime capacity need qualification.")

    # Detect cycles before reachability or ownership comparisons; never recurse a cycle.
    state = {}
    cyclic = False
    for origin in waves:
        if state.get(origin) == 2:
            continue
        stack = [(origin, False)]
        while stack:
            node, leaving = stack.pop()
            if leaving:
                state[node] = 2
                continue
            if state.get(node) == 1:
                fail("waves.depends_on", "Dependency cycle includes " + node)
                cyclic = True
                break
            if state.get(node) == 2:
                continue
            state[node] = 1
            stack.append((node, True))
            stack.extend((dep, False) for dep in reversed(deps[node]))
        if cyclic:
            return report(errors, warnings)

    ancestors = {}
    for identity in waves:
        reached, pending = set(), list(deps[identity])
        while pending:
            dep = pending.pop()
            if dep not in reached:
                reached.add(dep)
                pending.extend(deps[dep])
        ancestors[identity] = reached

    def check_owners(where, identities):
        implementations = [sid for sid in identities if shards[sid].get("role") == "implementation"]
        if len(set(implementations)) != len(implementations):
            fail(where, "An implementation shard cannot be active in multiple concurrent waves.")
        owners = sorted(set(sid for sid in identities if shards[sid].get("role") == "implementation"))
        for index, first in enumerate(owners):
            for second in owners[index + 1:]:
                for left in safe_paths[first]:
                    for right in safe_paths[second]:
                        if overlaps(left, right):
                            fail(where, "Concurrent ownership overlaps: %s:%s and %s:%s." % (first, left, second, right))
        workers = [sid for sid in identities if shards[sid].get("role") != "coordinator"]
        if len(workers) != len(set(workers)):
            fail(where, "An active worker or reviewer cannot occupy multiple concurrent waves.")
        reviewers = [sid for sid in set(workers) if shards[sid].get("role") in ("security", "quality")]
        if positive_int(capacity.get("reviewer_slots")) and len(reviewers) > capacity["reviewer_slots"]:
            fail(where, "Concurrent reviewers exceed the declared reviewer limit.")
        if reviewers and implementations:
            fail(where, "A candidate review cannot overlap implementation changes.")
        if {shards[sid].get("role") for sid in reviewers} == {"security", "quality"}:
            fail(where, "Security must precede Quality; concurrent reviews are refused.")
        slots = max(1, len(set(workers)) + overhead)
        if positive_int(capacity.get("limit")) and slots > capacity["limit"]:
            fail(where, "Concurrent waves need %s active slots including coordinator overhead, exceeding %s." % (slots, capacity["limit"]))

    security_waves = {wid for wid in waves if any(shards[sid].get("role") == "security" for sid in active[wid])}
    quality_waves = {wid for wid in waves if any(shards[sid].get("role") == "quality" for sid in active[wid])}
    if not security_waves or not quality_waves:
        fail("waves", "Schedule both Security and Quality review waves.")
    for wid in quality_waves:
        implementations = {ancestor for ancestor in ancestors[wid] if waves[ancestor].get("implementation") is True}
        prior = security_waves & ancestors[wid]
        if not any(implementations <= ancestors[review] for review in prior):
            fail("waves." + wid + ".depends_on", "Quality needs preceding Security on the same candidate; all preceding implementation must be covered.")
    for wid in waves:
        if waves[wid].get("implementation") is True and not any(wid in ancestors[review] for review in quality_waves):
            fail("waves." + wid, "Every implementation wave needs a later ordered candidate review; changes after final Quality are refused.")

    # Independent waves can run together; check every maximal compatible wave set.
    identities = list(waves)
    compatible = {wid: {other for other in identities if other != wid and other not in ancestors[wid] and wid not in ancestors[other]} for wid in identities}
    seen_sets = set()

    def maximal_sets(chosen, candidates, excluded):
        if not candidates and not excluded:
            yield chosen
            return
        union = candidates | excluded
        pivot = max(union, key=lambda node: len(candidates & compatible[node])) if union else None
        for node in sorted(candidates - (compatible[pivot] if pivot else set())):
            yield from maximal_sets(chosen | {node}, candidates & compatible[node], excluded & compatible[node])
            candidates.remove(node)
            excluded.add(node)

    # Stop combinatorial plans before enumerating more than 4096 compatible sets.
    for group in maximal_sets(set(), set(identities), set()):
        slots = tuple(sorted(group))
        if slots not in seen_sets:
            seen_sets.add(slots)
            check_owners("waves[" + ",".join(slots) + "]", [sid for wid in group for sid in active[wid]])
        if len(seen_sets) > 4096:
            fail("waves", "Concurrency graph exceeds 4096 compatible wave sets; simplify the plan.")
            break
    return report(errors, warnings)


def report(errors, warnings):
    return {"verdict": "PASS" if not errors else "FAIL", "errors": errors, "warnings": warnings, "limitations": LIMITATIONS.copy()}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", help="JSON file to read, or - for standard input")
    args = parser.parse_args(argv)
    try:
        raw = sys.stdin.read() if args.handoff == "-" else Path(args.handoff).read_text(encoding="utf-8")
        def unique_keys(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError("Duplicate JSON object key: " + key)
                result[key] = value
            return result

        data = json.loads(raw, object_pairs_hook=unique_keys)
        result = validate(data)
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        result = report([{"path": "$", "message": "Cannot read or validate JSON: " + str(exc)}], [])
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
