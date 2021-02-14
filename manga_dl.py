import requests #to get images from web
import shutil #to save it locally

## Set up the image URL and filename
image_url = "https://9nrdzhwmm5q6e.9tx6ed0zftkz4.mangadex.network:44199/TrG7TGfCpjIxwISB5JIEF5IgOUR0qI-FpqnWzBJbGgxTWlv6enY6SsIYmfawn12PtahT6vAludTBZDErfZ4WOa5V1gkTiBEeesHOWapx_moQjzk0xAWNrlzqsuAuKpMh7_2e3B8iZlpogbNZ0XZEcIYsKN-zaX2Kp2q9et4aP_ukFYlvB-blgJryXNBOxuDOCOlJxWn8uk18VjxBt_yWYQr8P9N-vA/data/088583bf54406c94bbb90c15af4a38bc/x1.jpg"
filename = image_url.split("/")[-1]

# Open the url image, set stream to True, this will return the stream content.
r = requests.get(image_url, stream = True)

# Check if the image was retrieved successfully
if r.status_code == 200:
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    r.raw.decode_content = True
    # Open a local file with wb ( write binary ) permission.
    with open(filename,'wb') as f:
        shutil.copyfileobj(r.raw, f)
    print('Image sucessfully Downloaded: ',filename)
else:
    print('Image Couldn\'t be retreived')
