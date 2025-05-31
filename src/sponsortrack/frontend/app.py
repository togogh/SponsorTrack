import gradio as gr
from sponsortrack.backend.video import Video


def submit(url):
    video = Video(url)
    segments_info = video.fetch_segments_info()
    return "", segments_info


with gr.Blocks() as demo:
    with gr.Row():
        gr.Markdown("""
# SponsorTrack
Extract sponsorship information from Youtube videos
        """)

    with gr.Row():
        with gr.Column(scale=1):
            url = gr.Textbox(
                label="Youtube URL", placeholder="https://www.youtube.com/watch?v=XXXXXXXX"
            )
            examples = gr.Examples(
                examples=[
                    "https://youtu.be/ofKe4b169ts",
                    "https://youtu.be/NxCfacrnbFU",
                    "https://www.youtube.com/watch?v=AienZMjqAg4&t=424s",
                ],
                inputs=[url],
            )
            submit_btn = gr.Button("Get Sponsor Info", variant="primary")
            segments = gr.State([])
            submit_btn.click(fn=submit, inputs=[url], outputs=[url, segments], api_name="submit")

        with gr.Column(scale=2):

            @gr.render(inputs=segments)
            def render_count(arr):
                if len(arr) != 0:
                    gr.Markdown(
                        f"Found {len(arr)} sponsored segment{'' if len(arr) == 1 else 's'} for https://www.youtube.com/watch?v={arr[0]['parent_video_id']}"
                    )
                    for i, segment in enumerate(arr):
                        with gr.Accordion(
                            label=f"{segment['sponsor_info']['sponsor_name']}", open=False
                        ):
                            gr.HTML(f"""
                                <iframe
                                    width="560"
                                    height="315"
                                    src="https://www.youtube.com/embed/{segment["parent_video_id"]}?start={int(segment["start_time"])}"
                                    frameborder="0"
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                                    referrerpolicy="strict-origin-when-cross-origin"
                                    allowfullscreen>
                                </iframe>""")
                            gr.TextArea(
                                label="Description",
                                value=segment["sponsor_info"]["sponsor_description"],
                            )
                            gr.Textbox(
                                label="Offer", value=segment["sponsor_info"]["sponsor_offer"]
                            )
                            gr.Textbox(
                                label="Links",
                                value=", ".join(segment["sponsor_info"]["sponsor_links"]),
                            )


demo.queue().launch(show_error=True, share=True)
