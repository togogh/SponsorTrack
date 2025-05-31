<a id="readme-top"></a>

<!-- ABOUT THE PROJECT -->
## About The Project

![SponsorTrack Screen Shot][product-screenshot]

[View Demo]("https://huggingface.co/spaces/togogh/SponsorTrack")

SponsorTrack is an open-source Python project that extracts and compiles Youtube sponsorship information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Hosted
Do this if you just want to get sponsorship information

1. Go to the [HF Space]("https://huggingface.co/spaces/togogh/SponsorTrack") where the app is hosted.
2. Plug in a Youtube URL, and hit submit. Sponsorship information (Who sponsored this video? What offers did they have? What links did they share?) will populate the page shortly.

### Local
Do this if you want to edit the code

#### Prerequisites

- [python](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [HuggingFace account](https://huggingface.co)
- (Optional - to avoid IpBlock errors when querying Youtube) [WebShare Proxies](https://www.webshare.io/?referral_code=vxw83x5vljc7)

#### Installation

1. Create a [new HuggingFace token](https://huggingface.co/settings/tokens/new?ownUserPermissions=inference.serverless.write&tokenType=fineGrained) with "Make calls to Inference Providers" enabled.

    (Optional) Sign up for the Rotating Residential proxies plan in Webshare (the Free tier or Static Residential plan won't work). Then change your connection method to Rotating Proxy Endpoint and take note of your proxy username and password.

2. Clone the repo
3. Create a .env file in the project root directory and set the following variables:
    - HF_TOKEN = HuggingFace token
    - WS_PROXY_UN = Webshare proxy username
    - WS_PROXY_PW = Webshare proxy password
4. Start the app server
    ```sh
    uv run --env-file .env src\sponsortrack\frontend\app.py
    ```
5. Open the localhost/public url where the server is running
6. In the app, input the Youtube URL you want to get sponsorship info of
7. After a little wait, the app will populate with this info

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] Local Gradio app to get YT sponsorship info
- [x] Hosted Gradio app - Currently in [HuggingFace Spaces](https://huggingface.co/spaces/togogh/SponsorTrack)
- [ ] Hosted database for storing sponsorship info
- [ ] Web app with charts and stats (similar to [Graphtreon](https://graphtreon.com/))

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

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
    - Every merge runs pytest to make sure new changes don't break the project. Please run `uv run pytest` before creating a pull request so you don't run into issues with merging later.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: images/screenshot.png