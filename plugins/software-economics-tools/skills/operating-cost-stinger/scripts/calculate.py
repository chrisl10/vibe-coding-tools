"""Calculate explicit monthly scenarios, fee floors and shared credits offline."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path
from typing import Any

ZERO = Decimal("0")
MAX_AMOUNT = Decimal("1000000000000")
MAX_BYTES = 262144


class InputError(ValueError):
    """Input does not satisfy the explicit cost-model contract."""


def fields(value: Any, keys: str, label: str) -> dict[str, Any]:
    required = set(keys.split())
    if not isinstance(value, dict) or set(value) != required:
        raise InputError(f"{label}: fields must be exactly {', '.join(sorted(required))}")
    return value


def text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 200:
        raise InputError(f"{label}: expected 1 to 200 characters")
    if any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise InputError(f"{label}: control characters prohibited")
    return value


def numeric(value: Any) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
        raise InputError("numeric field: expected decimal string or JSON number")
    if isinstance(value, str) and not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", value):
        raise InputError("numeric field: expected unsigned decimal notation")
    if len(str(value)) > 64:
        raise InputError("numeric field: representation too long")
    try:
        amount = Decimal(value)
    except InvalidOperation as exc:
        raise InputError("numeric field: invalid decimal") from exc
    if not amount.is_finite() or amount.is_signed() or amount > MAX_AMOUNT:
        raise InputError("numeric field: must be finite, nonnegative and at most 1000000000000")
    if len(amount.as_tuple().digits) > 24 or amount.as_tuple().exponent < -6:
        raise InputError("numeric field: maximum 24 digits and six fractional places")
    return amount


def dated(value: Any) -> str:
    result = text(value, "observed_at")
    try:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", result):
            raise ValueError("format")
        date.fromisoformat(result)
    except ValueError as exc:
        raise InputError("observed_at: expected ISO calendar date") from exc
    return result


def rows(value: Any, maximum: int, label: str) -> list[Any]:
    if not isinstance(value, list) or len(value) > maximum:
        raise InputError(f"{label}: expected list with at most {maximum} entries")
    return value


def unique_names(items: list[Any], label: str) -> set[str]:
    names = [text(item.get("name"), label + ".name") if isinstance(item, dict)
             else text(None, label) for item in items]
    if len(names) != len(set(names)):
        raise InputError(label + ": duplicate name")
    return set(names)


def stringify(value: Any) -> Any:
    if isinstance(value, Decimal):
        if value == ZERO:
            return "0"
        result = format(value, "f")
        return result.rstrip("0").rstrip(".") if "." in result else result
    if isinstance(value, list):
        return [stringify(item) for item in value]
    if isinstance(value, dict):
        return {key: stringify(item) for key, item in value.items()}
    return value


def scenario_model(value: Any) -> dict[str, Any]:
    scenario = fields(value, "name providers credit_pools labor", "scenario")
    name = text(scenario["name"], "scenario.name")
    if name not in {"low", "base", "high"}:
        raise InputError("scenario.name: expected low, base or high")
    providers = rows(scenario["providers"], 30, "providers")
    if not providers:
        raise InputError("providers: at least one provider required")
    provider_names = unique_names(providers, "provider")
    pools: dict[str, dict[str, Any]] = {}
    pool_rows = rows(scenario["credit_pools"], 30, "credit_pools")
    unique_names(pool_rows, "credit_pool")
    for value in pool_rows:
        pool = fields(value, "name amount scope eligible_providers", "credit_pool")
        pool_name = text(pool["name"], "credit_pool.name")
        scope = text(pool["scope"], "credit_pool.scope")
        if scope not in {"usage", "total"}:
            raise InputError("credit_pool.scope: expected usage or total")
        eligible = [text(v, "eligible provider") for v in rows(pool["eligible_providers"], 30, "eligible_providers")]
        if not eligible or len(eligible) != len(set(eligible)) or not set(eligible) <= provider_names:
            raise InputError("credit_pool: eligible providers must be distinct known provider names")
        pools[pool_name] = {"available": numeric(pool["amount"]), "scope": scope,
                            "eligible": set(eligible), "allocated": ZERO}
    outputs: list[dict[str, Any]] = []
    for value in providers:
        provider = fields(value, "name region plan observed_at source fee_mode fee_amount meters credit_allocations", "provider")
        provider_name = text(provider["name"], "provider.name")
        for key in ("region", "plan", "source"):
            text(provider[key], "provider." + key)
        dated(provider["observed_at"])
        mode = text(provider["fee_mode"], "fee_mode")
        if mode not in {"additive", "minimum"}:
            raise InputError("fee_mode: expected additive or minimum")
        fee = numeric(provider["fee_amount"])
        meters = rows(provider["meters"], 100, "meters")
        unique_names(meters, "meter")
        usage = ZERO
        meter_outputs = []
        for value in meters:
            meter = fields(value, "name unit quantity allowance rate", "meter")
            unit = text(meter["unit"], "meter.unit")
            quantity, allowance, rate = (numeric(meter[key]) for key in ("quantity", "allowance", "rate"))
            billable = max(ZERO, quantity - allowance)
            cost = billable * rate
            usage += cost
            meter_outputs.append({"name": meter["name"], "unit": unit,
                                  "quantity": quantity, "allowance": allowance, "rate": rate,
                                  "billable_quantity": billable, "cost": cost})
        credits = {"usage": ZERO, "total": ZERO}
        allocated: set[str] = set()
        for value in rows(provider["credit_allocations"], 30, "credit_allocations"):
            allocation = fields(value, "pool amount", "allocation")
            pool_name = text(allocation["pool"], "allocation.pool")
            if pool_name not in pools or pool_name in allocated:
                raise InputError("allocation: pool must exist and appear once per provider")
            allocated.add(pool_name)
            pool = pools[pool_name]
            if provider_name not in pool["eligible"]:
                raise InputError("allocation: provider is not eligible for this pool")
            amount = numeric(allocation["amount"])
            pool["allocated"] += amount
            if pool["allocated"] > pool["available"]:
                raise InputError("allocation: shared pool budget exceeded")
            credits[pool["scope"]] += amount
        if credits["usage"] > usage:
            raise InputError("allocation: usage credit exceeds metered usage")
        net_usage = usage - credits["usage"]
        charge = fee + net_usage if mode == "additive" else max(fee, net_usage)
        if credits["total"] > charge:
            raise InputError("allocation: total credit exceeds eligible charge")
        outputs.append({"name": provider_name, "region": provider["region"], "plan": provider["plan"],
                        "observed_at": provider["observed_at"], "source": provider["source"],
                        "meters": meter_outputs, "gross_usage": usage, "usage_credit": credits["usage"],
                        "fee_mode": mode, "fee_amount": fee, "before_total_credit": charge,
                        "total_credit": credits["total"], "cash_cost": charge - credits["total"]})
    paid, unpaid = ZERO, ZERO
    labor_rows = rows(scenario["labor"], 100, "labor")
    unique_names(labor_rows, "labor")
    for value in labor_rows:
        labor = fields(value, "name hours hourly_rate kind", "labor")
        kind = text(labor["kind"], "labor.kind")
        amount = numeric(labor["hours"]) * numeric(labor["hourly_rate"])
        if kind == "paid":
            paid += amount
        elif kind == "unpaid":
            unpaid += amount
        else:
            raise InputError("labor.kind: expected paid or unpaid")
    provider_cash = sum((row["cash_cost"] for row in outputs), ZERO)
    return {"name": name, "providers": outputs, "credit_pools": [
        {"name": key, "available": pool["available"], "allocated": pool["allocated"],
         "unused": pool["available"] - pool["allocated"]} for key, pool in pools.items()],
        "provider_cash": provider_cash, "paid_operator_labor": paid,
        "monthly_cash_estimate": provider_cash + paid, "unpaid_time_valuation": unpaid,
        "monthly_cost_with_time_valuation": provider_cash + paid + unpaid}


def model(value: Any) -> dict[str, Any]:
    obj = fields(value, "currency period observed_at evidence scenarios", "input")
    currency = text(obj["currency"], "currency")
    if not re.fullmatch(r"[A-Z]{3}", currency) or obj["period"] != "month":
        raise InputError("input: expected three-letter uppercase currency and period month")
    dated(obj["observed_at"])
    text(obj["evidence"], "evidence")
    scenarios = rows(obj["scenarios"], 3, "scenarios")
    if unique_names(scenarios, "scenario") != {"low", "base", "high"}:
        raise InputError("scenarios: exactly low, base and high required")
    with localcontext() as context:
        context.prec = 64
        result = {"model": "monthly-operating-cost-v1", "currency": currency,
                  "period": "month", "observed_at": obj["observed_at"], "evidence": obj["evidence"],
                  "scenarios": [scenario_model(row) for row in scenarios]}
        return stringify(result)


def json_number(value: str) -> Decimal:
    if len(value) > 64:
        raise InputError("JSON number: representation too long")
    try:
        return numeric(Decimal(value))
    except InvalidOperation as exc:
        raise InputError("JSON number: invalid decimal exponent") from exc


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InputError("JSON duplicate key")
        result[key] = value
    return result


def reject_constant(value: str) -> Any:
    raise InputError("JSON nonfinite constant prohibited")


def load_input(path: Path) -> Any:
    if not path.is_file():
        raise InputError("input must be an explicit regular JSON file")
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise InputError("input exceeds 262144 bytes")
    return json.loads(raw.decode("utf-8"), parse_float=json_number, parse_int=json_number,
                      object_pairs_hook=unique_object, parse_constant=reject_constant)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    try:
        output = model(load_input(args.input))
    except (InputError, OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        message = str(exc) if isinstance(exc, InputError) else "input could not be read or parsed"
        sys.stderr.write("Input error: " + message + "\n")
        return 2
    sys.stdout.write(json.dumps(output, indent=2, ensure_ascii=True, allow_nan=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
