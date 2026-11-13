# Accessibility

At **Scalar Phos**, we believe that artificial intelligence research, parameter-efficient training pipelines, and developer tooling should be accessible to everyone. We are committed to lowering barriers for developers, researchers, and contributors of all abilities—whether they interact with our repository via command-line utilities, documentation, or local web interfaces.

This document outlines our accessibility commitments, expectations for contributors, and how you can report barriers or request assistance.

## Priorities

We strive to make the Scalar Phos ecosystem usable across diverse assistive technologies and environments. Our aspirational targets focus on:
* **Screen Reader Compatibility:** Ensuring repository documentation (`README.md`, guides) and local web interfaces (such as the Gradio chat app in `deployment/`) are clearly structured and properly labeled.
* **Command-Line Clarity:** Designing our CLI utilities (`setup.py`, `download.py`) with high-contrast monochrome formatting, clear section breaks, and descriptive plain-text prompts rather than relying solely on color cues.
* **Plain Language:** Explaining complex AI concepts, model architectures (QLoRA, GGUF), and installation instructions clearly and directly.

*Note: Formal conformance claims (such as WCAG targets) will be published following dedicated third-party evaluations as the project matures.*

## Contributor expectations

When contributing code, documentation, or tooling to Scalar Phos, we ask that you keep accessibility in mind:
* **Documentation & Markdown:** Use proper heading hierarchies (`#`, `##`, `###`), descriptive link text (avoiding generic phrases like "click here"), and clean code block formatting.
* **CLI & User Interfaces:** If you add or modify user-facing CLI scripts or web apps (e.g., Gradio components), ensure elements have proper text labels, keyboard navigation support, and fallback behaviors for non-visual users.
* **Pull Request Context:** Include notes in your pull request describing how user-facing changes were tested for accessibility or readability.

## Reporting accessibility issues

If you encounter an accessibility barrier while using our documentation, CLI tools, or web applications, please let us know so we can fix it. 

You can report barriers by opening an issue on our [GitHub Issues tab](https://github.com/scalar-ai/scalar-phos/issues) and selecting the **Bug Report** template, or by starting a discussion in our community channel. 

Please provide as much helpful context as you can, such as:
* The task you were trying to complete.
* The specific command, script, or URL involved.
* The observed behavior versus what you expected.
* Your operating system, terminal emulator, browser, or assistive technology (optional).

### Severity

We prioritize accessibility issues based on how strongly they affect a user's ability to participate:
* **Low:** Minor typographical, contrast, or formatting glitches in documentation that do not block understanding.
* **Medium:** Awkward navigation or missing labels in CLI scripts or web apps that slow down task completion.
* **High / Critical:** Complete blocks preventing screen reader users or keyboard-only users from executing core scripts (`setup.py`, `download.py`) or reading documentation.

### How we respond

Maintainers will review reported accessibility issues during standard triage cycles. You can expect:
* An initial response or acknowledgment within 3 to 5 business days.
* Status tracking via GitHub issue labels.
* Collaborative testing with reporters where feasible to verify fixes.

## Ownership and maintenance

Accessibility maintenance is overseen jointly by the **Scalar Phos core maintainers**. Responsibilities include reviewing incoming accessibility feedback, auditing documentation structure, and ensuring new code contributions adhere to our usability standards. Ownership is reviewed biannually during community roadmap updates.

## Supported environments

Scalar Phos tooling and interfaces have been tested across the following environments:
* **Operating Systems:** Linux (Ubuntu 22.04+), macOS (Ventura / Sonoma / Sequoia), and Windows 11 (WSL2 and native PowerShell).
* **Terminals:** Standard modern terminal emulators supporting UTF-8 encoding and ANSI escape codes.
* **Web Browsers (for Gradio Chat UI):** Latest stable releases of Google Chrome, Mozilla Firefox, Apple Safari, and Microsoft Edge.
* **Assistive Technologies:** Standard screen readers (such as VoiceOver and NVDA) interacting with structured markdown documentation and web components.

## Known limitations

We are actively working to improve, but acknowledge the following current limitations:
* **CLI Color Telemetry:** Our diagnostic script (`setup.py`) and downloader (`download.py`) use ANSI terminal colors and box-drawing characters for visual clarity. While functional in standard terminals, some custom screen-reader configurations may read these characters aloud. We plan to add a plain-text/no-color flag in a future release.
* **Complex Math Notation:** Advanced mathematical formulas in research guides may occasionally lack full semantic markup.

## Feedback and improvements

We welcome suggestions on how to improve this accessibility statement or our project practices. If you have ideas or feedback, please open a pull request or start a discussion in the repository. For active barriers, please use the issue reporting process outlined above.
