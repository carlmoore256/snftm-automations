# download a video from a blackdove webpage

# 1: On blackdove webpage, inspect and go to network tab, search for .m3u8
# 2: Copy the url
# 3: Run the following command in terminal
# ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i "https://unified-streaming.blackdove.com/out/v1/3b32c884e7a2439a9f1089f92150d7cd/31cc4035db75429eac9169c58803da85/52294a61cf094cb8b547fc4f8b80597c/index.m3u8?aws.manifestfilter=video_height:1-600" -c copy ~/Downloads/test-video.mp4
from subprocess import Popen, PIPE
import argparse

def download_video(url, output_path):
    cmd = f'ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i "{url}" -c copy {output_path}'
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    p_status = p.wait()
    print(output)
    print(err)
    
if __name__ == "__main__":
    download_video("https://unified-streaming.blackdove.com/out/v1/e31528a696944f8fa10fd9db988ec138/31cc4035db75429eac9169c58803da85/52294a61cf094cb8b547fc4f8b80597c/index.m3u8?aws.manifestfilter=video_height:1-600",
               "~/Documents/SNFTM_Utilities/data/blackdove/AnnaLucia_Loom_0_25.mp4")
    # parser = argparse.ArgumentParser()
    # parser.add_argument('url', help='URL of the video to download')
    # parser.add_argument('output_path', help='Path to save the video to')
    # args = parser.parse_args()
    # download_video(args.url, args.output_path)