---
name: client-project-folder-setup
version: 1.0
description: Creates a hierarchical folder structure for clients and their associated projects.
trigger:
  - "create folders for clients and projects"
  - "set up client project directories"
  - "make client project structure"
params:
  client_projects:
    type: object
    description: A dictionary where keys are client names (string) and values are lists of project folder names (list of strings).
    examples:
      - { "Tiba Gift comp.": ["01_Al_Wahi_Gift_Shop", "02_Holy_Quran_Gift_Shop"], "Qahwitna comp.": ["11_Najdi_Coffee"] }
---

This skill automates the creation of a nested folder structure for various clients and their projects. It's useful for setting up new projects or ensuring consistent folder organization.

**Workflow:**

1.  **Define `client_projects`:** Prepare a Python dictionary mapping client names to a list of their respective project folder names.
2.  **Execute the skill:** Call this skill with the `client_projects` dictionary.

**Python Implementation:**

The skill uses the `os.makedirs` function to create directories. It iterates through the `client_projects` dictionary, creating a top-level folder for each client and then subfolders for each project under the client's directory.

```python
import os

def create_client_project_folders(base_path, client_projects):
    """
    Creates a hierarchical folder structure for clients and their projects.

    Args:
        base_path (str): The root directory where client folders will be created.
        client_projects (dict): A dictionary where keys are client names (string)
                                and values are lists of project folder names (list of strings).
    """
    os.makedirs(base_path, exist_ok=True)
    print(f"Ensured base path exists: {base_path}")

    for client, folders in client_projects.items():
        client_path = os.path.join(base_path, client)
        os.makedirs(client_path, exist_ok=True)
        print(f"Created client folder: {client_path}")
        for folder in folders:
            project_path = os.path.join(client_path, folder)
            os.makedirs(project_path, exist_ok=True)
            print(f"Created project folder: {project_path}")

# Example usage (this part would be dynamically generated or called by the agent)
# client_projects_data = {
#     "Tiba Gift comp.": ["01_Al_Wahi_Gift_Shop", "02_Holy_Quran_Gift_Shop", "06_As_Safiyyah_Giftshop", "07_Khair_Al_Khalq_Store"],
#     "Tezkarat Trading Com.": ["09_Tzkarat_Store"],
#     "Rateeb Trading Com.": ["10_Rateeb_Store"],
#     "Qahwitna comp.": ["11_Najdi_Coffee", "08_Qahwatna_Al_Safiya_Cafe", "04_Hira_Cafe", "03_Qahwatna_Cafe"]
# }
#
# create_client_project_folders("/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Reports/Sister_Companies", client_projects_data)
```

**Pitfalls:**

*   **Permissions:** Ensure the agent has write permissions to the `base_path`.
*   **Existing Folders:** The `exist_ok=True` argument prevents errors if folders already exist, but be aware that it won't overwrite existing files/folders within those directories.
*   **Path issues:** Always use absolute paths for `base_path` to avoid unexpected directory creation.
