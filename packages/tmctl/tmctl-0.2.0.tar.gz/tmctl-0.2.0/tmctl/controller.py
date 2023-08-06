from dataclasses import dataclass
import datetime
import json
import logging
import os
import time

import requests
import yaml


@dataclass
class CommonOption:
    admin_url: str
    output: str = "json"
    indent: int = 4


@dataclass
class CommonResponse:
    status: bool
    error: dict = None
    data: dict = None


class AdminClient(object):
    def __init__(self, common_option: CommonOption, base_url: str = None):
        self._common_option = common_option
        self._admin_url = self._common_option.admin_url
        self._output = self._common_option.output
        self._indent = self._common_option.indent

        self._base_url = base_url

    def _response_to_object(self, response: dict) -> CommonResponse:
        return CommonResponse(
            status=response.get("status", False),
            error=response.get("error", None) or {},
            data=response.get("data", None) or {},
        )

    def _extract_namespace(self, cluster) -> str:
        settings = cluster.get("settings", None) or {}
        namespace = settings.get("namespace", None) or None

        changed_name = cluster["name"].replace("_", "-")

        namespace = namespace or changed_name

        return namespace

    def _parse_proxy_service(self, yamls_str) -> str:
        find = False
        proxy_name = None

        for each in yaml.load_all(yamls_str, Loader=yaml.Loader):
            if find:
                break

            if not isinstance(each, dict):
                continue

            kind = each.get("kind", "")
            if kind == "Service":
                port_list = each["spec"]["ports"]
                for port_spec in port_list:
                    if port_spec["port"] == 8088:
                        find = True
                        proxy_name = each["metadata"]["name"]

        return proxy_name

    def _send_delete(self, url) -> bool:
        response = requests.delete(self._admin_url + url)

        if response.ok:
            logging.debug(
                f"url: {self._admin_url + url}, response ok, {response.status_code}, {response.text}"
            )
            return self._response_to_object(response.json()).status
        else:
            logging.debug(
                f"url: {self._admin_url + url}, response not ok, {response.status_code}, {response.text}"
            )
            return False

    def _send_get(self, url, params=None) -> CommonResponse:
        params = params or {}
        response = requests.get(self._admin_url + url, params=params)

        if response.ok:
            return self._response_to_object(response.json())
        else:
            return CommonResponse(
                status=False,
                error={"status_code": response.status_code, "text": response.text},
                data=None,
            )

    def _send_binary_post(self, url, file_path, form_data):
        files = {"file": open(file_path, "rb")}
        # data = { "name": "test_name-changed", "target_path": "/etc/trino/test/222" }

        response = requests.post(self._admin_url + url, data=form_data, files=files)
        if response.ok:
            return self._response_to_object(response.json())
        else:
            raise requests.exceptions.HTTPError(response.status_code)

    def _send_download(self, url, params=None):
        # res = requests.get(url + f"/v1/files/1/download")
        # return res.content ? or write to file?
        response = requests.get(self._admin_url + url, params=params)
        if response.ok:
            return response.content
        else:
            raise requests.exceptions.HTTPError(response.status_code)

    def _send_post(self, url, json_data: dict = None, form_data: dict = None):
        json_data = json_data or {}
        response = requests.post(self._admin_url + url, data=form_data, json=json_data)

        if response.ok:
            return self._response_to_object(response.json())
        else:
            logging.debug(response.text)
            raise requests.exceptions.HTTPError(response.status_code)

    def _yaml_load_all(self, filepath):
        yamls = []

        for each in yaml.load_all(open(filepath, "r"), Loader=yaml.Loader):
            yamls.append(each)

        return yamls

    def delete(self, name: str, model_id: int = None):
        delete_response = None
        identifier = model_id or name
        return_value = None

        if model_id:
            delete_response = self._send_delete(f"{self._base_url}/{model_id}")
        elif name:
            response = self._send_get(f"{self._base_url}", params={"name": name})

            if response.status:
                models = response.data
                if models:
                    model = models[0]

                    model_id = model["id"]

                    delete_response = self._send_delete(f"{self._base_url}/{model_id}")

        if delete_response:
            return_value = f"identifier: {identifier} is successfully deleted!"
        else:
            return_value = f"identifier: {identifier} does not be successfully deleted!"

        return return_value

    def get(self, name):
        response = self._send_get(f"{self._base_url}", {"name": name})

        if response.status:
            for each in response.data:
                self.print(each)

    def list(self):
        response = self._send_get(self._base_url)
        if response.status:
            self.print(response.data)

    def ls(self):
        return self.list()

    def print(self, dictionary):
        dictionary = dictionary or {}
        if self._output == "json":
            print(json.dumps(dictionary, indent=self._indent))
        elif self._output == "yaml":
            print(yaml.dump(dictionary, indent=self._indent))

    def rm(self, name: str, model_id: int = None):
        return self.delete(name, model_id)


