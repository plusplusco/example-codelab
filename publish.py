import argparse, requests

token = "71e296f577e9f263d85eccab467f811faab66a18"
codelab_id = "ad52def9-9008-4098-b2b7-d72e5cfd12e8"
domain = "demo.plusplus.app"


def get_presigned_post(token, codelab_id):
    """Get the pre-signed post details."""
    url = f"https://{domain}/endpoints/codelabs/upload/api/{codelab_id}/pre-sign/"
    response = requests.post(url, headers={'authorization': token})
    if response.status_code != 200:
        print(response)
        raise SystemExit("Failed to generate pre-signed post. "
                         "Do you have the API update feature enabled?")
    return response.json()

def upload_file(token, data, filename):
    """Upload file with pre-signed post."""
    upload_data = data['upload_data']
    response = requests.post(upload_data['url'],
                             data=upload_data['fields'],
                             files={'file': open(filename, "rb")})

    if response.status_code != 204:
        print(response)
        raise SystemExit("Failed to upload file")

def update_version(token, codelab_id, data):
    """Update the codelab version by pointing to the uploaded file."""

    url = f"https://{domain}/endpoints/codelabs/upload/api/{codelab_id}/version/"
    response = requests.post(url,
                             headers={'authorization': token},
                             data={'read_url': data['read_url']})

    if response.status_code != 200:
        print(response)
        raise SystemExit("Failed to update version")


def main(token, codelab_id, filename):
    data = get_presigned_post(token, codelab_id)
    upload_file(token, data, filename)
    update_version(token, codelab_id, data)
    url = f"https://{domain}/a/codelabs/{codelab_id}/"
    print(f"Success! See {url}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sample client to publish a codelab to PlusPlus.')
    parser.add_argument("--token", help="Auth token from plusplus")
    parser.add_argument("--codelab_id", help="Codelab public ID")
    parser.add_argument("--filename", help="Zip file to upload")
    args = parser.parse_args()
    main(args.token, args.codelab_id, args.filename)
