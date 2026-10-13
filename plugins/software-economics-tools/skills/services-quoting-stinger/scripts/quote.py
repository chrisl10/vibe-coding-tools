"""Offline supplied-cost quotation arithmetic; proposals are never acceptance."""
import argparse
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext
import json
from pathlib import Path
import sys

NUMBERS = ("owner_hours", "owner_cost_per_hour", "subcontractor_cost", "fixed_cost", "contingency_fraction", "pricing_fraction", "pass_through_cost")
FIELDS = (*NUMBERS, "name", "basis", "currency", "period", "pricing_mode")


def number(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
        raise ValueError("number: require decimal string or JSON number")
    if isinstance(value, str) and len(value) > 100:
        raise ValueError("number: text too long")
    try:
        value = Decimal(value)
    except InvalidOperation:
        raise ValueError("number: invalid decimal") from None
    if not value.is_finite() or not 0 <= value <= Decimal("1e9"):
        raise ValueError("number: require finite nonnegative value at most 1 billion")
    if not -12 <= value.as_tuple().exponent <= 12 or len(value.as_tuple().digits) > 30:
        raise ValueError("number: precision/exponent outside supported bounds")
    return value


def calculate(data):
    if not isinstance(data, dict) or set(data) != {"scenarios"}:
        raise ValueError("input: require exactly scenarios")
    if not isinstance(data["scenarios"], list) or not 1 <= len(data["scenarios"]) <= 20:
        raise ValueError("scenarios: require 1 to 20")
    results, names = [], set()
    with localcontext() as ctx:
        ctx.prec = 60
        for scenario in data["scenarios"]:
            if not isinstance(scenario, dict) or set(scenario) != set(FIELDS):
                raise ValueError("scenario: missing or unknown field")
            for field in ("name", "basis", "currency", "period", "pricing_mode"):
                if not isinstance(scenario[field], str) or not scenario[field].strip() or len(scenario[field]) > 4000:
                    raise ValueError(f"{field}: require bounded nonempty text")
            if scenario["name"] in names:
                raise ValueError("scenario: duplicate name")
            names.add(scenario["name"])
            if scenario["period"] not in ("project", "month") or scenario["pricing_mode"] not in ("markup", "margin"):
                raise ValueError("scenario: unsupported period or pricing mode")
            n = {field: number(scenario[field]) for field in NUMBERS}
            fraction = n["pricing_fraction"]
            if not n["contingency_fraction"] <= 1 or (scenario["pricing_mode"] == "margin" and not fraction < 1) or (scenario["pricing_mode"] == "markup" and fraction > 10):
                raise ValueError("fractions: contingency 0..1; markup 0..10; margin 0..<1")
            labour = n["owner_hours"] * n["owner_cost_per_hour"]
            cash = n["subcontractor_cost"] + n["fixed_cost"]
            reserve = (labour + cash) * n["contingency_fraction"]
            cost = labour + cash + reserve
            price = cost * (1 + fraction) if scenario["pricing_mode"] == "markup" else cost / (1 - fraction)
            money = lambda amount: format(amount.quantize(Decimal(".01"), rounding=ROUND_HALF_UP), "f")
            results.append({"name": scenario["name"], "basis": scenario["basis"], "currency": scenario["currency"], "period": scenario["period"],
                            "owner_labour_value": money(labour), "baseline_cash": money(cash + n["pass_through_cost"]),
                            "contingency_reserve": money(reserve), "service_cost_basis": money(cost), "service_price": money(price),
                            "proposed_total": money(price + n["pass_through_cost"]), "planned_surplus": money(price - cost),
                            "effective_service_margin": format((price - cost) / price, "f") if price else None})
    return {"status": "PROPOSED_NOT_ACCEPTED", "scenarios": results}


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError("JSON: duplicate key")
        result[key] = value
    return result


def constant(value):
    raise ValueError("JSON: nonfinite constant")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        with args.input.open(encoding="utf-8") as stream:
            content = stream.read(100001)
        if len(content) > 100000:
            raise ValueError("JSON: input exceeds 100000 characters")
        data = json.loads(content, parse_float=number, parse_constant=constant, object_pairs_hook=pairs)
        print(json.dumps(calculate(data), indent=2, allow_nan=False))
    except (ValueError, OSError, RecursionError) as error:
        print(f"quote error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
