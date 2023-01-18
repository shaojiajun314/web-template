cd /backend
chmod +x requirement.txt
pip3 install -r requirement.txt
python3 manage.py makemigrations
python3 manage.py migrate

if [ "$MODE" = "dev" ]; then # todo
    echo "mode dev"
    python3 manage.py runserver 0.0.0.0:8000
else
    echo "mode production"
    daphne Web.asgi:application -b 0.0.0.0 -p 8000
fi