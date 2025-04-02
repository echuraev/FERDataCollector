# FERDataCollector

FERDataCollector is a GUI application which should help to researchers to record short videos with
different emotion or engagement classes and use them to create their own datasets. Moreover, this
application can be used for collecting user's data and create personalized models.

![FERDataCollector screencast](docs/FERDataCollector.gif)

## Installation
1. Install all requirements: `pip install -r requirements.txt`
2. Run application: `python3 app.py`

## Usage
1. Select the output directory where the video files will be stored.
2. Select the required video length.
3. Select the required data type for video recording: `Emotions` or `Engagement`.
4. After this setup, click `Start data collection` button.
5. The label below `Start data collection` button will display the class to be recorded.
6. Use the `Record video` and `Play video` buttons to record the required video file and play it
   back if you need to review the recording. Recording starts in 3 seconds after pressing the
   `Record video` button. An information message will appear at the bottom of the application
   window. Once recording begins, a text message will be displayed in the top-left corner of the
   video widget.
7. Press `Save recorded video` if you are satisfied with the recorded video. The label displaying
   the class name will then update to a new value, allowing you to start recording a video for a new
   class.
