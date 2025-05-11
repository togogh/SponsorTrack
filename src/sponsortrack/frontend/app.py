import gradio as gr
from sponsortrack.backend.download_video import download_video
from sponsortrack.backend.parse_video_id import parse_video_id


# Get video_id input
# Download video
# Download metadata
# Download transcipt
# Download sponsorblock info
# Cut multimedia to the sponsored segments
# Map multimedia to same vector space
# Create prompt from mapping
# Send prompt
# Parse prompt
# Display response


def submit(video_url):
    parse_video_id(video_url)
    download_video(video_url)
    download_metadata(video_url)

with gr.Blocks() as demo:
    video_url = gr.Textbox(label="Video URL")
    output = gr.Textbox(label="Output Box")
    submit_btn = gr.Button("Submit")
    submit_btn.click(fn=submit, inputs=video_url, outputs=output, api_name="submit")

demo.launch()
