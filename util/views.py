import tarfile
from .models import logs

# Create your views here.

def offsite_backup(request):
    # create tarball for offloading
    obj = logs.objects.create()
    with tarfile.open('archive.tar.gz', 'w:gz') as archive:
        archive.add('/home/ubuntu/backups/*')
        archive.add('/home/ubuntu/funartstudios/*')
        print('file create')
        logs.objects.filter(pk=obj.pk).update(user=request.user, log=archive.list)
        print('log written')
