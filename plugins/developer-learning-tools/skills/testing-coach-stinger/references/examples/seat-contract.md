# Completed synthetic contract exercise

A practice room has 10 seats. `remaining(booked)` accepts only Python integers excluding booleans, from 0 through 10 inclusive. It returns the remaining seat count and has no I/O. Invalid input raises ValueError. This is an authored contract, not a product policy.

| Case | Expected | Independent reason |
|---|---|---|
| 0 | 10 | Nothing booked, all ten available |
| 1 | 9 | One of ten used |
| 9 | 1 | One remains before full capacity |
| 10 | 0 | Full capacity |
| -1, 11 | ValueError | Outside stated domain |
| True, 1.5, "1", None | ValueError | Wrong stated type |
| k to k+1, k from 0 to 9 | remaining decreases by one | One additional seat booked |

The [fixed fixture](seat-fixture.py) runs the same independent tests against a correct implementation and three deliberate faults: an extra remaining seat, clamping invalid values, and accepting booleans. Expected-failing runs are separately marked. The relationship test alone passes the extra-seat fault, showing why exact examples matter. No real learner response exists; understanding PENDING. No product/browser/provider/native-host coverage claim follows.
