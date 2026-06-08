import librosa
import numpy as np

def extract_features(file_path):

    try:

        # LOAD AUDIO
        audio, sample_rate = librosa.load(
            file_path,
            sr=22050
        )

        # VERY SHORT AUDIO FIX
        if len(audio) < 2048:

            audio = np.pad(
                audio,
                (0, 2048 - len(audio)),
                mode='constant'
            )

        # EXTRACT MFCC
        mfccs = librosa.feature.mfcc(
            y=audio,
            sr=sample_rate,
            n_mfcc=40
        )

        # TAKE MEAN
        mfccs_scaled = np.mean(
            mfccs,
            axis=1
        )

        # FORCE FIXED SIZE
        mfccs_scaled = np.resize(
            mfccs_scaled,
            (40,)
        )

        return mfccs_scaled.astype(np.float32)

    except Exception as e:

        print("ERROR:", file_path)

        print(e)

        return None