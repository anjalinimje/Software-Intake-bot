import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Software Intake Portal",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Banner
st.markdown("""
<div style="
background-color:#1F2937;
padding:20px;
border-radius:10px;
text-align:center;">

<h1 style="
color:white;
margin:0;">
🤖 Software Intake Portal
</h1>

<p style="
color:#D1D5DB;
font-size:18px;">
PSADT • SCCM • Intune Application Packaging Assistant
</p>

</div>
""",
unsafe_allow_html=True)

st.write("")

st.info(
    "📦 Collect application details, dependencies, silent switches, detection rules and packaging requirements."
)



# Application Information

st.header("Application Details")


app_name = st.text_input(
    "Application Name"
)

vendor = st.text_input(
    "Vendor Name"
)

current_version = st.text_input(
    "Current Installed Version"
)

required_version = st.text_input(
    "Required Version"
)


# Installer Details

st.header("Installer Information")


installer_type = st.selectbox(
    "Installer Type",
    [
        "EXE",
        "MSI",
        "MSIX",
        "ZIP"
    ]
)


architecture = st.radio(
    "Architecture",
    [
        "x64",
        "x86",
        "ARM"
    ]
)


admin_required = st.radio(
    "Requires Admin Rights?",
    [
        "Yes",
        "No"
    ]
)


# Upgrade Information

st.header("Upgrade Details")


higher_version = st.radio(
    "Higher Version Available?",
    [
        "Yes",
        "No",
        "Unknown"
    ]
)


auto_upgrade = st.radio(
    "Supports Auto Upgrade?",
    [
        "Yes",
        "No",
        "Need Validation"
    ]
)



# Dependencies

st.header("Dependencies")


dependencies = st.multiselect(
    "Select Dependencies",
    [
        ".NET Framework",
        ".NET Desktop Runtime",
        "Visual C++ Redistributable",
        "Java Runtime",
        "WebView2 Runtime",
        "SQL Driver",
        "Browser Extension",
        "Others",
        "None"
    ]
)

# Ask for Version and Install Order if dependency selected

if dependencies and "None" not in dependencies:

    st.subheader("Dependency Details")

    for dep in dependencies:

        st.text_input(
            f"{dep} - Required Version",
            key=f"{dep}_version"
        )

        st.selectbox(
            f"{dep} - Install Order",
            options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            key=f"{dep}_order"
        )

        st.divider()

# Silent Commands

st.header("Silent Switch Information")


install_cmd = st.text_input(
    "Silent Install Command"
)


uninstall_cmd = st.text_input(
    "Silent Uninstall Command"
)


# Reboot Requirement
st.header("Reboot Requirement")

reboot_required = st.radio(
    "Requires Reboot After Installation?",
    [
        "Yes",
        "No",
        "Unknown"
    ]
)

# Running Applications

st.header("Running Process Check")

st.write(
    "Select common applications that must be closed before installation."
)

common_apps = st.multiselect(
    "Common Applications",
    [
        "chrome",
        "msedge",
        "firefox",
        "outlook",
        "teams",
        "winword",
        "excel",
        "powerpnt",
        "AcroRd32",
        "None"
    ]
)

custom_apps = st.text_input(
    "Additional Processes (comma separated)"
)

# Combine all processes

all_processes = common_apps.copy()

if custom_apps:
    additional = [
        app.strip()
        for app in custom_apps.split(",")
        if app.strip()
    ]

    all_processes.extend(additional)

# Remove duplicates

all_processes = list(set(all_processes))

# Generate PSADT Command

if all_processes:

    psadt_command = (
        f'Show-InstallationWelcome -CloseApps "{",".join(all_processes)}"'
    )

    st.subheader("Generated PSADT Command")

    st.code(
        psadt_command,
        language="powershell"
    )

else:

    psadt_command = "No applications need to be closed."


# Detection Logic
st.header("Detection Logic")    

detection_method = st.selectbox(
    "Detection Method",
    [
        "MSI Product Code",
        "File",
        "Folder",
        "Registry Key",
        "Registry Value",
        "Other"
    ]
)

if detection_method == "MSI Product Code":

    st.text_input(
        "Product Code (GUID)",
        placeholder="{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}"
    )


elif detection_method == "File":

    st.text_input("File Name")
    st.text_input("File Path")
    st.text_input("File Version")

elif detection_method == "Folder":

    st.text_input("Folder Name")
    st.text_input("Folder Path")

elif detection_method == "Registry Key":

    st.selectbox(
        "Registry Hive",
        ["HKLM", "HKCU", "HKCR", "HKU"]
    )

    st.text_input("Registry Key Path")

elif detection_method == "Registry Value":

    st.selectbox(
        "Registry Hive",
        ["HKLM", "HKCU", "HKCR", "HKU"]
    )

    st.text_input("Registry Key Path")
    st.text_input("Registry Value Name")
    st.text_input("Expected Value")
    st.text_input("Version")


elif detection_method == "Other":

    st.text_area("Provide Detection Logic")   

# --------------------------------------------------
# Generate Report
# --------------------------------------------------

if st.button("Generate Packaging Report"):

    report = {
        "Application Name": app_name,
        "Vendor": vendor,
        "Current Version": current_version,
        "Required Version": required_version,
        "Installer Type": installer_type,
        "Architecture": architecture,
        "Admin Rights Required": admin_required,
        "Higher Version Available": higher_version,
        "Auto Upgrade Supported": auto_upgrade,
        "Dependencies": dependencies,
        "Silent Install Command": install_cmd,
        "Silent Uninstall Command": uninstall_cmd,
        "Applications To Close": all_processes,
        "PSADT Command": psadt_command,
        "Reboot Required": reboot_required,
        "Detection Method": detection_method
    }

    st.success("Packaging Report Generated")

    st.json(report)

    # Download Report as CSV
    
    df = pd.DataFrame([report])
    df.to_csv("packaging_report.csv", index=False)
    st.download_button(
        label="Download Packaging Report as CSV",
        data=df.to_csv(index=False),
        file_name="packaging_report.csv",
        mime="text/csv"
    )

    

