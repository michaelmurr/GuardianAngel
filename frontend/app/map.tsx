// app/map.tsx
import { useAuth, useClerk, useSSO } from '@clerk/clerk-expo'
import BottomSheet, { BottomSheetView } from '@gorhom/bottom-sheet'
import { ChevronDown, Plus, Siren } from '@tamagui/lucide-icons'
import { PrimaryBtn } from 'components/PrimaryBtn'
import { API_URL } from 'constants/Key'
import * as Location from 'expo-location'
import { useRouter } from 'expo-router'
import * as TaskManager from 'expo-task-manager'
import { useSendWebSocket } from 'hooks/useSendWebsocket'
import React, { useCallback, useEffect, useRef, useState } from 'react'
import { Animated, Dimensions, Pressable, StyleSheet, TouchableOpacity, View } from 'react-native'
import MapView, { Marker } from 'react-native-maps'
import { SafeAreaView } from 'react-native-safe-area-context'
import { Avatar, Button, H4, Input, Text, XStack, YStack } from 'tamagui'


const LOCATION_TASK_NAME = 'background-location-task'

if (!TaskManager.isTaskDefined(LOCATION_TASK_NAME)) {
        TaskManager.defineTask(LOCATION_TASK_NAME, ({ data, error }) => {
                if (error) {
                        console.error(error)
                        return
                }

                if (data) {
                        const { locations } = data
                        const location = locations[0]
                        if (location) {
                                console.log('📍 Background location:', location.coords)
                        }
                }
        })
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
        const [countdown, setCountdown] = useState(15)
        const [isPanicActive, setIsPanicActive] = useState(false)
        const [showSelectRoute, setShowSelectRoute] = useState(false);
        const [city, setCity] = useState('')
        const [housenr, setHousenr] = useState('')
        const [street, setStreet] = useState('')
        const [postalcode, setPostalcode] = useState('')
        const { width, height } = Dimensions.get('window')
        const [panicAnim] = useState(new Animated.Value(70)) // initial size
        const [showIcon, setShowIcon] = useState(true)
        const [destination, setDestination] = useState(null)
        const [startedRoute, setStartedRoute] = useState('');
        const [addedGuardians, setAddedGuardians] = useState([])
        const send = useSendWebSocket();
        const guardians = [
                { id: '1', username: 'alice' },
                { id: '2', username: 'bob' },
                { id: '3', username: 'charlie' },
                { id: '4', username: 'david' },
        ]


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

        const filteredGuardians = searchTerm.trim() === ''
                ? alreadyAdded
                : guardians.filter(g =>
                        g.username.toLowerCase().includes(searchTerm.trim().toLowerCase())
                )

        const snapPoints = ['25%', '90%']
        const members = [
                { name: 'Anna', avatar: 'https://i.pravatar.cc/150?img=1' },
                { name: 'Ben', avatar: 'https://i.pravatar.cc/150?img=2' },
                { name: 'Clara', avatar: 'https://i.pravatar.cc/150?img=3' },
                { name: 'David', avatar: 'https://i.pravatar.cc/150?img=4' },
        ]

        useEffect(() => {
                fetchCurrentLocation()
        }, [])

        async function fetchCurrentLocation() {
                const latest = await Location.getCurrentPositionAsync({})
                setLocation(latest)
        }

        async function startTracking() {
                const { status: fg } = await Location.requestForegroundPermissionsAsync()
                const { status: bg } = await Location.requestBackgroundPermissionsAsync()

                if (fg !== 'granted' || bg !== 'granted') {
                        alert('Permission to access location was denied')
                        return
                }

                const started = await Location.hasStartedLocationUpdatesAsync(LOCATION_TASK_NAME)
                if (!started) {
                        await Location.startLocationUpdatesAsync(LOCATION_TASK_NAME, {
                                accuracy: Location.Accuracy.Highest,
                                timeInterval: 10000,
                                distanceInterval: 20,
                                showsBackgroundLocationIndicator: true,
                                foregroundService: {
                                        notificationTitle: 'Tracking your location',
                                        notificationBody: 'Location tracking is active in background',
                                },
                        })
                        console.log('✅ Started background location task')
                } else {
                        console.log('⚠️ Task already running')
                }
        }

        const latitude = location?.coords?.latitude ?? 0
        const longitude = location?.coords?.longitude ?? 0

        const handleSheetChanges = useCallback((index: number) => {
                index === 0 ? setShowSetDestination(false) : setShowSetDestination(true)
        }, [])

        const expandSheet = () => bottomSheetRef.current?.snapToIndex(1)
        const collapseSheet = () => bottomSheetRef.current?.snapToIndex(0)

        function triggerPanic() {
                setShowIcon(false)
                setIsPanicActive(true)
                setCountdown(15)

                Animated.timing(panicAnim, {
                        toValue: Math.max(width, height) * 1.5,
                        duration: 500,
                        useNativeDriver: false,
                }).start(() => {
                        console.log('🚨 PANIC MODE ACTIVATED')
                })
        }

        useEffect(() => {
                if (!isPanicActive || countdown <= 0) return

                const interval = setInterval(() => {
                        setCountdown((prev) => {
                                if (prev === 1) {
                                        clearInterval(interval)
                                        console.log('✅ PANIC TIMEOUT COMPLETE') // Replace with real action
                                        setShowIcon(true);
                                        setIsPanicActive(false);
                                }
                                return prev - 1
                        })
                }, 1000)

                return () => clearInterval(interval)
        }, [isPanicActive, countdown])


        useEffect(() => {
                (async () => {
                        try {
                                const token = await getToken();
                                const res = await fetch(`${API_URL}/people/all?parameter=${searchTerm}`, {
                                        headers: {
                                                Authorization: `Bearer ${token}`
                                        }
                                })

                                const json = await res.json();
                                console.log(
                                        '%cfrontend/app/map.tsx:162 json',
                                        'color: #007acc;',
                                        JSON.stringify(json, null, "\t")
                                );


                                setuser(json)
                        } catch (e) {
                                console.log(e)
                        }
                })();
        }, [searchTerm])

        const handleAddedGuardians = async () => {
                const token = await getToken();
                const res = await fetch(`${API_URL}/friends/all`, {

                        method: 'GET',
                        headers: {
                                Authorization: `Bearer ${token}`
                                ,
                        }
                })
                const json = await res.json();
        }

        useEffect(() => {
                (async () => {
                        let returnedGuardians = await handleAddedGuardians()
                        setAddedGuardians(returnedGuardians);
                })()
        }, [])


        const handleAddUser = async (username: string) => {

                const stringified = JSON.stringify({ friend_username: username });
                console.log(stringified)
                const token = await getToken();

                const res = await fetch(`${API_URL}/friends/add`, {
                        method: 'POST',
                        headers: {
                                Authorization: `Bearer ${token}`
                        },
                        body: stringified
                })
                if (res.ok) return console.log('response is ok');
        }

        const submitRoute = async () => {
                const token = await getToken();

                const res = await fetch(`${API_URL}/routes/coordinates`, {
                        method: "POST",
                        headers: {
                                Authorization: `Bearer ${token}`,
                                'Content-Type': 'application/json'

                        },
                        body: JSON.stringify({ house_number: housenr, street, city, postal_code: postalcode })
                })
                const json = await res.json();
                console.log(json)
                setDestination(json);
                collapseSheet();

        }

        if (!location) {
                return (
                        <SafeAreaView style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
                                <Text>📍 Loading location...</Text>
                                <PrimaryBtn onPress={startTracking}>Start Location Updates</PrimaryBtn>
                                <PrimaryBtn onPress={fetchCurrentLocation}>Get Current Location</PrimaryBtn>
                                <PrimaryBtn onPress={async () => await signOut()}>Sign out</PrimaryBtn>
                        </SafeAreaView>
                )
        }



        if (users.length) return (
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
                                {destination && <Marker coordinate={{ latitude: destination.lat, longitude: destination.lng }} />}
                        </MapView>

                        {/* Red expanding panic circle */}
                        {isPanicActive && (
                                <>
                                        <Animated.View
                                                style={{
                                                        position: 'absolute',
                                                        top: '50%',
                                                        left: '50%',
                                                        width: 70,
                                                        height: 70,
                                                        borderRadius: 35,
                                                        backgroundColor: 'red',
                                                        transform: [
                                                                { translateX: -35 },
                                                                { translateY: -35 },
                                                                {
                                                                        scale: panicAnim.interpolate({
                                                                                inputRange: [70, Math.max(width, height) * 1.25],
                                                                                outputRange: [1, Math.max(width, height) * 1.5 / 70],
                                                                        }),
                                                                },
                                                        ],
                                                        zIndex: 998,
                                                }}
                                        />
                                        <View
                                                style={{
                                                        position: 'absolute',
                                                        top: '50%',
                                                        left: '50%',
                                                        transform: [{ translateX: -25 }, { translateY: -25 }],
                                                        zIndex: 999,
                                                }}
                                        >
                                                <Text
                                                        style={{
                                                                fontSize: 36,
                                                                color: 'white',
                                                                fontWeight: 'bold',
                                                        }}
                                                >
                                                        {countdown}
                                                </Text>
                                        </View>
                                </>
                        )}

                        {/* Original panic button (only shown if not active) */}
                        {!isPanicActive && (
                                <Pressable
                                        onPress={triggerPanic}
                                        style={{
                                                position: 'absolute',
                                                bottom: 230,
                                                left: 20,
                                                width: 70,
                                                height: 70,
                                                borderRadius: 35,
                                                backgroundColor: 'red',
                                                justifyContent: 'center',
                                                alignItems: 'center',
                                        }}

                                >
                                        <Siren size="$4" color="white" />
                                </Pressable>
                        )}




                        <BottomSheet
                                ref={bottomSheetRef}
                                index={0}
                                snapPoints={snapPoints}
                                onAnimate={handleSheetChanges}
                        >
                                {showSelectRoute ? (
                                        <BottomSheetView style={styles.contentContainer}>
                                                <YStack px="$4" gap={"$4"}>
                                                        <YStack>

                                                                <XStack width="100%" justify="space-between" alignItems="center" gap="$2">

                                                                        <H4 fontWeight="700">Select your destination</H4>
                                                                        <Plus onPress={expandSheet} size="$3" />
                                                                </XStack>
                                                                <XStack  >

                                                                        {members.map((member, id) => {
                                                                                return (
                                                                                        <Avatar circular size="$4" key={id}>
                                                                                                <Avatar.Image accessibilityLabel={id} src={member.avatar} />
                                                                                        </Avatar>
                                                                                )
                                                                        })}
                                                                </XStack>
                                                        </YStack>
                                                </YStack>

                                                <YStack width="95%" px="$2" gap="$2" justify={"space-between"} height={"80%"}>
                                                        <YStack gap={"$2"}>
                                                                <XStack justify={'space-between'} mt="$4">


                                                                        <Input
                                                                                value={street}
                                                                                onChangeText={setStreet}
                                                                                placeholder="Street"
                                                                                alignSelf="center"
                                                                                width={"70%"}
                                                                        />
                                                                        <Input
                                                                                value={housenr}
                                                                                onChangeText={setHousenr}
                                                                                placeholder="Housenr."
                                                                                alignSelf="center"
                                                                                width={"29%"}

                                                                        />
                                                                </XStack>
                                                                <Input
                                                                        value={city}
                                                                        onChangeText={setCity}
                                                                        placeholder="City"
                                                                        width="100%"
                                                                        alignSelf="center"
                                                                />
                                                                <Input
                                                                        value={postalcode}
                                                                        onChangeText={setPostalcode}
                                                                        placeholder="Postal Code"
                                                                        width="100%"
                                                                        alignSelf="center"
                                                                />



                                                        </YStack>
                                                        <YStack gap="$2">

                                                                <PrimaryBtn onPress={async () => submitRoute()} icon={ChevronDown} theme="gray" marginTop="$4">
                                                                        Start
                                                                </PrimaryBtn>
                                                                <PrimaryBtn onPress={() => setShowSelectRoute(false)} icon={ChevronDown} theme="gray" marginTop="$4">
                                                                        Back
                                                                </PrimaryBtn>
                                                        </YStack>
                                                </YStack>

                                        </BottomSheetView>
                                ) : (

                                        <BottomSheetView style={styles.contentContainer}>
                                                <YStack px="$4" gap={"$4"}>
                                                        <YStack>

                                                                <XStack width="100%" justify="space-between" alignItems="center" gap="$2">

                                                                        <H4 fontWeight="700">Add Guardians</H4>
                                                                        <Plus onPress={expandSheet} size="$3" />
                                                                </XStack>
                                                                <XStack  >

                                                                        {members.map((member, id) => {
                                                                                return (
                                                                                        <Avatar circular size="$4" key={id}>
                                                                                                <Avatar.Image accessibilityLabel={id} src={member.avatar} />
                                                                                        </Avatar>
                                                                                )
                                                                        })}
                                                                </XStack>
                                                        </YStack>

                                                </YStack>

                                                <YStack width="95%" px="$2" gap="$2" justify={"space-between"} height={"80%"}>
                                                        <YStack>

                                                                <Input
                                                                        value={searchTerm}
                                                                        onChangeText={setSearchTerm}
                                                                        placeholder="Search by username"
                                                                        width="100%"
                                                                        alignSelf="center"
                                                                        marginVertical="$4"
                                                                />

                                                                <YStack gap="$2" flexWrap="wrap">
                                                                        {users.map((user, idx) => (
                                                                                <XStack
                                                                                        key={idx}
                                                                                        justify="space-between"
                                                                                        alignItems="center"
                                                                                        bg="$white2"
                                                                                        py="$2"
                                                                                        pr="$4"
                                                                                        pl="$2"
                                                                                        rounded="$4"
                                                                                        borderColor="$white5"
                                                                                        borderWidth="1"
                                                                                >
                                                                                        <XStack flex={1} gap="$4" alignItems="center" width={80}>
                                                                                                <Avatar circular size="$4">
                                                                                                        <Avatar.Image accessibilityLabel={user.name} src={members[idx].avatar} />
                                                                                                </Avatar>
                                                                                                <Text fontWeight="500" fontSize="$5" width={"100%"}>{user.name}</Text>
                                                                                        </XStack>
                                                                                        <TouchableOpacity onPress={() => handleAddUser(user.username)}>

                                                                                                <XStack alignItems="center" >
                                                                                                        <Plus color="$white11" />
                                                                                                        <Text fontWeight="500" color="$white11">Add</Text>
                                                                                                </XStack>
                                                                                        </TouchableOpacity>
                                                                                </XStack>
                                                                        ))}
                                                                </YStack>
                                                        </YStack>

                                                        <PrimaryBtn onPress={() => setShowSelectRoute(true)} icon={ChevronDown} theme="gray" marginTop="$4">
                                                                Next
                                                        </PrimaryBtn>
                                                </YStack>

                                        </BottomSheetView>
                                )}
                        </BottomSheet>
                </View>
        )
}

const styles = StyleSheet.create({
        contentContainer: {
                flex: 1,
                alignItems: 'center',
        },
})
