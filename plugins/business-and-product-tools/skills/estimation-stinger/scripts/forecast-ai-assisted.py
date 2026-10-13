#!/usr/bin/env python3
"""Deterministic individual-project scenario accounting, using supplied inputs only."""
import argparse
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_HALF_UP, localcontext
import json
from pathlib import Path
import sys

MAX_DAYS = 36600
MAX_VALUE = Decimal("1000000000")
EFFORT = ("engineering_hours", "learning_hours", "verification_hours", "rework_hours")
COST = ("one_time_cash", "monthly_cash", "cash_per_owner_hour", "owner_hourly_value")


def keys(obj, expected, label):
    if not isinstance(obj, dict) or set(obj) != set(expected):
        raise ValueError(f"{label}: require exactly {', '.join(expected)}")


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
        raise ValueError(f"{label}: use a decimal string or JSON number")
    if isinstance(value, str) and len(value) > 100:
        raise ValueError(f"{label}: numeric text too long")
    try:
        result = Decimal(value)
    except InvalidOperation:
        raise ValueError(f"{label}: invalid decimal") from None
    if not result.is_finite() or result < 0 or result > MAX_VALUE:
        raise ValueError(f"{label}: require finite value between 0 and {MAX_VALUE}")
    if not -12 <= result.as_tuple().exponent <= 12 or len(result.as_tuple().digits) > 30:
        raise ValueError(f"{label}: unsupported precision; at most 30 digits and 12 decimal orders")
    return result


def text(value, label):
    if not isinstance(value, str) or not value.strip() or len(value) > 4000:
        raise ValueError(f"{label}: require nonempty text, at most 4000 characters")
    return value


def integer(value, label, maximum):
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError(f"{label}: require integer between 0 and {maximum}")
    return value


def calculate(data):
    keys(data, ("start_date", "hours_per_day", "usable_fraction", "weekdays", "currency", "cost_basis", "scenarios"), "input")
    try:
        start = date.fromisoformat(text(data["start_date"], "start_date"))
    except ValueError:
        raise ValueError("start_date: require valid ISO date YYYY-MM-DD") from None
    if data["start_date"] != start.isoformat():
        raise ValueError("start_date: require ISO date YYYY-MM-DD")
    daily = number(data["hours_per_day"], "hours_per_day")
    fraction = number(data["usable_fraction"], "usable_fraction")
    if not 0 < daily <= 24 or not 0 < fraction <= 1:
        raise ValueError("hours_per_day must be in (0,24]; usable_fraction must be in (0,1]")
    weekdays = data["weekdays"]
    if not isinstance(weekdays, list) or not 1 <= len(weekdays) <= 7:
        raise ValueError("weekdays: require 1 to 7 distinct integers")
    for day in weekdays:
        integer(day, "weekday", 6)
    if len(set(weekdays)) != len(weekdays):
        raise ValueError("weekdays: duplicate weekday")
    currency = text(data["currency"], "currency")
    cost_basis = text(data["cost_basis"], "cost_basis")
    scenarios = data["scenarios"]
    if not isinstance(scenarios, list) or not 1 <= len(scenarios) <= 20:
        raise ValueError("scenarios: require 1 to 20 scenarios")
    outputs, names = [], set()
    with localcontext() as ctx:
        ctx.prec = 60
        for scenario in scenarios:
            keys(scenario, ("name", "basis", *EFFORT, *COST, "dependencies"), "scenario")
            name = text(scenario["name"], "name")
            if name in names:
                raise ValueError("scenario: duplicate name")
            names.add(name)
            basis = text(scenario["basis"], "basis")
            effort = sum((number(scenario[k], k) for k in EFFORT), Decimal(0))
            costs = {k: number(scenario[k], k) for k in COST}
            hours = effort / fraction
            days = int((hours / daily).to_integral_value(rounding=ROUND_CEILING))
            if days > MAX_DAYS:
                raise ValueError("scenario: exceeds supported working-day horizon")
            # Start date is day zero. Completion occurs at the end of the last scheduled day.
            offset, consumed = 0, 0
            while consumed < days:
                if offset > MAX_DAYS:
                    raise ValueError("scenario: exceeds supported calendar-day horizon")
                try:
                    current = start + timedelta(days=offset)
                except OverflowError:
                    raise ValueError("scenario: completion exceeds supported date range") from None
                if current.weekday() in weekdays:
                    consumed += 1
                if consumed < days:
                    offset += 1
            dependencies = scenario["dependencies"]
            if not isinstance(dependencies, list) or len(dependencies) > 100:
                raise ValueError("dependencies: require list with at most 100 entries")
            dependency_names = set()
            external_offset = 0
            for dependency in dependencies:
                keys(dependency, ("name", "ready_after_calendar_days"), "dependency")
                dep_name = text(dependency["name"], "dependency.name")
                if dep_name in dependency_names:
                    raise ValueError("dependencies: duplicate name")
                dependency_names.add(dep_name)
                external_offset = max(external_offset, integer(dependency["ready_after_calendar_days"], "ready_after_calendar_days", MAX_DAYS))
            release_offset = max(offset, external_offset)
            try:
                release = start + timedelta(days=release_offset)
                build = start + timedelta(days=offset)
            except OverflowError:
                raise ValueError("scenario: release exceeds supported date range") from None
            span = release_offset + 1 if days or external_offset else 0
            # Planning convention: recurring cash is charged in started 30-day blocks.
            blocks = (span + 29) // 30
            cash = costs["one_time_cash"] + costs["monthly_cash"] * blocks + costs["cash_per_owner_hour"] * hours
            owner_value = costs["owner_hourly_value"] * hours
            money = lambda value: format(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), "f")
            outputs.append({"name": name, "basis": basis, "effective_project_hours": format(effort, "f"),
                            "scheduled_owner_hours": format(hours, "f"), "working_days": days,
                            "build_completion_date": build.isoformat(), "release_ready_date": release.isoformat(),
                            "elapsed_calendar_days": release_offset, "active_calendar_span_days": span,
                            "recurring_30_day_blocks": blocks, "direct_cash": money(cash),
                            "owner_time_value": money(owner_value)})
    return {"kind": "conditional_scenarios_not_probabilities", "currency": currency,
            "cost_basis": cost_basis, "scenarios": outputs}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"JSON: duplicate key {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"JSON: nonfinite constant {value}")


def parse_decimal(value):
    """Validate lexical length and Decimal bounds before accepting a JSON float."""
    return number(value, "JSON decimal")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        with args.input.open(encoding="utf-8") as stream:
            content = stream.read(100001)
        if len(content) > 100000:
            raise ValueError("JSON: input exceeds 100000 characters")
        data = json.loads(content, parse_float=parse_decimal, parse_constant=reject_constant, object_pairs_hook=unique_object)
        print(json.dumps(calculate(data), indent=2, allow_nan=False))
    except (ValueError, OSError, RecursionError) as error:
        print(f"forecast error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
