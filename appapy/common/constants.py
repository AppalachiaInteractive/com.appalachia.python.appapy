npm_registry = f"http://localhost:4873"
output_folder = "dist"
root_dir = "com.appalachia"
command_dir = f"{root_dir}/appa/cmd"
legal_dir = f"{root_dir}/org/legal"
license_dir = f"{legal_dir}/licenses"
common_dirs = [
    f"{root_dir}/appa/templates/.common",
    f"{legal_dir}/project-template"
]
DRY_RUN = False
