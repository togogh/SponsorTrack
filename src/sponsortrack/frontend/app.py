import gradio as gr
from sponsortrack.backend.video import Video


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


def submit(url):
    video = Video(url)
    try:
        video.fetch_info()
        return "Fetched video"
    except ValueError as err:
        return f"Error: {str(err)}"


with gr.Blocks() as demo:
    url = gr.Textbox(label="Video URL")
    output = gr.Textbox(label="Output Box")
    submit_btn = gr.Button("Submit")
    submit_btn.click(fn=submit, inputs=url, outputs=output, api_name="submit")

demo.launch()
