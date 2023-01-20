import requests
import json

auth = {'token_type': 'Bearer', 'expires_in': 3599, 'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImZhY2QxYjA5YzA0ZTg4NDJiYTYwNzhkMjIwNDhiMGUwZjYxN2FkNTFmYjY0OWU4NmQ2ZTk2NGM2YWRmNjc4ZGYwNzYyZWNiY2RkYzE1YjZmIn0.eyJhdWQiOiJhcHAiLCJqdGkiOiJmYWNkMWIwOWMwNGU4ODQyYmE2MDc4ZDIyMDQ4YjBlMGY2MTdhZDUxZmI2NDllODZkNmU5NjRjNmFkZjY3OGRmMDc2MmVjYmNkZGMxNWI2ZiIsImlhdCI6MTY3NDIwMzk0OCwibmJmIjoxNjc0MjAzOTQ4LCJleHAiOjE2NzQyMDc1NDcsInN1YiI6IlNwZWVkaW5ldF9ob2xvZCIsInNjb3BlcyI6W119.idwdpqa1lKxyoLbzxUVPZPmSwsyC07fiAW9uyVfsAunrdna2rIL0TigfepNPEoO_9l09No0ZGggwz8XaxLgFnOuVktRObZSVcvwtFRR8fEsnKaQQwGuj8I2NoSm2tsZiDf4Z-Zhen04GBrgQC1oA4Rh2CB3h1AxBTxb0-O_GN6koiKLq0AN4JoZRQ27_H_Jb5aZGJCffZtG_HEdiL04NEqo7hVDgjVmGQ5R0H1l60dwfUzyV4cH0Ofq25vvYEicXnZbqK-NvzYNmrEmDs5YwS135XrRnRoNlABgQO-mcQCIMqxhGExq_SPl_1pZ6Z-zl8yTfS9J7tU976CuNvyTUCA', 'refresh_token': 'def50200e1ddf80e5b95c3a3800d9f7809c4618bced2f3fdfedfcc07a701d6278c1262e7b5801fb6b78d71e7faee33fcf7dcb696345241e38b82f742541c13688b46dc9bc0f91a21953fe552dcd1a3dacf32c50e9fd78b21ca21228eb419586fc1b0d9c90800bd665a34200f3b8b9ddf16d577f4136b6e7938548a83c88a96b5593b6875fd954b85f0a7e94dd6dda3a9c06846bfbe7c759cba03b17a752a0710f2b50f32da3ee32c2687b5b42548c24a03f86fa0ec70b83a8866df8a346f9e4e2111a256d59a9c6544362155b3cad60f556f72a0ef55bc507de8c6357b9855c0b5869eb3552273ae293fdf8a039e05014a688e937117f93d276af572aa52e0f067ef9de3a3d04b6b561c0469dc460bc02f8f6c1657eda4722c1e02a34ff9cb7ac034d960cacaf05b9f955c266c54cbfe549dfd911ffaffc7a211ba3a82bfd79a08f59b6a2407ae83e8c08dff11931edd140e5714eb2b5e028496c16ed3e51978baf1e96b15d4c355db25f3f2d1a3cbfecb150f'}

# url = 'https://master.sibset.ru:9090/token'
# payload = {
#     "grant_type": "password",
#     "username": "Speedinet_holod",
#     "password": "e3u91Bdyy2",
#     "client_id": "app",
#     "client_secret": "secret",
#     "access_type": "offline"
# }

url = 'https://master.sibset.ru:9090/api/v1/tickets?fields=id'
session = requests.Session()

# Send a GET request to the login page to get the csrf_token
# response = session.get(url)
# csrf_token = response.cookies['csrftoken']

# Add the csrf_token to the login payload
headers = {'access_token': f'Bearer {auth["access_token"]}',
           'Accept': 'application/json',
           }

# Send a POST request with the login payload to log in
response = session.get(url, headers=headers)
# print(response.content)
# print(response.cookies)
print(response.json())

# Send a GET request to the applications page
# response = session.get('https://master.sibset.ru/applications/')

# Parse the response content as JSON
# data = json.loads(response.content)

# Print the list of applications
# print(data)
