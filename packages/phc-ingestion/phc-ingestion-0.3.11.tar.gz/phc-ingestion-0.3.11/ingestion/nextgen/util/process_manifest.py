from ruamel.yaml import YAML
from logging import Logger
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal


def extract_patient_data(pdf_in_file: str):
    patient_data = {}
    patient_data["patientInfo"] = {}

    for page_layout in extract_pages(pdf_in_file, maxpages=1):
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                row_text = element.get_text()
                row_text_lower = row_text.lower()

                if (
                    "patientLastName" not in patient_data
                    and "Patient Name".lower() in row_text_lower
                ):
                    patientNameArray = row_text.split(":")[1].strip().split(",")
                    patient_data["patientInfo"]["firstName"] = patientNameArray[1].strip()
                    patient_data["patientLastName"] = patient_data["patientInfo"][
                        "lastName"
                    ] = patientNameArray[0].strip()
                elif "patientDOB" not in patient_data and "Birthdate".lower() in row_text_lower:
                    patient_data["patientDOB"] = patient_data["patientInfo"][
                        "dob"
                    ] = row_text.split(":")[1].strip()
                elif "mrn" not in patient_data and "MRN #".lower() in row_text_lower:
                    patient_data["mrn"] = row_text.split(":")[1].strip()
                elif (
                    "gender" not in patient_data["patientInfo"]
                    and "Gender".lower() in row_text_lower
                ):
                    patient_data["patientInfo"]["gender"] = row_text.split(":")[1].strip()

    return patient_data


def process_manifest(pdf_in_file: str, root_path: str, prefix: str, files: dict, log: Logger):
    yaml = YAML()
    manifest = {}
    manifest["testType"] = "NextGen"
    manifest.update(extract_patient_data(pdf_in_file))
    manifest_path = f"{root_path}/{prefix}.ga4gh.genomics.yml"
    log.info(f"Saving file to {manifest_path}")
    with open(manifest_path, "w") as file:
        yaml.dump(manifest, file)

    return manifest_path
