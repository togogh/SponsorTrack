<a id="readme-top"></a>

# 🛰️ SponsorTrack

**Extract, analyze, and organize YouTube sponsorship data using FastAPI, Gradio, and SponsorBlock.**

[![License](https://img.shields.io/github/license/togogh/SponsorTrack?style=for-the-badge)](LICENSE)
![Last Commit](https://img.shields.io/github/last-commit/togogh/SponsorTrack?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/togogh/SponsorTrack?style=for-the-badge)
![Issues](https://img.shields.io/github/issues/togogh/SponsorTrack?style=for-the-badge)

[View Demo](https://huggingface.co/spaces/togogh/SponsorTrack) • [View API Docs](https://api.sponsortrack.org/docs)

---

## 📚 Table of Contents

- [About The Project](#-about-the-project)
- [Built With](#-built-with)
- [Getting Started](#-getting-started)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

<!-- ABOUT THE PROJECT -->
## 📖 About The Project

![SponsorTrack Screen Shot][product-screenshot]

SponsorTrack is an open-source Python project that extracts and compiles Youtube sponsorship information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## 🧰 Built With

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-FF4B4B?style=for-the-badge&logo=gradio&logoColor=white)

[![Uses youtube-transcript-api](https://img.shields.io/badge/Uses-youtube--transcript--api-blue?style=for-the-badge)](https://github.com/jdepoix/youtube-transcript-api)
[![Uses SponsorBlock](https://img.shields.io/badge/Uses-SponsorBlock-purple?style=for-the-badge)](https://github.com/ajayyy/SponsorBlock)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## 🥁 Getting Started

<details>
<summary><strong>🖥️ Hosted (For End Users)</strong></summary>

1. Go to the [HF Space](https://huggingface.co/spaces/togogh/SponsorTrack) where the app is hosted.
2. Plug in a Youtube URL/id, and hit submit. Sponsorship information like the sponsor's name, available coupon codes, and links, should populate the page shortly.

</details>

<details>
<summary><strong>💻 Local Setup (For Developers)</strong></summary>

#### Prerequisites

- [python](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- postgres db (if hosted, ssh details are needed in .env)
    - create 3 schemas: prod, dev, and test
- [Huggingface](https://huggingface.co/) and/or [OpenRouter](https://openrouter.ai/) account 

#### Installation

1. Clone the repo

2. Create a .env file in the project root directory and set the env vars needed in [settings.py](src/backend/core/settings.py)

3. (If using SSH) SSH into the server hosting your postgres db by running
    ```sh
    ./sshdb.sh
    ```

4. Populate your schemas with tables using:
    ```sh
    python src/backend/utils/refresh_schema.py schema_name
    ```
    Replace `schema_name` with the name of the schema you want to populate (ex. `python src/backend/utils/refresh_schema.py dev`)

5. Start the backend server
    ```sh
    uv run fastapi run src/backend/main.py
    ```
    The terminal should say that the server is running, and you should be able to open http://127.0.0.1:8000/docs (though you might need to replace the host) and see the API docs

6. In a separate terminal, start the frontend server
    ```sh
    uv run src/frontend/app.py
    ```
    You should see a message like:
    ```sh
    * Running on local URL:  http://127.0.0.1:7860
    ```
    If you open the link, you should be able to see the Gradio UI

7. In the app, input the Youtube URL/id you want to get sponsorship info of

8. After a little wait, the app will populate with this info
</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## 🛣 Roadmap

- [x] Local Gradio app to get YT sponsorship info
- [x] Hosted Gradio app - Currently in [HuggingFace Spaces](https://huggingface.co/spaces/togogh/SponsorTrack)
- [x] Hosted database for storing sponsorship info - Currently hosted in Droplet
- [x] API service
- [ ] Queuing / Batching
- [ ] Review mechanism
- [ ] Web app with charts and stats (similar to [Graphtreon](https://graphtreon.com/))
- [ ] Sponsored segment predictor

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## 📥 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
    - Every commit is checked and formatted with ruff. If your commit fails, that means it needs further cleaning. Simple formatting changes are automatically fixed by ruff, you just need to stage them to your commit. But more complex fixes may be needed, ruff will specify where.
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
    - You need at least 1 approval before you can merge to main
    - Every merge runs pytest to make sure new changes don't break the project. Please run `uv run pytest` before creating a pull request so you don't run into issues with merging later (note that a test schema is required for several of these tests).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## 📰 License

Distributed under the GNU GPLv3 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: images/screenshot.png
