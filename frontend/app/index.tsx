import { useAuth } from '@clerk/clerk-expo'
import { HeadingH1 } from 'components/Headings'
import * as Location from 'expo-location'
import { useRouter } from 'expo-router'
import * as TaskManager from 'expo-task-manager'
import { useLocationTracker } from 'hooks/useLocationTracker'
import React, { useEffect } from 'react'
import { Text, View } from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'
export default function Index() {
        const { isSignedIn } = useAuth();
        const router = useRouter();
        useEffect(() => {
                // if (!isSignedIn) return router.replace("/addGuardians") //change to sign-in


        })




        // const LOCATION_TASK_NAME = 'background-location-task'

        // TaskManager.defineTask(LOCATION_TASK_NAME, ({ data, error }) => {
        //         if (error) {
        //                 console.error(error)
        //                 return
        //         }

        //         if (data) {
        //                 const { locations } = data
        //                 const location = locations[0]

        //                 if (location) {
        //                         console.log(locations)
        //                         // Send location to WebSocket
        //                         // const socket = new WebSocket('wss://your-server.com')
        //                         // socket.onopen = () => {
        //                         //         socket.send(JSON.stringify(location.coords))
        //                         //         socket.close()
        //                         // }
        //                 }
        //         }
        // })

        const { location, errorMsg } = useLocationTracker()
        return (
                <SafeAreaView>
                        {location ? (
                                <Text>{JSON.stringify(location)}</Text>
                        ) : null}
                </SafeAreaView>
        )
}
