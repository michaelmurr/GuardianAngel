import { useAuth } from '@clerk/clerk-expo'
import { useRouter } from 'expo-router'
import { useEffect } from 'react'
import { ActivityIndicator, View } from 'react-native'

export default function Index() {
        const { isLoaded, isSignedIn } = useAuth()
        const router = useRouter()

        useEffect(() => {
                if (!isLoaded) return

                if (isSignedIn) {
                        console.log('signed in')
                        router.replace('/map')
                } else {
                        console.log('not signed in')
                        router.replace('/sign-in')
                }
        }, [isLoaded, isSignedIn])

        return (
                <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
                        <ActivityIndicator size="large" />
                </View>
        )
}
