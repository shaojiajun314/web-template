cd /backend
chmod +x requirement.txt
pip3 install -r requirement.txt -i $PIP_SOURCE
python3 manage.py makemigrations
python3 manage.py migrate

if [ ! -d "/backend/static" ]; then
    python3 manage.py collectstatic
fi

if [ -d "var/log" ]; then
    echo "var/log exist"
    else
    mkdir "var"
    mkdir "var/log"
fi

unlink /tmp/supervisor.sock
supervisord -c supervisord.conf
bash