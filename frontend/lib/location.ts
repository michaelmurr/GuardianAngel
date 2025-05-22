import * as Location from "expo-location";

export async function startLocationUpdates() {
  const { status } = await Location.requestBackgroundPermissionsAsync();
  if (status !== "granted") {
    console.error("Permission not granted");
    return;
  }

  await Location.startLocationUpdatesAsync("background-location-task", {
    accuracy: Location.Accuracy.Highest,
    timeInterval: 5000, // 5 seconds
    distanceInterval: 5, // meters
    showsBackgroundLocationIndicator: true,
    foregroundService: {
      notificationTitle: "Tracking location",
      notificationBody: "Your location is being used",
    },
  });
}