class File(AdminClient):
    def __init__(self, common_option: CommonOption):
        super(File, self).__init__(common_option, "/v1/files")

    def download(self, name, path=None):
        path = path or "./"
        response = self._send_get(f"{self._base_url}", {"name": name})

        if response.status:
            file = response.data[0]

            binary = self._send_download(f"{self._base_url}/{file['id']}/download")

            if binary:
                file_path = os.path.join(path, file["file_name"])
                with open(file_path, "wb") as _f:
                    _f.write(binary)

                self.print("download success.")
            else:
                self.print("empty binary")
        else:
            self.print("cannot download file")

    def submit(self, path):
        yamls = self._yaml_load_all(path)

        for each in yamls:
            version = each.get("version", None)
            action_type = each.get("type", None)

            if version in ["v1/file"]:
                file_config = each.get("file", None) or {}
                name = file_config.get("name", None)
                file_path = file_config.get("file_path", None)
                target_path = file_config.get("target_path", None)

                if not name:
                    print("invalid name", name)
                    break

                if action_type == "create":
                    file_exists = os.path.exists(file_path)

                    if (not file_path) or (not file_exists):
                        print("invalid file_path", file_path)
                        break

                    response = self._send_binary_post(
                        "/v1/files",
                        file_path,
                        form_data={"name": name, "target_path": target_path},
                    )

                    if response.status:
                        self.print(response.data)
                    else:
                        logging.warning("file failed")
                elif action_type == "update":
                    file_id = file_config.get("id", None)

                    if file_id:
                        if file_path:
                            file_exists = os.path.exists(file_path)

                            if (not file_path) or (not file_exists):
                                print("invalid file_path", file_path)
                                break

                            response = self._send_binary_post(
                                f"/v1/files/{file_id}",
                                file_path,
                                form_data={
                                    "name": name,
                                    "target_path": target_path,
                                },
                            )
                        else:
                            response = self._send_post(
                                f"/v1/files/{file_id}",
                                form_data={
                                    "name": name,
                                    "target_path": target_path,
                                },
                            )

                        if response.status:
                            self.print(response.data)
                        else:
                            logging.warning("file submit failed")


class Catalog(AdminClient):
    def __init__(self, common_option: CommonOption):
        super(Catalog, self).__init__(common_option, "/v1/catalogs")

    def list(self):
        response = self._send_get("/v1/catalogs")
        if response.status:
            self.print(response.data)

    def ls(self):
        self.list()

    def rm(self, name: str = None, catalog_id: int = None):
        return self.delete(name, catalog_id)

    def submit(self, path):
        yamls = self._yaml_load_all(path)

        for each in yamls:
            version = each.get("version", None)
            action_type = each.get("type", None)

            if version in ["v1/catalog"]:
                catalog_config = each.get("catalog", None) or {}
                name = catalog_config.get("name", None)
                catalog_type = catalog_config.get("catalog_type", None)
                properties = catalog_config.get("properties", None)

                if not name:
                    print("invalid name", name)
                    break

                if not catalog_type:
                    print("invalid chart name", catalog_type)
                    break

                if action_type == "create":
                    response = self._send_post(
                        "/v1/catalogs",
                        json_data={
                            "name": name,
                            "catalog_type": catalog_type,
                            "properties": properties,
                        },
                    )

                    if response.status:
                        self.print(response.data)
                    else:
                        logging.warning("chart submit failed")
                elif action_type == "update":
                    catalog_id = catalog_config.get("id", None)

                    if catalog_id:
                        response = self._send_post(
                            f"/v1/catalogs/{catalog_id}",
                            json_data={
                                "name": name,
                                "catalog_type": catalog_type,
                                "properties": properties,
                            },
                        )

                        if response.status:
                            self.print(response.data)
                        else:
                            logging.warning("catalog submit failed")


