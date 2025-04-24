# daily arXiv digest - LLM-enhanced

<<<<<<< HEAD
# How to use
This repo will daily crawl arXiv papers about **cs.CV and cs.CL**, and use **DeepSeek** to summarize the papers in **Chinese**.
If you wish to crawl other arXiv categories, use other LLMs or other language, please follow the bellow instructions.
=======
## About

This tool will daily crawl [https://arxiv.org](https://arxiv.org) and use LLMs to summarize them.

> This project is based on [dw-dengwei/daily-arXiv-ai-enhanced](https://github.com/dw-dengwei/daily-arXiv-ai-enhanced), with custom enhancements and changes.

## How to use

This repo will daily crawl arXiv papers about **cs.HC, cs.LG, cs.CL**, and use **ChatGPT** to summarize the papers.
If you wish to crawl other arXiv categories or use other LLMs, please follow the bellow instructions.
>>>>>>> 6d1eb9e (refactor: redesign ai package logic and generate logic)
Otherwise, you can directly use this repo. Please star it if you like :)

**Instructions:**

1. Fork this repo to your own account
2. Go to: your-own-repo -> Settings -> Secrets and variables -> Actions
3. Go to Secrets. Secrets are encrypted and are used for sensitive data
4. Create two repository secrets named `OPENAI_API_KEY`, and input corresponding values.
5. Go to Variables. Variables are shown as plain text and are used for non-sensitive data
6. Create the following repository variables:
    1. `CATEGORIES`: separate the categories with ",", such as "cs.HC,cs.LG,cs.CL"
    2. `MODEL_NAME` such as "gpt-4o-mini"
7. Go to your-own-repo -> Actions -> `daily-arXiv-digest`
8. You can manually click **Run workflow** to test if it works well (it may takes about one hour).
By default, this action will automatically run every day
You can modify it in `.github/workflows/run.yml`

## Content

_**Last update: April 24, 2025 at 09:14 PM**_

## 2025

### 📅 April 🌟

- [2025-04-24](data/2025-04-24.md)


## Related tools

- ICML, ICLR, NeurIPS list: [https://dw-dengwei.github.io/OpenReview-paper-list/index.html](https://dw-dengwei.github.io/OpenReview-paper-list/index.html)
