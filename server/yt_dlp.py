
import sys
import json
import struct

# from tenacity import retry, stop_after_attempt, wait_fixed
import subprocess
import sys, os
import struct, json
import json, sys,struct

#download_directory = os.path.join(os.path.expanduser("~"), "videos")
download_directory = os.path.join("/tmp", "videos")
os.makedirs(download_directory, exist_ok=True)

# YT_DLP_BINARY = '/opt/homebrew/bin/yt-dlp'
YT_DLP_BINARY = '/opt/homebrew/bin/yt-dlp'

# # app = typer.Typer()

def filepath(url):
    return get_file_path(url)

# @retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def get_file_path(url):
    path = f'{download_directory}/%(id)s-%(uploader)s.%(ext)s'
    command = [
            YT_DLP_BINARY,
            '-o', path,
            "--print", "filename",
            url
        ]
    # Execute the yt-dlp command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        final_path = result.stdout.strip()
        # print(f"extracted file path {url} to {final_path} successfully!")
        return final_path
    else:
        raise Exception(f'extract fail {result.returncode} for {url}')

def download(url):
    path = get_file_path(url)
    do_download(url, path)
    return { "url": url, "path": path } 

# @retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def do_download(url, path):
    import os 
    os.makedirs(download_directory, exist_ok=True)

    command = [
            YT_DLP_BINARY,
            '-o', path,
            url
        ]
    # Execute the yt-dlp command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return path
    else:
        raise Exception(f'Download failed for {url}')

def read_message():
    """
    Reads a single message from stdin. Each message starts with a 4-byte
    little-endian integer indicating the message length.
    """
    # Read the 4-byte length prefix
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        return None  # No message received, exit gracefully
    message_length = struct.unpack('I', raw_length)[0]
    # Read the message data (JSON payload)
    message_data = sys.stdin.buffer.read(message_length).decode('utf-8')
    return message_data

def send_message(message_text):
    """
    Sends a message to stdout with a 4-byte little-endian length prefix.
    """
    # Encode the message as JSON
    response_json = json.dumps({"response": message_text})
    encoded_content = response_json.encode('utf-8')
    content_length = len(encoded_content)
    # Write the length prefix
    sys.stdout.buffer.write(struct.pack('I', content_length))
    # Write the message content
    sys.stdout.buffer.write(encoded_content)
    sys.stdout.flush()

if __name__ == "__main__":
    try:
        while True:
            # Read a message from Chrome
            message = read_message()
            if message is None:
                break  # Exit if no message is received

            # Process the message (in this case, just echo it back)
            # You can add your own processing logic here
            download(message)
            send_message(f"Received: {message}")

    except Exception as e:
        # Send an error response back to Chrome
        error_message = f"An error occurred: {str(e)}"
        send_message(error_message)
        # Optionally, log the error to stderr or a file for debugging
        print(error_message, file=sys.stderr)
        sys.exit(1)
