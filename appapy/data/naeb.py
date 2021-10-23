import os
from typing import IO, Tuple
from html.parser import HTMLParser
import json
import csv


class ExtractedUsage:
    def __init__(self):
        self.scientific_name: str = ""
        self.usda_symbol: str = ""
        self.common_names: str = ""
        self.family: str = ""
        self.family_apg: str = ""
        self.native_tribe: str = ""
        self.use_category: str = ""
        self.use_subcategory: str = ""
        self.notes: str = ""
        self.record: int = ""
        self.id: int = 0
        self.documentation: str = ""


class NaebHTMLParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool) -> None:

        super().__init__(convert_charrefs=convert_charrefs)
        self.usage = ExtractedUsage()

    def reset_usage(self):
        self.usage = ExtractedUsage()

    def handle_starttag(self, tag: str, attrs: list[Tuple[str, str]]) -> None:
        pass

    def handle_endtag(self, tag: str) -> None:
        pass

    def handle_data(self, data: str) -> None:

        data = data.strip()

        hit = False
        if data.startswith("Scientific name: "):
            self.usage.scientific_name = data.replace("Scientific name: ", "").strip().strip("\r\n\t ")
            hit = True
        elif data.startswith("USDA symbol: "):
            self.usage.usda_symbol = data.replace("USDA symbol: ", "").replace(" (", "").strip()            
            hit = True
        elif data.startswith("Common names: "):
            self.usage.common_names = data.replace("Common names: ", "").strip()
            hit = True
        elif data.startswith("Family: "):
            self.usage.family = data.replace("Family: ", "").strip()
            hit = True
        elif data.startswith("Family (APG): "):
            self.usage.family_apg = data.replace("Family (APG): ", "").strip()
            hit = True
        elif data.startswith("Native American Tribe: "):
            self.usage.native_tribe = data.replace(
                "Native American Tribe: ", ""
            ).strip()
            hit = True
        elif data.startswith("Use category: "):
            self.usage.use_category = data.replace("Use category: ", "").strip()
            hit = True
        elif data.startswith("Use sub-category: "):
            self.usage.use_subcategory = data.replace("Use sub-category: ", "").strip()
            hit = True
        elif data.startswith("Notes: "):
            self.usage.notes = data.replace("Notes: ", "").strip()
            hit = True
        elif data.startswith("RECRD: "):
            self.usage.record = (
                data.replace("RECRD: ", "").replace(f"id: {self.usage.id}", "").strip()
            )
            hit = True
        elif " page " in data:
            self.usage.documentation = data.strip().strip("\r\n\t ")
            hit = True


def process():

    base_path = "C:\\Users\\Chris\\Desktop\\naeb\\naeb.brit.org\\uses"
    output_path = "C:\\Users\\Chris\\Desktop\\naeb\\naeb.brit.org\\uses.csv"
    parser = NaebHTMLParser(convert_charrefs=True)
    usages = list[ExtractedUsage]()

    for dir_path, dir_names, file_names in os.walk(base_path):
        for use_id in dir_names:

            if not use_id.isnumeric():
                continue

            use_directory_path = os.path.join(dir_path, use_id)
            use_file_path = os.path.join(use_directory_path, "index.htm")

            if not os.path.isfile(use_file_path):
                print(f"Missing {use_file_path}")
                continue

            try:
                with open(use_file_path, mode="r", encoding="utf-8") as fs:
                    content = fs.read()

                    parser.usage.id = use_id
                    parser.feed(content)

                    usages.append(parser.usage)

                    parser.reset_usage()

            except UnicodeError as ue:
                print(ue)

        break

    header = [
        "scientific_name",
        "usda_symbol",
        "common_names",
        "family",
        "family_apg",
        "native_tribe",
        "use_category",
        "use_subcategory",
        "notes",
        "record",
        "id",
        "documentation",
    ]

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as csvfile:
        writer = csv.writer(csvfile,dialect='excel')
        
        writer.writerow(header)
        for usage in usages:
            writer.writerow(
                [
                    usage.scientific_name,
                    usage.usda_symbol,
                    usage.common_names,
                    usage.family,
                    usage.family_apg,
                    usage.native_tribe,
                    usage.use_category,
                    usage.use_subcategory,
                    usage.notes,
                    usage.record,
                    usage.id,
                    usage.documentation,
                ]
            )
