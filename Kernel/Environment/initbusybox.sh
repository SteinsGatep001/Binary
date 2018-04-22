#!/bin/sh

touch etc/passwd
touch etc/group
echo '''root:x:0:0:root:/root:/bin/sh
fish:x:1000:1000:suctf:/home/fish:/bin/sh''' >> etc/passwd

echo '''root:x:0:
tty:x:4:
fish:x:1000:''' >> etc/group

