# What these two dependency files tell you

The [manifest](../references/examples/manifest-learning/fixtures/package.json) says what this fictional project requests. The [lockfile](../references/examples/manifest-learning/fixtures/package-lock.json) records selected dependency entries. Neither proves the packages are installed or safe. [F1]

The manifest lists lesson-widget with the requested range `^1.2.0`. The lockfile records lesson-widget at `1.2.3`. That entry also requires lesson-color at `0.4.0`, so lesson-color is an indirect dependency in this supplied graph even though the project's dependency list does not name it. [F2]

lesson-checker appears as a development dependency at `2.0.0`; its lock entry is marked dev. That describes its category in these records, not a guarantee it cannot affect security or execute code. [F3]

Think of the manifest as a shopping plan and the lockfile as a receipt listing selected items and the parts those items need. A receipt does not prove the goods are in your house or that they are safe. Likewise, these files do not establish installed files, successful checks or vulnerability results. [F1, illustration]

The manifest declares npm `11.21.0` and a Node runtime range. The exercise supplies no running CLI evidence. Its check script names `scripts/check.mjs`, but that file is not supplied; a script name alone is not a passing test. [F4]

For matching npm v11 behavior, npm ci checks consistency against the lockfile instead of fixing a mismatch and then installs the project. It can remove node_modules, so reading these records is separate from running installation. Nothing was installed in this exercise. official npm ci source.

Check your understanding: Which file gives the requested lesson-widget range, which gives the recorded concrete version, and what additional evidence would prove a check actually passed?

Reader response: Pending. Understanding: Pending. Runtime, installation and security qualification: Unproven.