class Cluster(AdminClient):
    def __init__(self, url):
        super(Cluster, self).__init__(url, "/v1/clusters")

    def delete(self, name, force=False, refresh=1, timeout=120):
        response = self._send_get("/v1/clusters", {"name": name})

        if response.status:
            clusters = response.data

            if clusters:
                cluster = clusters[0]
                health_check = self._health_check_status(cluster["id"])

                if health_check:
                    if force:
                        self.off(name=name, refresh=refresh, timeout=timeout)
                    else:
                        print("Cluster is on. please off the cluster first.")
                        logging.warning("Cluster is on. please off the cluster first.")
                        return

            super().delete(name)

    def _health_check_status(self, cluster_id):
        response = self._send_get(f"/v1/clusters/{cluster_id}/gateway/health")

        if response.status:
            logging.debug(f"{response.data}")
            return True
        else:
            return False

    def _waiting_release(self, release_id, refresh, timeout):
        start_time = datetime.datetime.now(datetime.timezone.utc)

        response = self._send_get(f"/v1/releases/{release_id}")
        finished = False
        timeout_flag = False
        release = response.data[0] if response.status else None

        while release.get("status", "QUEUED") not in ["FINISHED", "FAILED"]:
            time.sleep(refresh)

            current_time = datetime.datetime.now(datetime.timezone.utc)

            if (current_time - start_time).seconds > timeout:
                timeout_flag = True
                break

            response = self._send_get(f"/v1/releases/{release_id}")
            release = response.data[0] if response.status else None
            self.print(release)

        if timeout_flag:
            finished = False
        else:
            finished = True

        return finished

    def _waiting_and_get_release_log(self, release_id, refresh, timeout):
        start_time = datetime.datetime.now(datetime.timezone.utc)

        response = self._send_get(f"/v1/releases/{release_id}/log")
        celery_response = response.data[0] if response.status else None

        timeout_flag = False
        while celery_response.get("state", "PENDING") not in ["SUCCESS", "FAILURE"]:
            time.sleep(refresh)
            current_time = datetime.datetime.now(datetime.timezone.utc)

            if (current_time - start_time).seconds > timeout:
                timeout_flag = True
                break

            response = self._send_get(f"/v1/releases/{release_id}/log")
            celery_response = response.data[0] if response.status else None

            self.print(celery_response)

        if timeout_flag:
            response = None

        return celery_response

    def _execute_and_get_helm_release_log(self, url, refresh, timeout):
        response = self._send_post(url)
        release = response.data[0] if response.status else None

        release_id = release["id"]

        self.print(release)

        if not self._waiting_release(release_id, refresh, timeout):
            return None

        log_response = self._waiting_and_get_release_log(release_id, refresh, timeout)

        return log_response

    def _do_install(self, cluster_id, refresh, timeout):
        return self._execute_and_get_helm_release_log(
            f"/v1/clusters/{cluster_id}/install", refresh, timeout
        )

    def _do_upgrade(self, cluster_id, refresh, timeout):
        return self._execute_and_get_helm_release_log(
            f"/v1/clusters/{cluster_id}/upgrade", refresh, timeout
        )

    def list(self):
        response = self._send_get(self._base_url)

        if response.status:
            clusters = response.data

            for cluster in clusters:
                cluster["status"] = (
                    "ON" if self._health_check_status(cluster["id"]) else "OFF"
                )

            self.print(clusters)

    def ls(self):
        self.list()

    def get(self, name):
        response = self._send_get("/v1/clusters", {"name": name})

        if response.status:
            clusters = response.data

            if clusters:
                cluster = clusters[0]

                cluster["status"] = (
                    "ON" if self._health_check_status(cluster["id"]) else "OFF"
                )

                self.print(cluster)

    def status(self, name, refresh=1, timeout=120):
        cluster = None

        response = self._send_get("/v1/clusters", params={"name": name})

        if response.status:
            clusters = response.data

            if clusters:
                cluster = clusters[0]

        if not cluster:
            return

        cluster_status_response = self._execute_and_get_helm_release_log(
            f"/v1/clusters/{cluster['id']}/status", refresh, timeout
        )

        response_log = cluster_status_response.get("log", {}) or {}
        return_value = response_log.get("return", {}) or {}

        is_cluster_installed = len(return_value.get("stdout", "")) > 0

        proxy_status_response = self._execute_and_get_helm_release_log(
            f"/v1/clusters/{cluster['id']}/proxy/status", refresh, timeout
        )

        response_log = proxy_status_response.get("log", {}) or {}
        return_value = response_log.get("return", {}) or {}

        is_proxy_installed = len(return_value.get("stdout", "")) > 0

        status = {
            "cluster installed:": is_cluster_installed,
            "proxy installed:": is_proxy_installed,
            "cluster status (health check):": self._health_check_status(cluster["id"]),
        }

        self.print(status)

    def rm(self, name, force=False, refresh=1, timeout=120):
        return self.delete(name, force, refresh, timeout)

    def submit(self, path):
        yamls = self._yaml_load_all(path)

        for each in yamls:
            version = each.get("version", None)
            action_type = each.get("type", None)

            if version in ["v1/cluster"]:
                cluster_config = each.get("cluster", None) or {}
                name = cluster_config.get("name", None)

                direct_on = cluster_config.get("direct_on", True)

                chart_name = cluster_config.get("chart", None)

                params = {"name": chart_name}

                response = self._send_get("/v1/charts", params=params)

                chart_id = None
                if response.status:
                    charts = response.data
                    if charts:
                        chart_id = charts[0]["id"]

                    if not chart_id:
                        raise Exception("invalid chart options")

                catalog_config = cluster_config.get("catalogs", None) or []

                catalog_list = []

                for catalog_name in catalog_config:
                    response = self._send_get(f"/v1/catalogs?name={catalog_name}")

                    if response.status:
                        catalogs = response.data

                        if catalogs:
                            catalog_list.append(catalogs[0]["id"])

                file_config = cluster_config.get("files", None) or []

                file_list = []

                for file_name in file_config:
                    response = self._send_get(f"/v1/files?name={file_name}")

                    if response.status:
                        files = response.data

                        if files:
                            file_list.append(files[0]["id"])

                settings = cluster_config.get("settings", None) or {}

                if not name:
                    print("invalid name", name)
                    break

                if not chart_id:
                    print("invalid chart id or chart_name", chart_id, chart_name)
                    break

                if action_type == "create":
                    response = self._send_post(
                        "/v1/clusters",
                        json_data={
                            "name": name,
                            "chart_id": chart_id,
                            "catalog_list": catalog_list,
                            "file_list": file_list,
                            "settings": settings,
                        },
                    )

                    if response.status:
                        clusters = response.data

                        if clusters:
                            cluster = clusters[0]
                            self.print(cluster)
                            if direct_on:
                                self.on(cluster_id=cluster["id"], is_update=False)
                    else:
                        logging.warning("cluster submit failed")
                elif action_type == "update":
                    cluster_id = cluster_config.get("id", None)

                    if cluster_id:
                        response = self._send_post(
                            f"/v1/clusters/{cluster_id}",
                            json_data={
                                "name": name,
                                "chart_id": chart_id,
                                "catalog_list": catalog_list,
                                "file_list": file_list,
                                "settings": settings,
                            },
                        )

                        if response.status:
                            clusters = response.data

                            if clusters:
                                cluster = clusters[0]
                                self.print(cluster)
                                if direct_on:
                                    self.on(cluster_id=cluster_id, is_update=True)
                        else:
                            logging.warning("cluster submit failed")
                    else:
                        logging.warning("cluster id is unknown.")

    def on(self, name=None, cluster_id=None, is_update=False, refresh=1, timeout=120):
        cluster = None
        cluster_identifer = name or cluster_id

        if cluster_id:
            response = self._send_get(f"/v1/clusters/{cluster_id}")

            if response.status:
                cluster = response.data[0]
        elif name:
            response = self._send_get("/v1/clusters", params={"name": name})

            if response.status:
                clusters = response.data
                if clusters:
                    cluster = clusters[0]

        if not cluster:
            logging.warning(f"cluster: {cluster_identifer} is invalid")
            return

        cluster_id = cluster["id"]
        namespace_name = self._extract_namespace(cluster)

        response = {}

        if is_update:
            response = self._do_upgrade(cluster_id, refresh, timeout)
        else:
            response = self._do_install(cluster_id, refresh, timeout)

        response_log = response.get("log", {}) or {}
        return_value = response_log.get("return", {}) or {}

        if response_log.get("success", False) or False:
            logging.info(return_value)
            logging.info("cluster install is succeeded!")
            logging.info("try to register proxy to api gateway...")
        else:
            logging.warning(response_log)
            logging.warning("cluster install failed")
            return

        proxy_manifest = self._execute_and_get_helm_release_log(
            f"/v1/clusters/{cluster_id}/proxy/manifest", refresh, timeout
        )

        if not proxy_manifest:
            logging.warning("getting cluster proxy information is failed")
            return None

        response_log = proxy_manifest.get("log", {}) or {}
        return_value = response_log.get("return", {}) or {}

        if response_log.get("success", False) or False:
            pass
        else:
            logging.warning("get proxy info failed")
            return

        proxy_name = self._parse_proxy_service(return_value.get("stdout", ""))

        service_name = f"""{proxy_name}.{namespace_name}"""

        response = self._send_post(
            f"/v1/clusters/{cluster_id}/gateway/register",
            {"service_name": service_name},
        )

        logging.info(response)

    def off(self, name=None, cluster_id=None, refresh=1, timeout=120):
        cluster = None

        if cluster_id:
            response = self._send_get(f"/v1/clusters/{cluster_id}")

            if response.status:
                cluster = response.data[0]
        if name:
            response = self._send_get("/v1/clusters", params={"name": name})

            if response.status:
                clusters = response.data
                if clusters:
                    cluster = clusters[0]

        if not cluster:
            logging.warning("cluster id or name is invalid")
            return

        cluster_id = cluster["id"]

        response = self._send_delete(f"/v1/clusters/{cluster_id}/gateway/deregister")
        logging.info(response)

        uninstall_response = self._execute_and_get_helm_release_log(
            f"/v1/clusters/{cluster_id}/uninstall", refresh, timeout
        )

        if not uninstall_response:
            self.print("cluster uninstall is failed")
        else:
            self.print("cluster uninstall is succeeded!")


