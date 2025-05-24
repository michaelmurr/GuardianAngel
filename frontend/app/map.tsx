// app/map.tsx
import { useAuth, useClerk, useSSO } from '@clerk/clerk-expo'
import BottomSheet, { BottomSheetView } from '@gorhom/bottom-sheet'
import { ChevronDown, Plus, Siren } from '@tamagui/lucide-icons'
import AddGuardianBottomView from 'components/AddGuardianBottomView'
import PanicButton from 'components/PanicButton'
import { PrimaryBtn } from 'components/PrimaryBtn'
import SelectedRouteBottomView from 'components/SelectedRouteBottomView'
import exp from 'constants'
import { API_URL } from 'constants/Key'
import * as Location from 'expo-location'
import { useRouter } from 'expo-router'
import * as TaskManager from 'expo-task-manager'
import { useSendWebSocket } from 'hooks/useSendWebsocket'
import React, { useCallback, useEffect, useRef, useState } from 'react'
import { Animated, Dimensions, Pressable, StyleSheet, TouchableOpacity, View } from 'react-native'
import MapView, { Geojson, Marker, Polyline } from 'react-native-maps'
import { SafeAreaView } from 'react-native-safe-area-context'
import { Avatar, Button, H4, Input, Text, XStack, YStack, ZStack } from 'tamagui'


const LOCATION_TASK_NAME = 'background-location-task'

if (!TaskManager.isTaskDefined(LOCATION_TASK_NAME)) {
        TaskManager.defineTask(LOCATION_TASK_NAME, ({ data, error }) => {
                if (error) {
                        console.error(error);
                        return;
                }

                if (data) {
                        const { locations } = data;
                        const location = locations[0];
                        if (location) {
                                console.log("📍 Background location:", location.coords);
                        }
                }
        });
}


async function fetchCurrentLocationFunny() {
        const { status } = await Location.requestForegroundPermissionsAsync()
        if (status !== 'granted') {
                console.warn('Permission to access location was denied')
                return null
        }

        const location = await Location.getCurrentPositionAsync({})
        const { latitude, longitude } = location.coords

        const start_ll = `${latitude}, ${longitude}`
        return { start_ll }

}

