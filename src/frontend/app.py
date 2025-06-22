import gradio as gr
import requests
from requests.adapters import HTTPAdapter, Retry
from urllib.parse import urlencode


def submit(youtube_id, youtube_url):
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])

    s.mount("http://", HTTPAdapter(max_retries=retries))
    if youtube_id != "":
        if youtube_url != "":
            raise ValueError("Only 1 of id or url must be submitted")
        params = {
            "id": youtube_id,
        }
    else:
        if youtube_url != "":
            params = {
                "url": youtube_url,
            }
        else:
            raise ValueError("1 of id or url must be submitted.")

    encoded_params = urlencode(params)
    url = f"http://127.0.0.1:8000/videos/sponsorships/?{encoded_params}"

    response = s.get(url)
    sponsorship_info = response.json()
    return "", "", sponsorship_info


callback = gr.CSVLogger(dataset_file_name="flagged_sponsorships.csv")

with gr.Blocks() as demo:
    with gr.Row():
        gr.Markdown("""
# SponsorTrack
Extract sponsorship information from Youtube videos
        """)

    with gr.Row():
        with gr.Column(scale=1):
            id = gr.Textbox(label="Youtube ID", placeholder="XXXXXXXX")
            url = gr.Textbox(
                label="Youtube URL", placeholder="https://www.youtube.com/watch?v=XXXXXXXX"
            )
            examples = gr.Examples(
                examples=[
                    ["9sTsI4tpATk", ""],
                    ["rhgwIhB58PA", ""],
                    ["", "https://youtu.be/ofKe4b169ts"],
                    ["", "https://youtu.be/NxCfacrnbFU"],
                    ["", "https://www.youtube.com/watch?v=AienZMjqAg4&t=424s"],
                ],
                inputs=[id, url],
            )
            submit_btn = gr.Button("Get Sponsor Info", variant="primary")
            sponsorship_info = gr.State([])
            submit_btn.click(
                fn=submit, inputs=[id, url], outputs=[id, url, sponsorship_info], api_name="submit"
            )

        with gr.Column(scale=2):

            @gr.render(inputs=[sponsorship_info])
            def render_count(sponsorship_info):
                try:
                    arr = sponsorship_info["sponsorships"]
                    found = gr.Markdown(
                        value=f"Found {len(arr)} sponsored segment{'' if len(arr) == 1 else 's'} for https://www.youtube.com/watch?v={sponsorship_info['youtube_id']}",
                        label="Results",
                    )
                    for i, sponsorship in enumerate(arr):
                        with gr.Accordion(label=f"{sponsorship['sponsor_name']}", open=False):
                            video_preview = gr.HTML(
                                label="Video Preview",
                                value=f"""
                                <iframe
                                    width="560"
                                    height="315"
                                    src="https://www.youtube.com/embed/{sponsorship["youtube_id"]}?start={int(sponsorship["start_time"])}"
                                    frameborder="0"
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                                    referrerpolicy="strict-origin-when-cross-origin"
                                    allowfullscreen>
                                </iframe>""",
                            )
                            description = gr.TextArea(
                                label="Description",
                                value=sponsorship["sponsor_description"],
                            )
                            offer = gr.Textbox(label="Offer", value=sponsorship["sponsor_offer"])
                            links = gr.Textbox(
                                label="Links",
                                value=sponsorship["sponsor_links"],
                            )
                            coupon_code = gr.Textbox(
                                label="Coupon Code", value=sponsorship["sponsor_coupon_code"]
                            )
                            callback.setup(
                                [found, video_preview, description, offer, links, coupon_code],
                                "data",
                            )
                            btn = gr.Button("Flag")
                            btn.click(
                                lambda *args: (callback.flag(list(args)), None)[1],
                                [found, video_preview, description, offer, links, coupon_code],
                                [],
                                preprocess=False,
                            )
                except Exception:
                    pass


demo.queue().launch(show_error=True)
