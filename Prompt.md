# 🎯 Mission: Initialize Mobile Automation Framework

**Role**: You are a Senior SDET & Software Architect.
**Context**: You are building a scalable, 3-layer Mobile Automation Framework (Appium + Pytest + Allure) based on the "Design as Constraint" philosophy.

## 🧠 Memory Bank Activation (CRITICAL)
Before writing a single line of code, you MUST read and internalize the following files in `.vscode/memory-bank/`:
1.  **`architecture.md`**: This is the LAW. Do not violate the 3-layer structure (Pages/Workflows/TestCases).
2.  **`tech-stack.md`**: Use ONLY the libraries listed here (e.g., Appium-Python-Client > 3.1.0, Loguru).
3.  **`implementation-plan.md`**: This is your roadmap.
4.  **`product-requirements.md`**: This is your acceptance criteria.
5.  **`progress.md`**: You must update this file after completing tasks.

## ⚡ Operational Rules (The "Vibe" Protocols)
1.  **Skeleton First**: When implementing a class, verify against the User's Specs. If specs are generic, follow standard POM patterns.
2.  **No Hallucinations**: Do not import libraries that are not in `requirements.txt` or `tech-stack.md`.
3.  **Strict Typing**: Use Python type hints (`def func(self, name: str) -> bool:`) everywhere.
4.  **Auto-Documentation**: Add docstrings to every public method explaining *what* it does.
5.  **Self-Correction**: If you edit a file, verify it doesn't break `architecture.md` rules (e.g., NO assertions in Pages).

## 🎬 Action Item: Phase 1.1 & 1.2
I want you to start the implementation now.

**Step 1**: Check `implementation-plan.md`. We are at **Phase 1: Infrastructure**.
**Step 2**: Create the directory structure exactly as defined in the Architecture.
**Step 3**: Create the foundational files:
   - `requirements.txt` (Populate it with the content we defined).
   - `.gitignore` (Populate it with the content we defined).
   - `pytest.ini` (Basic config).
   - `.env.example` (Template).
   - `config/global_config.py` (Basic skeleton).
   - `utils/file_helper.py` (Implement `get_project_root` immediately as it is a dependency for everything else).

**Step 4**: When you are done with the file creation, check off `[x]` the corresponding items in `progress.md` and report back to me.

**GO.**