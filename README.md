# Personal Information Detection

<p align="center">This project scans for any personal information in images that you wouldn't want out in the internet (like phone numbers, credit card numbers, names, addresses, IP addresses, etc) by using Optical Character Recognition, Natural Language Processing, Regular Expressions and object detection systems.</p>

Personal Information in images is often overlooked, especially when posting to sites like Instagram where everyone can see the pictures you upload. People seldom check if there is any information in the background of their pictures that might leak personal information on a public site. My project tries to automate this process by checking the image for information that can be harmful if leaked in the public.

## Installation and usage:
- Clone the repository
- Download the darknet.zip file from the releases tab, and unzip it into a folder named `darknet` to be placed in the directory of the cloned repository
- Run `pip install -r requirements.txt` to download all necessary dependencies
- If you have a supported GPU, download CUDA and CUDNN on your system for faster running of the detection algorithm
- Run `streamlit run pii.py` to run the detection algorithm, and upload the picture to the website opened.

