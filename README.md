<a id="readme-top"></a>

<!-- ABOUT THE PROJECT -->
## About The Project

![SponsorTrack Screen Shot][product-screenshot]

SponsorTrack is an open-source Python project that makes it easy to keep track of Youtube sponsors.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

This project is currently set up to run locally.

### Prerequisites

- [python](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [HuggingFace account](https://huggingface.co)
- (Optional - to avoid IpBlock errors when querying Youtube) [NordVPN account](https://nordvpn.com/)

### Installation

1. Create a [new HuggingFace token](https://huggingface.co/settings/tokens/new?ownUserPermissions=inference.serverless.write&tokenType=fineGrained) with "Make calls to Inference Providers" enabled
2. Clone the repo
    ```sh
    git clone https://github.com/togogh/SponsorTrack.git
    ```
3. Create a .env file in the root directory and set HF_ACCESS_TOKEN to your new HuggingFace token 
4. (Optional) Add path to NordVPN in [config](src\sponsortrack\config.py) file
4. Start the app server
    ```sh
    uv run src\sponsortrack\frontend\app.py
    ```
5. Open the localhost url where the server is running
6. In the app, input the Youtube URL you want to get sponsorship info of
7. After a little wait, the app will populate with this info

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] Local Gradio app to get YT sponsorship info
- [ ] Hosted Gradio app + database for storing sponsorship info
- [ ] Web app with charts and stats

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: images/screenshot.png