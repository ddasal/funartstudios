import tarfile
from .models import logs

# Create your views here.

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
        print('file created')
        logs.objects.filter(pk=obj.pk).update(user=request.user, log=archive.list)
        print('log written')
