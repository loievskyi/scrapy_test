import os
import json
import urllib.parse


class UdataTestPipeline:
    def process_item(self, item, spider):
        country = "Germany"
        parsed_url = urllib.parse.urlparse(item["url"])
        domain = parsed_url.netloc.replace("-", "_")
        object_urn = parsed_url.path.split("/")[-2]

        directory_path = self._get_directory_path(country, domain)
        self._create_directory(directory_path)
        file_path = os.path.join(directory_path, f"{object_urn}.json")

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(dict(item), file, ensure_ascii=False, indent=4)

        return item

    def _get_directory_path(self, country, domain):
        return os.path.join("..", "data_files", country, domain)

    def _create_directory(self, directory_path):
        os.makedirs(directory_path, exist_ok=True)
