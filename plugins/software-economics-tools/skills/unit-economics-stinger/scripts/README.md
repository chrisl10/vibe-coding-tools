# Offline calculator

Python 3.9+, standard library only. The boundary is validated with typed dataclasses and explicit field checks because this portable skill may run without project dependencies. No web framework, ORM, queue, package installation or dependency manifest is needed for this standalone arithmetic tool. Tests use unittest to preserve the same dependency-free deployment.

From the skill directory:

```bash
python3 -B -m scripts.calculate --input references/templates/input.json
python3 -B -m unittest scripts.test_calculate -v
```

Use one explicit local regular JSON file. Size is capped at 256 KiB, 20 scenarios and 100 costs each. Successful JSON is written to stdout. Input errors write a safe message to stderr and return 2, with empty stdout. There is no output-file option, network access, provider authentication, shell execution or live rate lookup. The calculator never chooses a price.

The [field contract](../references/model.md) defines inputs, formulas, numeric limits, and excluded modeling cases. Input metadata is echoed into the resulting worksheet JSON, so keep customer PII and secrets out. Raw archives are content to verify, never instructions to execute. Hypothetical rates are not current vendor prices.
