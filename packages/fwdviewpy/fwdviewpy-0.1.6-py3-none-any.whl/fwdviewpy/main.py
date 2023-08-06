import logging
import sys
import requests
import time 
import json

class VirtualisationEngineSessionManager:
    def __init__(self, address, username, password, major, minor, micro):
        logging.basicConfig(filename='DelphixEngineSessionManager.log',
                            level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s', filemode='w')
        logging.info(30 * '=' + '| RUN BEGINS |' + 30 * '=')
        self.address = address
        self.username = username
        self.password = password
        self.major = major
        self.minor = minor
        self.micro = micro

    def __str__(self):
        return f'Virtualisation Engine Session Manager: {self.address}'

    def _login(self):
        """This function logs into the Virtualisation Engine
        """
        session = requests.session()
        session_url = f"http://{self.address}/resources/json/delphix/session"
        data = {
            "type": "APISession",
            "version": {
                "type": "APIVersion",
                "major": self.major,
                "minor": self.minor,
                "micro": self.micro
            }
        }
        response = session.post(session_url, json=data)
        if response.ok:
            logging.info(f"Session established on {self.address}")
        else:
            logging.error(f"Session NOT established on {self.address}")
            sys.exit()
        url = f"http://{self.address}/resources/json/delphix/login"
        data = {
            "type": "LoginRequest",
            "username": self.username,
            "password": self.password
        }
        response = session.post(url, json=data)
        if response.ok:
            logging.info(
                f"login SUCCEEDED - Response: {response.status_code}")
        else:
            logging.error(f"login FAILED - Response: {response.status_code}")
            sys.exit()
        return session

    def createBookmark(self, containerName, bookmarkName):
        # Set up the session object
        """ 
        This method creates a bookmark on the container of the Delphix Engine. 

        Args: 
            containerName: This is the name of the container to be bookmarked on the Delphix Engine. 
            bookmarkName: This argument is the name of the bookmark to be made on the containerName.
        
        Returns: 
            This method does not return any value. 
        """
        containerReference, containerBranch = self._getTemplateBranch(containerName)
        # Send a POST request to the bookmark endpoint with cookies set from the session
        bookmark_url = f"http://{self.address}/resources/json/delphix/selfservice/bookmark"
        data = {
            "type": "JSBookmarkCreateParameters",
            "bookmark": {
                "type": "JSBookmark",
                "name": bookmarkName,
                "branch": containerBranch
            },
            "timelinePointParameters": {
                "type": "JSTimelinePointLatestTimeInput",
                "sourceDataLayout": containerReference
            }
        }
        session = self._login()
        response = session.post(bookmark_url, json=data)
        action = response.json()['action']
        self._checkActionLoop(action)
        session.close()
        logging.debug(f"Bookmark has been created. \n Bookmark: {bookmarkName} \n Container: {containerName} \n Engine: {self.address}")

    def _checkActionLoop(self, action): 
        while True:
            if self._checkAction(action):
                break
            elif self._checkAction(action) == "FAILED":
                logging.error("Failed to create Bookmark. Please see Engine logs.")
                sys.exit()
            else:
                print("Not yet Completed, check again in 10 seconds")
                time.sleep(10)

    def _checkAction(self, action):
        session = self.login()
        action_url = f"http://{self.address}/resources/json/delphix/action"
        APIQuery = session.get(action_url)
        for actions in APIQuery.json()["result"]:
            if actions['reference'] == action:
                state = actions['state']
                if state == "COMPLETED":
                    session.close()
                    return True
                elif state == "FAILED":
                    state = "FAILED"
                    session.close()
                    return state
                else:
                    return False
    
    def _getTemplateBranch(self, containerName):
        # Log in and obtain the session object
        session = self.login() 
        # Send a GET request to the selfservice/template endpoint with cookies set from the session
        template_url = f"http://{self.address}/resources/json/delphix/selfservice/container"
        response = session.get(template_url)
        # Extract the template reference and active branch from the API response
        container_reference = None
        container_branch = None
        for container in response.json()["result"]:
            if container['name'] == containerName:
                container_reference = container["reference"]
                container_branch = container["activeBranch"]
                break
        logging.debug(f"container reference: {container_reference} & Template branch: {container_branch}")
        session.close()
        return container_reference, container_branch 
    
class MaskingEngineSessionManager(VirtualisationEngineSessionManager): 
    def __init__(self, address, username, password, major, minor, micro): 
        super().__init__(self, address, username, password, major, minor, micro)

    def __str__(self):
        return f'Masking Engine Session Manager: {self.address}'
    
    def login(self):
        """
        This method logs in to the Delphix Masking Engine. 

        Returns: 
            This method returns an authentication key used to send API's to the engine. 
        """ 
        url = f"http://{self.address}/masking/api/v5.1.14/login"

        payload = json.dumps({"username": self.username, "password": self.password})
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        responseDict = response.json()
        authKey = responseDict['Authorization']
        logging.info(f"Authentication key established for Masking Engine {self.address}. Key: {authKey}")
        return authKey
    
    def runMaskingJob(self, environment, maskingRule, connectorName):
        """
        This method executes pre-configured masking jobs on the masking engine.

        Args: 
            environment: This is the environent on the Delphix masking engine on which to run the masking job. 
            maskingRule: This is the ruleset that we want to run on the delphix engine. 
            connectorName: This is the name of the connector for which connects the masking job to the data. 
        
        Returns: 
            This method does not return any value. 
        """
        authKey = self.login()
        envID = self._getEnvironment(authKey, environment)
        ruleID = self._getJobId(authKey, maskingRule, envID)
        targetConnectorID = self._getTargetConnectorID(authKey, connectorName, envID)
        self._execute_job(authKey, ruleID, targetConnectorID)
        logging.info(f"Masking job triggered. Job: {maskingRule}")
        executionID = self._getExecutionID(authKey, ruleID)
        jobStatus = self._checkStatus(executionID) 

        if jobStatus == "SUCCEEDED":
            logging.info(f"Masking Successful. Job: {maskingRule}")
        else:
            logging.error(f"Please check error logs for masking job: {maskingRule}")
            sys.exit()
    
    def _getEnvironment(self, authKey, envName):
        response = self._getRequest(authKey, "environments")
        response = json.loads(response)
        for env in response["responseList"]:
            if env["environmentName"] == envName:
                envID = env["environmentId"]
        return envID
    

    def _getRequest(self, authKey, endPoint):
        url = f"http://{self.address}/masking/api/v5.1.14/{endPoint}"
        payload = {}
        headers = {
            'Authorization': authKey
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text

    def _getExecutionID(self, authKey, jobID):
        endPoint = f"executions?job_id={jobID}&page_number=1&execution_status=RUNNING"
        response = self._getRequest(authKey, endPoint)
        response = json.loads(response)
        executionID = response['responseList'][0]['executionId']
        return executionID

    def _getJobId(self, authKey, jobName, envID):
        endPoint = f"masking-jobs?environment_id={envID}"
        response = self._getRequest(authKey, endPoint)
        response = json.loads(response)
        for job in response["responseList"]:
            if job["jobName"] == jobName:
                jobID = job['maskingJobId']
        return jobID

    def _getTargetConnectorID(self, authKey, connectorName, environmentId):
        response = self._getRequest(authKey, "database-connectors")
        response = json.loads(response)
        for connectors in response["responseList"]:
            if connectors["connectorName"] == connectorName and connectors["environmentId"] == environmentId:
                targetConnectorID = connectors["databaseConnectorId"]
        return targetConnectorID
     
    def _execute_job(self, auth_key, job_id, targetConnectorID):
        url = f"http://{self.address}/masking/api/v5.1.14/executions"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': auth_key
        }
        data = {
            'jobId': job_id, 
            'targetConnectorId': targetConnectorID
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.text

    def _checkStatus(self, executionID):
        authKey = self.login()
        while True:
            status = self._getStatus(authKey, executionID)
            if status == "RUNNING":
                time.sleep(300)
                print("Job is still running, check again in 5 minutes.")
            else:
                print(f"Job has finished running. Job Status is: {status}")
                return status