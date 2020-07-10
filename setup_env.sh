#!/bin/sh

# PYTHONPATH에 timo 추가
echo "export PYTHONPATH=$(pwd)/timo:$PYTHONPATH" >> ~/.bashrc

# timo를 명령어로 실행할 수 있게 경로 추가
sudo echo -e '#!/bin/bash\npython ${PYTHONPATH}/core.py "$@"' > /usr/bin/timo
chmod +x /usr/bin/timo
