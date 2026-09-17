#!/usr/bin/env bash
# Собирает бандл медиа из локального media/ и кладёт его в /tmp/opencode.
# Загрузить в GitHub Release как asset «media-bundle.tar.gz»:
#   gh release upload latest media-bundle.tar.gz   (или через веб-UI репозитория)
set -euo pipefail
cd /mnt/my-files/python_projects/my_site
tar -czf /tmp/opencode/media-bundle.tar.gz -C media .
ls -lh /tmp/opencode/media-bundle.tar.gz