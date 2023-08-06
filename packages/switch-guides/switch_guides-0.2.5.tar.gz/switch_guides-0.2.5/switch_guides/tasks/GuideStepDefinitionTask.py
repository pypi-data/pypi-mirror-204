# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


from abc import abstractmethod
from io import StringIO
import logging
import sys
import pandas
import requests
import switch_api as sw

from ..exceptions import InvalidStepApiReponseException, InvalidStepStatusReponseException
from ..models.api import SwitchGuideStepApiResponse, SwitchGuideStepProcessInput
from ..models.literals import STATUS_STATE

from ..models.step import SwitchGuideStepComponent, SwitchGuideStepDefinition, SwitchGuideStepDefinitionUiAssets, SwitchGuideStepStatus
from ..utils.utils import ApiInputs, _column_name_cap, get_journeys_endpoint
from switch_api.pipeline.pipeline import Task

class GuideStepDefinitionTask(Task):
    logger = None

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setLevel(logging.INFO)
        self.logger.handlers.clear()
        self.logger.addHandler(consoleHandler)
        formatter = logging.Formatter('%(asctime)s  switch_guides.%(module)s.%(funcName)s  %(levelname)s: %(message)s',
                                      datefmt='%Y-%m-%dT%H:%M:%S')
        consoleHandler.setFormatter(formatter)
    
    @property
    @abstractmethod
    def definition(self) -> SwitchGuideStepDefinition:
        """"Structure of the Journey Step"""
        return None

    @abstractmethod
    def check_status(self, api_inputs: ApiInputs, journey_input: SwitchGuideStepProcessInput) -> SwitchGuideStepStatus:
        """This method will be called to understand current status of the step.
        Ideally the method is very quick and limits calls to retrieve data only for building current status. 

        Args:
            api_inputs (ApiInputs): Provides state for calling Switch Platform APIs.

        Returns:
            SwitchGuideStepStatus: response containing the status of the step or None
        """
        return None
    
    @abstractmethod
    def check_ui_assets(self, step_status: SwitchGuideStepStatus, guide_input: SwitchGuideStepProcessInput) -> SwitchGuideStepDefinitionUiAssets:
        """This method will be called to understand what would be the ui assets based on the status.
        Method can return empty response, None, or call Super method if not required.
        Ideally this method should not involve any external calls. 

        Args:
            step_status (SwitchGuideStepStatus): The journey step status to evaluate.

        Returns:
            SwitchGuideStepDefinitionUiAssets: response containing UiAsset overrides.
        """
        return None
    
    @abstractmethod
    def check_ui_component(self, api_inputs: ApiInputs, step_status: SwitchGuideStepStatus, journey_input: SwitchGuideStepProcessInput) -> SwitchGuideStepComponent:
        """This method is called to return any component overrides
        Method can return empty response, None, or call Super method if not required.
        Ideally this method should not involve any external calls. 

        Args:
            api_inputs (ApiInputs): Provides state for calling Switch Platform APIs.
            step_status (SwitchGuideStepStatus): The journey step status to evaluate.
            journey_input (SwitchGuideStepProcessInput): Information specific to a Journey

        Returns:
            SwitchGuideStepComponent: response containing ui component override or None
        """
        return None

    @abstractmethod
    def process(self, api_inputs: ApiInputs, journey_input: SwitchGuideStepProcessInput) -> SwitchGuideStepApiResponse:
        """ This method requires user wait for completion. 
        How long this method should run depends on how long a user is willing to wait on the page. 
        Use GuideStepDefinitionAsyncTask if you want to run this method in background.

        This method will be called by the Guides Backend under two conditions.
            1. When user completes the requirements of a component associated with this step.
        
        Add your logic here to extract, process, and export data how ever you see fit.
        """
        return None

    def publish_update(self, api_inputs: ApiInputs, guide_input: SwitchGuideStepProcessInput, 
            completion_percentage: int, step_state: STATUS_STATE, force_update = False,
            enable_progress_component: bool = False):
        """
        Publishes an update to the step progress to the Switch Platform.

        Args:
            api_inputs (ApiInputs): Provides state for calling Switch Platform APIs.
            guide_input (SwitchGuideStepProcessInput): Information specific to a Journey
            completion_percentage (int): Percentage of completion of the step.
            step_state (STATUS_STATE): The state of the step.
            force_update_percentage (bool, optional): Force update the percentage. 
                When True percentages are updated even when lower than current percentage. Defaults to False.
            enableInprogressComponent (bool, optional): Enable the inprogress component. Defaults to False.
        """

        return self.update_step_progress(
            api_inputs=api_inputs, 
            guide_id=guide_input.journey_id, 
            completion_percentage=completion_percentage, 
            step_state=step_state, 
            force_update_percentage=force_update,
            enable_progress_component=enable_progress_component
        )

    def update_step_progress(self, api_inputs: ApiInputs, guide_id, completion_percentage: int, 
            step_state: STATUS_STATE, force_update_percentage = False, progressData: dict = {}, enable_progress_component: bool = False):

        progress_update_url = f"{get_journeys_endpoint(api_inputs)}/projects/{api_inputs.api_project_id}/guides/{guide_id}/update-progress"
        sw.pipeline.logger.info(progress_update_url)

        progress_update_response = requests.request("POST", progress_update_url,
            headers=api_inputs.api_headers.default,
            json={
                "stepId": str(self.id),
                "completionPercentage": completion_percentage,
                "forceUpdatePercentage": force_update_percentage,
                "state": step_state,
                "progressData": progressData,
                "enableInprogressComponent": enable_progress_component
            })

        if progress_update_response.status_code != 200:
            if progress_update_response.text:
                sw.pipeline.logger.error(f"Failed to update step progress: \
                    StatusCode={progress_update_response.status_code} Message={progress_update_response.text}")
            return False

        response = progress_update_response.json()
        if "hasErrors" not in response:
            sw.pipeline.logger.error(f"Failed to update step progress")
            return False
        
        if response["hasErrors"]:
            sw.pipeline.logger.error(f"Failed to update step progress: ErrorMessage={response['errorMessage']}")
            return False

        return True
    
    def update_component(self, response: SwitchGuideStepApiResponse, component: SwitchGuideStepComponent):
        if (response == None or type(response) is not SwitchGuideStepApiResponse):
            self.logger.error('Provided response model is not a valid')
            raise InvalidStepApiReponseException('Expected valid SwitchGuideStepApiResponse')
        
        response.component = component
        
    def update_status(self, response: SwitchGuideStepApiResponse, status: SwitchGuideStepStatus):
        if (response == None or type(response) is not SwitchGuideStepApiResponse):
            self.logger.error('Provided response model is not a valid')
            raise InvalidStepApiReponseException('Expected SwitchGuideStepApiResponse')
        
        if (status == None):
            self.logger.error('Provided Step Status model is not a valid')
            raise InvalidStepStatusReponseException('Expected valid SwitchGuideStepStatus')
        
        if (status.type != self.definition.status.type):
            self.logger.error('Step Status type cannot be changed via script. Please update the definition model.')
            raise InvalidStepStatusReponseException('Cannot update Step Status type via script')
        
        response.status = status

    def register(self, api_inputs: ApiInputs):
        if api_inputs == None or api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
            self.logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        script_response = sw.pipeline.Automation.register_task(api_inputs, self)

        _, register = (0, script_response) if type(script_response) is pandas.DataFrame else script_response

        self.logger.info(register)

        if (register.size == 0):
            self.logger.error(
                "Journey Definition registration was unsuccessful")
            return pandas.DataFrame()

        headers = api_inputs.api_headers.default

        json_payload = {
            "scriptDriverId": str(self.id)
        }

        journey_endpoint = get_journeys_endpoint(api_inputs=api_inputs)

        url = f"{journey_endpoint}/projects/{api_inputs.api_project_id}/definitions/steps/register"
        self.logger.info("Sending request: POST %s", url)

        response = requests.post(url, json=json_payload, headers=headers)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            self.logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                              response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            self.logger.error(
                'No data returned for this API call. %s', response.request.url)
            return response_status, pandas.DataFrame()

        response_data = pandas.read_json(StringIO(response.text), typ='Series').to_frame().T
        response_data.rename(columns = {'driverId':'guideStepDefinitionId'}, inplace = True)
        response_data.columns = _column_name_cap(response_data.columns)

        return response_status, response_data