# Contributing to Derian's Cyber Class

Thank you for wanting to help improve Derian's Cyber Class! This guide explains how to add questions, fix errors, and submit improvements.

---

## Types of Contributions Welcome

- **New practice questions** for any of the four certification paths
- **Corrections** to existing questions or explanations
- **Content updates** when CompTIA releases a new exam version (e.g., SY0-801 replacing SY0-701)
- **UI improvements** — styling, accessibility, mobile responsiveness
- **New features** — study modes, performance tracking, exam simulation

---

## Before You Start

1. **Check for duplicates.** Search the existing questions in `index.html` before writing a new one. Each question should cover a unique topic or angle. The existing questions are stored in the `const RAW` JavaScript object near the top of the file.

2. **Map to an official exam objective.** Every question should align with a specific domain from CompTIA's official exam objectives:
   - [A+ Core 1 (220-1201) Objectives](https://www.comptia.org/training/resources/exam-objectives/comptia-a-220-1201-exam-objectives)
   - [A+ Core 2 (220-1202) Objectives](https://www.comptia.org/training/resources/exam-objectives/comptia-a-220-1202-exam-objectives)
   - [Network+ (N10-009) Objectives](https://www.comptia.org/training/resources/exam-objectives/comptia-network-n10-009-exam-objectives)
   - [Security+ (SY0-701) Objectives](https://www.comptia.org/training/resources/exam-objectives/comptia-security-sy0-701-exam-objectives)

3. **No brain dump material.** Questions must be original and written in your own words. Do not copy or closely paraphrase questions from actual CompTIA exams, practice test vendors, or any paid/unpaid brain dump source.

---

## Question Format

All questions follow this exact JSON schema. Your question **must** match this structure:

```json
{
  "domain": "Domain 1 – Mobile Devices",
  "topic": "Wireless Charging",
  "difficulty": "easy",
  "question": "The full question text ending in a question mark?",
  "choices": {
    "A": "First answer choice",
    "B": "Second answer choice",
    "C": "Third answer choice",
    "D": "Fourth answer choice"
  },
  "answer": "B",
  "explanation": "A detailed explanation covering: why the correct answer is right, why each wrong answer is wrong, the underlying concept, any exam tips, and related topics. Good explanations are 150–400 words."
}
```

### Field Rules

| Field | Rules |
|-------|-------|
| `domain` | Must match the exact domain string used in that cert path. See examples below. |
| `topic` | Short label for the topic (2–5 words). Used for filtering. |
| `difficulty` | `"easy"`, `"medium"`, or `"hard"` |
| `question` | The question text. Should be clear and unambiguous. Avoid trick questions. |
| `choices` | Exactly four choices: A, B, C, D. Each should be a plausible distractor. |
| `answer` | Single uppercase letter: `"A"`, `"B"`, `"C"`, or `"D"` |
| `explanation` | Thorough explanation. Teach the concept, not just the answer. Include exam tips where relevant. |

### Valid Domain Strings by Certification

**A+ Core 1 (QUESTIONS_APLUS1):**
- `"Domain 1 – Mobile Devices"`
- `"Domain 2 – Networking"`
- `"Domain 3 – Hardware"`
- `"Domain 4 – Virtualization and Cloud Computing"`
- `"Domain 5 – Hardware and Network Troubleshooting"`

**A+ Core 2 (QUESTIONS_APLUS2):**
- `"Domain 1 – Operating Systems"`
- `"Domain 2 – Security"`
- `"Domain 3 – Software Troubleshooting"`
- `"Domain 4 – Operational Procedures"`

**Network+ (QUESTIONS_NETPLUS):**
- `"Domain 1 – Networking Concepts"`
- `"Domain 2 – Network Implementation"`
- `"Domain 3 – Network Operations"`
- `"Domain 4 – Network Security"`
- `"Domain 5 – Network Troubleshooting"`

**Security+ (QUESTIONS — the legacy key name):**
- Use the official SY0-701 domain names.

---

## Writing a Good Question

### ✅ Do
- Base questions on real-world IT scenarios ("A technician notices..." / "A user reports...")
- Write plausible wrong answers that a less-prepared student might choose
- Use the explanation to teach the broader concept, not just confirm the answer
- Include memory aids, mnemonics, or comparison tables in explanations where helpful
- Mention related topics that are likely to appear in the same exam section
- Cross-reference related ports, speeds, standards, and terminology

### ❌ Don't
- Write questions with trick phrasing designed to mislead rather than test knowledge
- Use "all of the above" or "none of the above" as answer choices
- Write one-line explanations — they don't help students learn
- Add questions that are identical in concept to an existing question (even with different wording)
- Include vendor-specific content not covered by CompTIA objectives (e.g., Cisco IOS commands not tested on Network+)

---

## Where to Insert Questions

Open `index.html` and find the `const RAW = {` declaration near the top of the `<script>` section. The question arrays for each certification are:

- A+ Core 1: `QUESTIONS_APLUS1: [...]`
- A+ Core 2: `QUESTIONS_APLUS2: [...]`
- Network+: `QUESTIONS_NETPLUS: [...]`
- Security+: `QUESTIONS: [...]`

Add your new question object to the end of the appropriate array, before the closing `]`. Make sure to add a comma after the previous question's closing `}` before your new question.

Example:
```javascript
// ...existing last question...
  {
    "domain": "Domain 3 – Hardware",
    "topic": "Existing Topic",
    // ...
  },          // <-- comma here
  {
    "domain": "Domain 3 – Hardware",
    "topic": "Your New Topic",
    "difficulty": "easy",
    "question": "Your new question?",
    "choices": { "A": "...", "B": "...", "C": "...", "D": "..." },
    "answer": "A",
    "explanation": "Your detailed explanation..."
  }           // <-- no comma on the last entry
]
```

---

## Updating the UI Question Counts

After adding questions, update the displayed counts in two places in `index.html`:

1. **Splash screen banner** — search for `QUESTIONS READY` and update the number.
2. **Cert card stat** — search for the cert's color code and update the Questions stat value:
   - A+ Core 1: `color:#ff8c42`
   - A+ Core 2: `color:#ff4466`
   - Network+: `color:#4db8ff`
   - Security+: `color:#00d4c8`
3. **Cert meta line** — search for the cert's pass score (e.g., `Pass: 675 scaled`) and update the question count at the end of the line.

---

## Submitting Your Changes

1. Fork the repository on GitHub.
2. Create a new branch:
   ```bash
   git checkout -b add-aplus1-storage-questions
   ```
3. Make your changes to `index.html` (and update this README if the question counts changed).
4. Verify the JSON is still valid — paste the `RAW` object contents into [jsonlint.com](https://jsonlint.com) to check for syntax errors.
5. Open `index.html` in a browser and test your new questions manually.
6. Submit a Pull Request with a clear description of what you added or changed.

---

## Reporting Issues

If you find an incorrect answer, a poorly worded explanation, outdated content, or a UI bug, please open a GitHub Issue with:

- The question text (or a screenshot)
- What the current answer/explanation says
- What it should say, with a source or reference

---

## Code of Conduct

Be respectful, constructive, and helpful. This is a free study resource built to help people pass their IT certifications — contributions should serve that mission.
