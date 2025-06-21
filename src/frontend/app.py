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
    segments_info = response.json()
    return "", "", segments_info


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
            segments = gr.State([])
            submit_btn.click(
                fn=submit, inputs=[id, url], outputs=[id, url, segments], api_name="submit"
            )

        with gr.Column(scale=2):

            @gr.render(inputs=segments)
            def render_count(arr):
                if len(arr) != 0:
                    gr.Markdown(
                        f"Found {len(arr)} sponsored segment{'' if len(arr) == 1 else 's'} for https://www.youtube.com/watch?v={arr[0]['youtube_id']}"
                    )
                    for i, segment in enumerate(arr):
                        with gr.Accordion(label=f"{segment['sponsor_name']}", open=False):
                            gr.HTML(f"""
                                <iframe
                                    width="560"
                                    height="315"
                                    src="https://www.youtube.com/embed/{segment["youtube_id"]}?start={int(segment["start_time"])}"
                                    frameborder="0"
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                                    referrerpolicy="strict-origin-when-cross-origin"
                                    allowfullscreen>
                                </iframe>""")
                            gr.TextArea(
                                label="Description",
                                value=segment["sponsor_description"],
                            )
                            gr.Textbox(label="Offer", value=segment["sponsor_offer"])
                            gr.Textbox(
                                label="Links",
                                value=", ".join(segment["sponsor_links"]),
                            )
                            gr.Textbox(label="Coupon Code", value=segment["sponsor_coupon_code"])


demo.queue().launch(show_error=True)
