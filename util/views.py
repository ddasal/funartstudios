import tarfile
from django.contrib.auth.decorators import permission_required

from django.shortcuts import redirect, render
from .models import logs

# Create your views here.

permission_required('util.add_logs')
def offsite_backup(request):
    # create tarball for offloading
    obj = logs.objects.create()
    with tarfile.open('archive.tar.gz', 'w:gz') as archive:
        try:
            archive.add('/home/ubuntu/backups/')
        except:
            pass
        try:
            archive.add('../funartstudios/')
        except:
            pass
        try:
            contents = 'offsite backup archive file created'
            logs.objects.filter(pk=obj.pk).update(user=request.user, log=contents)
        except:
            pass
    return redirect('/')