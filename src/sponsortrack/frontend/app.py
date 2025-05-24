import gradio as gr
from sponsortrack.backend.video import Video


def submit(url):
    video = Video(url)
    try:
        segments_info = video.fetch_segments_info()
        sponsors_info = [s["sponsor_info"] for s in segments_info]
        return sponsors_info
    except ValueError as err:
        return f"Error: {str(err)}"


with gr.Blocks() as demo:
    url = gr.Textbox(label="Video URL")
    output = gr.Textbox(label="Output Box")
    submit_btn = gr.Button("Submit")
    submit_btn.click(fn=submit, inputs=url, outputs=output, api_name="submit")

demo.launch()
