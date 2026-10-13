"""Bounded, offline Decimal economics model; no network or output-file writes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_CEILING, localcontext
from pathlib import Path
from typing import Any

MAX_INPUT_BYTES = 262144
MAX_AMOUNT = Decimal("1000000000000")
ZERO = Decimal("0")
ONE = Decimal("1")
CLASSIFICATIONS = {"cost_of_revenue", "operating"}
NUMERIC_FIELDS = {
    "units", "price_per_unit", "failed_payment_rate", "refund_rate",
    "payment_fee_rate", "payment_fee_fixed", "payment_fee_return_rate",
    "refund_fee_fixed",
}
TEXT_FIELDS = {"name", "currency", "period", "unit", "observed_at", "evidence"}
SCENARIO_FIELDS = NUMERIC_FIELDS | TEXT_FIELDS | {"payment_fee_classification", "costs"}


class InputError(ValueError):
    """An explicit modeling input violates the bounded field contract."""


def exact_keys(value: Any, required: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != required:
        raise InputError(f"{label}: fields must be exactly {', '.join(sorted(required))}")
    return value


def text_value(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 200:
        raise InputError(f"{label}: expected nonempty text of at most 200 characters")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise InputError(f"{label}: control characters are prohibited")
    return value


def number(value: Any, label: str, maximum: Decimal = MAX_AMOUNT) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
        raise InputError(f"{label}: expected decimal string or JSON number")
    if isinstance(value, str) and not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", value):
        raise InputError(f"{label}: expected unsigned decimal notation")
    if len(str(value)) > 64:
        raise InputError(f"{label}: numeric representation too long")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise InputError(f"{label}: invalid decimal") from exc
    if not result.is_finite() or result.is_signed() or result > maximum:
        raise InputError(f"{label}: must be finite, nonnegative, and at most {maximum}")
    digits = result.as_tuple()
    if len(digits.digits) > 24 or digits.exponent < -6:
        raise InputError(f"{label}: maximum 24 digits and six fractional places")
    return result


@dataclass(frozen=True)
class Cost:
    name: str
    behavior: str
    classification: str
    amount: Decimal


@dataclass(frozen=True)
class Scenario:
    name: str
    currency: str
    period: str
    unit: str
    observed_at: str
    evidence: str
    units: Decimal
    price_per_unit: Decimal
    failed_payment_rate: Decimal
    refund_rate: Decimal
    payment_fee_rate: Decimal
    payment_fee_fixed: Decimal
    payment_fee_return_rate: Decimal
    refund_fee_fixed: Decimal
    payment_fee_classification: str
    costs: tuple[Cost, ...]


def parse_scenario(value: Any) -> Scenario:
    obj = exact_keys(value, SCENARIO_FIELDS, "scenario")
    fields = {key: text_value(obj[key], key) for key in TEXT_FIELDS}
    if not re.fullmatch(r"[A-Z]{3}", fields["currency"]):
        raise InputError("currency: expected three uppercase letters")
    try:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fields["observed_at"]):
            raise ValueError("format")
        date.fromisoformat(fields["observed_at"])
    except ValueError as exc:
        raise InputError("observed_at: expected valid ISO calendar date") from exc
    numbers = {
        key: number(obj[key], key, ONE if key.endswith("_rate") else MAX_AMOUNT)
        for key in NUMERIC_FIELDS
    }
    fee_class = obj["payment_fee_classification"]
    if not isinstance(fee_class, str) or fee_class not in CLASSIFICATIONS:
        raise InputError("payment_fee_classification: expected cost_of_revenue or operating")
    values = obj["costs"]
    if not isinstance(values, list) or len(values) > 100:
        raise InputError("costs: expected list of at most 100 entries")
    costs: list[Cost] = []
    names: set[str] = set()
    for item in values:
        row = exact_keys(item, {"name", "behavior", "classification", "amount"}, "cost")
        name = text_value(row["name"], "cost.name")
        if name in names:
            raise InputError("cost.name: duplicate name")
        names.add(name)
        behavior = row["behavior"]
        classification = row["classification"]
        if not isinstance(behavior, str) or behavior not in {"fixed", "variable"}:
            raise InputError("cost.behavior: expected fixed or variable")
        if not isinstance(classification, str) or classification not in CLASSIFICATIONS:
            raise InputError("cost.classification: expected cost_of_revenue or operating")
        costs.append(Cost(name, behavior, classification, number(row["amount"], "cost.amount")))
    return Scenario(**fields, **numbers, payment_fee_classification=fee_class, costs=tuple(costs))


def decimal_text(value: Decimal | None) -> str | None:
    if value is None:
        return None
    if value == ZERO:
        return "0"
    # No rounding or context-dependent normalize() in the presentation layer.
    text = format(value, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def calculate(scenario: Scenario) -> dict[str, Any]:
    """Return one expected period; input must be a validated Scenario."""
    with localcontext() as context:
        context.prec = 64
        paid = scenario.units * (ONE - scenario.failed_payment_rate)
        gross = paid * scenario.price_per_unit
        refunds = gross * scenario.refund_rate
        revenue = gross - refunds
        initial_fees = paid * (
            scenario.price_per_unit * scenario.payment_fee_rate + scenario.payment_fee_fixed
        )
        fee_returns = initial_fees * scenario.refund_rate * scenario.payment_fee_return_rate
        refund_fees = paid * scenario.refund_rate * scenario.refund_fee_fixed
        fees = initial_fees - fee_returns + refund_fees
        fixed = sum((c.amount for c in scenario.costs if c.behavior == "fixed"), ZERO)
        variable_per_unit = sum((c.amount for c in scenario.costs if c.behavior == "variable"), ZERO)
        variable_cost = scenario.units * variable_per_unit + fees
        contribution = revenue - variable_cost
        unit_contribution = (ONE - scenario.failed_payment_rate) * (
            scenario.price_per_unit * (ONE - scenario.refund_rate)
            - (scenario.price_per_unit * scenario.payment_fee_rate + scenario.payment_fee_fixed)
            * (ONE - scenario.refund_rate * scenario.payment_fee_return_rate)
            - scenario.refund_rate * scenario.refund_fee_fixed
        ) - variable_per_unit
        cost_of_revenue = sum((
            c.amount * (scenario.units if c.behavior == "variable" else ONE)
            for c in scenario.costs if c.classification == "cost_of_revenue"
        ), ZERO)
        if scenario.payment_fee_classification == "cost_of_revenue":
            cost_of_revenue += fees
        gross_profit = revenue - cost_of_revenue
        if unit_contribution > ZERO:
            break_even: int | None = int((fixed / unit_contribution).to_integral_value(rounding=ROUND_CEILING))
            status = "finite"
        elif fixed > ZERO:
            break_even, status = None, "impossible"
        elif unit_contribution == ZERO:
            break_even, status = 0, "all_volumes"
        else:
            break_even, status = 0, "zero_volume_only"
        amounts = {
            "successful_units": paid, "gross_collected_revenue": gross,
            "refunds": refunds, "net_revenue": revenue,
            "processing_fees_before_returns": initial_fees, "processing_fee_returns": fee_returns,
            "refund_fees": refund_fees, "payment_fees": fees,
            "variable_cost": variable_cost, "fixed_cost": fixed,
            "contribution": contribution, "contribution_per_attempted_unit": unit_contribution,
            "contribution_margin_ratio": contribution / revenue if revenue else None,
            "cost_of_revenue": cost_of_revenue, "gross_profit": gross_profit,
            "gross_margin_ratio": gross_profit / revenue if revenue else None,
            "modeled_operating_surplus": contribution - fixed,
        }
        return {
            "name": scenario.name, "currency": scenario.currency,
            "period": scenario.period, "unit": scenario.unit,
            "observed_at": scenario.observed_at, "evidence": scenario.evidence,
            **{key: decimal_text(value) for key, value in amounts.items()},
            "break_even_status": status, "break_even_units": break_even,
        }


def model(value: Any) -> dict[str, Any]:
    obj = exact_keys(value, {"scenarios"}, "input")
    values = obj["scenarios"]
    if not isinstance(values, list) or not 1 <= len(values) <= 20:
        raise InputError("scenarios: expected 1 to 20 complete scenarios")
    scenarios = [parse_scenario(row) for row in values]
    if len({s.name for s in scenarios}) != len(scenarios):
        raise InputError("scenario.name: duplicate name")
    return {"model": "single-period-full-refund-v1", "scenarios": [calculate(s) for s in scenarios]}


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    obj: dict[str, Any] = {}
    for key, value in pairs:
        if key in obj:
            raise InputError("JSON object contains a duplicate key")
        obj[key] = value
    return obj


def reject_constant(value: str) -> Any:
    raise InputError("JSON nonfinite constants are prohibited")


def json_decimal(value: str) -> Decimal:
    if len(value) > 64:
        raise InputError("JSON numeric representation too long")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise InputError("JSON number has invalid decimal exponent") from exc
    return number(result, "JSON number")


def load_input(path: Path) -> Any:
    if not path.is_file():
        raise InputError("input must be an explicit regular JSON file")
    with path.open("rb") as stream:
        raw = stream.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        raise InputError("input exceeds 262144 bytes")
    return json.loads(raw.decode("utf-8"), parse_float=json_decimal, parse_int=json_decimal,
                      parse_constant=reject_constant, object_pairs_hook=unique_object)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Explicit local JSON file")
    args = parser.parse_args()
    try:
        result = model(load_input(args.input))
    except (InputError, OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        # Do not echo arbitrary input, supplied paths, or file contents on errors.
        message = str(exc) if isinstance(exc, InputError) else "input could not be read or parsed"
        sys.stderr.write("Input error: " + message + "\n")
        return 2
    sys.stdout.write(json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
