import argparse
import requests
import time

APP_URI = 'https://api-cloud.browserstack.com/app-automate/espresso/v2/app'
TEST_URI = 'https://api-cloud.browserstack.com/app-automate/espresso/v2/test-suite'
BUILD_URI = 'https://api-cloud.browserstack.com/app-automate/espresso/v2/build'
STATUS_URI = 'https://api-cloud.browserstack.com/app-automate/espresso/v2/builds/{}'

def main(args: argparse.Namespace) -> None:
    app_files = {
        'file': open(args.app_path, 'rb')
    }
    app_response = requests.post(
        APP_URI,
        files=app_files,
        auth=(args.username, args.access_key)
    )
    app_response_json = app_response.json()

    print(app_response)
    print(app_response_json)

    if not app_response.ok:
        exit(1)

    test_files = {
        'file': open(args.test_path, 'rb')
    }
    test_response = requests.post(
        TEST_URI,
        files=test_files,
        auth=(args.username, args.access_key)
    )
    test_response_json = test_response.json()

    print(test_response)
    print(test_response_json)

    if not test_response.ok:
        exit(1)

    build_headers = {
        'Content-Type': 'application/json'
    }
    build_data = {
        'app': app_response_json['app_url'],
        'testSuite': test_response_json['test_suite_url'],
        'project': args.project_name,
        'devices': [
            'Google Pixel 6 Pro-12.0'
        ]
    }
    build_response = requests.post(
        BUILD_URI,
        headers=build_headers,
        json=build_data,
        auth=(args.username, args.access_key)
    )
    build_response_json = build_response.json()

    print(build_response)
    print(build_response_json)

    if not build_response.ok:
        exit(1)

    if build_response_json['message'] != 'Success':
        exit(1)

    prev_duration = 0
    while True:
        time.sleep(10)
        status_response = requests.get(
            STATUS_URI.format(build_response_json['build_id']),
            auth=(args.username, args.access_key)
        )
        status_response_json = status_response.json()
        duration = status_response_json['duration']

        print(status_response)
        print(status_response_json)

        if not status_response.ok:
            exit(1)

        if prev_duration == duration:
            break
        prev_duration = duration

    if status_response_json['status'] != 5:
        exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True)
    parser.add_argument('--access_key', required=True)

    parser.add_argument('--project_name', required=True)
    parser.add_argument('--app_path', required=True)
    parser.add_argument('--test_path', required=True)
    args = parser.parse_args()

    main(args)