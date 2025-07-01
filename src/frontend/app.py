import gradio as gr
import requests
from requests.adapters import HTTPAdapter, Retry
from urllib.parse import urlencode

s = requests.Session()
retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
s.mount("http://", HTTPAdapter(max_retries=retries))


def submit(youtube_id, youtube_url):
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


def flag(field, id, entity, input):
    if entity == "video":
        url = f"http://127.0.0.1:8000/videos/flag?youtube_id={id}"
    elif entity == "sponsorship":
        url = f"http://127.0.0.1:8000/videos/sponsorships/flag?sponsorship_id={id}"
    elif entity == "sponsored_segment":
        url = f"http://127.0.0.1:8000/videos/sponsored-segments/flag?sponsorship_id={id}"
    data = {"field_flagged": field}
    response = s.post(url, json=data)
    if response.status_code == 200:
        gr.Info(f"Flagged {field}.")
    return input


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
                    youtube_id = sponsorship_info["youtube_id"]
                    with gr.Row():
                        with gr.Column(scale=2):
                            found = gr.Markdown(
                                value=f"Found {len(arr)} sponsored segment{'' if len(arr) == 1 else 's'} for https://www.youtube.com/watch?v={sponsorship_info['youtube_id']}",
                                label="Results",
                            )
                        with gr.Column(scale=1):
                            num_sponsored_segments_btn = gr.Button("Flag: # of sponsored segments")
                            num_sponsored_segments_btn.click(
                                lambda x: flag("num_sponsored_segments", youtube_id, "video", x),
                                [found],
                                [found],
                            )

                    for i, sponsorship in enumerate(arr):
                        print(sponsorship)
                        sponsorship_id = sponsorship["id"]
                        with gr.Accordion(label=f"{sponsorship['sponsor_name']}", open=True):
                            sponsor_name_btn = gr.Button("Flag: Sponsor name")
                            sponsor_name_btn.click(
                                lambda: flag("sponsor_name", sponsorship_id, "sponsorship", None),
                                [],
                                [],
                            )
                            with gr.Row():
                                with gr.Column(scale=2):
                                    video_preview = gr.HTML(
                                        label="Video Preview",
                                        value=f"""
                                        <iframe
                                            width="560"
                                            height="315"
                                            src="https://www.youtube.com/embed/{youtube_id}?start={int(sponsorship["start_time"])}"
                                            frameborder="0"
                                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                                            referrerpolicy="strict-origin-when-cross-origin"
                                            allowfullscreen>
                                        </iframe>""",
                                    )
                                with gr.Column(scale=1):
                                    start_time_btn = gr.Button("Flag: Start time")
                                    start_time_btn.click(
                                        lambda x: flag(
                                            "start_time", sponsorship_id, "sponsored_segment", x
                                        ),
                                        [video_preview],
                                        [video_preview],
                                    )
                            with gr.Row():
                                with gr.Column(scale=2):
                                    description = gr.TextArea(
                                        label="Description",
                                        value=sponsorship["sponsor_description"],
                                    )
                                with gr.Column(scale=1):
                                    sponsor_description_btn = gr.Button("Flag: Description")
                                    sponsor_description_btn.click(
                                        lambda x: flag(
                                            "sponsor_description", sponsorship_id, "sponsorship", x
                                        ),
                                        [description],
                                        [description],
                                    )
                            with gr.Row():
                                with gr.Column(scale=2):
                                    offer = gr.TextArea(
                                        label="Offer", value=sponsorship["sponsor_offer"]
                                    )
                                with gr.Column(scale=1):
                                    sponsor_offer_btn = gr.Button("Flag: Offer")
                                    sponsor_offer_btn.click(
                                        lambda x: flag(
                                            "sponsor_offer", sponsorship_id, "sponsorship", x
                                        ),
                                        [offer],
                                        [offer],
                                    )
                            with gr.Row():
                                with gr.Column(scale=2):
                                    links = gr.TextArea(
                                        label="Links",
                                        value=sponsorship["sponsor_links"],
                                    )
                                with gr.Column(scale=1):
                                    sponsor_links_btn = gr.Button("Flag: Links")
                                    sponsor_links_btn.click(
                                        lambda x: flag(
                                            "sponsor_links", sponsorship_id, "sponsorship", x
                                        ),
                                        [links],
                                        [links],
                                    )
                            with gr.Row():
                                with gr.Column(scale=2):
                                    coupon_code = gr.TextArea(
                                        label="Coupon Code",
                                        value=sponsorship["sponsor_coupon_code"],
                                    )
                                with gr.Column(scale=1):
                                    sponsor_coupon_code_btn = gr.Button("Flag: Coupon code")
                                    sponsor_coupon_code_btn.click(
                                        lambda x: flag(
                                            "sponsor_coupon_code", sponsorship_id, "sponsorship", x
                                        ),
                                        [coupon_code],
                                        [coupon_code],
                                    )
                except Exception:
                    pass


demo.queue().launch(show_error=True)
