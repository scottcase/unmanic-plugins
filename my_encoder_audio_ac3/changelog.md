
**<span style="color:#56adda">0.0.10</span>**
- update test_stream_needs_processing.
- 
**<span style="color:#56adda">0.0.9</span>**
- add option to also ignore eac3 audio.

**<span style="color:#56adda">0.0.8</span>**
- add check in calculate_bitrate and custom_stream_mapping to set channels to 6 if channels > 6.  ffmpeg cannot encode > 6 channels of ac3 audio.

**<span style="color:#56adda">0.0.7</span>**
- fix stray character in custom stream mapping function

**<span style="color:#56adda">0.0.6</span>**
- add an '-ac` parameter to encoder to avoid unsupported channel layout error when normalizing 6 channel streams

**<span style="color:#56adda">0.0.5</span>**
- Update FFmpeg helper
- Remove support for v1 plugin executor
- Fix bug where "Write your own FFmpeg params" options were not being applied correctly to the FFmpeg command

**<span style="color:#56adda">0.0.4</span>**
- Update FFmpeg helper
- Add platform declaration

**<span style="color:#56adda">0.0.3</span>**
- Enabled support for v2 plugin executor

**<span style="color:#56adda">0.0.2</span>**
- Ensure no static vars are used with when stream mapping

**<span style="color:#56adda">0.0.1</span>**
- initial version
