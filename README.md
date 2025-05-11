# Plan

The goal is to build a web app like Graphtreon, but for Youtube sponsorships.

Objects involved:
1. Youtubers
2. Sponsors
3. Videos

Questions:
1. Who sponsored this video?

What sort of interface do we want?
How about let's start with...
There's an input, you plug in a video id, and it will return the sponsorship data.

But we want this to be stored in a database.


Phases:
1. Get sponsorship data given a video id
2. Store the raw information in a document database
3. Match sponsors to a sponsor_id
4. Create page for each database object

# Assumptions:
1. English
2. Sponsorship information exists in sponsorblock

# Steps:
Get video_id input
Download video
Download metadata
Download transcipt
Download sponsorblock info
Cut multimedia to the sponsored segments
Map multimedia to same vector space
Create prompt from mapping
Send prompt
Parse prompt
Display response

# Tools
For now, gradio for the interface