class HelmChart(AdminClient):
    def __init__(self, url):
        super(HelmChart, self).__init__(url, "/v1/charts")

    def ls(self):
        self.list()

    def rm(self, name: str = None, chart_id: int = None):
        return self.delete(name, chart_id)

    def submit(self, path):
        yamls = self._yaml_load_all(path)

        for each in yamls:
            version = each.get("version", None)
            action_type = each.get("type", None)

            if version in ["v1/chart"]:
                chart_config = each.get("chart", None) or {}
                name = chart_config.get("name", None)
                chart_name = chart_config.get("chart_name", None)
                chart_version = chart_config.get("version", None)
                registry = chart_config.get("registry", None)
                repository = chart_config.get("repository", None)
                values = chart_config.get("values", None)

                if not name:
                    print("invalid name", name)
                    break

                if not chart_name:
                    print("invalid chart name", chart_name)
                    break

                if action_type == "create":
                    response = self._send_post(
                        "/v1/charts",
                        json_data={
                            "name": name,
                            "chart_name": chart_name,
                            "version": chart_version,
                            "registry": registry,
                            "repository": repository,
                            "values": values,
                        },
                    )

                    if response.status:
                        self.print(response.data[0])
                    else:
                        logging.warning("chart submit failed")
                elif action_type == "update":
                    chart_id = chart_config.get("id", None)

                    if chart_id:
                        response = self._send_post(
                            f"/v1/charts/{chart_id}",
                            json_data={
                                "name": name,
                                "chart_name": chart_name,
                                "version": chart_version,
                                "registry": registry,
                                "repository": repository,
                            },
                        )

                        if response.status:
                            self.print(response.data[0])
                        else:
                            logging.warning("chart submit failed")


