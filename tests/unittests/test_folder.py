from unittest import TestCase
from unittest.mock import MagicMock, patch

from grafana_api.model import APIModel
from grafana_api.folder import Folder


class FolderTestCase(TestCase):
    @patch("grafana_api.api.Api.call_the_api")
    def test_get_folders(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = list([{"title": None, "id": 12}])

        self.assertEqual(list([{"title": None, "id": 12}]), folder.get_folders())

    @patch("grafana_api.api.Api.call_the_api")
    def test_get_folders_error_response(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = list()

        with self.assertRaises(Exception):
            folder.get_folders()

    @patch("grafana_api.api.Api.call_the_api")
    def test_get_folder_by_uid(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict({"title": None, "id": 12})

        self.assertEqual(
            dict({"title": None, "id": 12}), folder.get_folder_by_uid("xty13y")
        )

    @patch("grafana_api.api.Api.call_the_api")
    def test_get_folder_by_uid_no_uid(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict()

        with self.assertRaises(ValueError):
            folder.get_folder_by_uid("")

    @patch("grafana_api.api.Api.call_the_api")
    def test_get_folder_by_uid_error_response(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict()

        with self.assertRaises(Exception):
            folder.get_folder_by_uid("xty13y")

    @patch("grafana_api.api.Api.call_the_api")
    def test_get_folder_by_id(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict({"title": None, "id": 12})

        self.assertEqual(dict({"title": None, "id": 12}), folder.get_folder_by_id(12))

    @patch("grafana_api.api.Api.call_the_api")
    def test_get_folder_by_id_no_id(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict()

        with self.assertRaises(ValueError):
            folder.get_folder_by_id(0)

    @patch("grafana_api.api.Api.call_the_api")
    def test_get_folder_by_id_error_response(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict()

        with self.assertRaises(Exception):
            folder.get_folder_by_id(10)

    @patch("grafana_api.api.Api.call_the_api")
    def test_create_folder(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict({"title": None, "id": 12})

        self.assertEqual(dict({"title": None, "id": 12}), folder.create_folder("test"))

    @patch("grafana_api.api.Api.call_the_api")
    def test_create_folder_specified_uid(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict({"title": None, "id": 12, "uid": "test"})

        self.assertEqual(
            dict({"title": None, "id": 12, "uid": "test"}),
            folder.create_folder("test", "test"),
        )

    @patch("grafana_api.api.Api.call_the_api")
    def test_create_folder_no_title(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict()

        with self.assertRaises(ValueError):
            folder.create_folder(MagicMock())

    @patch("grafana_api.api.Api.call_the_api")
    def test_create_folder_error_response(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict()

        with self.assertRaises(Exception):
            folder.create_folder("test")

    @patch("grafana_api.api.Api.call_the_api")
    def test_update_folder(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict({"title": "test1", "id": 12})

        self.assertEqual(
            dict({"title": "test1", "id": 12}),
            folder.update_folder("test", "test1", 10),
        )

    @patch("grafana_api.api.Api.call_the_api")
    def test_update_folder_no_uid(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict({"title": "test", "id": 12})

        self.assertEqual(
            dict({"title": "test", "id": 12}),
            folder.update_folder("test", uid="test", overwrite=True),
        )

    @patch("grafana_api.api.Api.call_the_api")
    def test_update_folder_overwrite_true(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict({"title": "test", "id": 12})

        self.assertEqual(
            dict({"title": "test", "id": 12}),
            folder.update_folder("test", "test", overwrite=True),
        )

    @patch("grafana_api.api.Api.call_the_api")
    def test_update_folder_no_title(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict()

        with self.assertRaises(ValueError):
            folder.update_folder(MagicMock(), MagicMock())

    @patch("grafana_api.api.Api.call_the_api")
    def test_update_folder_error_response(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict()

        with self.assertRaises(Exception):
            folder.update_folder("test", "test", 10)

    @patch("grafana_api.api.Api.call_the_api")
    def test_delete_folder(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value.status_code = 200

        self.assertEqual(None, folder.delete_folder("test"))

    @patch("grafana_api.api.Api.call_the_api")
    def test_delete_folder_no_uid(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value.status_code = 404

        with self.assertRaises(ValueError):
            folder.delete_folder("")

    @patch("grafana_api.api.Api.call_the_api")
    def test_delete_folder_error_response(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value.status_code = 404

        with self.assertRaises(Exception):
            folder.delete_folder("test")

    @patch("grafana_api.api.Api.call_the_api")
    def test_get_folder_permissions(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = list([{"folderId": "test"}])

        self.assertEqual(
            list([{"folderId": "test"}]), folder.get_folder_permissions("test")
        )

    @patch("grafana_api.api.Api.call_the_api")
    def test_get_folder_permissions_no_uid(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = list()
        with self.assertRaises(ValueError):
            folder.get_folder_permissions("")

    @patch("grafana_api.api.Api.call_the_api")
    def test_get_folder_permissions_error_response(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = list([{"test": "test"}])

        with self.assertRaises(Exception):
            folder.get_folder_permissions("test")

    @patch("grafana_api.api.Api.call_the_api")
    def test_update_folder_permissions(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict(
            {"message": "Dashboard permissions updated"}
        )

        self.assertEqual(
            None, folder.update_folder_permissions("test", dict({"test": "test"}))
        )

    @patch("grafana_api.api.Api.call_the_api")
    def test_update_folder_permissions_no_uid(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict()
        with self.assertRaises(ValueError):
            folder.update_folder_permissions("", dict())

    @patch("grafana_api.api.Api.call_the_api")
    def test_update_folder_permissions_error_response(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = dict({"message": "test"})

        with self.assertRaises(Exception):
            folder.update_folder_permissions("test", dict({"test": "test"}))

    @patch("grafana_api.folder.Folder.get_all_folder_ids_and_names")
    def test_get_folder_id_by_dashboard_path(self, all_folder_ids_and_names_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        all_folder_ids_and_names_mock.return_value = list([{"title": "test", "id": 12}])
        self.assertEqual(
            12, folder.get_folder_id_by_dashboard_path(dashboard_path="test")
        )

    def test_get_folder_id_by_dashboard_path_general_path(self):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        self.assertEqual(
            0, folder.get_folder_id_by_dashboard_path(dashboard_path="General")
        )

    def test_get_folder_id_by_dashboard_path_no_dashboard_path_defined(self):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        with self.assertRaises(ValueError):
            folder.get_folder_id_by_dashboard_path(dashboard_path="")

    @patch("grafana_api.folder.Folder.get_all_folder_ids_and_names")
    def test_get_folder_id_by_dashboard_path_no_title_match(
        self, all_folder_ids_and_names_mock
    ):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        all_folder_ids_and_names_mock.return_value = list(
            [{"title": None, "id": "xty13y"}]
        )
        with self.assertRaises(Exception):
            folder.get_folder_id_by_dashboard_path(dashboard_path="test")

    @patch("grafana_api.api.Api.call_the_api")
    def test_get_all_folder_ids_and_names(self, call_the_api_mock):
        model: APIModel = APIModel(host=MagicMock(), token=MagicMock())
        folder: Folder = Folder(grafana_api_model=model)

        call_the_api_mock.return_value = list(
            [{"title": "test", "id": 12, "test": "test"}]
        )

        self.assertEqual(
            list([{"title": "test", "id": 12}]), folder.get_all_folder_ids_and_names()
        )
