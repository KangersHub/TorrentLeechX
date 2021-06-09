# DHT
wget -O /app/tobrot/aria2/dht.dat https://github.com/P3TERX/aria2.conf/raw/master/dht.dat
wget -O /app/tobrot/aria2/dht6.dat https://github.com/P3TERX/aria2.conf/raw/master/dht6.dat
TRACKER=`curl -Ns https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/all.txt -: https://ngosang.github.io/trackerslist/trackers_all_http.txt -: https://newtrackon.com/api/all -: https://raw.githubusercontent.com/DeSireFire/animeTrackerList/master/AT_all.txt -: https://torrends.to/torrent-tracker-list/?download=latest | awk '$1' | tr '\n' ',' | cat`
ran=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 12 | head -n 1)
echo "Update tracker $TRACKER"
echo "bt-tracker=$TRACKER" >> /app/tobrot/aria2/aria2.conf
echo "Update peer-id-prefix=-qB4350-$ran"
echo "peer-id-prefix=-qB4350-$ran" >> /app/tobrot/aria2/aria2.conf

if [[ -n $RCLONE_CONFIG ]]; then
	echo "Rclone config detected"
	echo -e "$RCLONE_CONFIG" > /app/rclone.conf
fi