class MountFile(AdminClient):
    def __init__(self, url):
        super(MountFile, self).__init__(url, "/v1/mounts")

    def get(self, mount_path):
        response = self._send_get(f"{self._base_url}", {"mount_path": mount_path})

        if response.status:
            for each in response.data:
                self.print(each)

    def delete(self, mount_path: str, model_id: int = None):
        delete_response = None
        identifier = model_id or mount_path
        return_value = None

        if model_id:
            delete_response = self._send_delete(f"{self._base_url}/{model_id}")
        elif mount_path:
            response = self._send_get(
                f"{self._base_url}", params={"mount_path": mount_path}
            )

            if response.status:
                models = response.data
                if models:
                    model = models[0]

                    model_id = model["id"]

                    delete_response = self._send_delete(f"{self._base_url}/{model_id}")

        if delete_response:
            return_value = f"identifier: {identifier} is successfully deleted!"
        else:
            return_value = f"identifier: {identifier} does not be successfully deleted!"

        return return_value

    def download(self, mount_path, path=None):
        path = path or "./"
        response = self._send_get(f"{self._base_url}", {"mount_path": mount_path})

        if response.status:
            mount_file = response.data[0]

            binary = self._send_download(
                f"{self._base_url}/{mount_file['id']}/download"
            )

            if binary:
                file_path = os.path.join(path, mount_file["file_name"])
                with open(file_path, "wb") as _f:
                    _f.write(binary)

                self.print("download success.")
            else:
                self.print("empty binary")
        else:
            self.print("cannot download file")

    def submit(self, path):
        yamls = self._yaml_load_all(path)

        for each in yamls:
            version = each.get("version", None)
            action_type = each.get("type", None)

            if version in ["v1/mount"]:
                file_config = each.get("mount", None) or {}
                source_path = file_config.get("source_path", None)
                mount_path = file_config.get("mount_path", None)
                target_path = file_config.get("target_path", None)
                refresh = file_config.get("refresh", None) or False

                if not refresh:
                    if not source_path:
                        print("invalid path", source_path)
                        break

                    file_exists = os.path.exists(source_path)

                    if not file_exists:
                        print("invalid currnet source fil path", source_path)
                        break

                    if not mount_path:
                        print("invalid mount_path", mount_path)
                        break

                if action_type == "create":
                    response = None
                    if refresh:
                        response = self._send_post(
                            "/v1/mounts",
                            form_data={
                                "mount_path": mount_path,
                                "target_path": target_path,
                                "refresh": True,
                            },
                        )
                    else:
                        response = self._send_binary_post(
                            "/v1/mounts",
                            source_path,
                            form_data={
                                "mount_path": mount_path,
                                "target_path": target_path,
                            },
                        )

                    if response.status:
                        self.print(response.data)
                    else:
                        logging.warning("mount file create failed")
                elif action_type == "update":
                    mount_file_id = file_config.get("id", None)

                    if mount_file_id:
                        response = self._send_binary_post(
                            f"/v1/mounts/{mount_file_id}",
                            source_path,
                            form_data={
                                "mount_path": mount_path,
                                "target_path": target_path,
                            },
                        )

                        if response.status:
                            self.print(response.data)
                        else:
                            logging.warning("mount file update failed")
