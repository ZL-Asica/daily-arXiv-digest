# Daily arXiv Digest (LLM-enhanced)

## About

This tool will daily crawl [https://arxiv.org](https://arxiv.org) and use LLMs to summarize them (based on arXiv summary, comments, and raw pdf file). It also rate the suitability of the paper for you based on your personal background.

## Contents

_**Last update: April 26, 2025 at 05:28 PM**_

### 2025

#### 📅 April 🌟

- [2025-04-26](contents/2025-04-26.md)
- [2025-04-25](contents/2025-04-25.md)
- [2025-04-24](contents/2025-04-24.md)


## How to use

This repo will daily crawl arXiv papers about **cs.HC, cs.LG, cs.CL**, and use **ChatGPT** to summarize the papers.
If you wish to crawl other arXiv categories or use other LLMs, please follow the bellow instructions.
Otherwise, you can directly use this repo. Please star it if you like :)

**Instructions:**

1. Fork this repo to your own account
2. Go to: your-own-repo -> Settings -> Secrets and variables -> Actions
3. Go to Secrets (Secrets are encrypted and are used for sensitive data). Create two repository secrets:
   1. `OPENAI_API_KEY`: your OpenAI API key for model call
   2. `USER_BACKGROUND`: your personal background (prefer third person view), this will be injected into the system side prompt for the LLM to better assist and ranking whether the paper is useful for you. You can use Markdown syntax to format it. For example:
      ```makrdown
      The user is a PhD student in computer science who is interested in Human-Computer Interaction and natural language processing. She has a background in deep learning and has published several papers in top-tier conferences.
      ```
4. Go to Variables (Variables are shown as plain text and are used for non-sensitive data). Create the following repository variables:
    1. `CATEGORIES`: separate the categories with ",", such as "cs.HC,cs.LG,cs.CL"
    2. `MODEL_NAME` such as "gpt-4o-mini"
5. Go to your-own-repo -> Actions -> `daily-arXiv-digest`
6. You can manually click **Run workflow** to test if it works well (it may takes about half hour).
By default, this action will automatically run every day
You can modify it in `.github/workflows/run.yml`

## Related tools

> This project is based on [dw-dengwei/daily-arXiv-ai-enhanced](https://github.com/dw-dengwei/daily-arXiv-ai-enhanced), with custom enhancements and changes.

- ICML, ICLR, NeurIPS list: [https://dw-dengwei.github.io/OpenReview-paper-list/index.html](https://dw-dengwei.github.io/OpenReview-paper-list/index.html)
