cd /gin
chmod +x requirement.txt
apt update
apt install pip -y

# go run main.go

if [ -d "python/var/log" ]; then
    echo "var/log exist"
    else
    mkdir "python/var"
    mkdir "python/var/log"
fi

unlink /tmp/supervisor.sock
cd python
if [ -d "githubFileFetcher" ]; then
	echo "githubFileFetcher exist"
    else
	git clone https://github.com/shawTools/githubFileFetcher.git
fi
if [ -d "urlParser" ]; then
	echo "urlParser exist"
    else
	git clone https://github.com/shawTools/urlParser.git
fi
pip3 install -r requirement.txt -i $PIP_SOURCE
supervisord -c supervisord.conf
bash