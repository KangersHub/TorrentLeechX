# DHT
wget -q https://github.com/P3TERX/aria2.conf/raw/master/dht.dat
wget -q https://github.com/P3TERX/aria2.conf/raw/master/dht6.dat

TRACKER=$(curl -Ns https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/all.txtnexthttps://ngosang.github.io/trackerslist/trackers_all_http.txtnexthttps://newtrackon.com/api/allnexthttps://raw.githubusercontent.com/DeSireFire/animeTrackerList/master/AT_all.txt | awk '$1' | tr '\n' ',')
ran=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 12 | head -n 1)

echo "Update tracker $TRACKER"
echo "bt-tracker=$TRACKER" >> /app/aria2.conf

echo "Update peer-id-prefix=-qB4250-$ran"
echo "peer-id-prefix=-qB4250-$ran" >> /app/aria2.conf


if [[ -n $RCLONE_CONFIG ]]; then
	echo "Rclone config detected"
	echo -e "$RCLONE_CONFIG" > /app/rclone.conf
fi