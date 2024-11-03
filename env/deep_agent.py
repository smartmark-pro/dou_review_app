
import numpy as np
import json
import requests
import copy
import os
import streamlit as st


class DeepAgent:

    def __init__(self, position, model_path):
        self.model = None


    def post(self, infoset):

        os.environ['NO_PROXY']=st.secrets.remote.get("proxy_url")
        url = st.secrets.remote.get("algo_url")

        payload = json.dumps({
        "infoset": infoset,
        "username": "1",
        "token": "test",
        "requestid": "111"
        })
        headers = {
        'Content-Type': 'application/json'
        }
        # print(infoset)
        response = requests.request("POST", url, headers=headers, data=payload)

        # print(response.text)
        return response.json()
    def remote_act(self, infoset):
        infoset2 = copy.deepcopy(infoset)
        infoset_data = {}
        for k, v in infoset2.__dict__.items():
            if k == "card_play_action_seq":
                for i in range(len(v)):
                    v[i]= v[i][1]

            infoset_data[k] = v
        print(infoset_data)
        try:
            rs = self.post(json.dumps(infoset_data))
            return rs.get("best_action"), rs.get("best_action_confidence"), rs.get("action_list")
        except Exception as e:
            print(e)
            
            return self.act(infoset)
