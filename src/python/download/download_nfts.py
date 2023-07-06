import os
import requests
from bs4 import BeautifulSoup

# List of NFT URLs to download
nft_urls = [
    'https://opensea.io/assets/0x495f947276749ce646f68ac8c248420045cb7b5e/999999',
    'https://foundation.app/creators/s0m35rand0m/nft-drop-2-2',
    'https://rarible.com/token/0x60f80121c31a0d46b5279700f9df786054aa5ee5:225470',
    # Add more URLs here
]

# Directory to save downloaded NFTs
output_dir = 'nfts'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through each NFT URL and download the main content
for nft_url in nft_urls:
    # Send a GET request to the URL
    response = requests.get(nft_url)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the main content (usually an image) using CSS selectors
    content = soup.select_one('main img')
    if content is None:
        print(f'Error: could not find main content in {nft_url}')
        continue
    # Extract the URL of the main content
    content_url = content['src']
    # Construct a filename for the output file
    filename = os.path.join(output_dir, f'{os.path.basename(nft_url)}.jpg')
    # Send a GET request to the content URL and save the response to a file
    response = requests.get(content_url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f'Successfully downloaded {filename}')
