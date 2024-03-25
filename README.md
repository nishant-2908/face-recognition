# Face Recognitition Using Python for Windows
## This repository contains a project for Face Detection and Face Recognition using Python 3.11
## Start using this Project
- Download all files in zip
- Uninstall the existing version of python and install the [Python 3.11](https://www.python.org/downloads/release/python-390)
- Download the `dlib` python package from [here](https://github.com/eddiehe99/dlib-whl/blob/main/dlib-19.24.1-cp311-cp311-win_amd64.whl)
- Open terminal in the extracted folder and run the following commands
`pip install -r requirements.txt`
- Create a subfolder named `known_persons` in the same level as that of `capture_faces.py`  
- Add some photos into the directory (Caution: Do not add photos of a same person multiple times, one user one photo)  
  
- Open the `crime_history_samples.csv` in your desired CSV editor  
  
- Add some sample data according to your wish (Caution: The names mentioned in the first column of `crime_history_samples.csv` i.e. `Names` should match with the name of photo in the `known_persons` directory).  
  
- Run the `capture_faces.py` by executing the command `python capture_faces.py` in the extracted folder.  
### Caution: only use `.jpg` or `.png` pictures
