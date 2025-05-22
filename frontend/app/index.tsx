import { useAuth } from '@clerk/clerk-expo'
import { HeadingH1 } from 'components/Headings'
import { useRouter } from 'expo-router'
import React, { useEffect } from 'react'
import { Text, View } from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'

export default function Index() {
        const { isSignedIn } = useAuth();
        const router = useRouter();
        useEffect(() => {
                if (!isSignedIn) return router.replace("/addGuardians") //change to sign-in


        })

        return (
                <SafeAreaView>
                        WHAT
                </SafeAreaView>
        )
}
