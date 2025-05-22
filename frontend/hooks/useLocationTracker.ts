// hooks/useLocationTracker.ts
import * as Location from "expo-location";
import { useEffect, useState } from "react";

export function useLocationTracker() {
  const [location, setLocation] = useState<Location.LocationObject | null>(
    null
  );
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    let subscription: Location.LocationSubscription;

    (async () => {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== "granted") {
        setErrorMsg("Permission to access location was denied");
        return;
      }

      subscription = await Location.watchPositionAsync(
        {
          accuracy: Location.Accuracy.BestForNavigation,
          timeInterval: 5000, // in ms
          distanceInterval: 5, // in meters
        },
        (loc) => {
          setLocation(loc);
          console.log("New location:", loc.coords);
        }
      );
    })();

    return () => {
      subscription?.remove();
    };
  }, []);

  return { location, errorMsg };
}
