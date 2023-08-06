from .data_model import Session, ActivityBase, ActivityList
import requests
from typing import List, Optional
import os
import logging




class Client:

    def __init__(self, api_key:str) -> None:
        self.api_key=api_key    
        self.tracker_api_host_url = os.environ.get("TRACKER_HOST_URL","https://????")
        self.activities=[]
        

    
    def save_session(self, session:Session):
        try:
            response = requests.post(f"{self.tracker_api_host_url}/sessions", 
                        data=session.json(), 
                        headers={
                            "Authorization":f"Basic {self.api_key}", 
                            "Content-Type":"application/json"
                            }
                        )
            if response.status_code>300:
                logging.error(f"Error sending session to the server: Error {response.status_code} - {response.reason} ({response.text})")
        except Exception as ex:
            logging.exception(ex)

    def save_activities(self, session_id:str,   activities:List[ActivityBase]):
        try:
            payload = ActivityList(activities)
            response = requests.post(f"{self.tracker_api_host_url}/sessions/{session_id}/activities", 
                        data=payload.json(), 
                        headers={
                            "Authorization":f"Basic {self.api_key}", 
                            "Content-Type":"application/json"
                            }
                        )
            if response.status_code>300:
                logging.error(f"Error sending logs to server: Error {response.status_code} - {response.reason} ({response.text})")
            for act in activities:
                self.activities.append(act)
                print()
                print(act)
        except Exception as ex:
            logging.exception(ex)

    def get_session(self, session_id:str)-> Session:
        response = requests.get(f"{self.tracker_api_host_url}/sessions/{session_id}", headers={"Authorization":"Basic "+self.api_key})
        
    
        if response.status_code==200:
            return Session(**response.json())
        else:
            raise Exception(f"Error response from server: {response.status_code}: {response.text}")
        
