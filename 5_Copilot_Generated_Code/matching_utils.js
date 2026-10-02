function isWithinRadius(lat1, lon1, lat2, lon2, radiusKm) {
	const earthRadiusKm = 6371.0088;
	const toRadians = (degrees) => (degrees * Math.PI) / 180;
	const latitudeDifference = toRadians(lat2 - lat1);
	const longitudeDifference = toRadians(lon2 - lon1);

	const haversine =
		Math.sin(latitudeDifference / 2) ** 2 +
		Math.cos(toRadians(lat1)) *
			Math.cos(toRadians(lat2)) *
			Math.sin(longitudeDifference / 2) ** 2;
	const distanceKm =
		2 * earthRadiusKm * Math.asin(Math.sqrt(haversine));

	return distanceKm <= radiusKm;
}
