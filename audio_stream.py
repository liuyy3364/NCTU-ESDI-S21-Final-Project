
# def genHeader(samples, sampleRate=24000, bitsPerSample=16, channels=1):
#     datasize = samples * channels * bitsPerSample // 8
#     o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
#     o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
#     o += bytes("WAVE",'ascii')                                              # (4byte) File type
#     o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
#     o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
#     o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
#     o += (channels).to_bytes(2,'little')                                    # (2byte)
#     o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
#     o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
#     o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
#     o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
#     o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
#     o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
#     return o

# audio_sig_wrapper = [False]

# @app.route("/audio_feed")
# def audio_feed():
#     def generate():
#         blank = np.ones(1024).tobytes()
#         with open("audio_o.wav", "rb") as fmp3:
#             data = fmp3.read()
#             t = np.frombuffer(data,dtype="uint32",count=1024)
#         with open("audio_o.wav", "rb") as fmp3:
#             data = fmp3.read(1024)
#             i=0
#             while data:
#                 i+=1
#                 yield data
#                 data = fmp3.read(1024)
#     return Response(generate(), mimetype="audio/x-wav")
