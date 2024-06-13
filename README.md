# CloudflareDDNS
A (wip) docker container/python script that dynamically updates your DNS records on Cloudflare.

## Usage
### Docker (recommended)
1. Do one of the following:
    * Pull from ghcr.io:
    ```
    docker pull ghcr.io/morg-mov/cloudflareddns:master
    ```
    * Clone the repository and build the image: 
    ```
    git clone https://github.com/morg-mov/cloudflareddns
    cd cloudflareddns
    docker build -t ghcr.io/morg-mov/cloudflareddns .
    ```
2. Download and use [this](https://github.com/morg-mov/cloudflareddns/blob/main/docker-compose.yml) docker-compose file and edit it to your needs.
3. Create a .env file [or use a template](https://github.com/morg-mov/cloudflareddns/blob/main/.env.example) and [set at least the required variables](#variables).
4. Run the container with `docker-compose up -d` (or however you prefer).
### Python
1. Clone the repository
```
git clone https://github.com/morg-mov/cloudflareddns
cd cloudflareddns
```
2. Install dependencies with `pip install -r requirements.txt`
3. Run the script with `python cloudflareddns.py` (or however you prefer).
4. Create a .env file [or use a template](https://github.com/morg-mov/cloudflareddns/blob/main/.env.example) and [set at least the required variables](#variables).
5. Run the script with `python main.py` (or however you prefer).
## Variables
This image requires the use of multiple environment variables, many of which are required.
They can be defined either in your docker-compose file, or in a .env file if you're running the script directly.

### Required
`CF_TOKEN`: Your [Cloudflare API token](#get-a-cloudflare-api-token).

`CF_ZONE`: The zone (domain name) you wish to update.

`CF_DNSNAMES`: A comma-delimited string of DNS records you wish to update, e.g. `example.com,www.example.com`

### Optional
`CF_PROXIED`: Determines whether the records are proxied behind Cloudflare. Leave undefined to use the default value of `false`.

`DDNS_CHECKDELAY`: The delay between checks, in seconds. Leave undefined to use the default value of 300 (5 minutes).

## Get a Cloudflare API Token
1. Go to https://dash.cloudflare.com/profile/api-tokens.
2. Click `Create Token`.
3. Click `Use Template` beside `Edit zone DNS`.
4. Under `Zone Resources`, Click the third dropdown and select your domain name.
5. Change settings to your liking and click `Continue to Summary`.
6. Click `Create Token`.
7. Copy the token and store it somewhere safe. You cannot view it later.

# Legal Disclaimer
Copyright (C) 2024 morg.mov
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