export default function MapScreen() {
        const { isSignedIn, isLoaded } = useAuth()
        const { getToken } = useAuth();
        const { signOut } = useClerk()
        const router = useRouter()
        const [users, setuser] = useState([])
        const [location, setLocation] = useState<Location.LocationObject | null>(null)
        const [showSetDestination, setShowSetDestination] = useState(true)
        const bottomSheetRef = useRef<BottomSheet>(null)
        const [searchTerm, setSearchTerm] = useState('')
        const [safeZone, setSafeZone] = useState(null);
        const [countdown, setCountdown] = useState(15)
        const [isPanicActive, setIsPanicActive] = useState(false)
        const [showSelectRoute, setShowSelectRoute] = useState(false);
        const [city, setCity] = useState('Regensburg')
        const [housenr, setHousenr] = useState('8')
        const [street, setStreet] = useState('Reinhausen')
        const [postalcode, setPostalcode] = useState('93059')
        const { width, height } = Dimensions.get('window')
        const [panicAnim] = useState(new Animated.Value(70)) // initial size
        const [showIcon, setShowIcon] = useState(true)
        const [destination, setDestination] = useState(null)
        const [startedRoute, setStartedRoute] = useState('');
        const [addedGuardians, setAddedGuardians] = useState([])
        const [markerList, setMarkerList] = useState(null)
        const send = useSendWebSocket();
        const guardians = [
                { id: '1', username: 'alice' },
                { id: '2', username: 'bob' },
                { id: '3', username: 'charlie' },
                { id: '4', username: 'david' },
        ]

        useEffect(() => {
                if (!destination) return;

                console.log(
                        '%capp/map.tsx:91 destination',
                        'color: #007acc;',
                        JSON.stringify(destination, null, "\t")
                );

                (async () => {
                        const token = await getToken();
                        const start_ll = await fetchCurrentLocationFunny();

                        const returnobj = { ...start_ll, end_ll: `${destination.lat}, ${destination.lng}` }
                        console.log(
                                '%capp/map.tsx:103 returnobj',
                                'color: #007acc;',
                                JSON.stringify(returnobj, null, "\t")
                        );

                        const res = await fetch(`${API_URL}/routes/create`, {
                                method: "POST",
                                headers: {
                                        Authorization: `Bearer ${token}`,
                                        "Content-Type": "application/json"
                                },
                                body: JSON.stringify(returnobj)

                        })

                        const json = await res.json();

                        setMarkerList(json.coordinates)
                        setSafeZone({
                                type: "FeatureCollection",
                                features: [json.geoJson], // assuming `safeZone` is your single Feature
                        });
                        console.log(
                                '%capp/map.tsx:124 json.geoJson',
                                'color: #007acc;',
                                JSON.stringify(json.geoJson, null, "\t")
                        );

                })()
        }, [destination])

        useEffect(() => {

                let interval: NodeJS.Timeout

                const startStreaming = async () => {
                        const { status } = await Location.requestForegroundPermissionsAsync()
                        if (status !== 'granted') {
                                console.warn('Location permission denied')
                                return
                        }

                        interval = setInterval(async () => {
                                const location = await Location.getCurrentPositionAsync({})
                                const coords = location.coords

                                send({
                                        type: 'status',
                                        payload: {
                                                location: {
                                                        latitude: coords.latitude,
                                                        longitude: coords.longitude,
                                                },
                                                battery: 69.9,
                                                speed: 1
                                        },
                                })
                        }, 3000)
                }

                startStreaming()

                return () => {
                        clearInterval(interval)
                }
        }, [send])

        const alreadyAdded = guardians.slice(0, 2)

        const filteredGuardians =
                searchTerm.trim() === ""
                        ? alreadyAdded
                        : guardians.filter((g) =>
                                g.username.toLowerCase().includes(searchTerm.trim().toLowerCase())
                        );

        const snapPoints = ["25%", "90%"];
        const members = [
                { name: "Anna", avatar: "https://i.pravatar.cc/150?img=1" },
                { name: "Ben", avatar: "https://i.pravatar.cc/150?img=2" },
                { name: "Clara", avatar: "https://i.pravatar.cc/150?img=3" },
                { name: "David", avatar: "https://i.pravatar.cc/150?img=4" },
        ];

        useEffect(() => {
                fetchCurrentLocation();
        }, []);

        async function fetchCurrentLocation() {
                const latest = await Location.getCurrentPositionAsync({});
                setLocation(latest);
        }

        async function startTracking() {
                const { status: fg } = await Location.requestForegroundPermissionsAsync();
                const { status: bg } = await Location.requestBackgroundPermissionsAsync();

                if (fg !== "granted" || bg !== "granted") {
                        alert("Permission to access location was denied");
                        return;
                }

                const started = await Location.hasStartedLocationUpdatesAsync(
                        LOCATION_TASK_NAME
                );
                if (!started) {
                        await Location.startLocationUpdatesAsync(LOCATION_TASK_NAME, {
                                accuracy: Location.Accuracy.Highest,
                                timeInterval: 10000,
                                distanceInterval: 20,
                                showsBackgroundLocationIndicator: true,
                                foregroundService: {
                                        notificationTitle: "Tracking your location",
                                        notificationBody: "Location tracking is active in background",
                                },
                        });
                        console.log("✅ Started background location task");
                } else {
                        console.log("⚠️ Task already running");
                }
        }

        const latitude = location?.coords?.latitude ?? 0;
        const longitude = location?.coords?.longitude ?? 0;

        const handleSheetChanges = useCallback((index: number) => {
                index === 0 ? setShowSetDestination(false) : setShowSetDestination(true);
        }, []);

        const expandSheet = () => bottomSheetRef.current?.snapToIndex(1);
        const collapseSheet = () => bottomSheetRef.current?.snapToIndex(0);

        function triggerPanic() {
                setShowIcon(false);
                setIsPanicActive(true);
                setCountdown(15);

                Animated.timing(panicAnim, {
                        toValue: Math.max(width, height) * 1.5,
                        duration: 500,
                        useNativeDriver: false,
                }).start(() => {
                        console.log("🚨 PANIC MODE ACTIVATED");
                });
        }

        useEffect(() => {
                if (!isPanicActive || countdown <= 0) return;

                const interval = setInterval(() => {
                        setCountdown((prev) => {
                                if (prev === 1) {
                                        clearInterval(interval);
                                        console.log("✅ PANIC TIMEOUT COMPLETE"); // Replace with real action
                                        setShowIcon(true);
                                        setIsPanicActive(false);
                                }
                                return prev - 1;
                        });
                }, 1000);

                return () => clearInterval(interval);
        }, [isPanicActive, countdown]);

        useEffect(() => {
                (async () => {
                        try {
                                const token = await getToken();
                                const res = await fetch(
                                        `${API_URL}/people/all?parameter=${searchTerm}`,
                                        {
                                                headers: {
                                                        Authorization: `Bearer ${token}`,
                                                },
                                        }
                                );

                                const json = await res.json();
                                console.log(
          /*************  ✨ Windsurf Command ⭐  *************/
          /**
           * Retrieves the list of added guardians for the current user
           * @returns A JSON object containing the list of added guardians
           */
          /*******  a1215c48-9f4d-4b60-b1df-064161d0533e  *******/ "%cfrontend/app/map.tsx:162 json",
                                        "color: #007acc;",
                                        JSON.stringify(json, null, "\t")
                                );

                                setuser(json);
                        } catch (e) {
                                console.log(e);
                        }
                })();
        }, [searchTerm]);

        const handleAddedGuardians = async () => {
                const token = await getToken();
                const res = await fetch(`${API_URL}/friends/all`, {
                        method: "GET",
                        headers: {
                                Authorization: `Bearer ${token}`,
                        },
                });
                const json = await res.json();
        };

        useEffect(() => {
                (async () => {
                        let returnedGuardians = await handleAddedGuardians();
                        setAddedGuardians(returnedGuardians);
                })();
        }, []);

        const handleAddUser = async (username: string) => {
                const stringified = JSON.stringify({ friend_username: username });
                console.log(stringified);
                const token = await getToken();

                const res = await fetch(`${API_URL}/friends/add`, {
                        method: "POST",
                        headers: {
                                Authorization: `Bearer ${token}`,
                        },
                        body: stringified,
                });
                if (res.ok) return console.log("response is ok");
        };



        if (!location) {
                return (
                        <SafeAreaView
                                style={{ flex: 1, justifyContent: "center", alignItems: "center" }}
                        >
                                <Text>📍 Loading location...</Text>
                                <PrimaryBtn onPress={startTracking}>Start Location Updates</PrimaryBtn>
                                <PrimaryBtn onPress={fetchCurrentLocation}>
                                        Get Current Location
                                </PrimaryBtn>
                                <PrimaryBtn onPress={async () => await signOut()}>Sign out</PrimaryBtn>
                        </SafeAreaView>
                );
        }

        if (users.length)
                return (
                        <View style={{ flex: 1 }}>
                                <MapView
                                        style={{ flex: 1 }}
                                        showsUserLocation
                                        followsUserLocation
                                        initialRegion={{
                                                latitude,
                                                longitude,
                                                latitudeDelta: 0.01,
                                                longitudeDelta: 0.01,
                                        }}
                                        onPress={expandSheet}
                                >
                                        {destination && (
                                                <Marker
                                                        coordinate={{
                                                                latitude: destination.lat,
                                                                longitude: destination.lng,
                                                        }}
                                                />
                                        )}
                                        {safeZone && <Geojson
                                                geojson={safeZone}
                                                strokeColor="rgba(0, 0, 0, 0.4)"   // 40% opacity for stroke
                                                fillColor="rgba(0, 255, 0, 0.2)"
                                                zIndex={0}
                                                strokeWidth={2}
                                        />}
                                        {markerList && <Polyline
                                                coordinates={markerList ?? []}
                                                strokeColor="#007AFF"
                                                strokeWidth={4}
                                                zIndex={999}
                                        />}
                                </MapView>

                                {/* Red expanding panic circle */}
                                {isPanicActive && (
                                        <>
                                                <Animated.View
                                                        style={{
                                                                position: "absolute",
                                                                top: "50%",
                                                                left: "50%",
                                                                width: 70,
                                                                height: 70,
                                                                borderRadius: 35,
                                                                backgroundColor: "red",
                                                                transform: [
                                                                        { translateX: -35 },
                                                                        { translateY: -35 },
                                                                        {
                                                                                scale: panicAnim.interpolate({
                                                                                        inputRange: [70, Math.max(width, height) * 1.25],
                                                                                        outputRange: [1, (Math.max(width, height) * 1.5) / 70],
                                                                                }),
                                                                        },
                                                                ],
                                                                zIndex: 998,
                                                        }}
                                                />
                                                <View
                                                        style={{
                                                                position: "absolute",
                                                                top: "50%",
                                                                left: "50%",
                                                                transform: [{ translateX: -25 }, { translateY: -25 }],
                                                                zIndex: 999,
                                                        }}
                                                >
                                                        <Text
                                                                style={{
                                                                        fontSize: 36,
                                                                        color: "white",
                                                                        fontWeight: "bold",
                                                                }}
                                                        >
                                                                {countdown}
                                                        </Text>
                                                </View>
                                        </>
                                )}

                                {/* Original panic button (only shown if not active) */}
                                <Pressable
                                        onPress={triggerPanic}
                                        style={{
                                                position: "absolute",
                                                bottom: 230,
                                                left: 20,
                                                width: 70,
                                                height: 70,
                                                borderRadius: 35,
                                                backgroundColor: "red",
                                                justifyContent: "center",
                                                alignItems: "center",
                                        }}
                                >
                                        <Siren size="$4" color="white" />
                                </Pressable>
                                <BottomSheet
                                        ref={bottomSheetRef}
                                        index={0}
                                        snapPoints={snapPoints}
                                        onAnimate={handleSheetChanges}
                                >
                                        {showSelectRoute ? (
                                                <SelectedRouteBottomView
                                                        expandSheet={expandSheet}
                                                        getToken={getToken}
                                                        members={members}
                                                        street={street}
                                                        setStreet={setStreet}
                                                        housenr={housenr}
                                                        setHousenr={setHousenr}
                                                        city={city}
                                                        setCity={setCity}
                                                        postalcode={postalcode}
                                                        setPostalcode={setPostalcode}
                                                        setShowSelectRoute={setShowSelectRoute}
                                                        setDestination={setDestination}
                                                        collapseSheet={collapseSheet}
                                                />

                                        ) : (

                                                <AddGuardianBottomView
                                                        expandSheet={expandSheet}
                                                        members={members}
                                                        users={users}
                                                        searchTerm={searchTerm}
                                                        setSearchTerm={setSearchTerm}
                                                        handleAddUser={handleAddUser}
                                                        setShowSelectRoute={setShowSelectRoute}
                                                />

                                        )}
                                </BottomSheet>
                        </View>
                )
}

const styles = StyleSheet.create({
        contentContainer: {
                flex: 1,
                alignItems: "center",
        },
});
