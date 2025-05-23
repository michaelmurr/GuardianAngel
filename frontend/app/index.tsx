import { useAuth, useClerk } from '@clerk/clerk-expo'
import BottomSheet, { BottomSheetView } from '@gorhom/bottom-sheet'
import { ChevronDown, ChevronUp, Plus } from '@tamagui/lucide-icons'
import { HeadingH1 } from 'components/Headings'
import { PrimaryBtn } from 'components/PrimaryBtn'
import * as Location from 'expo-location'
import { useRouter } from 'expo-router'
import * as TaskManager from 'expo-task-manager'
import React, { memo, useCallback, useEffect, useRef, useState } from 'react'
import { StyleSheet, View } from 'react-native'
import MapView from 'react-native-maps'
import { SafeAreaView } from 'react-native-safe-area-context'
import { Avatar, Button, H4, H5, H6, Input, Sheet, Text, XStack, YStack } from 'tamagui'

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


export { LOCATION_TASK_NAME }
const spModes = ['percent', 'constant', 'fit', 'mixed'] as const

export default function Index() {
        const members = [
                { name: 'Anna', avatar: 'https://i.pravatar.cc/150?img=1' },
                { name: 'Ben', avatar: 'https://i.pravatar.cc/150?img=2' },
                { name: 'Clara', avatar: 'https://i.pravatar.cc/150?img=3' },
                { name: 'David', avatar: 'https://i.pravatar.cc/150?img=4' },
        ]
        const { isSignedIn, isLoaded } = useAuth()
        const [showSetDestination, setShowSetDestination] = useState(true)
        const { signOut } = useClerk()
        const router = useRouter()
        const [location, setLocation] = useState<Location.LocationObject | null>(null)
        React.useState<(typeof spModes)[number]>('percent')
        const bottomSheetRef = useRef<BottomSheet>(null);
        const [searchTerm, setSearchTerm] = useState('');
        const [guardians] = useState([
                { id: '1', username: 'alice' },
                { id: '2', username: 'bob' },
                { id: '3', username: 'charlie' },
                { id: '4', username: 'david' },
        ]);

        const alreadyAdded = guardians.slice(0, 2) // pretend these are already added

        const filteredGuardians =
                searchTerm.trim() === ''
                        ? alreadyAdded
                        : guardians.filter(g =>
                                g.username.toLowerCase().includes(searchTerm.trim().toLowerCase())
                        );

        const snapPoints = ['20%', '90%'];

        useEffect(() => {
                if (!isSignedIn && isLoaded) return router.replace('/sign-in')
        }, [isSignedIn])

        useEffect(() => {
                fetchCurrentLocation()
        }, [])

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

        async function fetchCurrentLocation() {
                const latest = await Location.getCurrentPositionAsync({})
                setLocation(latest)
        }

        const latitude = location?.coords?.latitude ?? 0
        const longitude = location?.coords?.longitude ?? 0





        // ref

        // callbacks
        const handleSheetChanges = useCallback((index: number) => {
                console.log('handleSheetChanges', index);
                index === 0 ? setShowSetDestination(false) : setShowSetDestination(true);
        }, []);

        const expandSheet = () => {
                bottomSheetRef.current?.snapToIndex(2); // Fully open (index of '90%')
        };

        const collapseSheet = () => {
                bottomSheetRef.current?.snapToIndex(0);
        };

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

        return (
                <>
                        <View style={{ flex: 1 }} >
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
                                />


                                {/* Floating Button */}
                                <YStack
                                        position="absolute"
                                        bottom={'$16'} // ⬅️ distance from the bottom in pixels
                                        left={0}
                                        right={0}
                                        background={"red"}
                                        px="$2"
                                >
                                </YStack>
                                <BottomSheet
                                        ref={bottomSheetRef}
                                        index={0} // Start at 50%
                                        snapPoints={snapPoints}
                                        onAnimate={handleSheetChanges}

                                >
                                        <BottomSheetView style={styles.contentContainer}>
                                                <YStack px="$4">

                                                        <XStack width="100%" p="$4" justify="space-between" alignItems="center" gap="$2">
                                                                <H4 fontWeight="700">Add Guardians</H4>
                                                                <Plus onPress={expandSheet} size="$3" />
                                                        </XStack>
                                                        {showSetDestination ? (
                                                                <PrimaryBtn>Set Destination</PrimaryBtn>

                                                        ) : null}
                                                </YStack>

                                                {/* 🔍 Search input */}

                                                {/* 🧑🏽‍🤝‍🧑🏽 List of guardians */}
                                                <YStack width="95%" px="$2" gap="$2">
                                                        <Input
                                                                value={searchTerm}
                                                                onChangeText={setSearchTerm}
                                                                placeholder="Search by username"
                                                                width="100%"
                                                                alignSelf="center"
                                                                marginVertical="$4"
                                                        />
                                                        <YStack gap="$2" flexWrap="wrap">

                                                                {members.map((member, idx) => (
                                                                        <XStack justify={'space-between'} alignItems="center" bg={'$white2'} py="$2" pr="$4" pl="$2" rounded={'$4'} borderColor={"$white5"} borderWidth={"1"}>

                                                                                <XStack gap="$4" key={idx} alignItems="center" width={80} >
                                                                                        <Avatar circular size="$4" >
                                                                                                <Avatar.Image
                                                                                                        accessibilityLabel="Nate Wienert"
                                                                                                        src={member.avatar}
                                                                                                />
                                                                                        </Avatar>
                                                                                        <Text fontWeight={'500'} fontSize="$5">{member.name}</Text>
                                                                                </XStack>
                                                                                <XStack alignItems="center" >
                                                                                        <Plus color={"$white11"} />
                                                                                        <Text fontWeight={'500'} color={"$white11"}>Add</Text>
                                                                                </XStack>
                                                                        </XStack>
                                                                ))}
                                                        </YStack>
                                                </YStack>

                                                <Button onPress={collapseSheet} icon={ChevronDown} theme="gray" marginTop="$4">
                                                        Close
                                                </Button>
                                        </BottomSheetView>

                                </BottomSheet>
                        </View>
                </>
        )

}


const styles = StyleSheet.create({
        container: {
                flex: 1,
                backgroundColor: 'grey',
        },
        contentContainer: {
                flex: 1,
                alignItems: 'center',
        },
});