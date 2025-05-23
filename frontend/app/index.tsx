import { useAuth, useClerk } from '@clerk/clerk-expo'
import BottomSheet, { BottomSheetView } from '@gorhom/bottom-sheet'
import { ChevronDown, ChevronUp } from '@tamagui/lucide-icons'
import { HeadingH1 } from 'components/Headings'
import { PrimaryBtn } from 'components/PrimaryBtn'
import * as Location from 'expo-location'
import { useRouter } from 'expo-router'
import * as TaskManager from 'expo-task-manager'
import React, { memo, useCallback, useEffect, useRef, useState } from 'react'
import { StyleSheet, View } from 'react-native'
import MapView from 'react-native-maps'
import { SafeAreaView } from 'react-native-safe-area-context'
import { Button, Input, Sheet, Text, YStack } from 'tamagui'

const LOCATION_TASK_NAME = 'background-location-task'

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
                        // send to server or websocket if needed
                }
        }
})

export { LOCATION_TASK_NAME }
const spModes = ['percent', 'constant', 'fit', 'mixed'] as const

export default function Index() {
        const { isSignedIn, isLoaded } = useAuth()
        const { signOut } = useClerk()
        const router = useRouter()
        const [location, setLocation] = useState<Location.LocationObject | null>(null)
        const [position, setPosition] = React.useState(0)
        const [open, setOpen] = React.useState(false)
        const [modal, setModal] = React.useState(true)
        const [innerOpen, setInnerOpen] = React.useState(false)
        const [snapPointsMode, setSnapPointsMode] =
                React.useState<(typeof spModes)[number]>('percent')
        const [mixedFitDemo, setMixedFitDemo] = React.useState(false)
        const bottomSheetRef = useRef<BottomSheet>(null);

        const isPercent = snapPointsMode === 'percent'
        const isConstant = snapPointsMode === 'constant'
        const isFit = snapPointsMode === 'fit'
        const isMixed = snapPointsMode === 'mixed'

        const snapPoints = ['25%', '90%'];

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
                                >

                                        <SafeAreaView>

                                                <PrimaryBtn onPress={expandSheet} icon={ChevronUp} theme="blue" bottom="$0">
                                                        Add People
                                                </PrimaryBtn>
                                        </SafeAreaView>
                                </MapView>

                                <BottomSheet
                                        ref={bottomSheetRef}
                                        index={1} // Start at 50%
                                        snapPoints={snapPoints}
                                        onChange={handleSheetChanges}
                                >
                                        <BottomSheetView style={styles.contentContainer}>
                                                <Text>Invite your friends 🎉</Text>
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
                padding: 36,
                alignItems: 'center',
        },
});