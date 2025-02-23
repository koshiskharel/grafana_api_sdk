import json
import logging

from .model import APIModel, APIEndpoints, RequestsMethods
from .folder import Folder
from .api import Api


class Dashboard:
    """The class includes all necessary methods to access the Grafana dashboard API endpoints

    Args:
        grafana_api_model (APIModel): Inject a Grafana API model object that includes all necessary values and information

    Attributes:
        grafana_api_model (APIModel): This is where we store the grafana_api_model
    """

    def __init__(self, grafana_api_model: APIModel):
        self.grafana_api_model = grafana_api_model

    def create_or_update_dashboard(
        self,
        dashboard_path: str,
        dashboard_json: dict,
        message: str,
        overwrite: bool = False,
    ):
        """The method includes a functionality to create the specified dashboard

        Args:
            dashboard_path (str): Specify the dashboard path in which the dashboard is to be placed
            dashboard_json (dict): Specify the inserted dashboard as dict
            message (str): Specify the message that should be injected as commit message inside the dashboard
            overwrite (bool): Should the already existing dashboard be overwritten (default False)

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            None
        """

        if len(dashboard_path) != 0 and dashboard_json != dict() and len(message) != 0:
            folder_id: int = Folder(
                self.grafana_api_model
            ).get_folder_id_by_dashboard_path(dashboard_path)

            dashboard_json_complete: dict = {
                "dashboard": dashboard_json,
                "folderId": folder_id,
                "message": message,
                "overwrite": overwrite,
            }

            api_call: dict = Api(self.grafana_api_model).call_the_api(
                f"{APIEndpoints.DASHBOARDS.value}/db",
                RequestsMethods.POST,
                json.dumps(dashboard_json_complete),
            )

            if api_call.get("status") != "success":
                logging.error(f"Check the error: {api_call}.")
                raise Exception
            else:
                logging.info("You successfully deployed the dashboard.")
        else:
            logging.error(
                "There is no dashboard_path or dashboard_json or message defined."
            )
            raise ValueError

    def delete_dashboard_by_name_and_path(
        self, dashboard_name: str, dashboard_path: str
    ):
        """The method includes a functionality to delete the specified dashboard inside the model

        Args:
            dashboard_name (str): Specify the dashboard name of the deleted dashboard
            dashboard_path (str): Specify the dashboard path in which the dashboard is to be placed

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            None
        """

        if len(dashboard_name) != 0 and len(dashboard_path) != 0:
            dashboard_uid: dict = self.get_dashboard_uid_and_id_by_name_and_folder(
                dashboard_name, dashboard_path
            )

            if len(dashboard_uid) != 0:
                api_call: dict = Api(self.grafana_api_model).call_the_api(
                    f"{APIEndpoints.DASHBOARDS.value}/uid/{dashboard_uid.get('uid')}",
                    RequestsMethods.DELETE,
                )

                if f"Dashboard {dashboard_name} deleted" != api_call.get("message"):
                    logging.error(f"Please, check the error: {api_call}.")
                    raise Exception
                else:
                    logging.info("You successfully destroyed the dashboard.")
            else:
                logging.error("Nothing to delete. There is no dashboard available.")
                raise ValueError
        else:
            logging.error("There is no dashboard_name or dashboard_path defined.")
            raise ValueError

    def get_dashboard_by_uid(self, uid: str) -> dict:
        """The method includes a functionality to get the dashboard from the specified uid

        Args:
            uid (str): Specify the uid of the dashboard

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            api_call (dict): Returns the dashboard
        """

        if len(uid) != 0:
            api_call: dict = Api(self.grafana_api_model).call_the_api(
                f"{APIEndpoints.DASHBOARDS.value}/uid/{uid}"
            )

            if api_call.get("dashboard") is None:
                logging.error(f"Please, check the error: {api_call}.")
                raise Exception
            else:
                return api_call
        else:
            logging.error("There is no dashboard uid defined.")
            raise ValueError

    def get_dashboard_home(self) -> dict:
        """The method includes a functionality to get the home dashboard

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            api_call (dict): Returns the home dashboard
        """

        api_call: dict = Api(self.grafana_api_model).call_the_api(
            f"{APIEndpoints.DASHBOARDS.value}/home"
        )

        if api_call.get("dashboard") is None:
            logging.error(f"Please, check the error: {api_call}.")
            raise Exception
        else:
            return api_call

    def get_dashboard_tags(self) -> list:
        """The method includes a functionality to get the all tags of all dashboards

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            api_call (list): Returns all dashboard tags
        """

        api_call: list = Api(self.grafana_api_model).call_the_api(
            f"{APIEndpoints.DASHBOARDS.value}/tags"
        )

        if api_call == list() or api_call[0].get("term") is None:
            logging.error(f"Please, check the error: {api_call}.")
            raise Exception
        else:
            return api_call

    def get_dashboard_uid_and_id_by_name_and_folder(
        self, dashboard_name: str, dashboard_path: str
    ) -> dict:
        """The method includes a functionality to extract the dashboard uid specified inside the model

        Args:
            dashboard_name (str): Specify the dashboard name of the dashboard
            dashboard_path (str): Specify the dashboard path of the dashboard

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            api_call (dict): Returns the dashboard uid and the id
        """

        if len(dashboard_name) != 0 and len(dashboard_path) != 0:
            folder_id: int = Folder(
                self.grafana_api_model
            ).get_folder_id_by_dashboard_path(dashboard_path)

            search_query: str = f"{APIEndpoints.SEARCH.value}?folderIds={folder_id}&query={dashboard_name}"
            dashboard_meta: list = Api(self.grafana_api_model).call_the_api(
                search_query
            )

            for dashboard_meta_object in dashboard_meta:
                if dashboard_meta_object.get("title") is not None:
                    if dashboard_meta_object.get("title") == dashboard_name:
                        if (
                            dashboard_meta_object.get("uid") is not None
                            and dashboard_meta_object.get("id") is not None
                        ):
                            return dict(
                                {
                                    "uid": dashboard_meta_object.get("uid"),
                                    "id": dashboard_meta_object.get("id"),
                                }
                            )
                        else:
                            logging.error("There is no uid or id defined.")
                            raise ValueError
                else:
                    logging.error("There is no title defined.")
                    raise ValueError
        else:
            logging.error("There is no dashboard_name or dashboard_path defined.")
            raise ValueError

    def get_dashboard_permissions(self, id: int) -> list:
        """The method includes a functionality to extract the dashboard permissions based on the specified id

        Args:
            id (int): Specify the id of the dashboard

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            api_call (list): Returns the dashboard permissions of a dashboard as list
        """

        if id != 0:
            api_call: list = Api(self.grafana_api_model).call_the_api(
                f"{APIEndpoints.DASHBOARDS.value}/id/{id}/permissions"
            )

            if api_call == list() or api_call[0].get("role") is None:
                logging.error(f"Please, check the error: {api_call}.")
                raise Exception
            else:
                return api_call
        else:
            logging.error("There is no dashboard id defined.")
            raise ValueError

    def get_dashboard_permissions_by_uid(self, uid: str) -> list:
        """The method includes a functionality to extract the dashboard permissions based on the specified uid

        Args:
            uid (str): Specify the uid of the dashboard

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            api_call (list): Returns the dashboard permissions of a dashboard as list
        """

        if len(uid) != 0:
            api_call: list = Api(self.grafana_api_model).call_the_api(
                f"{APIEndpoints.DASHBOARDS.value}/uid/{uid}/permissions"
            )

            if api_call == list() or api_call[0].get("role") is None:
                logging.error(f"Please, check the error: {api_call}.")
                raise Exception
            else:
                return api_call
        else:
            logging.error("There is no dashboard uid defined.")
            raise ValueError

    def update_dashboard_permissions(self, id: int, permission_json: dict):
        """The method includes a functionality to update the dashboard permissions based on the specified id and the permission json document

        Args:
            id (int): Specify the id of the dashboard
            permission_json (dict): Specify the inserted permissions as dict

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            None
        """

        if id != 0 and len(permission_json) != 0:
            api_call: dict = Api(self.grafana_api_model).call_the_api(
                f"{APIEndpoints.DASHBOARDS.value}/id/{id}/permissions",
                RequestsMethods.POST,
                json.dumps(permission_json),
            )

            if api_call.get("message") != "Dashboard permissions updated":
                logging.error(f"Please, check the error: {api_call}.")
                raise Exception
            else:
                logging.info("You successfully modified the dashboard permissions.")
        else:
            logging.error("There is no dashboard id or permission json defined.")
            raise ValueError

    def update_dashboard_permissions_by_uid(self, uid: str, permission_json: dict):
        """The method includes a functionality to update the dashboard permissions based on the specified uid and the permission json document

        Args:
            uid (str): Specify the uid of the dashboard
            permission_json (dict): Specify the inserted permissions as dict

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            None
        """

        if len(uid) != 0 and len(permission_json) != 0:
            api_call: dict = Api(self.grafana_api_model).call_the_api(
                f"{APIEndpoints.DASHBOARDS.value}/uid/{uid}/permissions",
                RequestsMethods.POST,
                json.dumps(permission_json),
            )

            if api_call.get("message") != "Dashboard permissions updated":
                logging.error(f"Please, check the error: {api_call}.")
                raise Exception
            else:
                logging.info("You successfully modified the dashboard permissions.")
        else:
            logging.error("There is no dashboard uid or permission json defined.")
            raise ValueError

    def get_dashboard_versions(self, id: int) -> list:
        """The method includes a functionality to extract the versions of a dashboard based on the specified id

        Args:
            id (int): Specify the id of the dashboard

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            api_call (list): Returns all dashboard versions of a dashboard as list
        """

        if id != 0:
            api_call: list = Api(self.grafana_api_model).call_the_api(
                f"{APIEndpoints.DASHBOARDS.value}/id/{id}/versions",
            )

            if api_call == list() or api_call[0].get("id") is None:
                logging.error(f"Please, check the error: {api_call}.")
                raise Exception
            else:
                return api_call
        else:
            logging.error("There is no dashboard id defined.")
            raise ValueError

    def get_dashboard_versions_by_uid(self, uid: str) -> list:
        """The method includes a functionality to extract the versions of a dashboard based on the specified uid

        Args:
            uid (str): Specify the id of the dashboard

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            api_call (list): Returns all dashboard versions of a dashboard as list
        """

        if len(uid) != 0:
            api_call: list = Api(self.grafana_api_model).call_the_api(
                f"{APIEndpoints.DASHBOARDS.value}/uid/{uid}/versions",
            )

            if api_call == list() or api_call[0].get("uid") is None:
                logging.error(f"Please, check the error: {api_call}.")
                raise Exception
            else:
                return api_call
        else:
            logging.error("There is no dashboard uid defined.")
            raise ValueError

    def get_dashboard_version(self, id: int, version_id: int) -> dict:
        """The method includes a functionality to extract a specified version of a dashboard based on the specified dashboard id and a version_id of the dashboard

        Args:
            id (int): Specify the id of the dashboard
            version_id (int): Specify the version_id of a dashboard

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            api_call (list): Returns a dashboard version of a dashboard as dict
        """

        if id != 0 and version_id != 0:
            api_call: dict = Api(self.grafana_api_model).call_the_api(
                f"{APIEndpoints.DASHBOARDS.value}/id/{id}/versions/{version_id}",
            )

            if api_call == dict() or api_call.get("id") is None:
                logging.error(f"Please, check the error: {api_call}.")
                raise Exception
            else:
                return api_call
        else:
            logging.error("There is no dashboard id or version_id defined.")
            raise ValueError

    def get_dashboard_version_by_uid(self, uid: str, version_id: int) -> dict:
        """The method includes a functionality to extract a specified version of a dashboard based on the specified dashboard uid and a version_id of the dashboard

        Args:
            uid (str): Specify the uid of the dashboard
            version_id (int): Specify the version_id of a dashboard

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            api_call (list): Returns a dashboard version of a dashboard as dict
        """

        if len(uid) != 0 and version_id != 0:
            api_call: dict = Api(self.grafana_api_model).call_the_api(
                f"{APIEndpoints.DASHBOARDS.value}/uid/{uid}/versions/{version_id}",
            )

            if api_call == dict() or api_call.get("uid") is None:
                logging.error(f"Please, check the error: {api_call}.")
                raise Exception
            else:
                return api_call
        else:
            logging.error("There is no dashboard uid or version_id defined.")
            raise ValueError

    def restore_dashboard_version(self, id: int, version: dict):
        """The method includes a functionality to restore a specified version of a dashboard based on the specified dashboard id and a version as dict of the dashboard

        Args:
            id (int): Specify the id of the dashboard
            version (dict): Specify the version_id of a dashboard

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            None
        """

        if id != 0 and version != dict():
            api_call: dict = Api(self.grafana_api_model).call_the_api(
                f"{APIEndpoints.DASHBOARDS.value}/id/{id}/restore",
                RequestsMethods.POST,
                json.dumps(version),
            )

            if (
                api_call.get("status") != "success"
                or api_call.get("message") is not None
            ):
                logging.error(f"Check the error: {api_call}.")
                raise Exception
            else:
                logging.info("You successfully restored the dashboard.")
        else:
            logging.error("There is no dashboard id or version_id defined.")
            raise ValueError

    def restore_dashboard_version_by_uid(self, uid: str, version: dict):
        """The method includes a functionality to restore a specified version of a dashboard based on the specified dashboard uid and a version as dict of the dashboard

        Args:
            uid (str): Specify the uid of the dashboard
            version (dict): Specify the version_id of a dashboard

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            None
        """

        if len(uid) != 0 and version != dict():
            api_call: dict = Api(self.grafana_api_model).call_the_api(
                f"{APIEndpoints.DASHBOARDS.value}/uid/{uid}/restore",
                RequestsMethods.POST,
                json.dumps(version),
            )

            if (
                api_call.get("status") != "success"
                or api_call.get("message") is not None
            ):
                logging.error(f"Check the error: {api_call}.")
                raise Exception
            else:
                logging.info("You successfully restored the dashboard.")
        else:
            logging.error("There is no dashboard uid or version_id defined.")
            raise ValueError

    def calculate_dashboard_diff(
        self,
        dashboard_id_and_version_base: dict,
        dashboard_id_and_version_new: dict,
        diff_type: str = "json",
    ) -> str:
        """The method includes a functionality to calculate the diff of specified versions of a dashboard based on the specified dashboard uid and the selected version of the base dashboard and the new dashboard and the diff type (basic or json)

        Args:
            dashboard_id_and_version_base (dict): Specify the version and id of the base dashboard
            dashboard_id_and_version_new (dict): Specify the version and id of the new dashboard
            diff_type (str): Specify the diff type (basic or json) (default json)

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            api_call (str): Returns the difference of the two specified dashboards
        """
        possible_diff_types: list = list(["basic", "json"])

        if diff_type.lower() in possible_diff_types:
            if (
                dashboard_id_and_version_base != dict()
                and dashboard_id_and_version_new != 0
            ):
                diff_object: dict = dict()
                diff_object.update({"base": dashboard_id_and_version_base})
                diff_object.update({"new": dashboard_id_and_version_new})
                diff_object.update({"diffType": diff_type.lower()})

                api_call: any = Api(self.grafana_api_model).call_the_api(
                    f"{APIEndpoints.DASHBOARDS.value}/calculate-diff",
                    RequestsMethods.POST,
                    json.dumps(diff_object),
                )

                if api_call.status_code != 200:
                    logging.error(f"Check the error: {api_call.text}.")
                    raise Exception
                else:
                    return api_call.text
            else:
                logging.error(
                    "There is no dashboard_uid_and_version_base or dashboard_uid_and_version_new defined."
                )
                raise ValueError
        else:
            logging.error(
                f"The diff_type: {diff_type.lower()} is not valid. Please specify a valid value."
            )
            raise ValueError
