from enum import Enum
from lifeomic_logging import scoped_logger

from ingestion.nextgen.util.process_cnv import process_cnv
from ingestion.nextgen.util.process_manifest import process_manifest
from ingestion.nextgen.util.process_structural import process_structural
from ingestion.nextgen.util.process_vcf import process_vcf


def process(
    account_id: str,
    vendor_files: dict,
    local_output_dir: str,
    source_file_id: str,
    prefix: str,
    phc_output_dir: str = ".lifeomic/nextgen",
) -> None:
    with scoped_logger(__name__) as log:
        cnv_path_name = process_cnv(
            xml_in_file=vendor_files["xmlFile"],
            root_path=local_output_dir,
            prefix=prefix,
            log=log,
        )
        manifest_path_name = process_manifest(
            pdf_in_file=vendor_files["pdfFile"],
            root_path=local_output_dir,
            prefix=prefix,
            files=vendor_files,
            log=log,
        )
        structural_path_name = process_structural(
            pdf_in_file=vendor_files["pdfFile"],
            root_path=local_output_dir,
            prefix=prefix,
            log=log,
        )
        somatic_vcf_meta_data = process_vcf(
            vcf_in_file=vendor_files["somaticVcfFile"],
            root_path=local_output_dir,
            prefix=prefix,
            sequence_type="somatic",
            log=log,
        )
        germline_vcf_meta_data = process_vcf(
            vcf_in_file=vendor_files["germlineVcfFile"],
            root_path=local_output_dir,
            prefix=prefix,
            sequence_type="germline",
            log=log,
        )

    return {
        "cnv_path_name": cnv_path_name,
        "manifest_path_name": manifest_path_name,
        "structural_path_name": structural_path_name,
        "somatic_vcf_meta_data": somatic_vcf_meta_data,
        "germline_vcf_meta_data": germline_vcf_meta_data,
    }
