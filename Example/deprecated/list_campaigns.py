#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example to list available campaigns from CLS result service.

(Replaced by result download in tsf_execution_service)
"""
import requests

# to start the result service, follow the instructions from https://github.8675.ccp.continental.exchange/caedge-simulation/clsim-result-srv
API_URL = "http://localhost:5003/api/"


def main():
    """List the available campaigns from the result service."""
    get_campaigns = API_URL + "campaign?status=SUCCESSFUL&page=1&per_page=20"
    response = requests.get(get_campaigns)
    campaigns = response.json()["campaigns"]
    for campaign in campaigns:
        campaign_url = campaign["url"]
        campaign_id = campaign_url.split("/")[-1]
        campaign_info = requests.get(campaign_url).json()
        campaign_label = campaign_info["label"]
        if campaign_label == "":
            campaign_label = "N/A"
        print(f"Campaign Label: {campaign_label}, Campaign ID: {campaign_id}")


if __name__ == "__main__":
    main()
