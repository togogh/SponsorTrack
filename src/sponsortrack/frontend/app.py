import gradio as gr
from sponsortrack.backend.video import Video


def submit(url, segments):
    segments_copy = segments.copy()
    video = Video(url)
    segments_info = video.fetch_segments_info()
    segments_copy.extend(segments_info)
    return "", segments_copy


with gr.Blocks() as demo:
    url = gr.Textbox(label="Youtube URL")
    submit_btn = gr.Button("Get Sponsor Info")
    segments = gr.State([])
    submit_btn.click(fn=submit, inputs=[url, segments], outputs=[url, segments], api_name="submit")

    @gr.render(inputs=segments)
    def render_count(arr):
        if len(arr) != 0:
            gr.Markdown(
                f"Found {len(arr)} sponsored segment{'' if len(arr) == 1 else 's'} for https://www.youtube.com/watch?v={arr[0]['parent_video_id']}"
            )
            for i, segment in enumerate(arr):
                with gr.Accordion(label=f"{segment['sponsor_info']['sponsor_name']}", open=False):
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
                        label="Description", value=segment["sponsor_info"]["sponsor_description"]
                    )
                    gr.Textbox(label="Offer", value=segment["sponsor_info"]["sponsor_offer"])
                    gr.Textbox(
                        label="Links", value=", ".join(segment["sponsor_info"]["sponsor_links"])
                    )


demo.queue().launch(show_error=True)
