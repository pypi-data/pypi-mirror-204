from logging import Logger


def process_cnv(xml_in_file: str, root_path: str, prefix: str, log: Logger):
    copy_number_path_name = f"{root_path}/{prefix}.copynumber.csv"
    log.info(f"Saving file to {copy_number_path_name}")
    with open(copy_number_path_name, "w") as f:
        f.write(
            "sample_id,gene,copy_number,status,attributes,chromosome,start_position,end_position,interpretation\n"
        )

    return copy_number_path_name
