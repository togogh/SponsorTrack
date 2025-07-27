import gradio as gr
import requests
from requests.adapters import HTTPAdapter, Retry
from urllib.parse import urlencode

s = requests.Session()
retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
s.mount("https://", HTTPAdapter(max_retries=retries))


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
    url = f"https://api.sponsortrack.org/videos/sponsorships/?{encoded_params}"

    response = s.get(url)
    sponsorship_info = response.json()
    return "", "", sponsorship_info


def flag(field, id, entity, input):
    if entity == "video":
        url = f"https://api.sponsortrack.org/videos/flag?youtube_id={id}"
    elif entity == "sponsorship":
        url = f"https://api.sponsortrack.org/videos/sponsorships/flag?sponsorship_id={id}"
    elif entity == "sponsored_segment":
        url = f"https://api.sponsortrack.org/videos/sponsored-segments/flag?sponsorship_id={id}"
    data = {"field_flagged": field}
    response = s.post(url, json=data)
    if response.status_code == 200:
        gr.Info(f"Flagged {field}.")
    return input


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("""
# SponsorTrack
                    
Extract sponsorship information from Youtube videos
                    
Want to use the API instead? [View API docs](https://api.sponsortrack.org/docs)
            """)
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
                    found = gr.Markdown(
                        value=f"Found {len(arr)} sponsored segment{'' if len(arr) == 1 else 's'} for https://www.youtube.com/watch?v={sponsorship_info['youtube_id']}",
                        label="Results",
                    )
                    num_sponsored_segments_btn = gr.Button("Flag wrong # of sponsored segments")
                    num_sponsored_segments_btn.click(
                        lambda x: flag("num_sponsored_segments", youtube_id, "video", x),
                        [found],
                        [found],
                    )

                    video_previews = []
                    descriptions = []
                    offers = []
                    links = []
                    coupon_codes = []

                    for i, sponsorship in enumerate(arr):
                        sponsorship_id = sponsorship["id"]
                        with gr.Accordion(label=f"{sponsorship['sponsor_name']}", open=False):
                            sponsor_name_btn = gr.Button("Flag wrong sponsor name")
                            sponsor_name_btn.click(
                                lambda: flag("sponsor_name", sponsorship_id, "sponsorship", None),
                                [],
                                [],
                            )
                            video_previews.append(
                                gr.HTML(
                                    label="Video Preview",
                                    value=f"""
                                <iframe
                                    src="https://www.youtube.com/embed/{youtube_id}?start={int(sponsorship["start_time"])}"
                                    frameborder="0"
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                                    referrerpolicy="strict-origin-when-cross-origin"
                                    style="margin: 0 auto; display: block; width: 100%; aspect-ratio: 16 / 9;"
                                    allowfullscreen>
                                </iframe>""",
                                )
                            )
                            start_time_btn = gr.Button("Flag wrong start time")
                            start_time_btn.click(
                                lambda x, sponsorship_id=sponsorship_id: flag(
                                    "start_time", sponsorship_id, "sponsored_segment", x
                                ),
                                [video_previews[i]],
                                [video_previews[i]],
                            )
                            descriptions.append(
                                gr.TextArea(
                                    label="Description",
                                    value=sponsorship["sponsor_description"],
                                )
                            )
                            sponsor_description_btn = gr.Button("Flag wrong description")
                            sponsor_description_btn.click(
                                lambda x, sponsorship_id=sponsorship_id: flag(
                                    "sponsor_description", sponsorship_id, "sponsorship", x
                                ),
                                [descriptions[i]],
                                [descriptions[i]],
                            )
                            offers.append(
                                gr.TextArea(label="Offer", value=sponsorship["sponsor_offer"])
                            )
                            sponsor_offer_btn = gr.Button("Flag wrong offer")
                            sponsor_offer_btn.click(
                                lambda x, sponsorship_id=sponsorship_id: flag(
                                    "sponsor_offer", sponsorship_id, "sponsorship", x
                                ),
                                [offers[i]],
                                [offers[i]],
                            )
                            links.append(
                                gr.TextArea(
                                    label="Links",
                                    value=sponsorship["sponsor_links"],
                                )
                            )
                            sponsor_links_btn = gr.Button("Flag wrong links")
                            sponsor_links_btn.click(
                                lambda x, sponsorship_id=sponsorship_id: flag(
                                    "sponsor_links", sponsorship_id, "sponsorship", x
                                ),
                                [links[i]],
                                [links[i]],
                            )
                            coupon_codes.append(
                                gr.TextArea(
                                    label="Coupon Code",
                                    value=sponsorship["sponsor_coupon_code"],
                                )
                            )
                            sponsor_coupon_code_btn = gr.Button("Flag wrong coupon code")
                            sponsor_coupon_code_btn.click(
                                lambda x, sponsorship_id=sponsorship_id: flag(
                                    "sponsor_coupon_code", sponsorship_id, "sponsorship", x
                                ),
                                [coupon_codes[i]],
                                [coupon_codes[i]],
                            )
                except Exception:
                    pass


demo.queue().launch(show_error=True)
