# Scalar AI — Acceptable Use Policy

**Last Updated:** 10 November 2026  
**Applies To:** All models, adapters, GGUF binaries, code, and datasets released by **Scalar AI** (including but not limited to `scalar-phos-pro`, `scalar-phos-flash`, and derivative weights).

---

## 1. Overview

At **Scalar AI**, our mission is to advance high-performance, open-weights language models through precision fine-tuning and quantization. We believe in open, accessible, and transparent AI development. To ensure our models are used safely, ethically, and responsibly, all downstream users, developers, and organizations must adhere to this Acceptable Use Policy.

By downloading, deploying, fine-tuning, or interacting with any Scalar AI model weights or artifacts, you agree to comply with this policy in full.

---

## 2. Universal Standards & Base License Adherence

Scalar AI models are built upon foundational open-source architectures (such as Meta's Llama family and Qwen series).

1. **Upstream License Compliance:** Users must strictly comply with the underlying base model license agreement (e.g., the *Llama 3.1 / 3.2 Community License Agreement*).
2. **Attribution:** Any public deployment, service, or fine-tune derived from Scalar AI weights should retain appropriate attribution to Scalar AI and the underlying base architecture.

---

## 3. Prohibited Uses

You may **NOT** use Scalar AI models, directly or indirectly, for any of the following purposes:

### 3.1 Illegal & Harmful Activities
* **Criminal Acts:** Generating content that promotes, facilitates, or encourages illegal activities, violence, or severe physical harm.
* **Cyberattacks & Exploits:** Generating malicious software, exploiting software vulnerabilities, or conducting unauthorized network intrusion or phishing attacks.
* **Child Exploitation:** Creating, distributing, or promoting child sexual abuse material (CSAM) or any content that exploits or harms minors.

### 3.2 Deception & Disinformation
* **Impersonation:** Generating false representations of real individuals, organizations, or government entities without clear disclosure.
* **Coordinated Inauthentic Behavior:** Generating automated spam, fake reviews, or large-scale dis/misinformation campaigns targeting public elections, civil processes, or public health.
* **Undisclosed AI Generation:** Deploying user-facing automated agents without informing end-users that they are interacting with an artificial intelligence system.

### 3.3 High-Risk Decision Making Without Human Oversight
* **Automated High-Stakes Decisions:** Using model outputs as the sole decision-maker for legal judgments, credit scoring, employment eligibility, housing access, or law enforcement.
* **Medical & Emergency Guidance:** Utilizing model outputs to provide unverified medical diagnoses, critical triage advice, or self-harm instructions.
* **Critical Infrastructure:** Controlling or operating life-critical infrastructure (e.g., power grids, aviation control, nuclear systems).

### 3.4 Harassment & Abuse
* **Hate Speech & Harassment:** Generating content that incites violence, promotes hatred, or encourages discrimination against individuals or groups based on race, ethnicity, religion, disability, gender, age, sexual orientation, or gender identity.
* **Non-Consensual Intimate Imagery:** Generating or manipulating non-consensual sexual or intimate content.

---

## 4. Responsible Deployment Recommendations

When deploying Scalar AI models (via LoRA, merged checkpoints, or GGUF quantization) into production environments, developers are strongly encouraged to:

1. **Implement Safety Guardrails:** Use output moderation filters, input sanitization, and system prompts tailored to your specific application domain.
2. **Conduct Domain Testing:** Test and evaluate fine-tuned checkpoints against relevant safety and domain-accuracy benchmarks prior to public launch.
3. **Maintain Human-in-the-Loop Oversight:** Keep qualified human oversight for high-risk applications involving domain-specific legal, financial, or technical advice.

---

## 5. Disclaimer of Liability

Scalar AI releases its open-weights models, code, and documentation **"AS IS" WITHOUT WARRANTY OF ANY KIND**, express or implied. Large language models can occasionally produce inaccurate, biased, or unexpected outputs ("hallucinations"). Scalar AI is not liable for any direct, indirect, incidental, or consequential damages resulting from the use or misuse of our released models.

---

## 6. Feedback & Reporting Violations

If you discover safety vulnerabilities, potential policy violations, or safety concerns regarding any Scalar AI model checkpoint, please reach out to us:

* **Hugging Face Community Tab:** [@scalar-ai](https://huggingface.co/scalar-ai)

We welcome community feedback and collaboration to make small, efficient AI safer for everyone.
