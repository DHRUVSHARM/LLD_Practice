## 🎯 Purpose

This repository provides a realistic simulation environment to prepare for **CodeSignal's Industry Coding Framework (ICF)** assessments. It mirrors the actual test format with multi-level coding problems where each subsequent level builds upon the previous one. This also serves as practice for LLD type questions 

Will continue to update with more questions and my customn solutions to them 

My solutions for each problem is under simulation.py 

## 💡 Inspiration

I've long observed that coding assessments—whether CodeSignal, LeetCode, or others—ultimately come down to **practice**. However, CodeSignal's platform doesn't offer practice tests that closely resemble their actual assessments.

After reading [How hackable are automated coding assessments?](https://yanirseroussi.com/2023/05/26/how-hackable-are-automated-coding-assessments/), I came to a deep realization: **CodeSignal is no different than the SAT**. More practice will definitively boost your score. This repo exists to fill that gap—giving you a realistic practice environment so you can walk into your assessment with confidence.

## 📊 Scoring & What You Need to Pass

### Score to Percentile Conversion

CodeSignal provides a [conversion table](https://support.codesignal.com/hc/en-us/articles/13260678794775-Converting-Historical-Coding-Score-Thresholds-to-Assessment-Score) to translate your score to a percentile ranking.

## 🚀 Usage

### Prerequisites

- Python 3.10+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/LibreSignal.git
   cd LibreSignal
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Implementing Your Solution

1. Navigate to the question folder (e.g., `Questions/bank_system/`)
2. Read the problem description in the level markdown files (`level1.md`, `level2.md`, etc.)
3. Implement your solution in `simulation.py`
4. **Start with Level 1 and progress sequentially** — just like the real test!

### Running Tests

Each level has its own test suite. Run tests for a specific level from the <u>**root directory**</u>:

#### 🏦 Bank System

```bash
# Test a specific level
pytest Questions/bank_system/test_bank_system.py::TestLevel1 -v
pytest Questions/bank_system/test_bank_system.py::TestLevel2 -v
pytest Questions/bank_system/test_bank_system.py::TestLevel3 -v
pytest Questions/bank_system/test_bank_system.py::TestLevel4 -v

# Run all tests
pytest Questions/bank_system/test_bank_system.py -v
```

#### 🗄️ In-Memory Database

```bash
# Test a specific level
pytest Questions/in_memory_database/test_in_memory_database.py::TestLevel1 -v
pytest Questions/in_memory_database/test_in_memory_database.py::TestLevel2 -v
pytest Questions/in_memory_database/test_in_memory_database.py::TestLevel3 -v
pytest Questions/in_memory_database/test_in_memory_database.py::TestLevel4 -v

# Run all tests
pytest Questions/in_memory_database/test_in_memory_database.py -v
```

## 📁 Project Structure

```
LibreSignal/
├── README.md
├── requirements.txt
└── Questions/
    ├── bank_system/
    │   ├── level1.md               # Level 1 requirements
    │   ├── level2.md               # Level 2 requirements
    │   ├── level3.md               # Level 3 requirements
    │   ├── level4.md               # Level 4 requirements
    │   ├── simulation.py           # Your implementation goes here
    │   ├── simulation_solution.py  # Reference solution
    │   └── test_bank_system.py     # Test suite
    └── in_memory_database/
        ├── level1.md               # Level 1 requirements
        ├── level2.md               # Level 2 requirements
        ├── level3.md               # Level 3 requirements
        ├── level4.md               # Level 4 requirements
        ├── simulation.py           # Your implementation goes here
        ├── simulation_solution.py  # Reference solution
        └── test_in_memory_database.py  # Test suite
```

## 📚 Official Documentation

For a deeper understanding of how CodeSignal's ICF works, refer to the official technical brief:

📄 [Industry Coding Skills Evaluation Framework Technical Brief](https://discover.codesignal.com/rs/659-AFH-023/images/Industry-Coding-Skills-Evaluation-Framework-CodeSignal-Skills-Evaluation-Lab-Short.pdf)

## ⏱️ Test Day Tips

1. **Read ALL levels first** — Understanding what's coming helps you design a modular solution from the start
2. **Don't over-engineer Level 1** — But do set up proper data structures
3. **Test frequently** — Run the test suite after implementing each method
4. **Manage your time** — ~70 minutes total, so roughly 15-20 min per level
5. **Partial credit exists** — If stuck on Level 4, make sure Levels 1-3 are solid

## 🤝 Contributing

Found a bug? Have a new question to add? Contributions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-question`)
3. Commit your changes (`git commit -m 'Add new question set'`)
4. Push to the branch (`git push origin feature/new-question`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

**Good luck with your assessment!** 🍀

*Remember: It's just practice. The more you do, the better you get.*

---

**Last Updated:** March 2, 2026  
*Made with [I-hate-doing-meaningless-coding-questions-but-I-want-a-job mindset] in Boston*
