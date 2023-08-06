# History

## 0.2.5

Added

* Following attributes to `SwitchGuideStepData`
  * request_data, request_timestamp, request_component_id

## 0.2.4

Added

* `options` attribute to `SwitchGuideStepProcessInput`
  * Allows Guide authors to provide additional options while processing the step
  * Attribute is optional and therefore Guide Step authors should take this into account

## 0.2.3

Added

* Option for explicitly enabling periodic status checking on Guide Definition level
* Usage
  * ```python
        def definition(self) -> sg.guide.SwitchGuideDefinition:
            return sg.guide.SwitchGuideDefinition(
                ...
                options=sg.guide.SwitchGuideDefinitionOptions(
                    enable_live_notification=True
                )
            )
    ```

## 0.2.1

Added

* Cache Extensions
  * Provides a convenient way of caching data scoped to a Guide
  * Cache is scoped to a Guide Instance and therefore is only available within a Guide Instance and Portfolio the Guide Instance belongs to.
  * Usage - Setter:
    * ```python
      import switch_guides as sg

      guide_id_example = 'dc25bbeb-8504-4ffa-9389-641cc48cc807'
      cache_key_example = 'my-data'

      cache_data = {
          'name': '<some-value>',
      }

      cache_result = sg.extensions.cache.set_cache(
          api_inputs=api_inputs, guide_id=guide_id_example, key=cache_key_example, val=cache_data)

      if not cache_result or not cache_result['success']:
          print('Error setting cache')
          return
      ```
  * Usage - Getter:
    * ```python
      import switch_guides as sg
      import json

      guide_id_example = 'dc25bbeb-8504-4ffa-9389-641cc48cc807'
      cache_key_example = 'my-data'

      cache_result = sg.extensions.cache.get_cache(
          api_inputs=api_inputs, guide_id=guide_id_example, key=cache_key_example)

      if not cache_result or not cache_result['success']:
          print('No cache found')
          return

      cache_data = json.loads(cache_result['data'])
      ```

## 0.1.19

Added

* publish_update function to GuideStepDefinitionTask base class
  * Allows live updates to be sent to UI when a step is being processed

## 0.1.18

Fixed

* Incorrect Marketplace User Type Default Value

## 0.1.17

Updated

* Guide Definition Tags structure

## 0.1.16

Added

* Step options to SwitchGuideStepDependency to control Step state per Guide definition
* Extend SwitchGuideDefinitionOptions with availableOnMarketplaceForUserType to control whether the Guide is visible on the Marketplace
  * Options are None, All, or SwitchUserOnly

## 0.1.15

Added

* Switch Forms Extensions
  * Provides convenience methods for building and fetching form data
    * See method documentation for more information
    * Usage:
      * ```python
        import switch_api as sw
        import switch_guides as sg

        # Build UI Component
        sg.extensions.forms.define_ui_component(form_id=form_id)

        # Fetch Form Data
        form_data = sg.extensions.forms.get_data(api_inputs=api_inputs, form_id=form_id)
        section = form_data.getSectionById(1) # or form_data.getSectionByName('Section Name') 
        field = section.getFieldById(1) # or form_data.getFieldByLabel('Field Label')
        field_value = field.value
        ```

## 0.1.14

Updated

* Improved Guide Definition Registration Responses
  * Errors associated with registration will be available in the responses
* Documentation for most Guide types and properties

Added

* Aliases for guide.models modules so they are accessible on top level import
  * Few Examples:
    * ```python
      import switch_guides as sg

      sg.tasks.GuideStepDefinitionTask
      sg.step.SwitchGuideStepDefinition
      sg.guide.SwitchGuideDefinition
      sg.api.SwitchGuideStepProcessInput
      ```
* GuideStepDefinitionBackgroundTask that runs process() function in the background allowing users to navigate away from the page.
  * Will work in conjunction with LivelyUI APIs so that user can be given live feedback on the progress of the process method.
* More step control options:
  * uiState now has `continueToNextStep` and `continueToNextStepWhenAvailable` available
  * we can now set uiState on process response without requiring status property to be set
    * Example:
      ```python
      # Instead of:
      return SwitchGuideStepApiResponse(
          status=SwitchGuideStepStatus(
              uiState=SwitchGuideStepStatusUiState(
                  returnToSummary=True
              )
          )
      )

      # We can set uiState as:
      return SwitchGuideStepApiResponse(
          uiState=SwitchGuideStepStatusUiState(
              returnToSummary=True
          )
      )
      ```

## 0.1.13

Initial Switch Guides Release
