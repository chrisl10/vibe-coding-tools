# Word Export Behavior

LibreOffice headless mode runs without its user interface. [C03]

## Conversion options

LibreOffice accepts PDF as an output format and lets the operator choose the output folder. [C04]

| Option | Meaning |
| --- | --- |
| --headless | Starts without the application interface. [C03] |
| --convert-to pdf | Selects PDF output. [C04] |
| --outdir | Selects the output directory. [C04] |

<!-- page -->

## Documented command shape

The official guide shows PDF conversion with an output folder. [C04]

```sh
soffice --headless --convert-to pdf --outdir reviewed report.doc
# Command options reference [C04]
```

## References

- [C03] LibreOffice command options; libreoffice-start-parameters.md; lines 76
- [C04] LibreOffice command options; libreoffice-start-parameters.md; lines 132
