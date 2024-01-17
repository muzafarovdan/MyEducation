# instantiate the pipeline
from pyannote.audio import Pipeline
pipeline = Pipeline.from_pretrained(
  "pyannote/speaker-diarization-3.1",
  use_auth_token="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")

# run the pipeline on an audio file
diarization = pipeline("audio.mp3", num_speakers=2)

# dump the diarization output to disk using RTTM format
with open("audio.mp3", "w") as rttm:
    diarization.write_rttm(rttm)
