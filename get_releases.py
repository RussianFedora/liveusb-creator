import re
from urlgrabber import urlread
from urlgrabber.grabber import URLGrabError

FEDORA_RELEASES = 'http://dl.fedoraproject.org/pub/fedora/linux/releases/'
RFREMIX_RELEASES = 'http://mirror.yandex.ru/fedora/russianfedora/releases/RFRemix/'
ARCHES = ('x86_64', 'i686', 'i386')

def get_fedora_releases(url):
    releases = []
    html = urlread(url)

    # RFRemix distributions can have '.' in version.
    # This code chooses the latest version for three last distributions.
    # It's mean for 18, 17.1, 17, 16.1, 16, 15.1 and so on it will be 18, 17.1 and 16.1

    # This code is dirty. Feel to free improve it.
    all_releases = re.findall(r'<a href="(\d+\.?\d?)/">', html)[::-1]
    target_releases = all_releases[:1]
    last_release = int(target_releases[0].split('.')[0])
    prev_release = last_release - 1
    for release in all_releases:
        if int(release.split('.')[0]) == prev_release:
            target_releases.append(release)
            prev_release = prev_release - 1
        if prev_release == last_release - 3:
            break

    for release in target_releases:
        for arch in ARCHES:
            arch_url = url + '%s/Live/%s/' % (release, arch)
            try:
                files = urlread(arch_url)
            except URLGrabError:
                continue
            for link in re.findall(r'<a href="(.*)">', files):
                if link.endswith('-CHECKSUM'):
                    checksum = urlread(arch_url + link)
                    for line in checksum.split('\n'):
                        try:
                            sha256, filename = line.split()
                            if filename.endswith('.iso') == False:
                                continue

                            if filename[0] == '*':
                                filename = filename[1:]
                            chunks = filename[:-4].split('-')
                            chunks.remove('Live')
                            name = ' '.join(chunks)
                            releases.append(dict(
                                name = name,
                                url = arch_url + filename,
                                sha256 = sha256,
                                ))
                        except ValueError:
                            pass
    return releases

pprint(get_fedora_releases(RFREMIX_RELEASES) + get_fedora_releases(FEDORA_RELEASES))
