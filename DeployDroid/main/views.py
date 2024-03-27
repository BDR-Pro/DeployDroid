# main/views.py
from django.shortcuts import render, HttpResponse
from .forms import InstallForm
import os
import uuid
from .models import ChocolateyPackage

MAIN_SCRIPT = """Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force
Install-Module -Name PowerShellGet -Force
iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex
"""

def script_to_exe(script):
    uuid_str = str(uuid.uuid4())
    ps1_filename = f'install_{uuid_str}.ps1'
    exe_filename = f'target_{uuid_str}.exe'
    with open(ps1_filename, 'w') as f:
        f.write(script)
    
    # Convert PS1 to EXE
    command = f"powershell.exe -ExecutionPolicy Bypass Invoke-ps2exe .\\{ps1_filename} .\\{exe_filename}"
    os.system(command)
    
    # Serve the EXE file to the user
    if os.path.exists(exe_filename):
        with open(exe_filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{exe_filename}"'
            
            # Cleanup: Delete temporary files
            os.remove(ps1_filename)
            os.remove(exe_filename)
            
            return response
    else:
        return HttpResponse("Failed to create the executable file.", status=500)

def install_view(request):
    if request.method == 'POST':
        form = InstallForm(request.POST)
        if form.is_valid():
            packages = form.cleaned_data['packages']
            ps_script = MAIN_SCRIPT
            
            for package in packages:
                ps_script += f"choco install {package.name} -y\n"
            return script_to_exe(ps_script)
    else:
        form = InstallForm()
        packages_by_category = {}
        for package in ChocolateyPackage.objects.all().order_by('category'):
            category = package.category  # Adjust according to your model
            if category not in packages_by_category:
                packages_by_category[category] = []
            packages_by_category[category].append(package)
        
    return render(request, 'main/install_form.html', {'form': form, 'packages_by_category': packages_by_category})
